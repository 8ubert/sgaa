// Função para formatar CEP
function formatarCEP(e) {
    let input = e.target.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    if (input.length > 8) input = input.slice(0, 8); // Limita a 8 dígitos
    if (input.length > 5) input = input.replace(/(\d{5})(\d)/, '$1-$2'); // Adiciona o traço
    e.target.value = input; // Atualiza o valor do input
}

// Aplicando o evento de input nos campos desejados
document.getElementById("cep").addEventListener("input", formatarCEP);
document.getElementById("cep2").addEventListener("input", formatarCEP);
