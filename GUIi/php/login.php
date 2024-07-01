<?php
session_start();
require 'config.php'; // Adjust the path as per your directory structure

$response = array('success' => false, 'message' => '');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $sql = "SELECT * FROM users WHERE username = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows == 1) {
        $user = $result->fetch_assoc();
        if ($user['state'] == 0) {
            $response['message'] = 'Your account is inactive.';
        } elseif (password_verify($password, $user['password'])) {
            $_SESSION['username'] = $user['username'];
            $_SESSION['role'] = $user['role'];
            $response['success'] = true;
            $response['message'] = 'Login successful.';
            $response['redirect'] = 'project/pages/home.html'; // Set the redirect path
        } else {
            $response['message'] = 'Invalid password.';
        }
    } else {
        $response['message'] = 'Username not found.';
    }
    
    $stmt->close();
    $conn->close();
}

header('Content-Type: application/json');
echo json_encode($response);
?>
