document.getElementById("RecSenhaForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (newPassword === confirmPassword) {
        document.getElementById("RecSenhaForm").style.display = "none";

        document.getElementById("successMessage").style.display = "block";
    } else {
        alert("As senhas não coincidem. Por favor, tente novamente.");
    }
});
