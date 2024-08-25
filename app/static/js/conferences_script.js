document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = document.querySelector(".mode-text");
    const userNameSpan = document.getElementById('user-name');
    const checkbox = document.getElementById('timeFilterCheckbox');
    const checkboxText = document.getElementById('checkboxText');


    const settingsButtons = document.querySelectorAll('.settings-btn');
    const modal = document.getElementById('settingsModal');
    const modalOverlay = document.getElementById('modalOverlay');
    
    // Modal elements
    const modalTitle = document.getElementById('modalTitle');
    const modalDatetime = document.getElementById('modalDatetime');
    const modalPresenters = document.getElementById('modalPresenters');
    const modalDuration = document.getElementById('modalDuration');
    const modalHall = document.getElementById('modalHall');
    const modalPointPresenter = document.getElementById('modalPointPresenter');
    const modalPointAttendance = document.getElementById('modalPointAttendance');
    const modalMaxLate = document.getElementById('modalMaxLate');
    const modalDepartment = document.getElementById('modalDepartment');
    const modalFacultyId = document.getElementById('modalFacultyId');
    const modalDepartmentId = document.getElementById('modalDepartmentId');
    const modalAddedBy = document.getElementById('modalAddedBy');

    settingsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');

            modalTitle.textContent = row.getAttribute('data-title');
            modalDatetime.textContent = row.getAttribute('data-datetime');
            modalPresenters.textContent = row.getAttribute('data-presenters');
            modalDuration.textContent = row.getAttribute('data-duration');
            modalHall.textContent = row.getAttribute('data-hall');
            modalPointPresenter.textContent = row.getAttribute('data-point-presenter');
            modalPointAttendance.textContent = row.getAttribute('data-point-attendance');
            modalMaxLate.textContent = row.getAttribute('data-max-late');
            modalDepartment.textContent = row.getAttribute('data-department');
            modalFacultyId.textContent = row.getAttribute('data-faculty-id');  // This is now the faculty name
            modalAddedBy.textContent = row.getAttribute('data-added-by');

            modal.classList.add('active');
            modalOverlay.classList.add('active');
        });
    });

    
    document.getElementById('closeModalBtn').addEventListener('click', function() {
    document.getElementById('settingsModal').classList.remove('active');
    document.getElementById('modalOverlay').classList.remove('active');
    });


    // Function to update the checkbox label text based on the checkbox state
    function updateCheckboxText() {
        if (checkbox.checked) {
            checkboxText.textContent = 'Show Upcoming Conferences Only';
        } else {
            checkboxText.textContent = 'Show Past Conferences Only';
        }
    }

    // Update text on page load
    updateCheckboxText();

    // Update text when the checkbox state changes
    checkbox.addEventListener('change', updateCheckboxText);
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
