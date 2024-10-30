// Função para selecionar o tipo de conta
function selectAccountType(type) {
    const buttons = document.querySelectorAll('.account-type-selection button');
    buttons.forEach(button => {
        button.classList.remove('selected');
    });

    const selectedButton = Array.from(buttons).find(button => button.textContent.includes(type === 'representante' ? 'Representante' : 'Professor'));
    selectedButton.classList.add('selected');

    document.getElementById('additionalFields').style.display = 'block';
    document.getElementById('professorFields').style.display = 'none';
    document.getElementById('representativeFields').style.display = 'none';

    if (type === 'representante') {
        document.getElementById('representativeFields').style.display = 'block';
    } else if (type === 'professor') {
        document.getElementById('professorFields').style.display = 'block';
    }
}

// Função pra e-mail
function addEmailField(targetId) {
    const extraEmailsDiv = document.getElementById(targetId);
    const addEmailButton = extraEmailsDiv.querySelector('p');

    const newEmailInput = document.createElement('input');
    newEmailInput.type = 'email';
    newEmailInput.name = 'emails[]';
    newEmailInput.placeholder = 'Outro E-mail';
    newEmailInput.required = true;

    extraEmailsDiv.insertBefore(newEmailInput, addEmailButton);
}

// Função pra telefone
function addPhoneField(targetId) {
    const extraPhonesDiv = document.getElementById(targetId);
    const newPhoneContainer = document.createElement('div');
    newPhoneContainer.style.display = 'flex';
    newPhoneContainer.style.alignItems = 'center';

    const newDDDInput = document.createElement('input');
    newDDDInput.type = 'text';
    newDDDInput.name = 'ddds[]';
    newDDDInput.placeholder = 'DDD';
    newDDDInput.required = true;
    newDDDInput.style.width = '50px';

    const newPhoneInput = document.createElement('input');
    newPhoneInput.type = 'text';
    newPhoneInput.name = 'telefones[]';
    newPhoneInput.placeholder = 'Número de Telefone';
    newPhoneInput.required = true;
    newPhoneInput.style.flex = '1';

    newPhoneContainer.appendChild(newDDDInput);
    newPhoneContainer.appendChild(newPhoneInput);

    extraPhonesDiv.insertBefore(newPhoneContainer, extraPhonesDiv.querySelector('p'));
}


document.getElementById('addEmail').onclick = () => addEmailField('extraEmails');
document.getElementById('addPhone').onclick = () => addPhoneField('extraPhones');
document.getElementById('addEmailRep').onclick = () => addEmailField('extraEmailsRep');
document.getElementById('addPhoneRep').onclick = () => addPhoneField('extraPhonesRep');

// Função pra qualificações
function addQualification() {
    const qualificacoesContainer = document.getElementById('qualificacoesContainer');
    const qualificationFields = document.createElement('div');
    qualificationFields.className = 'qualification-fields';
    
    const languageInput = document.createElement('input');
    languageInput.type = 'text';
    languageInput.name = 'idiomas[]';
    languageInput.placeholder = 'Idioma';
    
    const proficiencyInput = document.createElement('input');
    proficiencyInput.type = 'text';
    proficiencyInput.name = 'proficiencias[]';
    proficiencyInput.placeholder = 'Proficiência';
    
    qualificationFields.appendChild(languageInput);
    qualificationFields.appendChild(proficiencyInput);
    qualificacoesContainer.appendChild(qualificationFields);
}
