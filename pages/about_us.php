<!DOCTYPE html>
<!-- Coding By CodingNepal - www.codingnepalweb.com -->
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soran_Face</title>
    <!-- Google Fonts Link For Icons -->
    <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@48,400,0,0">
    <link rel="stylesheet" href="../css/about_us_style.css">
    <script src="../js/index_script.js" defer></script>
</head>

<body>
    <header>
        <nav class="navbar">
            <span class="hamburger-btn material-symbols-rounded">menu</span>
            <a href="../index.php" class="logo">
                <img src="../imag/Soran_Logo.png" alt="logo">
                <h2>Soran_Face</h2>
            </a>
            <ul class="links">
                <span class="close-btn material-symbols-rounded">close</span>
                <li><a href="../index.php">Home</a></li>
                <li><a href="about_us.php">About us</a></li>
                <li><a href="contact_us.php">Contact us</a></li>
            </ul>
            <button class="login-btn">LOG IN</button>
        </nav>
    </header>

    <div class="blur-bg-overlay"></div>
    <div class="form-popup">
        <span class="close-btn material-symbols-rounded">close</span>
        <div class="form-box login">
            <div class="form-details">
                <video autoplay muted loop class="background-video">
                    <source src="../imag/animation.mp4" type="video/mp4">
                </video>
                <h2>Welcome Back</h2>
            </div>
            <div class="form-content">
                <h2>LOGIN</h2>
                <form action="#">
                    <div class="input-field">
                        <input type="text" required>
                        <label>Email</label>
                    </div>
                    <div class="input-field">
                        <input type="password" required>
                        <label>Password</label>
                    </div>
                    <a href="contact_us.html" class="forgot-pass-link">Forgot password?</a>
                    <button type="submit">Log In</button>
                </form>
            </div>
        </div>
    </div>
    <section class="about-us">
        <div class="about">
            <h2>About Us</h2>
            <div class="images">
                <img src="../imag/girl.jpg" class="pic" />
                <img src="../imag/mohamad.jpg" class="pic" />
            </div>
            <div class="text">
                <h5>Front-end && back-end Developer & <span>Designer</span></h5>
                <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Expedita natus ad sed harum itaque ullam enim
                    quas,
                    veniam accusantium, quia animi id eos adipisci iusto molestias asperiores explicabo cum vero atque amet
                    corporis! Soluta illum facere consequuntur magni. Ullam dolorem repudiandae cumque voluptate consequatur
                    consectetur, eos provident necessitatibus reiciendis corrupti!</p>
                <div class="data">
                    <a href="#" class="hire">Contact Us</a>
                </div>
            </div>
        </div>
    </section>
    <footer class="footer">
        © 2023. All Rights Reserved. <a href="mailto:Soran_Face@idq">Soran_Face@idq</a>
    </footer>
</body>

</html>