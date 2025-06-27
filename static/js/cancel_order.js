$(document).ready(function () {
    $(document).on('click', '.cancel', function (e) {
        e.preventDefault();

        const cancelA = $(this);
        const order_id = $(this).data("order-id");
        const url_cancel = $(this).data("url-cancel");
        const url_repeat = $(this).data("url-repeat");
        const csrf_token = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url: url_cancel,
            data: {
                order_id: order_id,
                csrfmiddlewaretoken: csrf_token
            },

            success: function (data) {
                cancelA.attr("href", url_repeat)
                cancelA.removeClass("cancel").addClass("repeat")

                const cancelButton = $(`#${order_id}`);
                const statusBlock = $(`#status-${order_id}`);
                const dateText = $(`#datetext-${order_id}`);
                const timeInfo = $(`#time-${order_id}`);

                cancelButton.text("Повторить заказ");
                cancelButton.removeClass("btn-cancel").addClass("btn-repeat");

                statusBlock.text("Отменён");
                statusBlock.removeClass("status-processing").addClass("status-cancelled");

                dateText.text("Дата отмены заказа:");
                timeInfo.text(data.cancellation_date)
            }
        })
    })
})