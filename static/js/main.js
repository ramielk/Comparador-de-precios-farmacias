document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips everywhere
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Product form handling - auto submit on select change
    const productSelects = document.querySelectorAll('#product1, #product2');
    productSelects.forEach(select => {
        select.addEventListener('change', function() {
            this.form.submit();
        });
    });
    
    // Clear filters button handler
    const clearFiltersBtn = document.getElementById('clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Clear all filter inputs
            document.getElementById('category').value = '';
            document.getElementById('search').value = '';
            document.getElementById('availability').value = '';
            
            // Submit the form
            this.closest('form').submit();
        });
    }
    
    // Add animation to product comparison cards
    const productCards = document.querySelectorAll('.product-card, .product-detail-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'var(--card-shadow)';
        });
    });
    
    // Handle form submission for filters to prevent empty submissions
    const filterForms = document.querySelectorAll('form[data-filter-form]');
    filterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input, select');
            let hasValue = false;
            
            inputs.forEach(input => {
                if (input.value.trim() !== '') {
                    hasValue = true;
                }
            });
            
            if (!hasValue) {
                e.preventDefault();
                window.location.href = this.action;
            }
        });
    });
});
