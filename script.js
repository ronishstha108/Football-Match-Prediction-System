// ===== MOBILE NAVIGATION TOGGLE =====
// When the hamburger button is clicked, show or hide the nav links.

const hamburger = document.getElementById('hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', function () {
  navLinks.classList.toggle('open');
});

// Close the mobile menu when a nav link is clicked
navLinks.addEventListener('click', function (event) {
  if (event.target.tagName === 'A') {
    navLinks.classList.remove('open');
  }
});

// ===== SMOOTH SCROLLING =====
// Make all anchor links (#home, #features, etc.) scroll smoothly.

document.querySelectorAll('a[href^="#"]').forEach(function (link) {
  link.addEventListener('click', function (event) {
    const targetId = this.getAttribute('href');

    // Skip if href is just "#" (like the Login button)
    if (targetId === '#') return;

    event.preventDefault();

    const targetSection = document.querySelector(targetId);
    if (targetSection) {
      targetSection.scrollIntoView({ behavior: 'smooth' });
    }
  });
});