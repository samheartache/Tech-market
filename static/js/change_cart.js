$(document).ready(function () {
    $(document).on("click", ".increase, .reduce", function (e) {
        e.preventDefault();
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();
        const url = $(this).attr("action")
        const product_id = $(this).data("product-id")

        $.ajax({
            type: "POST",
            url: url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: csrf_token,
            },
            success: function(data) {
                prodAmount = data.product_amount
                if (prodAmount === 0) {
                    const cartBlock = document.getElementById(`${product_id}`);
                    cartBlock.remove();

                    if (data.amount === 0) {
                        const cartContainer = $('.cart-container');
                        cartContainer.html(data.cart_page);
                    }
                }

                else {
                    const amount = document.querySelector('.quantity')
                    amount.textContent = prodAmount
                }
            }
        })
    })

})