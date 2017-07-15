library(tidyverse)
library(purrr)
library(rvest)
library(stringr)

fetch_proj <- function(position = 0, offset = 0) { 
    
    url <- str_c(sep = "", 
                 "http://games.espn.com/ffl/tools/projections?",
                 "&slotCategoryId=", position,
                 "&startIndex=", offset)
    
    page <- read_html(url)
    
    df <- page %>% 
        html_node("#playertable_0") %>% 
        html_table()
    
    return(df)
}

params <- expand.grid(
    position = c(0, 2, 4, 6, 16, 17),
    offset = seq(0, 320, 40))

raw <- pmap(params, fetch_proj) %>% bind_rows()

proj <- raw %>% 
    mutate(PLAYERS = ifelse(is.na(PLAYERS), `DEFENSIVE PLAYERS`, PLAYERS)) %>% 
    select(name = PLAYERS, points = TOTAL) %>% 
    mutate(points = parse_number(points)) %>% 
    drop_na() %>% 
    separate(name, into = c("name", "metadata"), sep = ", ", fill = "right") %>% 
    mutate(name = str_replace(name, "D\\/ST\\sD\\/ST|\\*$","")) %>%
    mutate(metadata = str_replace(metadata, "^[^\\s]*\\s","")) %>% 
    mutate(metadata = str_replace(metadata, "IR|Q$|O|SSPD|D", "")) %>% 
    mutate(metadata = str_trim(metadata)) %>% 
    mutate(position = ifelse(is.na(metadata), "DEF", metadata)) %>% 
    select(position, name, points) %>% 
    mutate(source = "ESPN")

params <- tribble(
    ~pos, ~slots,
    "QB", 1,
    "WR", 3, 
    "RB", 2, 
    "TE", 1, 
    "K", 1,
    "DEF", 1
    ) %>% 
    mutate(slots = slots * 10)

replacement_player <- function(pos, slots) {
    rp <- proj %>% 
        filter(position == pos) %>% 
        arrange(desc(points)) %>% 
        filter(row_number() <= slots) %>% 
        group_by(position) %>% 
        summarise(rp = mean(points))
    
    return(rp)
}

rp <- pmap(params, replacement_player) %>% bind_rows()

proj_vorp <- proj %>% 
    left_join(rp, by = "position") %>% 
    mutate(vorp = points - rp) %>% 
    select(position, name, points, vorp) %>% 
    arrange(desc(vorp))
