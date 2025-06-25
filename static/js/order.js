document.addEventListener("DOMContentLoaded", function() {
    const deliveryOptions = document.querySelectorAll('input[name="delivery"]');
    const deliveryAddress = document.getElementById('delivery-address');

    deliveryOptions.forEach(option => {
        option.addEventListener("change", function () {
            if (this.value === "delivery") {
                deliveryAddress.style.display = "block";
            }

            else {
                deliveryAddress.style.display = "none";
            }
        })
    })
})