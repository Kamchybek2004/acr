const hamburger = document.createElement('div');
hamburger.classList.add('hamburger');
hamburger.innerHTML = '<span></span><span></span><span></span>';
document.querySelector('.nav').prepend(hamburger);

const navLeft = document.querySelector('.nav-left');
hamburger.addEventListener('click', () => {
    navLeft.style.display = navLeft.style.display === 'flex' ? 'none' : 'flex';
});