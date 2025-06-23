$(document).ready(function () {
    $(document).on("click", ".item-checkbox", function (e) {
        const product_id = $(this).data("product-id");
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();
        const url = $(this).data("url");
        const order_flag = $(this).prop("checked");
        
        $.ajax({
            type: "POST",
            url: url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: csrf_token,
                order_flag: order_flag,
            },
            success: function (data) {
                const totalPrice = document.getElementById("total-amount");
                const allPick = document.getElementById("select-all");
                const amountOrder = document.getElementById("selected-count")
                const orderButton = document.querySelector(".checkout-btn")

                if (data.all_flag) {
                    if (!orderButton) {
                        $(".order-block").html(data.order_button)
                    }
                    allPick.checked = true;
                }

                else {
                    if (!orderButton) {
                        $(".order-block").html(data.order_button)
                    }
                    allPick.checked = false;
                }

                if (data.total_price === 0) {
                    orderButton.remove()
                }

                totalPrice.textContent = `${data.total_price} ₽`
                amountOrder.textContent = data.amount_order
            }
        })
    })
})