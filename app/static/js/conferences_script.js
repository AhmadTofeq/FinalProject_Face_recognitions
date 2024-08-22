document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = document.querySelector(".mode-text");
    const userNameSpan = document.getElementById('user-name');
    const checkbox = document.getElementById('timeFilterCheckbox');
    const checkboxText = document.getElementById('checkboxText');

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
