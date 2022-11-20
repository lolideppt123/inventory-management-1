const passwordToggle = document.querySelector(".passwordToggle");
const passwordField = document.querySelector("#passwordField");

passwordToggle.addEventListener("click", showHidePasswordToggle);

function showHidePasswordToggle() {
    if (passwordToggle.textContent === "SHOW") {
        passwordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
        console.log("clicked");
    }
    else {
        passwordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
}