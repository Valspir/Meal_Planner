var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var serveStatic = require('serve-static');
var sqlite = require("better-sqlite3");


var db = new sqlite("./data/processedData.db");


async function get7recipes(req) {
  highID = req["_parsedOriginalUrl"]["query"].split("=")[1]
  var db = new sqlite("./data/processedData.db");
  var rows = db.prepare("SELECT recipeName FROM Recipes WHERE recipeID < "+highID+" ORDER BY recipeID DESC LIMIT 7").all();
  var recipes = [];
  /*console.log(rows)
  for(let i = 0; i < rows.length; i++) {
    recipes.push(rows[i]["recipeName"]);
  }
  db.close();
  console.log(recipes);*/
  return rows;
}



function findRecipe(keywords,serves) {
  sql = "SELECT recipeID,recipeName,meat,cost FROM Recipes WHERE serves > ?"
  keywords.forEach((keyword, i) => {


    //Do Nothing Yet
  });

  db.each(sql,[serves], (err, row) => {
    console.log(row);
  });
  db.close();
}

function search(req,res) {
  allArgs = decodeURI(req["_parsedOriginalUrl"]["query"]).split("&")
  //var db = new sqlite("./data/processedData.db");
  let procSQL = "(SELECT procText FROM AltText WHERE ingredientID=Ingredients.ingredientID LIMIT 1) LIKE '%"
  sql = "SELECT DISTINCT Recipes.recipeID as recipeID, recipeName, steps, saves, cost, serves, prepTime, cookTime FROM Recipes INNER JOIN Ingredients ON Recipes.recipeID=Ingredients.recipeID WHERE "
  rowArr = []
  for(let i = 0; i < allArgs.length; i++) {
    /*if(i%100 || i == allArgs.length-1) {
      rows = db.prepare(sql).all();
      for(row in rows) {
        rowArr.push(rows[row])
      }
      sql = "SELECT DISTINCT Recipes.recipeID as recipeID, recipeName, steps, saves, cost, serves, prepTime, cookTime FROM Recipes INNER JOIN Ingredients ON Recipes.recipeID=Ingredients.recipeID WHERE "

    }*/
    show=0
    var argName = allArgs[i].split("=")[0];
    var argValue = allArgs[i].split("=")[1];
    if(argName == "keywords") {
      argValue = argValue.replace("+", " ").replace("%2C",",").split(",")
      for(let j = 0; j < argValue.length; j++) {
        if(j > 0) {
          sql += " OR "
        }
        if(argValue[j][0] == " ") {
          argValue[j] = argValue[j].substring(1)
        }
        sql+="((Recipes.recipeName LIKE '%"+argValue[j]+"%') OR ("+procSQL+argValue[j]+"%'))"
      }
    }else if(argName == "serves") {
      sql +=" AND (Recipes.serves >= "+argValue+")"
    }else if(argName == "prepTime") {
      sql += " AND (Recipes.prepTime <= "+parseInt(argValue)+")"
    }else if(argName == "cookTime") {
      sql += " AND (Recipes.cookTime <= "+parseInt(argValue)+")"
    }else if(argName == "show") {
      show=1
      sql +=" ORDER BY saves DESC LIMIT "+argValue
    }
  }
  if(!show) {
    sql += "ORDER BY saves DESC LIMIT 30"
  }
  console.log("Done building")
  //rows = the_ALGORITHM(sql)
  //sql = "SELECT * FROM Recipes WHERE "
  /*for(row in rows) {
    if(row != 0) {
      sql += " OR "
    }
    sql += `recipeID=${rows[row]}`
  }*/
  rows = db.prepare(sql).all();
  allInfo = []
  console.log(rows.length)
  for(i = 0; i < rows.length; i++) {
    row = rows[i]
    sql = `SELECT AD.procText FROM (SELECT Ingredients.recipeID as recipeID, Ingredients.ingredientID as ingredientID, AltText.procText as procText FROM Ingredients INNER JOIN AltText ON Ingredients.ingredientID=AltText.ingredientID WHERE Ingredients.recipeID=${row.recipeID} GROUP BY AltText.ingredientID) as AD INNER JOIN Recipes ON AD.recipeID=Recipes.recipeID`
    ret = db.prepare(sql).all();
    row.ingredients = ret
    allInfo.push(row)
  }
  res.json(allInfo)
}

