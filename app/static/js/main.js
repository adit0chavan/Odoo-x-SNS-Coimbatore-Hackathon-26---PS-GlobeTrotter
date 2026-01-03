// Flash message auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});

// Form validation
function validateDates() {
    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');
    
    if (startDate && endDate) {
        endDate.min = startDate.value;
        startDate.addEventListener('change', function() {
            endDate.min = this.value;
        });
    }
}

document.addEventListener('DOMContentLoaded', validateDates);
