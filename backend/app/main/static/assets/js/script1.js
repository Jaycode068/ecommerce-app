$('#a-logout').click(function(){
    // Perform an AJAX request to the logout route and redirect the user
    $.ajax({
        url: 'http://localhost:5000/auth/v1/logout', // Assuming this is the correct logout route
        type: 'POST', // Use the appropriate HTTP method (GET, POST, etc.)
        success: function(response) {
            console.log(response)
            // Check the response from the server
            if (response && response.success) {
                // The logout was successful, redirect the user to the login page
                window.location.href = '/login'; // Redirect to the login page after successful logout
            } else {
                // The server returned an error message, handle it as needed
                console.error('Logout error:', response.error);
                // Optionally, display an error message to the user
            }
        },
        error: function(error) {
            // Handle any errors that occur during the logout request, if needed
            console.error('Logout error:', error);
        }
    });
});

$("#productForm").submit(function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Gather form data
    /** 
    let formData = {
        name:           $("#product-name").val(),
        description:    $('#description').val(),
        price:          $("#product-price").val(),
        category_id:    parseFloat($("#product-category").val()),
        image_filename: $("#image")[0]
    };**/

    // Create FormData object
    let formData = new FormData(); 

    // Add text fields 
    formData.append('name', $('#product-name').val());
    formData.append('description', $('#description').val());
    formData.append('price', parseFloat($("#product-price").val()));
    formData.append('category_id', $("#product-category").val());
    // Add file
    formData.append('image', $('#image')[0].files[0]); 

    $.ajax({
        url: 'http://localhost:5000/api/v1/product',
        method: 'POST',
        processData: false, // tell jQuery not to process as JSON
        contentType: false, // tell jQuery not to set contentType
        data: formData,
        success: function(response){
            console.log(response)
            // handle success
        },
        error: function(response){
            console.log(response)
        }
    });
});




