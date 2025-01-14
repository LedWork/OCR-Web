<template>
  <div>
    <nav class="navbar navbar-light bg-light fixed-top">
      <div class="container-fluid justify-content-center">
        <img
          src="../public/pck-logo.png"
          alt="PCK Logo"
          class="navbar-logo me-2"
        />
        <p class="navbar-brand mb-0 text-center">PCK-OCR</p>
      </div>
    </nav>
    <div class="content-container">
      <RouterView />
    </div>
  </div>
</template>

<style>
.navbar-logo {
  height: 60px;
  width: auto;
}

body {
  background-color: #c9c9c9;
  margin: 0;
  padding: 0;
}

html, body {
  height: 100%;
}

.content-container {
  padding-top: 50px;
}

.container-fluid {
  max-width: 100%;
}

</style>
