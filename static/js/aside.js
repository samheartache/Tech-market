function toggleDropdown(id, toggleElement) {
    const content = document.getElementById(id);
    const arrow = toggleElement.querySelector('.arrow');

    const isOpen = content.style.display === 'block';
    if (isOpen) {
        content.style.display = 'none';
        arrow.textContent = '▼';
        localStorage.setItem(id, 'closed');
    } else {
        content.style.display = 'block';
        arrow.textContent = '▲';
        localStorage.setItem(id, 'open');
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const dropdowns = ['category-list', 'price-filter'];

    dropdowns.forEach(function(id) {
        const savedState = localStorage.getItem(id);
        const content = document.getElementById(id);
        const toggle = document.querySelector(`[onclick*="${id}"]`);
        const arrow = toggle.querySelector('.arrow');

        if (savedState === 'open' || savedState === null) {
            content.style.display = 'block';
            arrow.textContent = '▲';
        } else {
            content.style.display = 'none';
            arrow.textContent = '▼';
        }
    });
});
