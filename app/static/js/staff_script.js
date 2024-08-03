document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = document.querySelector(".mode-text");
    const userNameSpan = document.getElementById('user-name');
    const registerBtn = document.querySelector('.register-btn');
    const registerForm = document.querySelector('.register-form');
    const updateBtns = document.querySelectorAll('.update-btn');
    const deleteButtons = document.querySelectorAll('.btn-delete');
    const dialog = document.querySelector('.dialog');
    const cancelBtn = dialog.querySelector('.cancel');
    const confirmDeleteBtn = dialog.querySelector('.delete');

    let currentForm = null; // Variable to keep track of the current form to be deleted

    // Toggle register form visibility
    if (registerBtn) {
        registerBtn.addEventListener('click', () => {
            registerForm.classList.toggle('show');
        });
    }

    // Fetch user's name and update the span
    fetch('/get_user_info', {
        method: 'GET',
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok - ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.username) {
            userNameSpan.textContent = data.username;
        } else {
            userNameSpan.textContent = 'Management';
        }
    })
    .catch(error => {
        console.error('Error fetching user info:', error.message);
        userNameSpan.textContent = 'Management';
    });

    // Toggle sidebar visibility
    if (toggle) {
        toggle.addEventListener("click", () => {
            sidebar.classList.toggle("close");
        });
    }

    // Toggle dark mode
    if (modeSwitch) {
        modeSwitch.addEventListener("click", () => {
            body.classList.toggle("dark");

            if (body.classList.contains("dark")) {
                modeText.innerText = "Light mode";
                localStorage.setItem("mode", "dark"); // Save mode to local storage
            } else {
                modeText.innerText = "Dark mode";
                localStorage.setItem("mode", "light"); // Save mode to local storage
            }
        });
    }

    // Check if mode is dark or light on page load
    const storedMode = localStorage.getItem("mode");
    if (storedMode === "dark") {
        body.classList.add("dark");
        modeText.innerText = "Light mode";
    } else {
        body.classList.remove("dark");
        modeText.innerText = "Dark mode";
    }

    // Show update form when Update button is clicked
    updateBtns.forEach(button => {
        button.addEventListener('click', (event) => {
            const id = event.target.getAttribute('data-id');
            const form = document.querySelector(`.user-form[data-id="${id}"]`);
            form.classList.toggle('hide');
        });
    });

   // Show confirmation dialog before deleting a user
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            currentForm = this.closest('form'); // Store the current form to be deleted
            dialog.classList.add('show'); // Show the confirmation dialog
        });
    });

    // Handle cancel button in the dialog
    cancelBtn.addEventListener('click', function() {
        dialog.classList.remove('show'); // Hide the confirmation dialog
        currentForm = null; // Reset the current form
    });

    // Handle confirm delete button in the dialog
    confirmDeleteBtn.addEventListener('click', function() {
        if (currentForm) {
            currentForm.submit(); // Submit the stored form
        }
        dialog.classList.remove('show'); // Hide the confirmation dialog
    });
});