function genMealPlan(req,res) {
  allArgs = decodeURI(req["_parsedOriginalUrl"]["query"]).split("&")
  sql = "SELECT * from Recipes ORDER BY RANDOM() LIMIT 50"
  row = the_ALGORITHM(sql)
  //console.log(row)
  sql = `SELECT * FROM Recipes WHERE recipeID=${row.Recipe2ID}`
  /*console.log(rows)
  for(row in rows) {
    if(row != 0) {
      sql += " OR "
    }
    sql += `recipeID=${rows[row]}`
  }*/
  rows = db.prepare(sql).all();
  allInfo = []

  for(i = 0; i < rows.length; i++) {
    row = rows[i]
    sql = `SELECT AD.procText FROM (SELECT Ingredients.recipeID as recipeID, Ingredients.ingredientID as ingredientID, AltText.procText as procText FROM Ingredients INNER JOIN AltText ON Ingredients.ingredientID=AltText.ingredientID WHERE Ingredients.recipeID=${row.recipeID} GROUP BY AltText.ingredientID) as AD INNER JOIN Recipes ON AD.recipeID=Recipes.recipeID`
    ret = db.prepare(sql).all();
    row.ingredients = ret
    allInfo.push(row)
  }
  res.json(allInfo)
}

function the_ALGORITHM(sql,user=[{0: 4, 1: 2, 73: 4, 74: 8, 75: 8, 76: 4, 77: 0, 78: 5, 79: 2,1509: 3, 1510: 0, 1511: 7, 2067: 1, 2068: 1}]) { //PLEASE REWRITE ME I AM SCREAMING IN PAIN
  allRows = []
  for(recipeKey in user[0]) {
    try {
      recipeID = user[0][recipeKey]
      not_sql = `SELECT
              i1.recipeID as Recipe1ID,
              (
              	SELECT
              		Recipes.recipeName
              	FROM Recipes
              		WHERE recipeID=i1.recipeID
              ) as Recipe1Name,
              r2.recipeID as Recipe2ID,
              r2.recipeName as Recipe2Name,
              COUNT(*) AS num_common_ingredients,
              ROUND(
              	(COUNT(*) * 100.0 /
                			(SELECT COUNT(*) FROM Ingredients WHERE recipeID = i1.recipeID) +
                 			(SELECT COUNT(*) FROM Ingredients WHERE recipeID = r2.recipeID) -
                 			COUNT(CASE WHEN i1.recipeID = r2.recipeID THEN 1 ELSE NULL END)),2
                 	) AS similarity_percentage
            FROM Ingredients AS i1
            JOIN Ingredients AS i2
            	ON i1.ingredientID = i2.ingredientID
            	AND i1.recipeID = ${recipeID}
            	AND i2.recipeID <> i1.recipeID
            JOIN (${sql}) AS r2
            	ON i2.recipeID = r2.recipeID
            GROUP BY r2.recipeID
            ORDER BY similarity_percentage DESC
            LIMIT 10
            `;
      var rows = db.prepare(not_sql).all();
      for(row in rows) {
        allRows.push(rows[row])
      }
    }catch{
      continue
    }
  }

  /*const recipeMap = {};
  allRows.forEach(function(recipe) {
    if (!recipeMap[recipe.Recipe2ID] || recipeMap[recipe.Recipe2ID] < recipe.similarity_percentage) {
      recipeMap[recipe.Recipe2ID] = recipe.similarity_percentage;
    }
  });
  const sortedRecipes = Object.entries(recipeMap).sort((a, b) => b[1] - a[1]).slice(0, 7);
  const top7recipes = sortedRecipes.map(recipe => recipe[0]);
  const top7scores = sortedRecipes.map(recipe => recipe[1]);*/


  return allRows[round(random.random()*11)]
}

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(serveStatic('public', { index: ['index.html']}));
app.use('/recipes', (req,res) => get7recipes(req).then(r => res.json(r)));
app.use('/search', (req,res) => search(req,res))//.then(r => res.json(r)));
app.use('/mealplan', (req,res) => genMealPlan(req,res))

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
/*app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});*/

module.exports = app;
