document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body');
    const sidebar = body.querySelector('nav');
    const toggle = body.querySelector(".toggle");
    const modeSwitch = body.querySelector(".toggle-switch");
    const modeText = document.querySelector(".mode-text");
    const userNameSpan = document.getElementById('user-name');

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
    

    async function getCameras() {
            const devices = await navigator.mediaDevices.enumerateDevices();
            return devices.filter(device => device.kind === 'videoinput');
        }

        async function startCamera(videoElement, deviceId) {
            if (navigator.mediaDevices.getUserMedia) {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        deviceId: deviceId ? { exact: deviceId } : undefined
                    }
                });
                videoElement.srcObject = stream;
            } else {
                alert('getUserMedia not supported on your browser!');
            }
        }

        async function init() {
            const cameras = await getCameras();
            const selectCamera1 = document.getElementById('select-camera1');
            const selectCamera2 = document.getElementById('select-camera2');

            cameras.forEach((camera, index) => {
                const option1 = document.createElement('option');
                const option2 = document.createElement('option');
                option1.value = camera.deviceId;
                option2.value = camera.deviceId;
                option1.text = camera.label || `Camera ${index + 1}`;
                option2.text = camera.label || `Camera ${index + 1}`;
                selectCamera1.appendChild(option1);
                selectCamera2.appendChild(option2);
            });

            // Start with the first available camera
            if (cameras.length > 0) {
                startCamera(document.getElementById('video1'), selectCamera1.value);
                startCamera(document.getElementById('video2'), selectCamera2.value);
            }

            selectCamera1.onchange = () => startCamera(document.getElementById('video1'), selectCamera1.value);
            selectCamera2.onchange = () => startCamera(document.getElementById('video2'), selectCamera2.value);
        }

        window.onload = init;

});
