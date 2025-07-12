$(document).ready(function() {
    $(document).on("submit", ".add-review form", function (e) {
        e.preventDefault();
        
        const form = $(this);
        const url = form.attr("action");
        const formData = form.serialize();

        $.ajax({
            type: "POST",
            url: url,
            data: formData,
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                const reviewContainer = $(".reviews-section");
                const averageRating = $(".include-rating-block")

                reviewContainer.html(data.reviews_page);
                averageRating.html(data.average_rating_block)

                form.find('textarea').val('');
                form.find('select').val('5');
            }
        })
    })
})