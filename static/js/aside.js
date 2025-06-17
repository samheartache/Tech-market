function updateArrow(id) {
    const dropdown = document.getElementById(id);
    const arrow = document.getElementById(`${id}-arrow`);
    if (dropdown && arrow) {
        arrow.textContent = dropdown.style.display === 'none' ? '▶' : '▼';
    }
}


function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    const isHidden = dropdown.style.display === 'none';
    
    dropdown.style.display = isHidden ? 'block' : 'none';
    localStorage.setItem(`dropdown_${id}_state`, isHidden ? 'open' : 'closed');
    updateArrow(id);
}


function  restoreDropdownState() {
    document.querySelectorAll('.dropdown-content').forEach(dropdown => {
        const id = dropdown.id;
        const savedState = localStorage.getItem(`dropdown_${id}_state`);

        dropdown.style.display = (savedState === 'closed') ? 'none' : 'block';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    restoreDropdownState();
    document.querySelectorAll('.dropdown-content').forEach(dropdown => {
        updateArrow(dropdown.id);
    });
});
