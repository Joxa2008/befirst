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

let checkboxCounter = 0;

function regCheckboxValidate() {
    let checkBoxInput = document.getElementsByClassName('reg-checkbox');
    let regSubmit = document.getElementById('reg-submit');
    if (checkboxCounter % 2) {
        regSubmit.classList.add('disabled');
        regSubmit.setAttribute('type', 'button')
    } else {
        regSubmit.classList.remove('disabled');
        regSubmit.setAttribute('type', 'submit')

    }
    checkboxCounter += 1;
}

// let profileUpdateCounter = 0;
//
// function userProfileUpdate() {
//     let profileBtn = document.getElementById('profile_update_btn');
//     let userBtn = document.getElementById('user_update_btn');
//
//     if (profileUpdateCounter % 2) {
//         userBtn.setAttribute('type', 'button')
//         profileBtn.setAttribute('type', 'submit')
//
//     } else {
//         userBtn.setAttribute('type', 'submit')
//         profileBtn.setAttribute('type', 'button')
//     }
//     profileUpdateCounter += 1
//     console.log(profileUpdateCounter);
// }