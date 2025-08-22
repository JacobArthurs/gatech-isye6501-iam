import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value

# Read data and ignore summary rows
data = pd.read_excel('./diet.xls', sheet_name="Sheet1")
data = data.iloc[:-3]

# Extract data
food_items = list(data['Foods'])
costs = dict(zip(food_items, data['Price/ Serving']))

# Define columns
nutrients = ["Calories", "Cholesterol mg", "Total_Fat g", "Sodium mg", "Carbohydrates g",
            "Dietary_Fiber g", "Protein g", "Vit_A IU", "Vit_C IU", "Calcium mg", "Iron mg"]

# Define nutritional constraints
min_constraints = {
    "Calories": 1500, "Cholesterol mg": 30, "Total_Fat g": 20, "Sodium mg": 800,
    "Carbohydrates g": 130, "Dietary_Fiber g": 125, "Protein g": 60, "Vit_A IU": 1000,
    "Vit_C IU": 400, "Calcium mg": 700, "Iron mg": 10
}
max_constraints = {
    "Calories": 2500, "Cholesterol mg": 240, "Total_Fat g": 70, "Sodium mg": 2000,
    "Carbohydrates g": 450, "Dietary_Fiber g": 250, "Protein g": 100, "Vit_A IU": 10000,
    "Vit_C IU": 5000, "Calcium mg": 1500, "Iron mg": 40
}

# Setup LP problem
prob = LpProblem("Diet Optimization", LpMinimize)
food_vars = {item: LpVariable(item, lowBound=0) for item in food_items}
prob += lpSum(costs[item] * food_vars[item] for item in food_items)

# Add nutrient constraints
for nutrient in nutrients:
    prob += lpSum(data.loc[i, nutrient] * food_vars[item] for i, item in enumerate(food_items)) >= min_constraints[nutrient]
    prob += lpSum(data.loc[i, nutrient] * food_vars[item] for i, item in enumerate(food_items)) <= max_constraints[nutrient]

# Solve LP problem
prob.solve()

# Print results
print("Optimal Diet:")
for item in food_items:
    if food_vars[item].varValue > 0:
        print(f"{item}: {food_vars[item].varValue:.2f} servings")
print(f"Total cost: ${value(prob.objective):.2f}")