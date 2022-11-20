const firstnameField = document.querySelector("#firstnameField");
const lastnameField = document.querySelector("#lastnameField");
const usernameField = document.querySelector("#usernameField");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const myForm = document.querySelector("#registrationForm");

const firstnamefeedback = document.querySelector(".firstname-feedback");
const lastnamefeedback = document.querySelector(".lastname-feedback");
const usernamefeedback = document.querySelector(".username-feedback");
const emailfeedback = document.querySelector(".email-feedback");
const formfeedback = document.querySelector(".form-feedback");
const passwordToggle = document.querySelector(".passwordToggle");

const usernameURL = "/authentication/validate-username";
const firstnameURL = "/authentication/validate-firstname";
const lastnameURL = "/authentication/validate-lastname";
const emailURL = "/authentication/validate-email";

const firstnameValidation = formFieldValidation(firstnameField, firstnamefeedback, firstnameURL);
const usernameValidation = formFieldValidation(usernameField, usernamefeedback, usernameURL);
const lastnameValidation = formFieldValidation(lastnameField, lastnamefeedback, lastnameURL);
const emailValidation = formFieldValidation(emailField, emailfeedback, emailURL);

firstnameField.addEventListener("keyup", firstnameValidation);
usernameField.addEventListener("keyup", usernameValidation);
lastnameField.addEventListener("keyup", lastnameValidation);
emailField.addEventListener("keyup", emailValidation);
passwordToggle.addEventListener("click", showHidePasswordToggle);
myForm.addEventListener("submit", formRegisterValidate);


function formFieldValidation(fieldName, feedback, fetchURL, formValidation = formfeedback) {
    return async function inner(e) {
        const targetFieldValue = e.target.value;
        console.log(targetFieldValue);

        fieldName.classList.remove("is-invalid");
        formValidation.style.display = "none";
        feedback.style.display = "none";

        const response = await fetch(fetchURL, { body: JSON.stringify({ fieldvalue: targetFieldValue }), method: "POST" });
        console.log(response);
        const processResponse = await response.json();

        console.log(processResponse);
        if (processResponse.msg_error) {
            fieldName.classList.add("is-invalid");
            feedback.style.display = "block";
            feedback.innerHTML = `<p>${processResponse.msg_error}</p>`;
        }
        if (processResponse.msg_valid) fieldName.classList.add("is-valid");
    }
}

function showHidePasswordToggle() {
    if (passwordToggle.textContent === "SHOW") {
        passwordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    }
    else {
        passwordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
}

function formRegisterValidate(e) {
    if (firstnameField.classList.contains('is-invalid') || lastnameField.classList.contains('is-invalid') || usernameField.classList.contains('is-invalid') || emailField.classList.contains('is-invalid') || passwordField.classList.contains('is-invalid')) {
        e.preventDefault();
        formfeedback.style.display = "block";
        formfeedback.innerHTML = `<p>Invalid Credentials</p>`;
    }
}

// lastnameField.addEventListener("keyup", e => {
//     console.log(777, 777);
//     const lastnameValue = e.target.value;

//     // Removes invalid styles when user type in correct info after an invalid info.
//     lastnameField.classList.remove("is-invalid");
//     lastnamefeedback.style.display = "none";

//     // Adds invalid styles when user type in invalid info.
//     if (lastnameValue.length > 0) {
//         fetch("/authentication/validate-lastname", {
//             body: JSON.stringify({ lastname: lastnameValue }),
//             method: "POST",
//         })
//             .then(response => {
//                 res = response.json();
//                 console.log(res);
//                 return res; //can only consume Response.json() once.
//             })
//             .then(response => {
//                 console.log("data", response);
//                 if (response.msg_error) {
//                     lastnameField.classList.add("is-invalid");
//                     lastnamefeedback.style.display = "block";
//                     lastnamefeedback.innerHTML = `<p>${response.msg_error}</p>`;
//                 }
//             })
//     }
// });

