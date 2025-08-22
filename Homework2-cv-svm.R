# install and load kernlab
install.packages("kernlab")
library(kernlab)

# set seed to ensure consistent results
set.seed(1)

# Split the data into training (80%) and testing (20%)
train_sample <- sample(1:nrow(credit_card_data.headers), size = 0.8 * nrow(credit_card_data.headers))
train_data <- credit_card_data.headers[train_sample, ]
test_data <- credit_card_data.headers[-train_sample, ]

# Split train_data into 10 groups
fold_splits <- cut(1:nrow(train_data), breaks = 10, labels = FALSE)
split_train_data <- split(train_data, fold_splits)

# Vector to store cross-validation accuracies
accuracy <- numeric(10)

# Set C value
c_value <- 0.00148

#Cross validation, k = 10
for (i in 1:10) {
  # Create folds
  validation_fold <- do.call(rbind, split_train_data[i])
  train_fold  <- do.call(rbind, split_train_data[-i])
  
  # Train the model using ksvm
  cv_model <- ksvm(x = as.matrix(train_fold[, 1:10]), y = train_fold[, 11], type = "C-svc", kernel = "vanilladot", C = c_value, scaled = TRUE)
  
  # Model prediction using validation_fold
  cv_pred <- predict(cv_model, as.matrix(validation_fold[, 1:10]))
  
  # Calculate accuracy for k fold
  accuracy[i] <- sum(cv_pred == validation_fold[, 11]) / nrow(validation_fold)
}

# Print the average cross validation accuracy
cat("CV accuracy average:", mean(accuracy))

# Evaluate the final model on test_data
final_model <- ksvm(x = as.matrix(train_data[,1:10]), y = train_data[,11], type="C-svc", kernel="vanilladot", C = c_value, scaled = TRUE)

# see what the model predicts
test_pred <- predict(final_model, test_data[,1:10])

# see what fraction of the model’s predictions match the actual classification
cat("Final model accuracy:", sum(test_pred == test_data[, 11]) / nrow(test_data))