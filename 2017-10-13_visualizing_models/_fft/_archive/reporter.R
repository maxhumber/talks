here::here()
library(tidyverse)
library(zoo)

# load data and format column names
raw <- read.csv("reporter-export-feb.csv")
names(raw) <- c(
    "gmt", "datetime", "lat", "long", "weather", "photos", "audio_db", 
    "audio", "steps", "where", "what", "who", "feeling", "moodji")

# wrangle data
reporter <- raw %>%
    select(datetime, feeling, where, what, who, weather) %>%
    mutate(log = 1:length(datetime)) %>%
    filter(!is.na(feeling)) %>%
    # normalize feeling
    mutate(feeling = (feeling - mean(feeling) / sd(feeling))) %>%
    filter(where != "") %>%
    mutate(datetime = as.Date(datetime, format = "%B %d, %Y %I:%M:%S%p")) %>%
    mutate(
        where = as.character(where),
        where = ifelse(
        where == "Velocity" & who == "No one", "MH-204", where),
        where = as.factor(where)) %>%
    mutate(
        what_type = ifelse(
            yes = "Working", no = NA,
            test = grepl("402|271|#fuckjeff|375|375,Reading|Studying", what)),
        what_type = ifelse(
            yes = "Browsing", no = what_type,
            test = grepl("YouTube|Facebook|TeuxDeux|Goodreads|ProductHunt|Reddit|Twitter|Instagram", what)),
        what_type = ifelse(
            yes = "Listening", no = what_type,
            test = grepl("Spotify|SoundCloud|Overcast|Music", what)),
        what_type = ifelse(
            yes = "Exercising", no = what_type,
            test = grepl("Swimming|Walking|Skiing", what)),
        what_type = ifelse(
            yes = "Reading", no = what_type,
            test = grepl("Learning|Reading", what)),
        what_type = ifelse(
            yes = "Gaming", no = what_type,
            test = grepl("Bananagrams|Dots|Exploding Kittens|Pocket Mortys|Games", what)),
        what_type = ifelse(
            yes = "Enjoying", no = what_type,
            test = grepl("^X$|Fucking|Cuddling|Sneaking|Tempeh|Hotubing", what)),
        what_type = ifelse(
            yes = "Commuting", no = what_type,
            test = grepl("Bus|Commuting|Moving|Uber|Traveling", what)),
        what_type = ifelse(
            yes = "Making", no = what_type,
            test = grepl("^R$|Pitching|Larry Smith|Xcode|Moodji|Velocity", what)),
        what_type = ifelse(
            yes = "Eating", no = what_type,
            test = grepl("Dinner|Cooking|Eating|Food|Flavour Tripping", what)),
        what_type = ifelse(
            yes = "Resting", no = what_type,
            test = grepl("Nothing|Resting|Napping|Sleep|Bed|Chilling", what)),
        what_type = ifelse(
            yes = "Partying", no = what_type,
            test = grepl("Drinking|Partying|Drunk|Wine|Socializing", what)),
        what_type = ifelse(
            yes = "Watching", no = what_type,
            test = grepl("YouTube|B99|House of Cards|Movie|Silicon Valley|Superbowl|TV|Zoolander", what)),
        what_type = ifelse(
            yes = "Applying", no = what_type,
            test = grepl("Call|Jobmine|Rejected|Interview", what)),
        what_type = ifelse(
            yes = "Working", no = what_type,
            test = grepl("Calendar|Cleaning|Haskell|Planning|Taxes|Installing", what)),
        what_type = ifelse(
            yes = "Recovering", no = what_type,
            test = grepl("Headache|Hungover|Sick", what)),
        what_type = ifelse(
            yes = "Shopping", no = what_type,
            test = grepl("Shopping", what)),
        what_type = ifelse(
            yes = "Showering", no = what_type,
            test = grepl("Showering", what)),
        what_type = ifelse(
            yes = "Other-ing", no = what_type,
            test = grepl("Haircut|Nspire|Talking|Phone", what)),
        what_type = as.factor(what_type)) %>%
    select(-what) %>%
    rename(what = what_type)

write_csv(reporter, "reporter_edit_1.csv")

    separate(
        who, into = c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 
        extra = "merge", sep = ",", fill = "right") %>%
    gather(
        key = dummy, value = who, 
        -log, -datetime, -weather, -feeling, -what, -where) %>%
    select(-dummy) %>%
    filter(!is.na(who)) %>%
    mutate(who = as.factor(who)) %>%
    mutate(
        where = ordered(where, levels=levels(where)[order(as.numeric(by(feeling, where, mean)))]),
        what = ordered(what, levels=levels(what)[order(as.numeric(by(feeling, what, mean)))]),
        who = ordered(who, levels=levels(who)[order(as.numeric(by(feeling, who, mean)))])) %>%
    droplevels() %>%
    group_by(where) %>%
    mutate(where.n = n()) %>%
    group_by(who) %>%
    mutate(who.n = n()) %>%
    group_by(what) %>%
    mutate(what.n = n())

saveRDS(reporter, file = "reporter.RDS"); rm(raw, reporter)
reporter <- readRDS("reporter.RDS")

ggplot(data = subset(reporter, where.n > 5), aes(
    x = where, y = feeling)) + 
    stat_summary(
        fun.y = "mean", 
        geom = "point", 
        fill = "#600047",
        color = "#770058",
        size = 4) + 
    scale_y_continuous(
        limits = c(-2.5, 2.5),
        breaks = c(-2.5, 0, 2.5),
        labels = c("", "", "")) + 
    coord_flip() + 
    ylab("") + 
    xlab("") + 
    theme_minimal() +
    theme(
        panel.grid.major.y = element_blank(),
        panel.grid.minor.x = element_blank(),
        # panel.grid.major.x = element_blank(),
        panel.background = element_rect(fill = "black", colour = "black"),
        plot.background = element_rect(fill = "black", colour = "black"),
        axis.title.x = element_text(colour = "white"),
        axis.title.y = element_text(colour = "white"),
        axis.text = element_text(colour = "white"))



ggplot(data = subset(reporter, where.n > 5), aes(
    x = where, y = feeling)) + 
    geom_boxplot(aes(
        ymin = ..lower.. , 
        ymax = ..upper.. ), 
        outlier.colour = NA,
        fill = "#770058",
        color = "#600047") + 
    scale_y_continuous(
        limits = c(-2.5, 5),
        breaks = c(-2.5, 0, 2.5, 5),
        labels = c("-2.5", "0", "+2.5", "+5")) + 
    coord_flip() + 
    ylab("Mood") + 
    xlab("") + 
    theme_minimal() +
    theme(
        panel.grid.major.y = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.background = element_rect(fill = "black", colour = "black"),
        plot.background = element_rect(fill = "black", colour = "black"),
        axis.title.x = element_text(colour = "white"),
        axis.title.y = element_text(colour = "white"),
        axis.text = element_text(colour = "white"))




