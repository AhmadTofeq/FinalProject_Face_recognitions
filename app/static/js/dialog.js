document.addEventListener('DOMContentLoaded', function() {
    // Function to setup dialog for different operations
    function setupDialog(buttonSelector, dialogId, confirmCallback) {
        const buttons = document.querySelectorAll(buttonSelector);
        const dialog = document.getElementById(dialogId);
        const cancelBtn = dialog.querySelector('.cancel');
        const confirmBtn = dialog.querySelector('.delete');

        let currentForm = null;

        buttons.forEach(button => {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                currentForm = this.closest('form');
                dialog.classList.add('show');
            });
        });

        cancelBtn.addEventListener('click', function() {
            dialog.classList.remove('show');
            currentForm = null;
        });

        confirmBtn.addEventListener('click', function() {
            if (currentForm) {
                confirmCallback(currentForm);
            }
            dialog.classList.remove('show');
            currentForm = null;
        });
    }

    // Logout dialog setup
    setupDialog('#logoutBtn', 'logoutDialog', function() {
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
            }
        })
        .catch(error => {
            console.error('Error during logout:', error);
        });
    });

    // Delete user dialog setup
    setupDialog('.btn-delete-user', 'deleteUserDialog', function(form) {
        form.submit();
    });

    // Delete staff dialog setup
    setupDialog('.btn-delete', 'deleteStaffDialog', function(form) {
        form.submit();
    });
});
