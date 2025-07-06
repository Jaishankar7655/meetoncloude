// Mobile menu toggle
document.getElementById('mobile-menu-button').addEventListener('click', function() {
    const mobileMenu = document.getElementById('mobile-menu');
    mobileMenu.classList.toggle('mobile-menu-enter-active');
    
    // Toggle aria-expanded attribute
    const expanded = this.getAttribute('aria-expanded') === 'true' || false;
    this.setAttribute('aria-expanded', !expanded);
    
    // Toggle icon between bars and times (x)
    const icon = this.querySelector('i');
    if (icon.classList.contains('fa-bars')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});

// User dropdown toggle
document.addEventListener('DOMContentLoaded', function() {
    const userMenuButton = document.getElementById('user-menu-button');
    if (userMenuButton) {
        userMenuButton.addEventListener('click', function() {
            const dropdown = document.getElementById('user-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('hidden');
                
                // Add animation classes
                if (dropdown.classList.contains('hidden')) {
                    dropdown.classList.remove('opacity-100', 'scale-100');
                    dropdown.classList.add('opacity-0', 'scale-95');
                } else {
                    dropdown.classList.remove('opacity-0', 'scale-95');
                    dropdown.classList.add('opacity-100', 'scale-100');
                }
                
                // Toggle aria-expanded attribute
                const expanded = this.getAttribute('aria-expanded') === 'true' || false;
                this.setAttribute('aria-expanded', !expanded);
            }
        });
    }

    // Close dropdown when clicking outside
    window.addEventListener('click', function(event) {
        const dropdown = document.getElementById('user-dropdown');
        const button = document.getElementById('user-menu-button');
        
        if (dropdown && button && 
            !dropdown.classList.contains('hidden') && 
            !button.contains(event.target) && 
            !dropdown.contains(event.target)) {
            dropdown.classList.add('hidden');
            dropdown.classList.remove('opacity-100', 'scale-100');
            dropdown.classList.add('opacity-0', 'scale-95');
            button.setAttribute('aria-expanded', 'false');
        }
    });

    // Add active state to current page in navbar
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            // Desktop links
            if (!link.classList.contains('bg-primary-dark')) {
                link.classList.add('bg-primary-dark');
            }
            
            // Mobile links - make sure we don't double-apply
            if (link.classList.contains('text-white') && !link.classList.contains('bg-primary-dark')) {
                link.classList.add('bg-primary-dark');
            }
        }
    });
});

// Handle responsiveness on resize
window.addEventListener('resize', function() {
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileButton = document.getElementById('mobile-menu-button');
    
    // If switching to desktop view while mobile menu is open, reset mobile menu
    if (window.innerWidth >= 768 && mobileMenu && mobileMenu.classList.contains('mobile-menu-enter-active')) {
        mobileMenu.classList.remove('mobile-menu-enter-active');
        if (mobileButton) {
            mobileButton.setAttribute('aria-expanded', 'false');
            const icon = mobileButton.querySelector('i');
            if (icon && icon.classList.contains('fa-times')) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    }
});