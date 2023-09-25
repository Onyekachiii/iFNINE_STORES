Sure! Here is an example of jQuery AJAX code to delete a product from the cart page of an ecommerce website:

```javascript
// Delete a product from the cart
function deleteProduct(productId) {
  $.ajax({
    url: '/cart/delete', // Specify the URL of the backend endpoint to handle the deletion
    type: 'POST', // Use POST method to send data
    
    data: {
      productId: productId // Pass the product ID to be deleted as a parameter
    },
    
    success: function(response) {
      // On success, remove the deleted product from the DOM
      $('#product-' + productId).remove();
      
      // Show a success message to the user
      $('#message').text('Product deleted successfully.');
    },
    
    error: function(xhr, status, error) {
      // Show an error message to the user
      $('#message').text('Error deleting product: ' + error);
    }
  });
}
```

In your HTML, you can have a button for each product in the cart with an `onClick` attribute to call the `deleteProduct` function:

```html
<button onclick="deleteProduct('123')">Delete</button>
```

Remember to replace `'123'` with the actual product ID.

For updating products in the cart, you can similarly use AJAX to send a request to a backend endpoint, passing the updated product information as parameters.

```javascript
// Update a product in the cart
function updateProduct(productId, quantity) {
  $.ajax({
    url: '/cart/update', // Specify the URL of the backend endpoint to handle the update
    type: 'POST', // Use POST method to send data
    
    data: {
      productId: productId, // Pass the product ID to be updated
      quantity: quantity // Pass the updated quantity of the product
    },
    
    success: function(response) {
      // On success, update the quantity in the DOM
      $('#quantity-' + productId).text(quantity);
      
      // Show a success message to the user
      $('#message').text('Product updated successfully.');
    },
    
    error: function(xhr, status, error) {
      // Show an error message to the user
      $('#message').text('Error updating product: ' + error);
    }
  });
}
```

And in your HTML, you can have input fields for the quantity of each product with an `onChange` attribute to call the `updateProduct` function:

```html
<input type="number" value="1" onchange="updateProduct('123', this.value)" />
```

Again, replace `'123'` with the actual product ID.