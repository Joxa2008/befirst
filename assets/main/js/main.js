function navDropDown() {
    document.getElementById("navdropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        let dropdowns = document.getElementsByClassName("dropdown-content");
        let i;
        for (i = 0; i < dropdowns.length; i++) {
            let openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

let submitButton = document.getElementById('search-submit');
let searchInput = document.getElementById('nav-search');

searchInput.addEventListener('input', function () {
    let valueInput = searchInput.value;
    if (valueInput.trim() !== '') {
        submitButton.style.visibility = 'visible';
        submitButton.style.width = '100px';
        submitButton.innerText = 'Search'
        submitButton.style.padding = '3px 5px';
    } else {
        submitButton.style.visibility = 'hidden';
        submitButton.style.padding = '0';
        submitButton.style.width = '0px';
        submitButton.innerText = ''

    }

});




