<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Contact_Us</title>
  <!-- Google Fonts Link For Icons -->
  <link rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@48,400,0,0">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css" />
  <link rel="stylesheet" href="../css/contact_us_style.css">
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

  <div class="container">
    <div class="content">
      <div class="left-side">
        <div class="address details">
          <i class="fas fa-map-marker-alt"></i>
          <div class="topic">Address</div>
          <div class="text-one">Iraq, Soran</div>
          <div class="text-two">Delzyan 06</div>
        </div>
        <div class="phone details">
          <i class="fas fa-phone-alt"></i>
          <div class="topic">Phone</div>
          <div class="text-one">+964 783 269 9909</div>
          <div class="text-two">+964 750 828 5828</div>
        </div>
        <div class="email details">
          <i class="fas fa-envelope"></i>
          <div class="topic">Email</div>
          <div class="text-one">ahmadtofeq192@gmail.com</div>
          <div class="text-two">mr5121@cs.soran.edu.iq</div>
        </div>
      </div>
      <div class="right-side">
        <div class="topic-text">Send us a message</div>
        <p>If you need help or any feedback or issue be free to tell us</p>
        <form action="#">
          <div class="input-box">
            <input type="text" placeholder="Enter your name" />
          </div>
          <div class="input-box">
            <input type="text" placeholder="Enter your email" />
          </div>
          <div class="input-box message-box">
            <textarea placeholder="Enter your message"></textarea>
          </div>
          <div class="button">
            <input type="button" value="Send Now" />
          </div>
        </form>
      </div>
    </div>
  </div>
  <footer class="footer">
    © 2023. All Rights Reserved. <a href="mailto:Soran_Face@idq">Soran_Face@idq</a>
  </footer>
</body>
</html>