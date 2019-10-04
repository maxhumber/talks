here::here()
library(tidyverse)

df <- read_csv("df.csv") %>% select(-log)

# 2 - test/train split

set.seed(111)
TI <- caret::createDataPartition(y=df$happy, p=0.80, list=FALSE)
train <- df[TI, ]
test <- df[-TI, ] 

# 3 - model

mod <- glm(happy ~ ., data=train, family='binomial')

# 4 - peak

summary(mod)

# 5 - predict

test$pred <- predict(mod, test, 'response')

# 6 - verify 

library(plotROC)

p <- ggplot(test, aes(d = happy, m = pred)) + geom_roc(labels=FALSE) + geom_abline(slope=1, lty=3)

calc_auc(p)$AUC

# confusion matrix 

test$pred <- predict(mod, test, type="response")
test$pred <- ifelse(test$pred >= 0.5, 1, 0)
table(test$happy, test$pred)

table(test$happy, test$pred) %>% 
  as_data_frame() %>% 
  rename(truth=Var1, decision=Var2) %>% 
  mutate(truth=ifelse(truth==1, "Happy", "Not Happy")) %>% 
  mutate(decision=ifelse(decision==1, "Happy", "Not Happy")) %>% 
  ggplot(aes(x = truth, y = decision)) + 
  geom_point(aes(shape=decision, color=truth, size=n), show.legend = FALSE) + 
  geom_text(aes(label = n)) + 
  scale_size_continuous(range = c(5, 20)) + 
  scale_color_manual(values = c("green", "red"))
  

########

# install.packages("FFTrees")  
library(FFTrees)

fft <- FFTrees(happy ~., data = train, main = "Happy", decision.labels = c("Not Happy", "Happy"))

plot(fft,tree=2)

inwords(fft)

importance <- fft$comp$rf$model$importance
importance <- data.frame(cue = rownames(fft$comp$rf$model$importance), importance = importance[,1])
importance <- importance[order(importance$importance),]
yarrr::pirateplot(formula = importance ~ cue, data = importance, sortx = "s", bar.f.o = .5, bar.f.col = "blue")

test$pred <- as.integer(predict(fft, data = test))
