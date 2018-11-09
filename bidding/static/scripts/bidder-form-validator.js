var submitButton = document.querySelector("#submit");
var mobileCheckout = document.querySelector("#id_mobile_checkout");
var emailAddress = document.querySelector("#id_email_address");

mobileCheckout.addEventListener("click", checkSubmitButton);
emailAddress.addEventListener("input", checkSubmitButton);

function checkSubmitButton() {
    if (mobileCheckout.checked && emailAddress.value=="") {
        submitButton.setAttribute("disabled", "true");
        emailAddress.classList.add("missing-value");
    }
    
    else {
        submitButton.removeAttribute("disabled");
        emailAddress.classList.remove("missing-value");
    }
}

