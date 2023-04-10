UPDATE Recipes
SET cost=(SELECT (ROUND(SUM((SELECT cost FROM Cost WHERE Cost.ingredientID=Ingredients.ingredientID)),2)) FROM Ingredients WHERE Ingredients.recipeID=Recipes.recipeID)
