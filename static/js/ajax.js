$(document).ready(function() {
    $(document).on("submit", ".cart-form", function(e) {
        e.preventDefault();
        
        const form = $(this);
        const button = form.find("button[type='submit']");
        const product_id = form.find("input[name='product_id']").val();
        const csrf_token = form.find("input[name='csrfmiddlewaretoken']").val();
        const isAddAction = button.hasClass("add_to_cart");

        $.ajax({
            type: "POST",
            url: form.attr("action"),
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: csrf_token
            },
            success: function(data) {
                if (isAddAction) {
                    form.attr("action", "/cart/remove/");
                    button.removeClass("add_to_cart").addClass("remove_from_cart");
                    button.text("Удалить из корзины");
                } else {
                    form.attr("action", "/cart/add_to_cart/");
                    button.removeClass("remove_from_cart").addClass("add_to_cart");
                    button.text("Добавить в корзину");
                }
            },
            error: function(xhr) {
                console.error("Ошибка:", xhr.responseText);
            }
        });
    });
});