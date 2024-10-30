//Script para selecionar qual tipo de calendário vai ser mostrado, isso inclui a aparição do calendário E a seleção do botão
document.addEventListener("DOMContentLoaded", function() {
    const BotaoMensal = document.getElementById('monthly-view');
    const BotaoSemanal = document.getElementById('weekly-view');
    const CalendarioMensal = document.getElementById('monthly-calendar');
    const CalendarioSemanal = document.getElementById('weekly-calendar');

    BotaoMensal.addEventListener('click', function() {
        BotaoMensal.classList.add('active');
        BotaoSemanal.classList.remove('active');
        CalendarioMensal.classList.remove('hidden');
        CalendarioSemanal.classList.add('hidden');
    });

    BotaoSemanal.addEventListener('click', function() {
        BotaoSemanal.classList.add('active');
        BotaoMensal.classList.remove('active');
        CalendarioSemanal.classList.remove('hidden');
        CalendarioMensal.classList.add('hidden');
    });
});

//Função para deixar a imagem de engrenagem selecionável, e consequentemente fazer aparecer as duas opções (por enquanto estão nomeadas como opção 1 e 2
//pois para cada tipo de usuário são opções diferentes, e isso será definido mais tarde, não sei se com o python ou pelo html msm)
function toggleMenu() {
    var menu = document.getElementById("config-menu");
    if (menu.style.display === "block") {
        menu.style.display = "none";
    } else {
        menu.style.display = "block";
    }
}

function agendamentos() {
    window.location.href = '/menu';
}

function disponibilidades() {
    window.location.href = '/config/disponibilidades';
}

function turmas() {
    window.location.href = '/config/turmas';
}

function account() {
    window.location.href = '/config/conta';
}

function logout() {
    alert("Você está sendo desconectado.");
    window.location.href = '/auth/logout';
}

function agendar1() {
    window.location.href = '/agendar';    
}