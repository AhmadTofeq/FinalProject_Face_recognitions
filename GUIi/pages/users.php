<?php
require '../php/users_processes.php';
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="stylesheet" href="../css/user.css">
    <link href='https://unpkg.com/boxicons@2.1.1/css/boxicons.min.css' rel='stylesheet'>
    <title>Users</title>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            fetch('../php/check-session.php', {
                method: 'GET',
                credentials: 'same-origin'
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Session check failed');
                    }
                    return response.json();
                })
                .then(data => {
                    if (!data.authenticated) {
                        window.location.href = '../index.php';
                    }
                })
                .catch(error => {
                    console.error('Error checking session:', error);
                });
        });
    </script>
</head>
<body>
    <nav class="sidebar close">
        <header>
            <div class="image-text">
                <span class="image">
                    <img src="../imag/soran.png" alt="">
                </span>
                <div class="text logo-text">
                    <span class="name">Soran_Face</span>
                    <span class="profession" id="user-name">Management</span>
                </div>
            </div>
            <i class='bx bx-chevron-right toggle'></i>
        </header>
        <div class="menu-bar">
            <div class="menu">
                <ul class="menu-links">
                    <li class="nav-link">
                        <a href="../pages/home.html" data-page="dashboard">
                            <i class='bx bx-home-alt icon'></i>
                            <span class="text nav-text">Dashboard</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a href="../pages/staff.html" data-page="staff">
                            <i class='bx bx-user-check icon'></i>
                            <span class="text nav-text">Staff</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a href="../pages/conferences.html" data-page="conferences">
                            <i class='bx bx-chalkboard icon'></i>
                            <span class="text nav-text">Conferences</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a href="../pages/r-conferences.html" data-page="r-conferences">
                            <i class='bx bx-registered icon'></i>
                            <span class="text nav-text">R-Conferences</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a href="../pages/test-camera.html" data-page="test-camera">
                            <i class='bx bx-video-recording icon'></i>
                            <span class="text nav-text">Test Camera</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a href="../pages/users.php" data-page="users" class="active">
                            <i class='bx bx-user icon'></i>
                            <span class="text nav-text">Users</span>
                        </a>
                    </li>
                    <li class="nav-link">
                        <a href="../pages/model-train.html" data-page="model-train">
                            <i class='bx bx-cube-alt icon'></i>
                            <span class="text nav-text">Model Train</span>
                        </a>
                    </li>
                </ul>
            </div>
            <div class="bottom-content">
                <li>
                    <a href="#" id="logoutBtn">
                        <i class='bx bx-log-out icon'></i>
                        <span class="text nav-text">Logout</span>
                    </a>
                </li>
                <li class="mode">
                    <div class="sun-moon">
                        <i class='bx bx-moon icon moon'></i>
                        <i class='bx bx-sun icon sun'></i>
                    </div>
                    <span class="mode-text text">Dark mode</span>
                    <div class="toggle-switch">
                        <span class="switch"></span>
                    </div>
                </li>
            </div>
        </div>
    </nav>
    <section class="home">
        <div class="page-content">
            <h2>Users</h2>
            <p>Manage users below.</p>

            <?php if (isset($message)) { ?>
                <div class="popup <?php echo $message_type; ?>">
                    <p class="below"><?php echo $message; ?></p>
                </div>
            <?php } ?>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Username</th>
                        <th>Role</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <?php if (!empty($users)) { ?>
                        <?php foreach ($users as $user) { ?>
                            <tr>
                                <td><?php echo htmlspecialchars($user['id']); ?></td>
                                <td><?php echo htmlspecialchars($user['name']); ?></td>
                                <td><?php echo htmlspecialchars($user['username']); ?></td>
                                <td><?php echo htmlspecialchars($user['role']); ?></td>
                                <td>
                                    <button class="update-btn" data-id="<?php echo htmlspecialchars($user['id']); ?>">Update</button>
                                    <form action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>" method="post" class="user-form hide" data-id="<?php echo htmlspecialchars($user['id']); ?>">
                                        <input type="hidden" name="id" value="<?php echo htmlspecialchars($user['id']); ?>">
                                        <label for="name">Name:</label>
                                        <input type="text" id="name" name="name" value="<?php echo htmlspecialchars($user['name']); ?>" required>
                                        <label for="username">Username:</label>
                                        <input type="text" id="username" name="username" value="<?php echo htmlspecialchars($user['username']); ?>" required>
                                        <label for="password">Password:</label>
                                        <input type="password" id="password" name="password">
                                        <label for="role">Role:</label>
                                        <select id="role" name="role" required>
                                            <option value="user" <?php echo $user['role'] == 'user' ? 'selected' : ''; ?>>User</option>
                                            <option value="admin" <?php echo $user['role'] == 'admin' ? 'selected' : ''; ?>>Admin</option>
                                        </select>
                                        <button type="submit" name="update" class="btn-update">Update</button>
                                        <button type="submit" name="delete" class="btn-delete">Delete</button>
                                    </form>
                                </td>
                            </tr>
                        <?php } ?>
                    <?php } else { ?>
                        <tr>
                            <td colspan="5">No users found.</td>
                        </tr>
                    <?php } ?>
                </tbody>
            </table>

            <!-- Register user form -->
            <div class="register-container">
                <button class="register-btn">
                    <i class='bx bx-plus'></i>
                </button>
                <div class="register-form hide">
                    <form id="register-user-form" action="../php/register_user.php" method="post">
                        <div class="form-group">
                            <label for="name">Name:</label>
                            <input type="text" id="name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="username">Username:</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <div class="form-group">
                            <label for="role">Role:</label>
                            <select id="role" name="role" required>
                                <option value="user">User</option>
                                <option value="admin">Admin</option>
                            </select>
                        </div>
                        <input type="submit" value="Register" class="submit-btn">
                    </form>
                </div>
            </div>
    </section>
    <script src="../js/users_script.js"></script>
</body>
</html>
