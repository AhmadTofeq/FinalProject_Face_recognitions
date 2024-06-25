document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = document.querySelector(".mode-text");
    const userNameSpan = document.getElementById('user-name');
    const contentDiv = document.getElementById('content');

    // Fetch user's name and update the span
    fetch('../php/get_user_info.php', {
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
            userNameSpan.textContent = data.username; // Update username in span
        } else {
            userNameSpan.textContent = 'Management'; // Default text if username not found
        }
    })
    .catch(error => {
        console.error('Error fetching user info:', error.message);
        userNameSpan.textContent = 'Management'; // Handle error by setting default text
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
        } else {
            modeText.innerText = "Dark mode";
        }
    });

    // Load content based on clicked navigation link
    const links = document.querySelectorAll('.nav-link a');

    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior

            const page = link.getAttribute('data-page');
            checkAuthorization(page);
        });
    });
    function loadPageContent(page) {
        fetch(`../pages/${page}.html`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Page not found - ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                contentDiv.innerHTML = data; // Set fetched HTML content
            })
            .catch(error => {
                console.error('Error fetching page content:', error);
                contentDiv.innerHTML = '<p>Page not found.</p>';
            });
    }
    
    function checkAuthorization(page) {
        fetch('../php/check-auth.php', {
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
            if (data.role === 'admin' || (data.role === 'user' && ['test-camera', 'conferences'].includes(page))) {
                loadPageContent(page);
            } else {
                alert('Unauthorized access!');
            }
        })
        .catch(error => console.error('Error checking authorization:', error));
    }

   
    const logoutBtn = document.getElementById('logoutBtn');

    logoutBtn.addEventListener('click', function(event) {
        event.preventDefault();

        fetch('../php/logout.php', {
            method: 'POST',
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Clear session and redirect to login page
                window.location.href = '../index.php'; // Adjust path as necessary
            } else {
                console.error('Logout failed:', data.message);
                // Optionally handle failed logout (e.g., show error message)
            }
        })
        .catch(error => {
            console.error('Error during logout:', error);
            // Optionally handle errors during logout
        });
    });
});

