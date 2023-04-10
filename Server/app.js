var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var serveStatic = require('serve-static');
var sqlite = require("better-sqlite3");


async function get7recipes() {
  var db = new sqlite("./data/processedData.db");
  var rows = db.prepare("SELECT recipeName FROM Recipes WHERE recipeID < 8").all();
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
  const db = new sqlite3.Database('./data/processedData.db');
  sql = "SELECT recipeID,recipeName,meat,cost FROM Recipes WHERE serves > ?"
  keywords.forEach((keyword, i) => {
    //Do Nothing Yet
  });

  db.each(sql,[serves], (err, row) => {
    console.log(row);
  });
  db.close();
}
\

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
app.use('/recipes', (req,res) => get7recipes().then(r => res.text(r)));

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
