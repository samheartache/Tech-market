$(document).ready(function () {
    const successMessage = $('#jq-notification')

    $(document).on('click', '.add_to_cart', function (e) {
        e.preventDefault();

        const product_id = $(this).data('product-id')
        const add_to_cart_url = $(this).attr('href')

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);

                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 5000);
            },
            error: function (data) {
                console.log('Ошибка при добавлении товара в корзину')
            },
        });
    });
});