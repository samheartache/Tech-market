$(document).ready(function () {
    $(document).on('click', '.repeat', function (e) {
        e.preventDefault();

        const repeatA = $(this);
        const order_id = $(this).data("order-id");
        const url_cancel = $(this).data("url-cancel");
        const url_repeat = $(this).data("url-repeat");
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: url_repeat,
            data: {
                order_id: order_id,
                csrfmiddlewaretoken: csrf_token
            },

            success: function (data) {
                repeatA.attr("href", url_cancel)
                repeatA.removeClass("repeat").addClass("cancel")

                const repeatButton = $(`#${order_id}`);
                const statusBlock = $(`#status-${order_id}`);
                const dateText = $(`#datetext-${order_id}`);
                const timeInfo = $(`#time-${order_id}`);

                repeatButton.text("Отменить заказ");
                repeatButton.removeClass("btn-repeat").addClass("btn-cancel");

                statusBlock.text("В обработке");
                statusBlock.removeClass("status-cancelled").addClass("status-processing");

                dateText.text("Примерное время доставки:");
                timeInfo.text(data.delivery_date);
            }
        })
    })
})