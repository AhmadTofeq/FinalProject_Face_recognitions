document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = document.querySelector(".mode-text");
    const userNameSpan = document.getElementById('user-name');


    function updateTime() {
        const now = new Date();
        const formattedTime = now.getFullYear() + '-' + 
                              String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                              String(now.getDate()).padStart(2, '0') + ' ' + 
                              String(now.getHours()).padStart(2, '0') + ':' + 
                              String(now.getMinutes()).padStart(2, '0') + ':' + 
                              String(now.getSeconds()).padStart(2, '0');
        document.getElementById('current-time').textContent = formattedTime;
    }

    // Update the time immediately and every second
    updateTime();
    setInterval(updateTime, 1000);
    
    const finishBtn = document.getElementById('finish-btn');
    const finishForm = document.getElementById('finish-form');
    const dialog = document.getElementById('DialogFinish');
    const overlay = document.getElementById('dialogOverlay');
    const cancelBtn = document.querySelector('.cancel');
    const confirmBtn = document.querySelector('.delete');

    // Show the dialog when the finish button is clicked
    finishBtn.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent form submission
        dialog.classList.add('show'); // Show dialog
        overlay.classList.add('show'); // Show overlay
    });

    // Hide the dialog if the cancel button is clicked
    cancelBtn.addEventListener('click', function () {
        dialog.classList.remove('show');
        overlay.classList.remove('show');
    });

    // Submit the form when the delete (confirm) button is clicked
    confirmBtn.addEventListener('click', function () {
        finishForm.submit(); // Submit the form programmatically
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
