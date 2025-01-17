document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById("id_password");
    const togglePasswordButton = document.getElementById("toggle-password-visibility");

    togglePasswordButton.addEventListener("click", () => {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePasswordButton.querySelector("img").src = "/static/img/eye.svg";
        } else {
            passwordInput.type = "password";
            togglePasswordButton.querySelector("img").src = "/static/img/eye-slash.svg";
        }
    });
});
