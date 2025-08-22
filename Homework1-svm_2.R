# install and load kernlab
install.packages("kernlab")
library(kernlab)

# set seed to ensure consistent results
set.seed(1)


# call ksvm. rbfdot is a non-linear kernel.
model <- ksvm(as.matrix(credit_card_data.headers[,1:10]), credit_card_data.headers[,11],
              type="C-svc", kernel="rbfdot", C=93.11104, scaled=TRUE)

# calculate a1…am
a <- colSums(model@xmatrix[[1]] * model@coef[[1]])
a

# calculate a0
a0 <- -model@b
a0

# see what the model predicts
pred <- predict(model, credit_card_data.headers[,1:10])
pred

# see what fraction of the model’s predictions match the actual classification
sum(pred == credit_card_data.headers[,11]) / nrow(credit_card_data.headers)

