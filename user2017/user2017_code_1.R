library(tidyverse)
library(rvest)
library(stringr)

get_movies <- function(ticker) {
    
    url <- str_c("https://www.hsx.com/security/view/", toupper(ticker))
    
    movie <- read_html(url) %>% 
        html_nodes(".credit a") %>% 
        html_text()
    
    link <- read_html(url) %>% 
        html_nodes(".credit a") %>% 
        html_attr("href")
    
    date <- read_html(url) %>% 
        html_nodes("strong") %>% 
        html_text() %>% 
        .[1:length(link)]
    
    df <- tibble(date, movie, link)
    
    return(df)
}

get_price <- function(link) {
    
    if (substr(link, 0, 1) == '/') {
        url <- str_c('https://www.hsx.com', link)
    } else {
        url <- str_c('https://www.hsx.com/security/view/', toupper(link))
    }
    
    df <- read_html(url) %>% 
        html_nodes(".value") %>% 
        html_text() %>% 
        as_tibble() %>% 
        mutate(value = parse_number(str_extract(., "(?<=\\$)[^\\s]+"))) %>% 
        rename(price = value) %>% 
        bind_cols(link = tibble(link))
    return(df)
}

get_prices <- function(df) {

    params <- df %>% select(link)
    
    prices <- pmap(params, get_price) %>% bind_rows()
    
    df <- prices %>% left_join(df, by = "link")
    
    return(df)
}

forward_tag <- function(df) {

    tag <- df %>% 
        mutate(date = as.Date(date, "%b %d, %Y")) %>% 
        drop_na() %>% 
        mutate(days = date - Sys.Date()) %>% 
        mutate(future = ifelse(days >= 0, 'Yes', 'No')) %>% 
        mutate(days = abs(days)) %>% 
        group_by(future) %>% 
        arrange(desc(future), days) %>% 
        mutate(idx = row_number()) %>% 
        ungroup() %>% 
        filter((idx == 1 & future == 'Yes') | (future == "No" & idx <= 5))

    forward <- tag %>% 
        filter(idx <= 4) %>% 
        pull(price) %>% 
        mean(.) %>% 
        round(., 2)
    
    return(forward)
}

adam_driver <- get_movies('adriv') %>% get_prices(.)
forward_tag(adam_driver)
get_price('adriv') %>% pull(price)
