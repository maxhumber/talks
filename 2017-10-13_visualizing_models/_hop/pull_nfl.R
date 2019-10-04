library(tidyverse)
library(rvest)
library(stringr)

nfl_week <- ceiling(as.numeric(Sys.Date() - as.Date("2017-09-06")) / 7 )

fetch_nfl <- function(week = 1, position = 1, offset = 0) {
    
    url <- str_c(sep = "",
        "http://fantasy.nfl.com/research/projections?", 
        "statType=weekProjectedStats&statWeek=", week,
            # QB - 1
            # RB - 2
            # WR - 3
            # TE - 4
            # K - 7
            # DEF - 8
        "&position=", position, 
            # increment by 25
        "&offset=", offset)
    
    page <- read_html(url)
    
    name <- page %>% 
        html_nodes("tbody") %>% 
        html_nodes("tr") %>% 
        html_nodes("td.playerNameAndInfo.first") %>% 
        html_text() %>% 
        as_tibble() %>% 
        rename(name = value)
    
    points <- page %>% 
        html_nodes("tbody") %>% 
        html_nodes("tr") %>% 
        html_nodes("td.stat.projected.numeric.last") %>% 
        html_text() %>% 
        as_tibble() %>% 
        rename(points = value)
    
    np <- bind_cols(name, points) %>% 
        mutate(week = week) %>% 
        mutate(position = position)
}

pull_nfl <- function(.season = FALSE) {

    if (.season == TRUE) {
        w <- nfl_week:17 
    } else {
        w <- nfl_week
    }
    
    params <- expand.grid(
        week = w,
        position = c(1, 2, 3, 4, 7, 8), 
        offset = seq(0, 300, 25)) %>% 
        filter(!(position %in% c(1, 4, 7, 8) & offset > 30))
    
    nfl_raw <- params %>% 
        pmap(fetch_nfl) %>% 
        bind_rows()
    
    pos_lookup <- tibble(
        position = c(1, 2, 3, 4, 7, 8),
        pos_real = c("QB", "RB", "WR", "TE", "K", "DEF"))
       
    nfl_clean <- nfl_raw %>% 
        left_join(pos_lookup, by = "position") %>% 
        select(position = pos_real, name, week, points) %>%
        filter(points != "-") %>% 
        mutate(points = as.numeric(points)) %>%
        mutate(name = str_replace(name, "\\-.*$", "")) %>% 
        mutate(name = str_replace(name, "\\sQB\\s|\\sRB\\s|\\sWR\\s|\\sTE\\s|\\sK\\s|\\DEF\\s", "")) %>% 
        mutate(name = str_replace(name, "\\sView Videos", "")) %>% 
        mutate(name = str_replace(name, "\\sView News", "")) %>% 
        mutate(name = str_trim(name)) %>% 
        mutate(source = "NFL.com") 
}
