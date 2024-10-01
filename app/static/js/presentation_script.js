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
            const container = document.querySelector(`.conference-form-container[data-id='${id}']`);
            container.classList.toggle('hide');
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

   $(document).ready(function() {
        $('#presenter').select2({
            placeholder: "Select presenters",
            allowClear: true,
            width: '100%',
            matcher: function(params, data) {
                if ($.trim(params.term) === '') {
                    return data;
                }
                if (data.text.toLowerCase().indexOf(params.term.toLowerCase()) > -1) {
                    return data;
                }
                return null;
            }
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
   document.querySelectorAll('.update-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const presentationId = this.getAttribute('data-id');
            const facultySelect = document.getElementById(`faculty_${presentationId}`);
            const departmentSelect = document.getElementById(`department_${presentationId}`);

            // Filter departments based on the selected faculty
            facultySelect.addEventListener('change', function() {
                const facultyId = this.value;

                Array.from(departmentSelect.options).forEach(option => {
                    if (option.value && option.getAttribute('data-faculty') !== facultyId) {
                        option.style.display = 'none';
                    } else {
                        option.style.display = 'block';
                    }
                });

                // Keep the current department selected if it matches the selected faculty
                if (departmentSelect.querySelector('option[selected]')) {
                    departmentSelect.value = departmentSelect.querySelector('option[selected]').value;
                } else {
                    departmentSelect.value = "";  // Reset the department selection if no match
                }
            });

            // Trigger change event to filter departments based on the initially selected faculty
            facultySelect.dispatchEvent(new Event('change'));
        });
    });
    // Show the preview box when 'Preview' button is clicked
    document.querySelectorAll('.preview-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const presentationId = this.getAttribute('data-id');
            const previewBox = document.querySelector(`.preview-box[data-id="${presentationId}"]`);
            previewBox.style.display = 'block';
        });
    });

    // Hide the preview box when 'Close' button is clicked
    document.querySelectorAll('.close-preview').forEach(function(button) {
        button.addEventListener('click', function() {
            const previewBox = this.closest('.preview-box');
            previewBox.style.display = 'none';
        });
    });


});
