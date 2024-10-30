function toggleMenu() {
    // Aqui você pode adicionar a funcionalidade do menu de configurações
    alert("Menu de configurações ativado!");
}

function toggleMenu() {
    var menu = document.getElementById("config-menu");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

//parte de linguas teste integração com python
document.addEventListener('DOMContentLoaded', function() {
    fetch('/languages')
        .then(response => response.json())
        .then(data => {
            const dropdown = document.getElementById('lingua-dropdown');
            data.languages.forEach(language => {
                const option = document.createElement('option');
                option.value = language;
                option.textContent = language;
                dropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Erro ao carregar as línguas:', error));
});

