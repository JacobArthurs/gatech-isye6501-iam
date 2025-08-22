import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value, LpBinary

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

# Define food selection and quantity
food_vars = {item: LpVariable(f"qty_{item}", lowBound=0) for item in food_items}
food_selected = {item: LpVariable(f"select_{item}", cat=LpBinary) for item in food_items}

# Minimize cost
prob += lpSum(costs[item] * food_vars[item] for item in food_items)

# Add nutrient constraints
for nutrient in nutrients:
    prob += lpSum(data.loc[i, nutrient] * food_vars[item] for i, item in enumerate(food_items)) >= min_constraints[nutrient]
    prob += lpSum(data.loc[i, nutrient] * food_vars[item] for i, item in enumerate(food_items)) <= max_constraints[nutrient]

# If food is selected, minimum 1/10 serving must be chosen
for item in food_items:
    prob += food_vars[item] <= 1000 * food_selected[item]
    prob += food_vars[item] >= 0.1 * food_selected[item]

# At most one of celery and frozen broccoli can be selected
celery_index = food_items.index("Celery, Raw") if "Celery, Raw" in food_items else -1
broccoli_index = food_items.index("Frozen Broccoli") if "Frozen Broccoli" in food_items else -1

if celery_index >= 0 and broccoli_index >= 0:
    celery = food_items[celery_index]
    broccoli = food_items[broccoli_index]
    prob += food_selected[celery] + food_selected[broccoli] <= 1

# Define meats
meat_categories = [
    "Roasted Chicken",
    "Poached Eggs",
    "Scrambled Eggs",
    "Bologna,Turkey",
    "Frankfurter, Beef",
    "Ham,Sliced,Extralean",
    "Kielbasa,Prk",
    "Pizza W/Pepperoni",
    "Taco",
    "Hamburger W/Toppings",
    "Hotdog, Plain",
    "Pork",
    "Sardines in Oil",
    "White Tuna in Water",
    "Splt Pea&Hamsoup",
    "Beanbacn Soup,W/Watr",
    "Vegetbeef Soup",
    "Neweng Clamchwd",
    "Chicknoodl Soup"
]

# At least 3 kinds of meat/poultry/fish/eggs must be selected
if len(meat_categories) > 0:
    prob += lpSum(food_selected[item] for item in meat_categories) >= 3

# Solve LP problem
prob.solve()

# Print results
print("Optimal Diet:")
for item in food_items:
    if food_vars[item].varValue > 0:
        print(f"{item}: {food_vars[item].varValue:.2f} servings")
print(f"Total cost: ${value(prob.objective):.2f}")