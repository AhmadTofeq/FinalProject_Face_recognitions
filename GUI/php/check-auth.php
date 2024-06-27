<?php
session_start();

if (isset($_SESSION['username']) && isset($_SESSION['role'])) {
    echo json_encode(['role' => $_SESSION['role']]);
} else {
    http_response_code(401);
    echo json_encode(['error' => 'Unauthorized']);
}
?>
