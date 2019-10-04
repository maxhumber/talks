library(tidyverse)
library(rvest)
library(stringr)

nfl_week <- ceiling(as.numeric(Sys.Date() - as.Date("2017-09-06")) / 7 )

fetch_espn <- function(week, position = 0, offset = 0) { 

    url <- str_c(sep = "", 
        "http://games.espn.com/ffl/tools/projections?",
        "&scoringPeriodId=", week, 
        "&seasonId=2017",
        "&slotCategoryId=", position,
        "&startIndex=", offset)
    
    page <- read_html(url)
    
    df <- page %>% 
        html_node("#playertable_0") %>% 
        html_table()
}

pull_espn <- function() {

    params <- expand.grid(
        week = nfl_week,
        position = c(0, 2, 4, 6, 16, 17),
        offset = seq(0, 320, 40)) %>% 
        filter(!(position %in% c(0, 6, 16, 17) & offset > 40))
    
    espn_raw <- params %>% 
        pmap(fetch_espn) %>% 
        bind_rows()
    
    espn_clean <- espn_raw %>% 
        mutate(PLAYERS = ifelse(is.na(PLAYERS), `DEFENSIVE PLAYERS`, PLAYERS)) %>% 
        select(name = PLAYERS, points = TOTAL) %>% 
        mutate(points = parse_number(points)) %>% 
        drop_na() %>% 
        mutate(week = nfl_week) %>% 
        separate(name, into = c("name", "junk"), sep = ", ", fill = "right") %>% 
        mutate(name = str_replace(name, "D\\/ST\\sD\\/ST|\\*$","")) %>%
        mutate(junk = str_replace(junk, "^[^\\s]*\\s","")) %>% 
        mutate(junk = str_replace(junk, "IR|Q$|O|SSPD|D", "")) %>% 
        mutate(junk = str_trim(junk)) %>% 
        mutate(position = ifelse(is.na(junk), "DEF", junk)) %>% 
        select(position, name, week, points) %>% 
        mutate(source = "ESPN")
}