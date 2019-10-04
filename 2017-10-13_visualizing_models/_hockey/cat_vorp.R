here::here()
library(tidyverse)

teams <- 10
slots <- 2

df <- read_csv("2017-2018 Fantasy Hockey Projections%2FRankings - Fantasy.csv") %>% 
  drop_na() %>% 
  filter(RANK != "RANK") %>% 
  select(-RANK, -PTS,-PIM) %>% 
  gather(key, value, -PLAYER, -TEAM, -POS) %>% 
  mutate(value = parse_number(value)) %>% 
  spread(key, value) 

avg <- df %>% 
  select(-GP) %>% 
  gather(key, value, -PLAYER, -TEAM, -POS) %>% 
  group_by(POS, key) %>% 
  mutate(stv = (value - mean(value)) / sd(value)) %>% 
  mutate(stv = round(stv, 2)) %>% 
  select(-value) %>% 
  spread(key, stv) %>% 
  mutate(total = `+/-` + A + BLOCKS + G + HITS + PPP + SOG)

df %>% 
  filter(PLAYER %in% c("Jake Muzzin", "Alec Martinez"))

df %>% 
  filter(PLAYER %in% c("Jake Muzzin", "Alec Martinez"))

team <- c(
  "Joe Pavelski", 
  "Patrice Bergeron",
  "Filip Forsberg",
  "Taylor Hall",
  "Blake Wheeler",
  "Viktor Arvidsson",
  "Brent Burns",
  "Mark Giordano",
  "Ivan Provorov",
  "John Carlson",
  "Colton Parayko",
  "Nick Foligno",
  "Henrik Zetterberg",
  "Alec Martinez")

team_df <- avg %>% 
  filter(PLAYER %in% team)


  mutate(fantasy_points = (
    G * 6 + # Goals
    A * 4 + # Assists
    `+/-` * 2 + # Plus/Minus
    PPP * 2 + # Power Play Points
    SOG * 0.9 + # Shots on Goal
    BLOCKS * 1 # Blocks
  )) %>% 
  mutate(fantasy_per_game = fantasy_points / GP) %>% 
  select(player = PLAYER, team = TEAM, position = POS, games = GP, fantasy_points) %>% 
  arrange(desc(fantasy_points))

replacement <- function(pos, slots) {
  
  rp <- df %>% 
    filter(position == pos) %>% 
    arrange(desc(fantasy_points)) %>% 
    filter(row_number() <= slots) %>% 
    group_by(position) %>% 
    summarise(vorp = mean(fantasy_points))
  
  return(rp)
}

vorp <- function(teams=10) {
  
  params <- tribble(
    ~pos, ~slots,
    "C", 2 * teams,
    "LW", 2 * teams, 
    "RW", 2 * teams, 
    "D", 4 * teams)
  
  rp <- params %>% 
    pmap(replacement) %>% 
    bind_rows()
  
  return(rp)
}

df_vorp <- vorp(teams=10)

draft_order <- df %>% 
  left_join(df_vorp, by = "position") %>% 
  mutate(vorp = fantasy_points - vorp) %>% 
  arrange(desc(vorp))

write_csv(draft_order, "draft_order.csv")
