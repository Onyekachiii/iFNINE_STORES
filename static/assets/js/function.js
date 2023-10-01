console.log("Hello World from function.js!")


// for category and vendor filter functionality

$(document).ready(function() {
    $(".filter-checkbox").on("click", function(){
        console.log("a checkbox has been clicked")

        let filter_object = {}

        $(".filter-checkbox").each(function() {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            filter_object[filter_key] = Array.from(document.querySelectorAll(`input[data-filter="${filter_key}"]:checked`)).map(function(el) {
                return el.value
            })
        })
        console.log("Filter Object: ", filter_object)
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function() {
                console.log("loading...")
            },
            success: function(response) {
                $("#filtered-product").html(response.data)
            }
        })

    })

    // for add to cart functionality

    $(".add-to-cart-btn").on("click", function(){

        let this_val = $(this)
        let index = this_val.attr("data-index")
        let quantity = $(".product-quantity-"+ index).val()
        let product_title = $(".product-title-"+ index).val()
        let product_image = $(".product-image-"+ index).val()
        let product_pid = $(".product-pid-"+ index).val()
        let product_id = $(".product-id-"+ index).val()
        let product_price = $(".current-product-price-"+ index).text()
    
    
        console.log("PRODUCT ID: ", product_id);
        console.log("PRODUCT PID: ", product_pid);
        console.log("PRODUCT QUANTITY: ", quantity);
        console.log("PRODUCT IMAGE: ", product_image);
        console.log("PRODUCT TITLE: ", product_title);
        console.log("PRODUCT PRICE: ", product_price);
    
        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'qty': quantity,
                'image': product_image,
                'title': product_title,
                'price': product_price
            },
            dataType: 'json',
            beforeSend: function(){
                console.log('Adding products to cart...');
            },
            success: function(response){
                this_val.html("✓")
                console.log('Added products to cart!');
                $(".cart-items-count").text(response.totalcartitems)
    
            }
        })
    })
    
    
    // To delete items from cart page
    
    $(".delete-product").on("click", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        console.log("PRODUCT ID: ", product_id)
    
        $.ajax({
            url:"/delete-from-cart",
            data:{
                "id":product_id,
            },
            dataType:'json',
            beforeSend:function(){
                this_val.hide();
            },
            success:function(response){
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    
    });
    
    
    // To update items from cart page
    
    $(".update-product").on("click", function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_qty = $(".product-qty-"+ product_id).val()
    
        console.log("PRODUCT ID: ", product_id);
        console.log("PRODUCT QTY: ", product_qty);
    
        $.ajax({
            url:'/update-cart',
            data:{
                'id':product_id,
                'qty':product_qty,
            },
            dataType:'json',
            beforeSend:function(){
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    
    });
    

    // Making default addresses
    $(document).on("click", ".make-default-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("ADDRESS ID: ", id)
        console.log("THIS VAL: ", this_val)

        $.ajax({
            url: '/make-default-address',
            data: {
                'id': id,
            },
            dataType: 'json',
            success: function(response){
                console.log("Default address updated")
                if (response.boolean == true){

                    $(".check").hide();
                    $(".action_btn").show();
                
                    $(".check-"+id).show();
                    $(".button-"+id).hide();
                }
            }

        })
    })

    // Adding to wishlist
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("PRODUCT ID: ", product_id)

        $.ajax({
            url: '/add-to-wishlist',
            data: {
                'id': product_id,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding to wishlist...")
            },
            success: function(response){
                this_val.html("✓")
                if (response.boolean === true){
                    console.log("Added to wishlist")
                }
                
            }
        })

    
    })

    // Removing from wishlist
    $(document).on("click", ".delete-wishlist-product", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("WISHLIST ID: ", wishlist_id)

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                'id': wishlist_id,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Removing from wishlist...")
            },
            success: function(response){
                $("#wishlist-list").html(response.data)
            }
        });
    })


    // Info from Contact Us page
    $(document).on("submit", "#contact-form-ajax", function(){
        e.preventDefault()
        console.log("Contact us form submitted")

        let full_name = $("#full_name").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let message = $("#message").val()

        console.log("FULL NAME: ", full_name)
        console.log("EMAIL: ", email)
        console.log("PHONE: ", phone)
        console.log("MESSAGE: ", message)

        $.ajax({
            url: '/ajax-contact-form',
            data: {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'message': message,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending message...")
            },
            success: function(response){
                console.log("Message sent")
                $("#contact-form-ajax").hide()
                $("#message-response").html("Message sent successfully")
            }
        })
    })

    $(".commentForm").submit(function(e) {
        e.preventDefault();
        
        $.ajax({
            data: $(this).serialize(),
    
            method: $(this).attr("method"),
    
            url: $(this).attr("action"),
            
            dataType: "json",
           
            success: function(response) {
                console.log("comment saved");
    
    
                if (response.bool == true) {
                    $("#review-resp").html("Review added successfully")
                    $(".hide-commentForm").hide()
                    $(".add-review").hide()
    
                    let _html =  '<div class="ec-t-review-item">'
                        _html += '<div class="ec-t-review-avtar">'
                        _html += '<img src="ifnine_stores/static/assets/images/review-image/1.jpg" alt=""/>'
                        _html += '</div>'

                        _html += '<div class="ec-t-review-content">'
                        _html += '<div class="ec-t-review-top">'
                        _html += '<div class="ec-t-review-name">'+ response.context.user +'</div>'
                        _html += '<div class="ec-t-review-rating">'

                        for (let i = 1; i <= response.content.rating; i++ ){
                            _html += '<i class="fi-rr-star text-danger"></i>'
                        }                
                        _html += '</div>'                        
                        _html += '</div>'

                        _html += '<div class="ec-t-review-bottom">'
                        _html += '<p>'+ response.content.review +'</p>'
                        _html += '</div>'
                        _html += '<div class="ec-t-review-bottom">'
                        _html += '<p>{{ r.date|date:"d M, Y" }}</p>'
                        _html += '</div>'
                        _html += '</div>'
                        _html += '</div>'

                        $(".comment-list").prepend(_html)
                    }
                
                
            }
        });
        
    });
    

});