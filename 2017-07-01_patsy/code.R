# PREAMBLE

library(tidyverse)

df <- read_csv("canada.csv")

ggplot(df, aes(x = beer, y = warm)) + 
    geom_point(aes(shape = family, color = factor(canada)), size = 2, alpha = 0.75) +
    scale_shape_manual(values = c('Yes' = 16, 'No' = 17)) + 
    scale_color_manual(values = c('0' = 'blue', '1' = 'red')) + 
    labs(shape = "Family", y = "Importance of Warm Climate", x = "Importance of Good Beer", color = "Canada")

# ACTUAL INSTRUCTIONS

# 0 - load the TIDYVERSE

library(tidyverse)

# 1 - load data

df <- read_csv("canada.csv")

# 2 - test/train split

TI <- caret::createDataPartition(y=df$canada, p=0.80, list=FALSE)
train <- df[TI, ]
test <- df[-TI, ] 

# 3 - model

mod <- glm(canada ~ beer + warm + family, data=train, family='binomial')

# 4 - peak

summary(mod)

# 5 - predict
 
test$pred <- predict(mod, test, 'response')

# 6 - verify 

library(plotROC)

p <- ggplot(test, aes(d = canada, m = pred)) + geom_roc()

calc_auc(p)$AUC



