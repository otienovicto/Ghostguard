// Display flash messages with a fade-out effect after a few seconds
window.onload = function() {
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 500); // Fade out duration
        }, 5000); // Show for 5 seconds
    });
};

// Form validation for the registration and login forms
function validateForm(form) {
    let isValid = true;

    const username = form.querySelector('input[name="username"]');
    const email = form.querySelector('input[name="email"]');
    const password = form.querySelector('input[name="password"]');
    
    // Validate username (should not be empty)
    if (username && username.value.trim() === '') {
        alert('Username is required.');
        isValid = false;
    }

    // Validate email format
    if (email && !validateEmail(email.value)) {
        alert('Please enter a valid email address.');
        isValid = false;
    }

    // Validate password (should not be empty)
    if (password && password.value.trim() === '') {
        alert('Password is required.');
        isValid = false;
    }

    return isValid;
}

// Basic email format validation
function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

// Handle file restoration process via AJAX (example)
document.querySelectorAll('.restore-btn').forEach((button) => {
    button.addEventListener('click', function(event) {
        const fileId = button.getAttribute('data-file-id');
        const restoreUrl = `/restore/${fileId}`;

        // Send AJAX request to restore the file
        fetch(restoreUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ file_id: fileId })
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert('File restored successfully!');
                location.reload();  // Reload the page to reflect the changes
            } else {
                alert('Error restoring the file.');
            }
        })
        .catch((error) => {
            alert('Error occurred: ' + error);
        });
    });
});

// Handle file download process via AJAX (example)
document.querySelectorAll('.download-btn').forEach((button) => {
    button.addEventListener('click', function(event) {
        const fileId = button.getAttribute('data-file-id');
        const downloadUrl = `/download/${fileId}`;

        // Send AJAX request to download the file
        fetch(downloadUrl)
        .then((response) => response.blob())
        .then((blob) => {
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `file_${fileId}`;  // Replace with actual file name if available
            link.click();
        })
        .catch((error) => {
            alert('Error occurred while downloading the file.');
        });
    });
});

// Logout functionality (if using localStorage/sessionStorage)
document.getElementById('logout-btn')?.addEventListener('click', function() {
    // Clear sessionStorage or localStorage if needed
    sessionStorage.removeItem('user_logged_in');
    location.href = '/login';  // Redirect to the login page after logout
});

// Example: Notification function to alert users
function showNotification(message, type = 'info') {
    const notificationContainer = document.createElement('div');
    notificationContainer.classList.add('notification', type);
    notificationContainer.textContent = message;
    document.body.appendChild(notificationContainer);

    setTimeout(() => {
        notificationContainer.remove();
    }, 4000); // Remove notification after 4 seconds
}

// Smooth scroll to anchor link
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
});

// Add additional scripts and event listeners below as needed
