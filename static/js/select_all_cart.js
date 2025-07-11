$(document).ready(function () {
    $(document).on("click", "#select-all", function (e) {
        const flag = $(this).prop("checked");
        const url = $(this).data("url")
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: url,
            data: {
                csrfmiddlewaretoken: csrf_token,
                flag: flag,
            },

            success: function (data) {
                const totalPrice = document.getElementById("total-amount");
                const amountOrder = document.getElementById("selected-count")
                const orderButton = document.querySelector(".checkout-btn")

                if (data.flag) {
                    document.querySelectorAll(".item-checkbox").forEach(checkbox => {checkbox.checked = false});
                    totalPrice.textContent = "0 ₽"
                    amountOrder.textContent = 0
                    orderButton.remove()
                }

                else {
                    if (!orderButton) {
                        $(".order-block").html(data.order_button)
                    }
                    document.querySelectorAll(".item-checkbox").forEach(checkbox => {checkbox.checked = true});
                    totalPrice.textContent = `${data.total_price} ₽`
                    amountOrder.textContent = data.amount_order
                }
            }
        })
    })
})