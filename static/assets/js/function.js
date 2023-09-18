console.log("Hello World from function.js!")

$("#commentForm").submit(function(e) {
    e.preventDefault();
    
    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),
        
        dataType: "json",
       
        success: function(response) {
            console.log("comment saved");


            if (response.bool== True) {
                $("#review-resp").html("Review added successfully")
                $(".hide-commentForm").hide()
                $(".add-review").hide()

                let _html = '<div class="ec-t-review-item">'<div class="ec-t-review-avtar">'
                    '<img src="{% static 'assets/images/review-image/1.jpg' %}" alt="" /></div>'
                    '<div class="ec-t-review-content">'
                    '<div class="ec-t-review-top">'
                    '<div class="ec-t-review-name">{{ r.user.username|title }}</div>'
                    '<div class="ec-t-review-rating">{{ r.rating }}</div>'
                    '</div>'
                    '<div class="ec-t-review-bottom">'
                    '<p>{{ r.review }}</p>'
                    '</div>'
                    '</div>'
                    '</div>'
            
        }
    });
    
});


