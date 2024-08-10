document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = document.querySelector(".mode-text");
    const userNameSpan = document.getElementById('user-name');
    const searchBar = document.getElementById('search-bar');
    const staffButtonsContainer = document.getElementById('staff-container');
    const staffButtons = staffButtonsContainer.getElementsByClassName('btn-staff');

    searchBar.addEventListener('input', function () {
        const query = searchBar.value.toLowerCase();

        Array.from(staffButtons).forEach(button => {
            const id = button.getAttribute('data-id').toLowerCase();
            const name = button.getAttribute('data-name').toLowerCase();

            if (id.includes(query) || name.includes(query)) {
                button.style.display = '';
            } else {
                button.style.display = 'none';
            }
        });
    });

    // Select the delete model button
    const deleteModelButton = document.querySelector('.btn.btn-3');
    // Select the dialog and the cancel/confirm buttons
    const dialog = document.getElementById('deleteStaffDialog');
    const cancelBtn = dialog.querySelector('.cancel');
    const confirmDeleteBtn = dialog.querySelector('.delete');

    let currentForm = null; // Store the current form to be deleted

    // Show confirmation dialog before deleting model data
    deleteModelButton.addEventListener('click', function(event) {
        event.preventDefault();
        currentForm = this.closest('form'); // Store the current form to be deleted
        dialog.classList.remove('hide'); // Show the confirmation dialog
        dialog.classList.add('show'); // Add show class for visibility
    });

    // Handle cancel button in the dialog
    cancelBtn.addEventListener('click', function() {
        dialog.classList.remove('show'); // Hide the confirmation dialog
        dialog.classList.add('hide'); // Add hide class for visibility
        currentForm = null; // Reset the current form
    });

    // Handle confirm delete button in the dialog
    confirmDeleteBtn.addEventListener('click', function() {
        if (currentForm) {
            currentForm.submit(); // Submit the stored form
        }
        dialog.classList.remove('show'); // Hide the confirmation dialog
        dialog.classList.add('hide'); // Add hide class for visibility
    });


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
    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("close");
    });

    // Toggle dark mode
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

    // Check if mode is dark or light on page load
    const storedMode = localStorage.getItem("mode");
    if (storedMode === "dark") {
        body.classList.add("dark");
        modeText.innerText = "Light mode";
    } else {
        body.classList.remove("dark");
        modeText.innerText = "Dark mode";
    }

    // Set active navigation link based on current page
    const links = document.querySelectorAll('.nav-link a');
    const currentPage = window.location.pathname.split('/').pop().split('.')[0]; // Get current page name

    links.forEach(link => {
        const page = link.getAttribute('data-page');
        if (page === currentPage) {
            link.parentElement.classList.add('active');
        } else {
            link.parentElement.classList.remove('active');
        }
    });

    
});
