function sendPasswordReset() {
    const resetEmail = document.getElementById('resetEmail').value;
    const initialMessage = document.getElementById('texto'); // Seleciona a mensagem inicial
    const modalContent = document.getElementById('modalContent');

    if (resetEmail) {
        // Oculta a mensagem inicial
        texto.style.display = 'none';

        // Mostra a mensagem de confirmação
        modalContent.innerHTML = '<h2>Mensagem Enviada</h2><p>Mensagem para redefinição de senha enviada! Verifique sua Caixa de Entrada ou Caixa de Spam.</p>';

        // Opcional: desabilitar o botão e o campo de entrada
        document.getElementById('resetEmail').style.display = 'none';
        document.getElementById('confirmResetButton').style.display = 'none';
    } else {
        alert('Por favor, insira um e-mail.');
    }
}
