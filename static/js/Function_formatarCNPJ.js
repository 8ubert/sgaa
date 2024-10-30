// Função para formatar CNPJ
function formatarCNPJ(e) {
    let input = e.target.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    if (input.length > 14) input = input.slice(0, 14); // Limita a 14 dígitos
    if (input.length > 2) input = input.replace(/(\d{2})(\d)/, '$1.$2'); // Adiciona o primeiro ponto
    if (input.length > 5) input = input.replace(/(\d{2})\.(\d{3})(\d)/, '$1.$2.$3'); // Adiciona o segundo ponto
    if (input.length > 8) input = input.replace(/(\d{2})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3/$4'); // Adiciona a barra
    if (input.length > 12) input = input.replace(/(\d{2})\.(\d{3})\.(\d{3})\/(\d{4})(\d)/, '$1.$2.$3/$4-$5'); // Adiciona o traço
    e.target.value = input; // Atualiza o valor do input
}

document.getElementById("cnpj").addEventListener("input", formatarCNPJ);
document.getElementById("cnpj2").addEventListener("input", formatarCNPJ);