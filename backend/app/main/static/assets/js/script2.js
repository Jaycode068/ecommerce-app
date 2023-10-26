// Initialize the cart object (you can use local storage, cookies, or a server for this)
let cart = [];

const availableProductsDiv = document.querySelector('#available-products');
const addToCartButtons = document.querySelectorAll('.add__to--cart__text');

//const addToCartButton = availableProductsDiv.querySelector('.add__to--cart__text');

//addToCartButtons.addEventListener('click', event => {
  // Prevent the default form submission behavior.
  //event.preventDefault();
addToCartButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();

      // Extract the product name and price from the DOM.
      const productName = document.querySelector('.product__items--content__subtitle').textContent;
      const productPrice = document.querySelector('.current__price').textContent;

      // Do something with the product name and price, such as adding them to the cart or displaying them in a modal.
      console.log(`Product Name: ${productName}`);
      console.log(`Product Price: ${productPrice}`);

        // Create a product object
        const product = {
            name: productName,
            price: productPrice,
        };

        // Add the product to the cart
        cart.push(product);

        //Adding cart to local storage
        localStorage.setItem('cart', JSON.stringify(cart));
      });
});


// Retrieve the cart from local storage
const savedCart = localStorage.getItem('cart');
if (savedCart) {
    cart = JSON.parse(savedCart);
}

// Loop through the cart and display the products in the table
if (cart) {
    cart.forEach(function(product) {
        // Create a new row in the cart table and fill in product details
        const newRow = `
                <tr class="cart__table--body__items">
                <td class="cart__table--body__list">
                    <div class="cart__product d-flex align-items-center">
                        <button class="cart__remove--btn" aria-label="search button" type="button">
                            <svg fill="currentColor" xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 24 24" width="16px" height="16px"><path d="M 4.7070312 3.2929688 L 3.2929688 4.7070312 L 10.585938 12 L 3.2929688 19.292969 L 4.7070312 20.707031 L 12 13.414062 L 19.292969 20.707031 L 20.707031 19.292969 L 13.414062 12 L 20.707031 4.7070312 L 19.292969 3.2929688 L 12 10.585938 L 4.7070312 3.2929688 z"/></svg>
                        </button>
                        <div class="cart__thumbnail">
                            <a href="/product-details"><img class="border-radius-5" src="/product/images/${product.image_filename}" alt="cart-product"></a>
                        </div>
                        <div class="cart__content">
                            <h4 class="cart__content--title"><a href="/product-details">${product.name}</a></h4>
                            <span class="cart__content--variant">COLOR: Blue</span>
                            <span class="cart__content--variant">WEIGHT: 2 Kg</span>
                        </div>
                    </div>
                </td>
                <td class="cart__table--body__list">
                    <span class="cart__price">${product.price}</span>
                </td>
                <td class="cart__table--body__list">
                    <div class="quantity__box">
                        <button type="button" class="quantity__value quickview__value--quantity decrease" aria-label="quantity value" value="Decrease Value">-</button>
                        <label>
                            <input type="number" class="quantity__number quickview__value--number" value="1" data-counter/>
                        </label>
                        <button type="button" class="quantity__value quickview__value--quantity increase" aria-label="quantity value" value="Increase Value">+</button>
                    </div>
                </td>
                <td class="cart__table--body__list">
                    <span class="cart__price end">£130.00</span>
                </td>
            </tr>
        `;

        // Append the new row to your cart table
        $('#cart__table').append(newRow);
    });
}
