from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from services.models import *
from services.util import *
from services.login_manager import login_manager


# Blueprints
auth = Blueprint('auth', __name__)
config = Blueprint('config', __name__)
main = Blueprint('main', __name__)

login_manager.login_view = "auth.login"

# Load user from database
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cnpj = request.form.get('cnpj')
        cnpj_only_num = remove_format(cnpj)   
        password = request.form.get('password')
        hashed_password = hash_password(password)
        user = Usuario.query.filter_by(CNPJ=cnpj_only_num).first()
    
        if user == None:
            flash('CNPJ não registrado', 'error')
        elif user.Senha != hashed_password:
            flash('Senha incorreta', 'error')
        else:
            login_user(user)
            print(user.is_authenticated, user.is_active, user.get_id)
            return redirect(url_for('main.menu'))

    return render_template('Login.html')


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        print('oi')
    return render_template('EsquecimentoDeSenha.html')


@auth.route('/change_password')
def change_password():
    return render_template('RecSenhaLogin.html')


@auth.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json()
        tipo = data.get('accountType')
        print(tipo)
        if tipo == 'professor':
            return redirect(url_for('auth.create_user.professor'))
        if tipo == 'representante':
            return redirect(url_for('auth.create_user.unidade'))
    return render_template('CriarConta.html')


@auth.route('/create_professor', methods=['POST'])
def create_professor():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    cpf_only_num = remove_format(cpf)
    cnpj = request.form.get('cnpj')
    cnpj_only_num = remove_format(cnpj)
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('pass2')
    cep = request.form.get('cep')
    numero = request.form.get('numero')
    email = request.form.get("email")
    ddd = request.form.get('ddd')
    telefone = request.form.get('telefone')
    idiomas = request.form.getlist('idiomas[]')
    proficiencias = request.form.getlist('proficiencias[]')

    if checkCPF(cpf_only_num) != True: flash(checkCPF(cpf_only_num), 'errorCPF')
    if checkCNPJ(cnpj_only_num) != True: flash(checkCNPJ(cnpj_only_num), 'errorCNPJ')
    if pass1 != pass2: flash("As senhas não coincidem", 'errorSenha')
    if checkCEP(cep) != True: flash(checkCEP(cep), 'errorCEP')
    if checkEmail(email) != True: flash("Email já está registrado", 'errorEmail')
    if checkTelefone(ddd, telefone) != True: flash("Telefone já está registrado", 'errorTelefone')
    if checkCPF(cpf_only_num) == True and checkCNPJ(cnpj_only_num) == True and pass1 == pass2 and checkCEP(cep) == True and checkEmail(email) == True and checkTelefone(ddd, telefone) == True:
        usuario = addProfessor(cep, nome, cnpj_only_num, numero, pass1, cpf_only_num, email, ddd, telefone, idiomas, proficiencias)
        login_user(usuario)
        return redirect(url_for('main.menu'))
    return render_template('CriarConta.html')


@auth.route('/create_unidade', methods=['POST'])
def create_unidade():
    nome = request.form.get('nome2')
    rede = request.form.get('rede')
    cnpj = request.form.get('cnpj2')
    cnpj_only_num = remove_format(cnpj)
    pass1 = request.form.get('pass3')
    pass2 = request.form.get('pass4')
    cep = request.form.get('cep2')
    numero = request.form.get('numero2')
    email = request.form.get('email2')
    ddd = request.form.get('ddd2')
    telefone = request.form.get('telefone2')

    if checkCNPJ(cnpj_only_num) != True: flash(checkCNPJ(cnpj_only_num), 'errorCNPJ')
    if pass1 != pass2: flash("As senhas não coincidem", 'errorSenha')
    if checkCEP(cep) != True: flash(checkCEP(cep), 'errorCEP')
    if checkEmail(email) != True: flash("Email já está registrado", 'errorEmail')
    if checkTelefone(ddd, telefone) != True: flash("Telefone já está registrado", 'errorTelefone')
    if checkCNPJ(cnpj_only_num) == True and pass1 == pass2 and checkCEP(cep) == True and checkEmail(email) == True and checkTelefone(ddd, telefone) == True:
        usuario = addUnidade(cep, nome, cnpj_only_num, numero, pass1, rede, email, ddd, telefone)
        login_user(usuario)
        return redirect(url_for('main.menu'))
    return render_template('CriarConta.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@config.route('/conta', methods=['GET'])
@login_required
def consultar_conta():
    user = Usuario.query.filter_by(id=current_user.id).first()
    cep = CEP.query.filter_by(id=user.idCEP).first()
    if user.Tipo == 'p':
        professor = Professor.query.filter_by(idUsuario=current_user.id).first()
        return render_template('ConsultarContaProfessor.html', user=user, professor=professor, cep=cep)
    if user.Tipo == 'u':
        unidade = Unidade.query.filter_by(idUsuario=current_user.id).first()
        return render_template('ConsultarContaUnidade.html', user=user, unidade=unidade, cep=cep)


@config.route('/editar_conta')
@login_required
def editar_conta():
    return render_template('editar_conta.html')


@config.route('/excluir_conta')
@login_required
def excluir_conta():
    return redirect(url_for('auth.login'))


@config.route('/disponibilidades')
@login_required
def disponibilidades():
    user = Usuario.query.filter_by(id=current_user.id).first()
    if user.Tipo == 'p':
        print()
    else:
        return 401


@config.route('/turmas')
@login_required
def turmas():
    user = Usuario.query.filter_by(id=current_user.id).first()
    if user.Tipo == 'u':
        print()
    else:
        return 401


@main.route("/")
def rootRedirect():
    if current_user.is_authenticated:
        return redirect(url_for('main.menu'))
    return redirect(url_for('auth.login'))


@main.route('/menu')
@login_required
def menu():
    return render_template('MenuAgendamentos.html')

@main.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    if request.method == 'POST':
        professor = request.form.get('professor')
        consulta = Usuario.query.filter_by(CNPJ=professor).first()
        if consulta == None:
            consulta = Professor.query.filter_by(CPF=professor).first()
            if consulta == None: flash('Professor não registrado', 'errorProf')
            #addAgendamento()
        #addAgendamento()
    
    return render_template('Agendar1.html', )