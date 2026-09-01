const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('#nav-links');
const year = document.querySelector('#year');

if (year) {
  year.textContent = new Date().getFullYear().toString();
}

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', isOpen.toString());
  });

  navLinks.addEventListener('click', (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      navLinks.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
}
