function toggleDropdown(id) {
    const categoryList = document.getElementById(id);
    if (categoryList.style.display === 'block') {
        categoryList.style.display = 'none';
    } 
    else {
        categoryList.style.display = 'block';
    }
}