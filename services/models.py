from sqlalchemy import  Column, Integer, String, Boolean, DateTime, Time, ForeignKey
from flask_login import UserMixin
from services.sqlalchemy import db

class CEP(db.Model):
    __tablename__ = 'CEP'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Valor = Column(String(length=8), nullable=False, unique=True)
    UF = Column(String(length=2), nullable=False)
    Cidade = Column(String(length=50), nullable=False)
    Bairro = Column(String(length=50), nullable=False)
    Lougradouro = Column(String(length=50))
    Complemento = Column(String(length=50))
    # Relationships
    usuarios = db.relationship('Usuario', backref='cep', lazy=True)

class Idioma(db.Model):
    __tablename__ = 'Idioma'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Valor = Column(String(length=50), nullable=False, unique=True)
    # Relationships
    proficiencias = db.relationship('Proficiencia', backref='idioma', lazy=True)

class Nivel(db.Model):
    __tablename__ = 'Nivel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Valor = Column(String(length=50), nullable=False, unique=True)
    # Relationships
    proficiencias = db.relationship('Proficiencia', backref='nivel', lazy=True)

class Proficiencia(db.Model):
    __tablename__ = 'Proficiencia'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idIdioma = Column(Integer, ForeignKey(Idioma.id), nullable=False)
    idNivel = Column(Integer, ForeignKey(Nivel.id), nullable=False)
    # Relationships
    qualificacoes = db.relationship('Qualificacao', backref='proficiencia', lazy=True)
    turmas = db.relationship('Turma', backref='proficiencia', lazy=True)

class Rede(db.Model):
    __tablename__ = 'Rede'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Valor = Column(String(length=50), nullable=False, unique=True)
    # Relationships
    unidades = db.relationship('Unidade', backref='rede', lazy=True)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idCEP = Column(Integer, ForeignKey(CEP.id), nullable=False)
    Nome = Column(String(length=50), nullable=False)
    CNPJ = Column(String(length=14), nullable=False, unique=True)
    Tipo = Column(String(length=1), nullable=False)
    NumeroEndereco = Column(String(length=7), nullable=False)
    Senha = Column(String(length=32), nullable=False)
    # Relationships
    emails = db.relationship('Email', backref='usuario', lazy=True)
    telefones = db.relationship('Telefone', backref='usuario', lazy=True)
    professor = db.relationship('Professor', backref='usuario', uselist=False, lazy=True)
    unidades = db.relationship('Unidade', backref='usuario', lazy=True)
    # Explicitly implement UserMixin methods
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

class Email(db.Model):
    __tablename__ = 'Email'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer, ForeignKey(Usuario.id), nullable=False)
    Valor = Column(String(length=50), nullable=False)

class Telefone(db.Model):
    __tablename__ = 'Telefone'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer, ForeignKey(Usuario.id), nullable=False)
    DDD = Column(String(length=2), nullable=False)
    Numero = Column(String(length=9), nullable=False)

class Professor(db.Model):
    __tablename__ = 'Professor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer, ForeignKey(Usuario.id), nullable=False)
    CPF = Column(String(length=11), nullable=False, unique=True)
    # Relationships
    qualificacoes = db.relationship('Qualificacao', backref='professor', lazy=True)
    disponibilidades = db.relationship('Disponibilidade', backref='professor', lazy=True)

class Unidade(db.Model):
    __tablename__ = 'Unidade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idRede = Column(Integer, ForeignKey(Rede.id), nullable=False)
    idUsuario = Column(Integer, ForeignKey(Usuario.id), nullable=False)
    # Relationships
    turmas = db.relationship('Turma', backref='unidade', lazy=True)

class Qualificacao(db.Model):
    __tablename__ = 'Qualificacao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idProfessor = Column(Integer, ForeignKey(Professor.id), nullable=False)
    idProficiencia = Column(Integer, ForeignKey(Proficiencia.id), nullable=False)

class Turma(db.Model):
    __tablename__ = 'Turma'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idProficiencia = Column(Integer, ForeignKey(Proficiencia.id), nullable=False)
    idUnidade = Column(Integer, ForeignKey(Unidade.id), nullable=False)
    Nome = Column(String(length=50), nullable=False)
    QuantidadeAlunos = Column(Integer, nullable=False)
    # Relationships
    agendamentos = db.relationship('Agendamento', backref='turma', lazy=True)

class Agendamento(db.Model):
    __tablename__ = 'Agendamento'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idTurma = Column(Integer, ForeignKey(Turma.id))
    Cancelado = Column(Boolean, nullable=False, default=False)
    # Relationships
    disponibilidades = db.relationship('Disponibilidade', backref='agendamento', lazy=True)

class Disponibilidade(db.Model):
    __tablename__ = 'Disponibilidade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    idAgendamento = Column(Integer, ForeignKey(Agendamento.id), nullable=False)
    idProfessor = Column(Integer, ForeignKey(Professor.id), nullable=False)
    Inicio = Column(DateTime, nullable=False)
    Duracao = Column(Time, nullable=False)