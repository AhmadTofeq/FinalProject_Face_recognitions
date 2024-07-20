<?php
session_start();

require 'config.php'; // Adjust the path as per your directory structure

if (!isset($_SESSION['role']) || $_SESSION['role'] !== 'admin') {
    header("HTTP/1.1 403 Forbidden");
    exit("You do not have permission to access this page.");
}

$message = '';
$message_type = '';

if (isset($_GET['message']) && isset($_GET['type'])) {
    $message = $_GET['message'];
    $message_type = $_GET['type'];
}

$query = "SELECT * FROM users WHERE state = 1";
$result = $conn->query($query);

$users = array();
if ($result && $result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $users[] = $row;
    }
} else {
    if (!$result) {
        $message = "Error: " . $conn->error;
        $message_type = "error";
    }
}

// Handle update and delete actions
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['update'])) {
        $id = $_POST['id'];
        $name = $_POST['name'];
        $username = $_POST['username'];
        $password = $_POST['password'] ? password_hash($_POST['password'], PASSWORD_BCRYPT) : null;
        $role = $_POST['role'];

        if ($password) {
            $sql = "UPDATE users SET name = ?, username = ?, password = ?, role = ? WHERE id = ?";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param("ssssi", $name, $username, $password, $role, $id);
        } else {
            $sql = "UPDATE users SET name = ?, username = ?, role = ? WHERE id = ?";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param("sssi", $name, $username, $role, $id);
        }

        if ($stmt->execute()) {
            $message = "User updated successfully.";
            $message_type = "success";
        } else {
            $message = "Error: " . $stmt->error;
            $message_type = "error";
        }
        $stmt->close();
    } elseif (isset($_POST['delete'])) {
        $id = $_POST['id'];
        $sql = "UPDATE users SET state = 0 WHERE id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("i", $id);

        if ($stmt->execute()) {
            $message = "User deleted successfully.";
            $message_type = "success";
        } else {
            $message = "Error: " . $stmt->error;
            $message_type = "error";
        }
        $stmt->close();
    }
}

$conn->close();
?>
