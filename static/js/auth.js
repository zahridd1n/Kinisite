// Auth Pages JavaScript

document.addEventListener('DOMContentLoaded', function() {
  // Password toggle functionality
  const toggleButtons = document.querySelectorAll('.password-toggle');
  
  toggleButtons.forEach(button => {
    button.addEventListener('click', function() {
      const input = this.previousElementSibling;
      const icon = this.querySelector('i');
      
      if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');
      } else {
        input.type = 'password';
        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');
      }
    });
  });

  // Form validation for signup
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', function(e) {
      const password = document.getElementById('password');
      const passwordConfirm = document.getElementById('password_confirm');
      
      if (password.value !== passwordConfirm.value) {
        e.preventDefault();
        alert('Parollar mos kelmaydi!');
        return false;
      }
      
      if (password.value.length < 6) {
        e.preventDefault();
        alert('Parol kamida 6 ta belgidan iborat bo\'lishi kerak!');
        return false;
      }
    });
  }

  // Input focus effects
  const inputs = document.querySelectorAll('.form-control');
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.querySelector('.input-icon')?.style.color = '#e50914';
    });
    
    input.addEventListener('blur', function() {
      this.parentElement.querySelector('.input-icon')?.style.color = '#a0a0a0';
    });
  });

  // Add loading state to buttons
  const authButtons = document.querySelectorAll('.auth-btn, .btn-google');
  authButtons.forEach(button => {
    button.addEventListener('click', function() {
      if (this.type === 'submit') {
        this.innerHTML = '<i class="bi bi-arrow-repeat"></i> Yuborilmoqda...';
        this.disabled = true;
        this.style.opacity = '0.7';
      }
    });
  });
});
