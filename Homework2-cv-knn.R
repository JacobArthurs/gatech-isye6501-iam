# install and load kknn
install.packages("kknn")
library(kknn)

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

# Set K value
k_value <- 5

#Cross validation, k = 10
for (i in 1:10) {
  # Create folds
  validation_fold <- do.call(rbind, split_train_data[i])
  train_fold  <- do.call(rbind, split_train_data[-i])
 
  # Train the model using kknn
  cv_model <- kknn(formula = train_fold[, 11] ~ ., train = train_fold, test = validation_fold, k = k_value, scale = TRUE, kernel = "optimal")
  
  # Get predictions
  cv_pred <- round(fitted(cv_model))
  
  # Calculate accuracy for k fold
  accuracy[i] <- sum(cv_pred == validation_fold[, 11]) / nrow(validation_fold)
}

# Print the average cross validation accuracy
cat("CV accuracy average:", mean(accuracy))

# Evaluate the final model on test_data
final_model <- kknn(formula = train_data[, 11] ~ ., train = train_data, test = test_data, k = k_value, scale = TRUE, kernel = "optimal")

# see what the model predicts
test_pred <- round(fitted(final_model))

# see what fraction of the model’s predictions match the actual classification
cat("Final model accuracy:", sum(test_pred == test_data[, 11]) / nrow(test_data))