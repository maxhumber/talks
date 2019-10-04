library(tidyverse)
library(rvest)
library(stringr)

nfl_week <- ceiling(as.numeric(Sys.Date() - as.Date("2017-09-06")) / 7 )

fetch_pros <- function(position = "qb") {
    
    url <- str_c(sep = "",
        "https://www.fantasypros.com/nfl/projections/",
        position, ".php?scoring=STD")
    
    page <- read_html(url) 
    
    name <- page %>% 
        html_nodes("tr") %>% 
        html_nodes(".player-label") %>% 
        html_text() %>% 
        as_tibble() %>% 
        filter(row_number() != 1) %>% 
        rename(name = value)
    
    points_child <- ifelse(
        position == "qb", 11, ifelse(
        position == "rb", 9, ifelse(
        position == "wr", 9, ifelse(
        position == "te", 6, ifelse(
        position == "k", 5, ifelse(
        position == "dst", 11, NA))))))
    
    points <- page %>% 
        html_nodes("tr") %>% 
        html_nodes(str_c(".center:nth-child(", points_child,")")) %>% 
        html_text() %>% 
        as_tibble() %>% 
        rename(points = value)
    
    pros <- bind_cols(name, points) %>% 
        mutate(week = nfl_week) %>% 
        mutate(pos = toupper(position))
}

pull_pros <- function() {
    
    params <- c("qb", "wr", "rb", "te", "k", "dst")
    
    pros_raw <- map(params, fetch_pros) %>% 
        bind_rows()
    
    pros_clean <- pros_raw %>% 
        mutate(points = as.numeric(points)) %>% 
        mutate(name = str_trim(name)) %>% 
        mutate(pos = ifelse(pos == "DST", "DEF", pos)) %>% 
        mutate(name = ifelse(pos == "DEF", name, str_replace(name, "\\s[^ ]+$", ""))) %>% 
        mutate(source = "Fantasy Pros")  %>% 
        select(position = pos, name, week, points, source)
}
