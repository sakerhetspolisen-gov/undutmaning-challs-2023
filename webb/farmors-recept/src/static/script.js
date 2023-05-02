$(function() {
  $.get("/dishes.php", function(data) {
    let dishList = document.getElementById("dish-list");
    Object.entries(data).forEach(([key, value]) => {
      let listItem = document.createElement("li");
      value[0] = value[0].toUpperCase();
      listItem.textContent = value[0].toUpperCase() + value.substring(1, 20);
      listItem.id = value;
      listItem.addEventListener("click", getIngredients);
      listItem.classList = "list-group-item dish-item p-3";
      dishList.appendChild(listItem);
    });
  });
});

function getIngredients(event) {
  $.ajax({
    type: 'POST',
    url: '/ingredients.php',
    data: JSON.stringify({dish: event.target.id}),
    contentType: 'application/json',
    dataType: 'json',
    success: function(response) {
      let dishItem = document.getElementById(event.target.id);
      let cardItem = document.createElement("div");
      cardItem.classList = "card-body details pt-3";
      let i = document.getElementById("ingredients");
      if (i) {
        i.remove();
      }
      cardItem.id = "ingredients";
      cardItem.textContent = "Ingredienser: " + response.ingredients + ".";
      dishItem.appendChild(cardItem);
      let hs = document.createElement("p");
      hs.classList = "details";

      // API does not accept spaces.
      let dish = event.target.id.replace(/ /g, "");

      // Orders from farmor.. Removed possibility to get secret_sauce
      hs.textContent = "Hemlig sås: ******* " + getSecretSauce(dish) + " dl.";
      cardItem.appendChild(hs);
    }
  });
}

function getSecretSauce(dish) {
  return $.ajax({
    type: 'POST',
    url: '/secret_sauce_quantity.php',
    data: JSON.stringify({dish: dish}),
    contentType: 'application/json',
    dataType: 'json',
    async: false,
    success: function(response) {
    }
  }).responseJSON.secret_sauce_quantity;
}
