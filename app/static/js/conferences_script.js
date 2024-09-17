document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = document.querySelector(".mode-text");
    const userNameSpan = document.getElementById('user-name');
    const checkbox = document.getElementById('timeFilterCheckbox');
    const checkboxText = document.getElementById('checkboxText');


    // Select all necessary elements
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
    const modalAddedBy = document.getElementById('modalAddedBy');
    const exportButton = document.getElementById('exportButton');
    const startButton = document.getElementById('startButton');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const modalActivityType = document.getElementById('modalActivityType');
    // Function to format date and time
    function formatDateTime(datetimeStr) {
        const options = { 
            year: 'numeric', month: 'long', day: 'numeric',
            hour: '2-digit', minute: '2-digit' 
        };
        const date = new Date(datetimeStr);
        return date.toLocaleDateString(undefined, options);
    }

    // Event listener for each settings button
    settingsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');

            // Retrieve data attributes from the selected row
            const presentationId = row.getAttribute('data-id');
            const title = row.getAttribute('data-title');
            const datetime = row.getAttribute('data-datetime');
            const presenters = row.getAttribute('data-presenters');
            const duration = row.getAttribute('data-duration');
            const hall = row.getAttribute('data-hall');
            const pointPresenter = row.getAttribute('data-point-presenter');
            const pointAttendance = row.getAttribute('data-point-attendance');
            const maxLate = row.getAttribute('data-max-late');
            const department = row.getAttribute('data-department');
            const facultyName = row.getAttribute('data-faculty-id');
            const activityType = row.getAttribute('data-activity-type'); // New line
            const addedBy = row.getAttribute('data-added-by');

            // Populate modal with retrieved data
            modalTitle.textContent = title || 'N/A';
            modalDatetime.textContent = datetime ? formatDateTime(datetime) : 'N/A';
            modalPresenters.textContent = presenters || 'N/A';
            modalDuration.textContent = duration ? `${duration} minutes` : 'N/A';
            modalHall.textContent = hall || 'N/A';
            modalPointPresenter.textContent = pointPresenter || 'N/A';
            modalPointAttendance.textContent = pointAttendance || 'N/A';
            modalMaxLate.textContent = maxLate ? `${maxLate} minutes` : 'N/A';
            modalDepartment.textContent = department || 'N/A';
            modalFacultyId.textContent = facultyName || 'N/A';
            modalActivityType.textContent = activityType || 'N/A';
            modalAddedBy.textContent = addedBy || 'N/A';

            // Check if the presentation date has passed
            const presentationDatetime = new Date(datetime);
            const currentDatetime = new Date();

            if (presentationDatetime < currentDatetime) {
                // Show the export button if the presentation has passed
                exportButton.style.display = 'inline-block';
                exportButton.onclick = function() {
                    // Implement export functionality here
                    alert('Export functionality is not yet implemented.');
                };
            } else {
                // Hide the export button if the presentation is upcoming
                exportButton.style.display = 'none';
            }

            // Set the href for the Start button dynamically
            startButton.href = `/start_conference/${presentationId}`;

            // Open the modal
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
            checkboxText.textContent = 'Show Upcoming presentation Only';
        } else {
            checkboxText.textContent = 'Show Past presentation Only';
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
