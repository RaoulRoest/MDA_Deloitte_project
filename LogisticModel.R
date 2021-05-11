library(tidyverse)  
library(modelr)     
library(broom)      
library(pROC)
library(caret)
# Load data 

trainset <- read.csv(data)
testset <- read.csv(data)

#Logistic
model_glm = glm(targval ~, data = trainset, family = "binomial") #every variable included
coef(model_glm)

pred1=predict(model_glm, type = "response") #probabilities

model_glm_pred = ifelse(predict(model_glm, type = "link") > 0.5, "Yes", "No") #Classification

calc_class_err = function(actual, predicted) { #training error
  mean(actual != predicted)
}

calc_class_err(actual = data$var, predicted = model_glm_pred)

train_con_mat = confusionMatrix(train_tab, positive = "Yes") #confusion matrix
getCM = c(train_con_mat$overall["Accuracy"], 
          train_con_mat$byClass["Sensitivity"], 
          train_con_mat$byClass["Specificity"])


plot(var ~ , data = data, 
     col = "red", pch = "|", ylim = c(-0.2, 1),
     main = "Classifying Prepayments")
abline(h = 0, lty = 3)
abline(h = 1, lty = 3)
abline(h = 0.5, lty = 2)
curve(predict(model_glm, data.frame(balance = x), type = "response"), 
      add = TRUE, lwd = 3, col = "dodgerblue")
abline(v = -coef(model_glm)[1] / coef(model_glm)[2], lwd = 2)

get_logistic_error = function(mod, data, res = "y", pos = 1, neg = 0, cut = 0.5) { #error for different cutoffs
  probs = predict(mod, newdata = data, type = "response")
  preds = ifelse(probs > cut, pos, neg)
  calc_class_err(actual = data[, res], predicted = preds)
}



model_1 = glm(variable ~ ., data = data, family = "binomial") #models with different predictors
model_2 = glm(variable ~ ., data = data, family = "binomial")
model_3 = glm(variable ~ ., data = data, family = "binomial")


model_list = list(model_1, model_2, model_3)
train_errors = sapply(model_list, get_logistic_error, data = data, 
                      res = "default", pos = "Yes", neg = "No", cut = 0.5)
test_errors  = sapply(model_list, get_logistic_error, data = data,
                      res = "default", pos = "Yes", neg = "No", cut = 0.5)



get_logistic_pred = function(mod, data, res = "y", pos = 1, neg = 0, cut = 0.5) {
  probs = predict(mod, newdata = data, type = "response")
  ifelse(probs > cut, pos, neg)
}

test_pred_1 = get_logistic_pred(model_glm, data = default_tst, res = "default", #different cutoffs to test
                                pos = "Yes", neg = "No", cut = 0.1)
test_pred_5 = get_logistic_pred(model_glm, data = default_tst, res = "default", 
                                pos = "Yes", neg = "No", cut = 0.5)
test_pred_9 = get_logistic_pred(model_glm, data = default_tst, res = "default", 
                                pos = "Yes", neg = "No", cut = 0.9)

test_tab_1 = table(predicted = test_pred_1, actual = testset$variable) #confusion matrices for the cutoffs
test_tab_5 = table(predicted = test_pred_5, actual = testset$variable)
test_tab_9 = table(predicted = test_pred_9, actual = testset$variable)

test_con_mat_1 = confusionMatrix(test_tab_1, positive = "Yes")
test_con_mat_5 = confusionMatrix(test_tab_5, positive = "Yes")
test_con_mat_9 = confusionMatrix(test_tab_9, positive = "Yes")

metrics = rbind(
  
  c(test_con_mat_1$overall["Accuracy"], 
    test_con_mat_1$byClass["Sensitivity"], 
    test_con_mat_1$byClass["Specificity"]),
  
  c(test_con_mat_5$overall["Accuracy"], 
    test_con_mat_5$byClass["Sensitivity"], 
    test_con_mat_5$byClass["Specificity"]),
  
  c(test_con_mat_9$overall["Accuracy"], 
    test_con_mat_9$byClass["Sensitivity"], 
    test_con_mat_9$byClass["Specificity"])
  
)

rownames(metrics) = c("c = 0.10", "c = 0.50", "c = 0.90")
metrics

library(pROC)
test_prob = predict(model_glm, newdata = testset, type = "response")
test_roc = roc(testset$var ~ test_prob, plot = TRUE, print.auc = TRUE)
as.numeric(test_roc$auc)

