console.log("Hello World from function.js!")

// $("#commentForm").submit(function(e) {
//     e.preventDefault();
    
//     $.ajax({
//         data: $(this).serialize(),

//         method: $(this).attr("method"),

//         url: $(this).attr("action"),
        
//         dataType: "json",
       
//         success: function(response) {
//             console.log("comment saved");


//             // if (response.bool== True) {
//             //     $("#review-resp").html("Review added successfully")
//             //     $(".hide-commentForm").hide()
//             //     $(".add-review").hide()

//             //     let _html = '<div class="ec-t-review-item">'<div class="ec-t-review-avtar">'
//             //         '<img src="{% static 'assets/images/review-image/1.jpg' %}" alt="" /></div>'
//             //         '<div class="ec-t-review-content">'
//             //         '<div class="ec-t-review-top">'
//             //         '<div class="ec-t-review-name">{{ r.user.username|title }}</div>'
//             //         '<div class="ec-t-review-rating">{{ r.rating }}</div>'
//             //         '</div>'
//             //         '<div class="ec-t-review-bottom">'
//             //         '<p>{{ r.review }}</p>'
//             //         '</div>'
//             //         '</div>'
//             //         '</div>'
            
//         }
//     });
    
// });



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
                this_val.hide();
            },
            success:function(response){
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    
    });
    


})