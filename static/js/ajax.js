$(document).ready(function() {

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
                } else {
                    button.removeClass("remove_from_cart").addClass("add_to_cart");
                    button.text("Добавить в корзину");
                    button.attr("href", button.data("add-url"));
                }
            }
        });
    });
});