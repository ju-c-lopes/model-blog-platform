let profileTrigger = document.querySelector('.profile-trigger');
let buttonDropDown = document.querySelector('.dropdown-arrow');
let profileDropdown = document.querySelector('.profile-dropdown');
let noUserImg = document.querySelector('.no-user--img');

if (profileTrigger) {
    profileTrigger.addEventListener('click', function() {
        buttonDropDown.style.transform = buttonDropDown.style.transform === 'rotate(180deg)' ? 'rotate(0deg)' : 'rotate(180deg)';
        profileDropdown.classList.toggle('active');
    });
}

if (noUserImg) {
    noUserImg.addEventListener('click', function() {
        console.log(profileDropdown.classList.contains('active'));
        if (profileDropdown.classList.contains('active')) {
            console.log('removendo');
            profileDropdown.classList.remove('active');
    } else {
        console.log('adicionando');
        profileDropdown.classList.add('active');
    }
});}
