$(document).ready(function() {
    $(document).on("click", ".remove_from_cart", function (e) {
        e.preventDefault();
        const product_id = $(this).data("product-id")
        const remove_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: remove_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                const cartBlock = document.getElementById(`${product_id}`);
                cartBlock.remove();

                const totalPrice = document.querySelector('.total-amount');
                totalPrice.textContent = data.price
                console.log(totalPrice)
            }
        })

    })
})