$(document).ready(function() {
    // jQuery code for dynamically populating category options
    $.ajax({
        url: 'http://localhost:5000/api/v1/categories', // Replace with the actual endpoint URL for fetching categories
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            let categorySelect = $('#product-category');
            $.each(response, function(index, category) {
                categorySelect.append('<option value="' + category.id + '">' + category.name + '</option>');
            });
        },
        error: function(response) {
            console.log(response);
        }
    });

    
    $.ajax({
        url: 'http://localhost:5000/api/v1/products',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            
            // Iterate through the data and populate the available-products div
            $('#available-products').on('click', '#addtocart', function(e) {
                let product_name = $(this).closest('.product__items--content').find('#pname').text();
                let product_id = $(this).closest('.product__items--content').find('#product_id').text();
                let user = $('#user_id').text();
                let price = $(this).closest('.product__items--content').find('#price').text();
                
                $.ajax({
                    url:        '/api/v1/cart_items',
                    method:     'POST',
                    contentType: 'application/json',
                    data:         JSON.stringify({product_id:product_id,user_id:user, quantity:1}),   
                    success:    function(res){
                        $('#modal').css('display', 'block');
                        $('#modal-item-name').text(itemName);

                        // Close modal
                        $('#close').click(function() {
                            $('#add-to-cart-modal').css('display', 'none');
                        });
                        
                    },

                    error: function(res){
                        console.log(res)
                    }
                });
            });
    
            $.each(data, function(index, product) {

                let productItem = `  
                                   
                <div class="col mb-30" >
                    <div class="product__items">
                        <div class="product__items--thumbnail">
                            <a class="product__items--link" href="/product-details">

                                <img class="product__items--img product__primary--img" src="/product/images/${product.image_filename}" alt="product-img">
                                <img class="product__items--img product__secondary--img" src="/product/images/${product.image_filename}" alt="product-img">
                            </a>
                            <div class="product__badge">
                                <span class="product__badge--items sale">Sale</span>
                            </div>
                        </div>
                        <div class="product__items--content">
                            <span class="product__items--content__subtitle" id="pname" >${product.name}</span>
                            <span class="visually-hidden" id=product_id>${product.id}</span>
                            <h3 class="product__items--content__title h4"><a href="/product-details">${product.description}</a></h3>
                            <div class="product__items--price">
                                <span class="current__price" id="price">$${product.price}</span>
                                <span class="price__divided"></span>
                                <span class="old__price">$78</span>
                            </div>
                <ul class="rating product__rating d-flex">
                                <li class="rating__list">
                                    <span class="rating__list--icon">
                                        <svg class="rating__list--icon__svg" xmlns="http://www.w3.org/2000/svg" width="14.105" height="14.732" viewBox="0 0 10.105 9.732">
                                        <path data-name="star - Copy" d="M9.837,3.5,6.73,3.039,5.338.179a.335.335,0,0,0-.571,0L3.375,3.039.268,3.5a.3.3,0,0,0-.178.514L2.347,6.242,1.813,9.4a.314.314,0,0,0,.464.316L5.052,8.232,7.827,9.712A.314.314,0,0,0,8.292,9.4L7.758,6.242l2.257-2.231A.3.3,0,0,0,9.837,3.5Z" transform="translate(0 -0.018)" fill="currentColor"></path>
                                        </svg>
                                    </span>
                                </li>
                                <li class="rating__list">
                                    <span class="rating__list--icon">
                                        <svg class="rating__list--icon__svg" xmlns="http://www.w3.org/2000/svg" width="14.105" height="14.732" viewBox="0 0 10.105 9.732">
                                        <path data-name="star - Copy" d="M9.837,3.5,6.73,3.039,5.338.179a.335.335,0,0,0-.571,0L3.375,3.039.268,3.5a.3.3,0,0,0-.178.514L2.347,6.242,1.813,9.4a.314.314,0,0,0,.464.316L5.052,8.232,7.827,9.712A.314.314,0,0,0,8.292,9.4L7.758,6.242l2.257-2.231A.3.3,0,0,0,9.837,3.5Z" transform="translate(0 -0.018)" fill="currentColor"></path>
                                        </svg>
                                    </span>
                                </li>
                                <li class="rating__list">
                                    <span class="rating__list--icon">
                                        <svg class="rating__list--icon__svg" xmlns="http://www.w3.org/2000/svg" width="14.105" height="14.732" viewBox="0 0 10.105 9.732">
                                        <path data-name="star - Copy" d="M9.837,3.5,6.73,3.039,5.338.179a.335.335,0,0,0-.571,0L3.375,3.039.268,3.5a.3.3,0,0,0-.178.514L2.347,6.242,1.813,9.4a.314.314,0,0,0,.464.316L5.052,8.232,7.827,9.712A.314.314,0,0,0,8.292,9.4L7.758,6.242l2.257-2.231A.3.3,0,0,0,9.837,3.5Z" transform="translate(0 -0.018)" fill="currentColor"></path>
                                        </svg>
                                    </span>
                                </li>
                                <li class="rating__list">
                                    <span class="rating__list--icon">
                                        <svg class="rating__list--icon__svg" xmlns="http://www.w3.org/2000/svg" width="14.105" height="14.732" viewBox="0 0 10.105 9.732">
                                        <path data-name="star - Copy" d="M9.837,3.5,6.73,3.039,5.338.179a.335.335,0,0,0-.571,0L3.375,3.039.268,3.5a.3.3,0,0,0-.178.514L2.347,6.242,1.813,9.4a.314.314,0,0,0,.464.316L5.052,8.232,7.827,9.712A.314.314,0,0,0,8.292,9.4L7.758,6.242l2.257-2.231A.3.3,0,0,0,9.837,3.5Z" transform="translate(0 -0.018)" fill="currentColor"></path>
                                        </svg>
                                    </span>
                                </li>
                                <li class="rating__list">
                                    <span class="rating__list--icon">
                                        <svg class="rating__list--icon__svg" xmlns="http://www.w3.org/2000/svg" width="14.105" height="14.732" viewBox="0 0 10.105 9.732">
                                        <path data-name="star - Copy" d="M9.837,3.5,6.73,3.039,5.338.179a.335.335,0,0,0-.571,0L3.375,3.039.268,3.5a.3.3,0,0,0-.178.514L2.347,6.242,1.813,9.4a.314.314,0,0,0,.464.316L5.052,8.232,7.827,9.712A.314.314,0,0,0,8.292,9.4L7.758,6.242l2.257-2.231A.3.3,0,0,0,9.837,3.5Z" transform="translate(0 -0.018)" fill="currentColor"></path>
                                        </svg>
                                    </span>
                                </li>
                            </ul>
                            <ul class="product__items--action d-flex">
                                <li class="product__items--action__list">
                                <a class="product__items--action__btn add__to--cart" id="addtocart">
                                <svg class="product__items--action__btn--svg" xmlns="http://www.w3.org/2000/svg" width="22.51" height="20.443" viewBox="0 0 14.706 13.534">
                                    <g transform="translate(0 0)">
                                        <g>
                                            <path data-name="Path 16787" d="M4.738,472.271h7.814a.434.434,0,0,0,.414-.328l1.723-6.316a.466.466,0,0,0-.071-.4.424.424,0,0,0-.344-.179H3.745L3.437,463.6a.435.435,0,0,0-.421-.353H.431a.451.451,0,0,0,0,.9h2.24c.054.257,1.474,6.946,1.555,7.33a1.36,1.36,0,0,0-.779,1.242,1.326,1.326,0,0,0,1.293,1.354h7.812a.452.452,0,0,0,0-.9H4.74a.451.451,0,0,1,0-.9Zm8.966-6.317-1.477,5.414H5.085l-1.149-5.414Z" transform="translate(0 -463.248)" fill="currentColor"></path>
                                            <path data-name="Path 16788" d="M5.5,478.8a1.294,1.294,0,1,0,1.293-1.353A1.325,1.325,0,0,0,5.5,478.8Zm1.293-.451a.452.452,0,1,1-.431.451A.442.442,0,0,1,6.793,478.352Z" transform="translate(-1.191 -466.622)" fill="currentColor"></path>
                                            <path data-name="Path 16789" d="M13.273,478.8a1.294,1.294,0,1,0,1.293-1.353A1.325,1.325,0,0,0,13.273,478.8Zm1.293-.451a.452.452,0,1,1-.431.451A.442.442,0,0,1,14.566,478.352Z" transform="translate(-2.875 -466.622)" fill="currentColor"></path>
                                        </g>
                                    </g>
                                </svg>
                            <span class="add__to--cart__text"> + Add to cart</span>
                        </a>
                                </li>
                                <li class="product__items--action__list">
                                    <a class="product__items--action__btn" href="/wishlist">
                                        <svg class="product__items--action__btn--svg" xmlns="http://www.w3.org/2000/svg" width="25.51" height="23.443" viewBox="0 0 512 512"><path d="M352.92 80C288 80 256 144 256 144s-32-64-96.92-64c-52.76 0-94.54 44.14-95.08 96.81-1.1 109.33 86.73 187.08 183 252.42a16 16 0 0018 0c96.26-65.34 184.09-143.09 183-252.42-.54-52.67-42.32-96.81-95.08-96.81z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"></path></svg>
                                        <span class="visually-hidden">Wishlist</span> 
                                    </a>
                                </li>
                                <li class="product__items--action__list">
                                    <a class="product__items--action__btn" data-open="modal1" href="javascript:void(0)">
                                        <svg class="product__items--action__btn--svg" xmlns="http://www.w3.org/2000/svg"  width="25.51" height="23.443" viewBox="0 0 512 512"><path d="M255.66 112c-77.94 0-157.89 45.11-220.83 135.33a16 16 0 00-.27 17.77C82.92 340.8 161.8 400 255.66 400c92.84 0 173.34-59.38 221.79-135.25a16.14 16.14 0 000-17.47C428.89 172.28 347.8 112 255.66 112z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32"/><circle cx="256" cy="256" r="80" fill="none" stroke="currentColor" stroke-miterlimit="10" stroke-width="32"/></svg>
                                        <span class="visually-hidden">Quick View</span>
                                    </a>
                                </li>
                                
                            </ul>
                        </div>
                    </div>
                </div>

                `;

                // Append product item to available-products div
                $('#available-products').append(productItem);
                
            });
        },
        error: function(error) {
           console.log(error)
        }
    });
});
