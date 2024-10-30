import hashlib
from services.consulta_cep import consulta_cep
from services.routes import *
from services.models import *

def hash_password(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    return md5_hash.hexdigest()

def remove_format(input):
    input = input.replace('.', '')
    input = input.replace('/', '')
    input = input.replace('-', '')
    return input

def validar_cnpj(cnpj):
    # Remove any non-digit characters
    cnpj = ''.join(filter(str.isdigit, cnpj))
    # Check if CNPJ has 14 digits
    if len(cnpj) != 14:
        return False
    # Check if all digits are the same
    if len(set(cnpj)) == 1:
        return False
    # Convert string to list of integers
    cnpj_elements = [int(char) for char in cnpj]
    # Weights for the first digit validation
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    # Weights for the second digit validation
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    # Calculate first verification digit
    sum1 = sum(w * n for w, n in zip(weights1, cnpj_elements[:12]))
    d1 = 11 - (sum1 % 11)
    if d1 >= 10:
        d1 = 0
    # Verify first digit
    if d1 != cnpj_elements[12]:
        return False
    # Calculate second verification digit
    sum2 = sum(w * n for w, n in zip(weights2, cnpj_elements[:13]))
    d2 = 11 - (sum2 % 11)
    if d2 >= 10:
        d2 = 0
    # Verify second digit
    if d2 != cnpj_elements[13]:
        return False
    return True

def validar_cpf(cpf):
    # Remove any non-numeric characters from CPF
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    # Check if CPF has 11 digits
    if len(cpf) != 11:
        return False
    # Check if all digits are the same
    if len(set(cpf)) == 1:
        return False
    # Calculate first digit
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    if int(cpf[9]) != digito1:
        return False
    # Calculate second digit
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    if int(cpf[10]) != digito2:
        return False
    return True

def addCEP(cep):
    consulta = consulta_cep(cep)
    cep = remove_format(cep)
    newCEP = CEP(Valor=cep, UF=consulta.get('uf'), Cidade=consulta.get('cidade'), Bairro=consulta.get('bairro'), Lougradouro=consulta.get('lougradouro'), Complemento=consulta.get('complemento'))
    db.session.add(newCEP)
    db.session.commit()

def addRede(valor):
    newRede = Rede(Valor = valor)
    db.session.add(newRede)
    db.session.commit()

def addUsuario(cep, nome, cnpj, tipo, numeroendereco, senha):
    newUsuario = Usuario(idCEP = cep, Nome = nome, CNPJ = cnpj, Tipo = tipo, NumeroEndereco = numeroendereco, Senha = senha)
    db.session.add(newUsuario)
    db.session.flush()
    user = Usuario.query.filter_by(CNPJ=cnpj).first()
    return user

def checkCNPJ(cnpj):
    if not validar_cnpj(cnpj): return "CNPJ inválido"
    cnpj_db = Usuario.query.filter_by(CNPJ=cnpj).first()
    if cnpj_db: return "CNPJ já registrado"
    return True

def checkCPF(cpf):
    if not validar_cpf(cpf): return "CPF inválido"
    cpf_db = Professor.query.filter_by(CPF=cpf).first()
    if cpf_db: return "CPF já registrado"
    return True

def checkCEP(cep):
    if consulta_cep(cep) == "CEP inválido" or consulta_cep(cep) == None: return "CEP inválido"
    return True

def checkEmail(email):
    email_db = Email.query.filter_by(Valor=email).first()
    if email_db: return False
    return True

def checkTelefone(ddd, numero):
    telefone_db = Telefone.query.filter_by(DDD=ddd, Numero=numero).first()
    if telefone_db: return False
    return True

def addEmail(valor, user_id):
    newEmail = Email(Valor=valor, idUsuario=user_id)
    db.session.add(newEmail)
    db.session.flush()

def addTelefone(ddd, numero, user_id):
    newTelefone = Telefone(DDD=ddd, Numero=numero, idUsuario=user_id)
    db.session.add(newTelefone)
    db.session.flush()

def addIdioma(idioma):
    idioma_db = Idioma.query.filter_by(Valor=idioma).first()
    if idioma_db != None:
        return idioma_db.id
    newIdioma = Idioma(Valor=idioma)
    db.session.add(newIdioma)
    db.session.flush()
    idioma_db = Idioma.query.filter_by(Valor=idioma).first()
    return idioma_db.id

def addNivel(nivel):
    nivel_db = Nivel.query.filter_by(Valor=nivel).first()
    if nivel_db != None:
        return nivel_db.id
    newNivel = Nivel(Valor=nivel)
    db.session.add(newNivel)
    db.session.flush()
    nivel_db = Nivel.query.filter_by(Valor=nivel).first()
    return nivel_db.id

def addProficiencia(idioma, nivel):
    idioma = addIdioma(idioma)
    nivel = addNivel(nivel)
    proficiencia_db = Proficiencia.query.filter_by(idIdioma=idioma, idNivel=nivel).first()
    if proficiencia_db != None:
        return proficiencia_db.id
    newProficiencia = Proficiencia(idIdioma=idioma, idNivel=nivel)
    db.session.add(newProficiencia)
    db.session.flush()
    proficiencia_db = Proficiencia.query.filter_by(idIdioma=idioma, idNivel=nivel).first()
    return proficiencia_db.id

def addQualificacao(idioma, nivel, professor_id):
    proficiencia = addProficiencia(idioma, nivel)
    qualificacao_db = Qualificacao.query.filter_by(idProfessor=professor_id, idProficiencia=proficiencia)
    if qualificacao_db != None:
        return
    newQualificacao = Qualificacao(idProfessor = professor_id, idProficiencia=proficiencia)
    db.session.add(newQualificacao)
    db.session.flush()

def addProfessor(cep, nome, cnpj, numeroendereco, senha, cpf, email, ddd, telefone, idiomas, proficiencias):
    try:
        cep_db = CEP.query.filter_by(Valor=remove_format(cep)).first()
        if not cep_db:
            addCEP(cep)
            db.session.flush()
            cep_db = CEP.query.filter_by(Valor=remove_format(cep)).first()
        usuario = addUsuario(cep_db.id, nome, cnpj, 'p', numeroendereco, hash_password(senha))

        newProfessor = Professor(idUsuario=usuario.id, CPF=cpf)
        db.session.add(newProfessor)
        db.session.flush()
        professor = Professor.query.filter_by(idUsuario=usuario.id).first()

        addEmail(email, usuario.id)
        addTelefone(ddd, telefone, usuario.id)
        for idioma, proficiencia in zip(idiomas, proficiencias):
            addQualificacao(idioma, proficiencia, professor.id)

        db.session.commit()
        return usuario
    except Exception as e:
        db.session.rollback()
        raise e

def addUnidade(cep, nome, cnpj, numeroendereco, senha, rede, email, ddd, telefone):
    try:
        cep_db = CEP.query.filter_by(Valor=remove_format(cep)).first()
        if not cep_db:
            addCEP(cep)
            db.session.flush()
            cep_db = CEP.query.filter_by(Valor=remove_format(cep)).first()
        rede_db = Rede.query.filter_by(Valor=rede).first()
        if not rede_db:
            addRede(rede)
            db.session.flush()
            rede_db = Rede.query.filter_by(Valor=rede).first()
        usuario = addUsuario(cep_db.id, nome, cnpj, 'u', numeroendereco, hash_password(senha))
        
        newUnidade = Unidade(idUsuario=usuario.id, idRede=rede_db.id)
        db.session.add(newUnidade)
        db.session.flush()

        addEmail(email, usuario.id)
        addTelefone(ddd, telefone, usuario.id)

        db.session.commit()
        return usuario
    except Exception as e:
        db.session.rollback()
        raise e