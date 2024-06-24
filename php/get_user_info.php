<?php
session_start();
header('Content-Type: application/json');

if (isset($_SESSION['username'])) {
    $response = [
        'username' => $_SESSION['username'],
        'role' => $_SESSION['role']
    ];
    echo json_encode($response);
} else {
    http_response_code(401); // Unauthorized status code
    echo json_encode(['error' => 'User not logged in']);
}
?>
