#libraries
library(dplyr)
library(caret)
library(glmnet)
library(e1071)
library(nnet)

#load data

mytrainf<-read.csv("C:/Users/arkal/Downloads/Test_train_time/Train/Train_OriginateData_2013-2020.csv", sep = ",")
mytrainf<-mytrainf[,-1]
mytestf<-read.csv("C:/Users/arkal/Downloads/Test_train_time/Test/Test_OriginateData_2013-2020.csv", sep = ",")
mytestf<-mytestf[,-1]

mytrainnames<-read.csv("C:/Users/arkal/Downloads/Test_train_time/Train/Train_columnNames_2013-2020.csv", sep = ";")
mytestnames<-read.csv("C:/Users/arkal/Downloads/Test_train_time/Test/Test_columnNames_2013-2020.csv", sep = ";")
mytrainnames<-t(mytrainnames)
mytestnames<-t(mytestnames)

names(mytrainf)<-mytrainnames
names(mytestf)<-mytestnames

a<-filter(mytrainf,mytrainf$prepayment_type_before_timestep_63==2)
mytrainf<-setdiff(mytrainf,a)
b<-filter(mytestf,mytestf$prepayment_type_before_timestep_63==2)
mytestf<-setdiff(mytestf,b)


mytrainf<-mytrainf[,-c(193:197)]
mytestf<-mytestf[,-c(193:197)]
mytrainf<-mytrainf[,-1]
mytestf<-mytestf[,-1]

mytrainf$prepayment_type_after_timestep_63<-as.factor(mytrainf$prepayment_type_after_timestep_63)
mytestf$prepayment_type_after_timestep_63<-as.factor(mytestf$prepayment_type_after_timestep_63)





set.seed(1245)

combined<-bind_rows(mytrainf,mytestf)




#lasso

X<-combined[,-192]



#Cleared manually state seller servicer

glmnet1<-cv.glmnet(x= model.matrix(~., X) , y=combined$prepayment_type_after_timestep_63, family = "multinomial", alpha=1)
glmnet1

c<-coef(glmnet1,s=glmnet1$lambda.1se)
c
d<-c[["2"]]@i
d<-d[-1]
variables<-colnames(mytrainf)[d] 



featdata<-mytrainf[,d]
featdata<-bind_cols(featdata,mytrainf$prepayment_type_after_timestep_63)
colnames(featdata)
names(featdata)[names(featdata) == "...58"] <- "prepayment_type_after_timestep_63"
feattest<-mytestf[,d]
feattest<-bind_cols(feattest,mytestf$prepayment_type_after_timestep_63)
names(feattest)[names(feattest) == "...58"] <- "prepayment_type_after_timestep_63"

#Logistic
#Full
model_glm = multinom(mytrainf$prepayment_type_after_timestep_63 ~., data = mytrainf) #every variable included
model_glm
coef(model_glm)

pred1=predict(model_glm, type = "probs") #probabilities
pred1

#Test ROC full
library(pROC)
test_prob = predict(model_glm, newdata = mytestf, type = "probs")
test_roc = multiclass.roc(mytestf$prepayment_type_after_timestep_63 ~ test_prob, print.auc = TRUE)
fullauc<-as.numeric(test_roc$auc)
fullauc

#Reduced
model_glm1 = multinom(featdata$prepayment_type_after_timestep_63 ~., data = featdata) #reduced
model_glm1
coef(model_glm1)

pred2=predict(model_glm1, type = "probs") #probabilities
pred2


#Test ROC reduced
test_prob = predict(model_glm1, newdata = feattest, type = "probs")
test_roc = multiclass.roc(feattest$prepayment_type_after_timestep_63 ~ test_prob, print.auc = TRUE)
redauc<-as.numeric(test_roc$auc)
redauc