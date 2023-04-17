(function () {
  select_variation = document.getElementById("select-variation");
  variation_price = document.getElementById("variation-price");
  variation_sale_price = document.getElementById("variation-sale-price");

  if (!select_variation) {
    return;
  }

  if (!variation_price) {
    return;
  }

  select_variation.addEventListener("change", function () {
    price = this.options[this.selectedIndex].getAttribute("data-price");
    sale_price =
      this.options[this.selectedIndex].getAttribute("data-sale-price");

    variation_price.innerHTML = price;

    if (variation_sale_price) {
      variation_sale_price.innerHTML = sale_price;
    }
  });
})();
