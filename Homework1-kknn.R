# install and load kknn
install.packages("kknn")
library(kknn)

# set seed to ensure consistent results
set.seed(1)

# create an empty vector to store predictions
pred <- numeric(nrow(credit_card_data.headers))

# loop through each data point
for (i in 1:nrow(credit_card_data.headers)) {
  model <- kknn(credit_card_data.headers[-i, 11] ~ ., credit_card_data.headers[-i,1:10], 
             credit_card_data.headers[i,], k=12, scale=TRUE)
  
  # store the prediction for the ith data point
  pred[i] <- round(fitted(model))
}

# see what the model predicts
pred

# see what fraction of the model’s predictions match the actual classification
sum(pred == credit_card_data.headers[, 11]) / nrow(credit_card_data.headers)
