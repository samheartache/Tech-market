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
                const prodAmount = data.product_amount;
                const totalPriceEl = document.querySelector(".total-amount")
                const sumPriceEl = document.getElementById(`sum - ${product_id}`)
                const totalAmount = document.getElementById("selected-count")

                if (prodAmount === 0) {

                    if (data.total_amount === 0) {
                        const cartContainer = $('.cart-container');
                        cartContainer.html(data.cart_page);
                    }

                    else {
                        const cartBlock = document.getElementById(`${product_id}`);
                        cartBlock.remove();

                        totalPriceEl.textContent = data.total_price
                    }
                }

                else {
                    const amount = document.getElementById(`q - ${product_id}`);
                    amount.textContent = prodAmount;

                    sumPriceEl.textContent = data.sum_price
                    totalPriceEl.textContent = data.total_price
                }

                totalAmount.textContent = data.amount_order
            }
        })
    })

})