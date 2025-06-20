$(document).ready(function() {
    function showNotification(message, isError = false) {
        const notification = $("#jq-notification");
        notification.stop(true, true)
            .removeClass('fade-out')
            .html(message)
            .css('opacity', 1)
            .show();
        
        if (isError) {
            notification.css('background-color', '#f44336'); // Красный для ошибок/удаления
        } else {
            notification.css('background-color', '#4CAF50'); // Зеленый для успешного добавления
        }
        
        setTimeout(function() {
            notification.addClass('fade-out');
            setTimeout(function() {
                notification.hide();
            }, 400);
        }, 1500);
    }

    $(document).on("click", ".add_to_cart, .remove_from_cart", function(e) {
        e.preventDefault();
        
        const button = $(this);
        const product_id = button.data("product-id");
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();
        const isAddAction = button.hasClass("add_to_cart");
        const url = isAddAction ? button.data("add-url") : button.data("remove-url");

        $.ajax({
            type: "POST",
            url: url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function(data) {
                if (isAddAction) {
                    button.removeClass("add_to_cart").addClass("remove_from_cart");
                    button.text("Удалить из корзины");
                    button.attr("href", button.data("remove-url"));
                    showNotification(data.message); // Зеленый фон
                } else {
                    button.removeClass("remove_from_cart").addClass("add_to_cart");
                    button.text("Добавить в корзину");
                    button.attr("href", button.data("add-url"));
                    showNotification(data.message, true); // Красный фон
                }
            },
            error: function(xhr) {
                const errorMsg = isAddAction 
                    ? "Ошибка при добавлении товара" 
                    : "Ошибка при удалении товара";
                showNotification(errorMsg, true);
                console.error(xhr.responseText);
            }
        });
    });
    
    $(window).scroll(function() {
        $("#jq-notification").css('top', 20 + $(window).scrollTop() + 'px');
    });
});