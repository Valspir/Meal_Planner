SELECT
  Ingredients.recipeID,
  Ingredients.ingredientID as iid,
  (SELECT
    procText
    FROM AltText
    WHERE ingredientID=Ingredients.ingredientID
    LIMIT 1),
  Cost.cost
FROM Ingredients
INNER JOIN Cost
  ON Ingredients.ingredientID=Cost.ingredientID
WHERE Ingredients.recipeID=1;
