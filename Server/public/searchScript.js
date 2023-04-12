const advancedSearchLabel = document.getElementById('advanced-search-label');
const advancedSearch = document.getElementsByClassName('advanced-search')[0];
const searchForm = document.getElementById('search-form');
const searchBox = document.getElementById('search-box');
const header = document.querySelector('header');
const searchContainer = document.querySelector('.search-container');

/*advancedSearchLabel.addEventListener('click', function() {
  advancedSearch.classList.toggle('active');
  if (advancedSearch.classList.contains("active")) {
    searchForm.classList.toggle('expanded');
    advancedSearch.style.display = 'block';
  } else {
    searchForm.classList.toggle('expanded');
    advancedSearch.style.display = 'none';
  }
});

document.addEventListener('click', function(event) {
  if (!searchContainer.contains(event.target)) {
    advancedSearch.classList.remove('active');
  }
});*/


function getCurrentURL() {
  return window.location.href
}
function searchRecipes() {
  var query = getCurrentURL().split("?")[1]
  const url = `/search?${query}`; // Replace with your actual API endpoint

  fetch(url)
    .then(response => response.json())
    .then(recipes => {
      const resultsList = document.getElementById('results');
      resultsList.innerHTML = '';

      recipes.forEach(recipe => {
        const listItem = document.createElement('li');
        const recipeDetails = document.createElement("div");
        const recipeName = document.createElement("h2");
        //link.href = `/recipe/${recipe.recipeName}`; // Replace with your actual recipe page URL
        recipeName.textContent = recipe.recipeName;
        listItem.appendChild(recipeName);

        const prepTime = document.createElement('p');
        prepTime.textContent = `Preparation time: ${recipe.prepTime} mins`;
        prepTime.style.fontSize = '0.8rem';
        listItem.appendChild(prepTime);

        // Append preparation time
        const cookTime = document.createElement('p');
        cookTime.textContent = `Cooking time: ${recipe.cookTime} mins`;
        cookTime.style.fontSize = '0.8rem';
        listItem.appendChild(cookTime);

        const servings = document.createElement('p');
        servings.textContent = `Servings: ${recipe.serves}`;
        servings.style.fontSize = '0.8rem';
        listItem.appendChild(servings);

        const cost = document.createElement('p');
        cost.textContent = `Recipe ID: ${recipe.recipeID}`;
        cost.style.fontSize = '0.8rem';
        listItem.appendChild(cost);

        listItem.addEventListener("click", (event) => {
          event.stopPropagation();
          if(document.getElementsByClassName("expanded").length == 1) {
            document.getElementsByClassName("expanded")[0].classList.toggle("expanded")
          }
          listItem.classList.toggle("expanded");
          listItem.addEventListener("click", (event) => {
            listItem.classList.toggle("expanded")
          });
        });

        steps=""
        JSON.parse(recipe.steps).forEach(step => {
          steps+="<br><br>    -"+step
          //document.getElementById("instructions").innerHTML += step+"\n";
        });
        ingredients = ""
        recipe.ingredients.forEach(ingredient => {
          ingredients+="<br>    -"+ingredient.procText
          //document.getElementById("instructions").innerHTML += step+"\n";
        });

        recipeDetails.classList.add("recipe-details");
        recipeDetails.innerHTML = `
          <p><strong>Prep Time:</strong> ${recipe.prepTime}</p>
          <p><strong>Cook Time:</strong> ${recipe.cookTime}</p>
          <p><strong>Servings:</strong> ${recipe.serves}</p>
          <p><strong>Saves:</strong> ${recipe.saves}</p>
          <p><strong>(Very) Rough Cost:</strong> ${Math.round(Math.floor(parseFloat(recipe.cost)*100),0)/100}</p>
          <p><strong>Instructions:</strong>${steps}</p>
          <br>
          <p><strong>Ingredients:</strong>${ingredients}</p>
        `;
        listItem.appendChild(recipeName);
        listItem.appendChild(recipeDetails);

        resultsList.appendChild(listItem);
      });
    })
    .catch(error => {
      console.error(error);
    });
}
searchRecipes()
