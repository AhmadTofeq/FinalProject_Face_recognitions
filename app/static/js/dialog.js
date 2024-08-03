// static/js/logout.js
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');
    const dialog = document.getElementById('logoutDialog');
    const cancelBtn = dialog.querySelector('.cancel');
    const deleteBtn = dialog.querySelector('.delete');

    logoutBtn.addEventListener('click', function(event) {
        event.preventDefault();
        dialog.classList.add('show');
    });

    cancelBtn.addEventListener('click', function() {
        dialog.classList.remove('show');
    });

    deleteBtn.addEventListener('click', function() {
        fetch('/logout', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                window.location.href = '/';
            } else {
                console.error('Logout failed:', data.message);
                dialog.classList.remove('show');
            }
        })
        .catch(error => {
            console.error('Error during logout:', error);
            dialog.classList.remove('show');
        });
    });
});
