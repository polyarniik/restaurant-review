document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('#burger');
    const nav = document.querySelector('#nav');

    burger.addEventListener('click', () => {
        burger.classList.toggle('header__burger_opened');
        nav.classList.toggle('header__nav_opened');
        document.body.classList.toggle('no-scroll');
    });
});