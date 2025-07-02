$(document).ready(function () {
    $(document).on("click", ".delete-review-btn", function (e) {
        e.preventDefault();

        const review_id = $(this).data("review-id");
        const url = $(this).data("delete-url");
        const csrfToken = $("[name=csrfmiddlewaretoken]").val();
        console.log(review_id)

        $.ajax({
            type: "POST",
            url: url,
            data: {
                review_id: review_id,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (data) {
                const reviewContainer = $(".reviews-section");
                reviewContainer.html(data.reviews_page);

                if ($(".review").length === 0) {
                    $(".reviews-list").html('<p class="no-reviews">Пока нет отзывов. Будьте первым!</p>');
                }
            }
        });
    });
});