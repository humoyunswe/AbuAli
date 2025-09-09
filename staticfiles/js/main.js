// Theme toggle functionality
function toggleTheme() {
    const body = document.body;
    const html = document.documentElement;
    const isDarkMode = body.getAttribute('data-theme') === 'dark';
    const newTheme = isDarkMode ? 'light' : 'dark';
    
    // Update both body and html
    body.setAttribute('data-theme', newTheme);
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcons(newTheme);
    
    // Force recalculation of CSS variables
    document.documentElement.style.setProperty('--force-update', Math.random());
    
    // Ensure all elements update properly
    setTimeout(() => {
        const allElements = document.querySelectorAll('*');
        allElements.forEach(element => {
            if (element.style.color || element.style.backgroundColor || element.style.borderColor) {
                element.style.transition = 'all 0.3s ease';
            }
        });
    }, 10);
}

// Language dropdown functionality
function toggleLanguageDropdown() {
    const dropdown = document.querySelector('.language-dropdown');
    const menu = document.getElementById('languageMenu');
    
    if (dropdown && menu) {
        dropdown.classList.toggle('active');
        menu.classList.toggle('active');
    }
}

// Close language dropdown when clicking outside
function closeLanguageDropdown(event) {
    const dropdown = document.querySelector('.language-dropdown');
    const menu = document.getElementById('languageMenu');
    
    if (dropdown && menu && !dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
        menu.classList.remove('active');
    }
}

// User menu functionality
function toggleUserMenu() {
    const userMenu = document.getElementById('userMenu');
    if (userMenu) {
        userMenu.classList.toggle('active');
    }
}

// Logout functionality
function logout() {
    // This should ideally be a POST request to a logout URL
    console.log('Logout action triggered');
    // Simulate logout for UI purposes
    const authGuest = document.getElementById('authGuest');
    const authUser = document.getElementById('authUser');
    if(authGuest && authUser) {
        authGuest.style.display = 'flex';
        authUser.style.display = 'none';
    }
    const userMenu = document.getElementById('userMenu');
    if (userMenu) {
        userMenu.classList.remove('active');
    }
}

function updateThemeIcons(theme) {
    const sunIcon = document.getElementById('theme-icon-sun');
    const moonIcon = document.getElementById('theme-icon-moon');
    const themeToggle = document.querySelector('.theme-toggle');

    if (sunIcon && moonIcon) {
        if (theme === 'dark') {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
            if (themeToggle) {
                themeToggle.setAttribute('title', 'Switch to light theme');
            }
        } else {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
            if (themeToggle) {
                themeToggle.setAttribute('title', 'Switch to dark theme');
            }
        }
    }
    
    // Update all theme-dependent elements
    const elementsToUpdate = document.querySelectorAll('.language-btn, .nav-link, .auth-btn, .theme-toggle');
    elementsToUpdate.forEach(element => {
        // Force style recalculation
        element.style.display = 'none';
        element.offsetHeight; // Trigger reflow
        element.style.display = '';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Load saved theme and set icons
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcons(savedTheme);
    
    // Add smooth transitions after page load
    setTimeout(() => {
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    }, 100);
    
    // Close language dropdown on outside click
    document.addEventListener('click', closeLanguageDropdown);

    // Close user menu on outside click
    document.addEventListener('click', function(event) {
        const userMenu = document.getElementById('userMenu');
        const userProfile = document.querySelector('.user-profile');
        
        if (userMenu && userProfile && !userProfile.contains(event.target) && !userMenu.contains(event.target)) {
            userMenu.classList.remove('active');
        }
    });

    // Password strength animation
    document.addEventListener('input', function(event) {
        if (event.target.type === 'password' && event.target.closest(".auth-page-container")) {
            const password = event.target.value;
            const formGroup = event.target.closest('.form-group');
            if (!formGroup) return;

            const strengthBar = formGroup.querySelector('.strength-bar');
            const strengthText = formGroup.querySelector('.strength-text');
            
            if (!strengthBar || !strengthText) return;

            let strength = 0;
            let text = 'Слабый пароль';
            let color = '#ef4444';
            
            if (password.length >= 8) strength++;
            if (/[a-z]/.test(password)) strength++;
            if (/[A-Z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[^A-Za-z0-9]/.test(password)) strength++;
            
            if (strength >= 2) {
                text = 'Средний пароль';
                color = '#f59e0b';
            }
            if (strength >= 4) {
                text = 'Сильный пароль';
                color = '#10b981';
            }
            
            strengthBar.style.width = (strength * 20) + '%';
            strengthBar.style.backgroundColor = color;
            strengthText.textContent = text;
        }
    });
    
    // Language selector enhancement
    const languageSelect = document.querySelector('.language-select');
    if (languageSelect) {
        languageSelect.addEventListener('focus', function() {
            this.parentElement.style.borderColor = 'var(--accent-primary)';
            this.parentElement.style.boxShadow = 'var(--shadow-md)';
        });
        
        languageSelect.addEventListener('blur', function() {
            this.parentElement.style.borderColor = 'var(--border)';
            this.parentElement.style.boxShadow = 'none';
        });
    }
    
    // Add keyboard navigation for theme toggle
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleTheme();
            }
        });
    }
    
    // Improve accessibility
    document.querySelectorAll('.auth-btn, .nav-link, .theme-toggle').forEach(element => {
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                this.click();
            }
        });
    });

    // Password toggle
    const passwordToggleButtons = document.querySelectorAll('.password-toggle');
    passwordToggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input[type="password"]');
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            this.textContent = isPassword ? '👁️' : '🔒';
        });
    });

    // Form submission handling
    const loginForm = document.querySelector('.auth-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('.form-submit');
            const submitText = submitButton.querySelector('.submit-text');
            const submitLoader = submitButton.querySelector('.submit-loader');

            // Disable form submission temporarily
            e.preventDefault();
            
            // Show loading state
            submitText.style.display = 'none';
            submitLoader.style.display = 'inline';
            submitButton.disabled = true;

            // Get form data
            const formData = new FormData(this);

            // Send AJAX request
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    // Success - redirect to home page
                    window.location.href = '/';
                } else {
                    // Error - show error message
                    return response.json().then(data => {
                        throw new Error(data.message || 'Error occurred');
                    });
                }
            })
            .catch(error => {
                // Handle error
                const formErrors = document.querySelector('.form-errors');
                if (formErrors) {
                    formErrors.style.display = 'block';
                    formErrors.textContent = error.message;
                }
            })
            .finally(() => {
                // Reset button state
                submitText.style.display = 'inline';
                submitLoader.style.display = 'none';
                submitButton.disabled = false;
            });
        });
    }
});
