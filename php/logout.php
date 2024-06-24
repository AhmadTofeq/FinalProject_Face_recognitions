<?php
session_start();
header('Content-Type: application/json');

// Perform logout actions
if (isset($_SESSION['username'])) {
    // Clear all session data
    $_SESSION = array();

    // Destroy the session
    if (ini_get("session.use_cookies")) {
        $params = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000,
            $params["path"], $params["domain"],
            $params["secure"], $params["httponly"]
        );
    }
    session_destroy();

    // Return success response
    echo json_encode(['success' => true]);
} else {
    // Return error response if not logged in
    echo json_encode(['success' => false, 'message' => 'User not logged in']);
}
?>
