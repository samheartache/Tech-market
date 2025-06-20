$(document).ready(function() {
    const notification = $("#jq-notification");
    
    function showNotification(message) {
        notification.stop(true, true)
            .removeClass('fade-out')
            .html(message)
            .css('opacity', 1)
            .show();
        
        setTimeout(function() {
            notification.addClass('fade-out');
            
            setTimeout(function() {
                notification.hide();
            }, 400);
        }, 1500);
    }
    
    $(document).on("click", ".add_to_cart", function(e) {
        e.preventDefault();
        
        const product_id = $(this).data("product-id");
        const add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function(data) {
                showNotification(data.message);
            },
            error: function() {
                showNotification("Ошибка при добавлении товара");
                notification.css('background-color', '#f44336');
            }
        });
    });
    
    $(window).scroll(function() {
        notification.css('top', 20 + $(window).scrollTop() + 'px');
    });
});