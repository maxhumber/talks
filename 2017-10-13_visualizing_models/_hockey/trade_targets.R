here::here()
library(tidyverse)
library(stringr)

raw <- read_csv("fantasy_hockey_rosters.csv")

df <- raw %>% 
  drop_na(Owner) %>% 
  select(
    owner = Owner, 
    player = `Forwards/Defensemen`,
    ranking_pre = `Pre-Season`,
    ranking_current = `Current`,
    G, A, `P/M` = `#ERROR!`, PPP, SOG, HIT, BLK) %>% 
  gather(key, value, -owner, -player) %>% 
  mutate(value = as.numeric(value)) %>% 
  spread(key, value) %>% 
  drop_na()

total_points <- df %>% 
  select(-player, -ranking_pre, -ranking_current) %>% 
  gather(key, value, -owner) %>% 
  mutate(value = as.numeric(value)) %>% 
  group_by(owner, key) %>% 
  summarise(total = sum(value)) %>% 
  spread(key, total)

category_std <- total_points %>% 
  gather(key, value, -owner) %>% 
  group_by(key) %>% 
  mutate(value = ((value - mean(value))/sd(value)) %>% round(2)) %>% 
  spread(key, value)
  
players <- df %>% 
  mutate(player = str_replace(player, "^(.*Notes)", "")) %>% 
  mutate(player = str_replace(player, "^(.*Note)", "")) %>% 
  mutate(team = word(player, 3)) %>% 
  mutate(position = word(player, 5)) %>% 
  mutate(player = word(player, 1, 2)) %>% 
  mutate(position = str_replace_all(position, "\nInjured|\nOut|\nDay\\-to\\-Day|\\-", "")) %>% 
  separate(position, into = c("position", "p2", "p3"), by = ",")

alternates <- players %>% 
  drop_na(p2) %>% 
  select(-position, -p3) %>% 
  rename(position = p2)

players <- players %>% 
  select(-p2, -p3) %>% 
  bind_rows(alternates)

player_cats <- players %>% 
  gather(category, points, -owner, -player, -ranking_current, -ranking_pre, -team, -position) %>% 
  group_by(position, category) %>% 
  mutate(aa = (points - mean(points)) %>% round(1)) %>% 
  # mutate(pts_std = ((points - mean(points))/sd(points)) %>% round(2)) %>% 
  select(-points) %>% 
  spread(category, aa)

player_targets <- player_cats %>% 
  filter((G >= 0 & PPP >= 0 & `P/M` >= 0))
  filter(owner == "Max" | (G >= 0 & PPP >= 0 & `P/M` >= 0))

comp_cats <- total_points %>%
  gather(category, points, -owner) %>% 
  group_by(category) %>% 
  mutate(sp = points - mean(points)) %>% 
  select(-points) %>% 
  spread(category, sp)


  mutate(unitization = ((points-mean(points))/(max(points) - min(points)))) %>% 
  
  spread()
                      
player_filter <- player_cats %>% filter(owner %in% c("Max", "Dan"))
