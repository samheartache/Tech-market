$(document).ready(function () {
    $(document).on("click", ".delete-review-btn", function (e) {
        e.preventDefault();

        const review_id = $(this).data("review-id");
        const url = $(this).data("delete-url");
        const flag = $(this).data("flag");
        const csrfToken = $("[name=csrfmiddlewaretoken]").val();
        console.log(review_id)

        $.ajax({
            type: "POST",
            url: url,
            data: {
                review_id: review_id,
                csrfmiddlewaretoken: csrfToken,
                flag: flag,
            },
            success: function (data) {
                if (!data.user_reviews_page) {
                    const reviewContainer = $(".reviews-section");
                    const averageRating = $(".include-rating-block");

                    averageRating.html(data.average_rating_block);
                    reviewContainer.html(data.reviews_page);

                    if ($(".review").length === 0) {
                        $(".reviews-list").html('<p class="no-reviews">Пока нет отзывов. Будьте первым!</p>');
                    }
                }

                else {
                    const reviewContainer = $(".reviews-section");
                    reviewContainer.html(data.user_reviews_page);
                }
            }
        });
    });
});