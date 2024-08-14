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
    registerBtn.addEventListener('click', () => {
        registerForm.classList.toggle('show');
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

    // Toggle conference update form visibility
    updateBtns.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const form = document.querySelector(`.conference-form[data-id='${id}']`);
            form.classList.toggle('hide');
        });
    });

    // Show confirmation dialog before deleting a conference
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

   $(document).ready(function () {
        $('.select2').select2({
            placeholder: "Select presenters",
            allowClear: true
        });
    });

    document.getElementById('faculty').addEventListener('change', function() {
    const facultyId = this.value;
    const departmentSelect = document.getElementById('department');
    
    // Reset the department select box
    departmentSelect.value = "";
    Array.from(departmentSelect.options).forEach(option => {
        if (option.value && option.getAttribute('data-faculty') !== facultyId) {
            option.style.display = 'none';
        } else {
            option.style.display = 'block';
        }
    });
});
});
