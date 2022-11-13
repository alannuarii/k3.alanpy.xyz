const inputPassword = document.querySelector(".input-password");

function show() {
  if (inputPassword.type === "password") {
    inputPassword.type = "text";
  } else {
    inputPassword.type = "password";
  }
}
