library(tidyverse)
library(rvest)
library(stringr)
library(curl)

nfl_week <- ceiling(as.numeric(Sys.Date() - as.Date("2017-09-06")) / 7 )

fetch_sharks <- function(week = 1, position = 97) {
  
    url <- str_c(sep = "",
         "http://www.fantasysharks.com/apps/bert/forecasts/projections.php?", 
         "League=-1",
             # QB + RB + WR + TE = 97
             # K - 7
             # DEF - 6
         "&Position=", position, 
             # NFL.com = 13
         "&scoring=", 13,
             # week 1 = 564, start at 563 + current week
         "&Segment=", 595 + week)
    
    page <- read_html(curl(url, handle = curl::new_handle("useragent" = "Mozilla/5.0")))
    
    name <- page %>% 
        html_nodes(".playerLink") %>% 
        html_text() %>% 
        as_tibble() %>% 
        rename(name = value)
    
    pos <- page %>% 
        html_nodes("#toolData td:nth-child(5)") %>% 
        html_text() %>% 
        as_tibble() %>% 
        rename(pos = value)
    
        # 97 - points in 14 
        # 7 - points in 15
        # 6 - points in 12
    points_child <- ifelse(position == 97, 14, ifelse(position == 7, 15, 12)) 

    points <- page %>%
        html_nodes(str_c("td:nth-child(", points_child,")")) %>%
        html_text() %>% 
        as_tibble() %>% 
        rename(points = value)
    
    if (position == 97) {
        np <- bind_cols(pos, name, points) %>% 
            mutate(week = week)
    } else {
        np <- bind_cols(name, points) %>% 
            mutate(week = week, pos = as.character(position))
    }
    
}

pull_sharks <- function(.season = FALSE) {
    
    if (.season == TRUE) {
        w <- nfl_week:17 
    } else {
        w <- nfl_week
    }

    params <- expand.grid(
        week = w, 
        position = c(97, 7, 6))

    sharks_raw <- params %>% 
        pmap(fetch_sharks) %>% 
        bind_rows()

    sharks_clean <- sharks_raw %>% 
        mutate(points = as.numeric(points)) %>% 
        mutate(position = ifelse(pos == "7", "K", ifelse(pos == "6", "DEF", pos))) %>% 
        separate(name, into = c("last", "first"), extra = "merge", sep = ", ") %>%
        mutate(last = str_trim(last), first = str_trim(first)) %>% 
        mutate(name = str_c(first, last, sep = " ")) %>% 
        select(position, name, week, points) %>% 
        mutate(source = "Fantasy Sharks")
}