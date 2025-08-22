# Set seed for consistent results
set.seed(1)

# Create and train k-means model with 3 clusters, using petal data
model <- kmeans(iris[, 3:4], centers = 3)

# Create a table to compare predicted clusters and species
cluster_table <- table(Predicted = model$cluster, Actual = iris[,5])
cluster_table

# For each cluster, assign the most likely species
cluster_species <- apply(cluster_table, 1, function(row) names(row)[which.max(row)])

# Map the model predicted clusters to species
predicted_species <- cluster_species[model$cluster]

# Create a table to compare predicted species and actual species
species_table <- table(Predicted = predicted_species, Actual = iris[,5])
species_table

# See what fraction of the model’s predictions match the actual classification
cat("Clustering accuracy:", sum(diag(species_table)) / nrow(iris))
