library(tidyverse)
library(ggridges)
here::here()

# devtools::install_github("dgrtwo/gganimate")
library(gganimate)

# turtles

turtles <- c(
    48, 24, 51, 12, 
    21, 41, 25, 23, 
    32, 61, 19, 24, 
    29, 21, 23, 13, 
    32, 18, 42, 18
)

turtles %>% mean() %>% round(1)

se <- function(x) sqrt(var(x)/length(x))
turtles %>% se() %>% round(1)

xbar <- numeric(10000)
for(i in 1:10000) {
    x <- sample(turtles, 20, replace=TRUE) %>% mean()
    xbar[i] <- x
}

df <- xbar %>% 
    as_data_frame() %>% 
    mutate(sim = row_number())

df %>% 
    ggplot(aes(x = value)) + 
    geom_histogram(binwidth = 1) +
    labs(x = "xbar")

df %>% 
    ggplot(aes(x = "Turtles", y = value)) +
    geom_boxplot()

df %>% 
    ggplot(aes(x = value)) + 
    geom_density(fill = "#ce0000", alpha = 1/2)

df %>% 
    summarise(
        mean = mean(value), 
        low = quantile(value, 0.025),
        high = quantile(value, 0.975)) %>% 
    ggplot(aes(x = "Turtle", y = mean)) +
    geom_errorbar(aes(ymin = low, ymax = high))

if(!exists("pull_nfl", mode = "function")) source("pull_nfl.R")
if(!exists("pull_sharks", mode = "function")) source("pull_sharks.R")
if(!exists("pull_pros", mode = "function")) source("pull_pros.R")
if(!exists("pull_espn", mode = "function")) source("pull_espn.R")

project <- function() {

    df_nfl <- pull_nfl()
    df_sharks <- pull_sharks()
    df_pros <- pull_pros()
    df_espn <- pull_espn()
    
    proj_all <- tibble() %>% 
        bind_rows(df_nfl) %>% 
        full_join(df_sharks) %>% 
        full_join(df_pros) %>% 
        full_join(df_espn)
}

df <- project()
df <- read_csv("df.csv")
write_csv(df, "df.csv")

home <- c(
    "Tyrod Taylor", "Jameis Winston",
    "Terrance West", "Ezekiel Elliott",
    "A.J. Green", "Larry Fitzgerald", "Adam Thielen", 
    "Marqise Lee",
    "Jack Doyle", 
    "Ka'imi Fairbairn",
    "Dallas Cowboys"
)

df %>% 
    filter(name %in% home) %>% 
    ggplot(aes(x = points, y = reorder(name, points), fill = position)) + 
    geom_density_ridges(scale = 1.25, alpha = 1) + 
    labs(y = "", x = "Fantasy Points", fill = "")

away <- c(
    "Matthew Stafford", "Jared Goff",
    "DeMarco Murray", "Jordan Howard",
    "Demaryius Thomas", "Sammy Watkins", "Jamison Crowder",
    "Eric Ebron",
    "Chris Carson",
    "Steven Hauschka",
    "New England Patriots"
)

sim <- function(df=df, players) {

    points <- df %>% 
        filter(name %in% players) %>% 
        group_by(name) %>% 
        sample_n(1, replace = TRUE) %>% 
        ungroup() %>% 
        summarise(total = sum(points)) %>% 
        pull(total)
        
    return(points)
}

sim(df, home)
sim(df, away)

sim_home <- replicate(100, sim(df, home))
sim_away <- replicate(100, sim(df, away))

sim_home <- sim_home %>% as_data_frame() %>% mutate(team = "home")
sim_away <- sim_away %>% as_data_frame() %>% mutate(team = "away")

sim_all <- bind_rows(sim_home, sim_away) %>% 
    group_by(team) %>% 
    mutate(sim = row_number())

sim_all %>% 
    ggplot(aes(y = value, x = team)) + 
    geom_boxplot() + 
    labs(x = "", y = "Fantasy Points")

sim_all %>% 
    ggplot(aes(x = value, fill = team)) + 
    geom_density(alpha = 1/2) + 
    scale_fill_manual(values = c("red", "blue")) + 
    labs(y = "", x = "Fantasy Points", fill = "")

sim_all %>% 
    ggplot(aes(x = team, y = value)) +
    geom_errorbar(aes(ymin = value, ymax = value)) + 
    labs(x = "", y = "Fantasy Points")

p <- sim_all %>% 
    ggplot(aes(x = team, y = value, frame = sim)) +
    geom_errorbar(aes(ymin = value, ymax = value)) + 
    labs(x = "", y = "Fantasy Points")

gganimate(p, title_frame = FALSE)
gganimate(p, filename = "hop1.gif", title_frame = FALSE)

p <- sim_all %>%
  ggplot(aes(x = team, y = value)) +
  geom_errorbar(aes(
    ymin = value, ymax = value, 
    frame = sim, cumulative = TRUE), 
    color = "grey80", alpha = 1/8) +
  geom_errorbar(aes(
    ymin = value, ymax = value, frame = sim), 
    color = "#00a9e0") +
  scale_y_continuous(limits = c(0, 150)) +
  theme(panel.background = element_rect(fill = "#FFFFFF")) +
  labs(title = "", y = "Fantasy Points", x = "")

gganimate(p, title_frame = FALSE)
gganimate(p, filename = "hop2.gif", title_frame = FALSE)
