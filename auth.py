from flask import Blueprint, render_template, redirect, url_for, request,flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import Usuario,db
from py2neo import NodeMatcher
#carrega flask e Agenda
auth = Blueprint('auth',__name__,url_prefix="/auth")
#rotas da aplicação
@auth.route('/login')
def login():
    return render_template('login.html') 
@auth.route('/login', methods=['POST','GET'])
def login_post():
    email = request.form.get('email')
    senha = request.form.get('senha')
    remember = True if request.form.get('remember') else False
    #user=Usuario.query.filter_by(login=login).first()
    user = Usuario(nome=None,email=email,senha=generate_password_hash(senha, method='sha256'),empresa=None)
    matcher=NodeMatcher(db.graph)
    m=matcher.match('usuario',email=user.email).first()
    if not m or not check_password_hash(m['senha'],senha):
        flash('Verifique seu login e tente de novo')
        return redirect(url_for('auth.login'))
    user.nome=m['nome']
    user.empresa=m['empresa']
    user.id=user.getId()
    print(type(user))
    login_user(user,remember=remember)
    #db.session['email']=email
    return redirect(url_for('main.profile'))
@auth.route('/signup')
def signup():
    return render_template('signup.html')
@auth.route('/signup',methods=['POST'])
def signup_post():
    nome=request.form.get('nome')
    email= request.form.get('email').lower()
    senha= request.form.get('senha').strip()
    empresa=request.form.get('empresa').strip()
    confirmacao=request.form.get('confirmacao').strip()
    #user = Usuario.query.filter_by(login=login).first()
    matcher = NodeMatcher(db.graph)
    #user = Usuario(nome=None,email=email,empresa=None,senha=None)
    user=matcher.match('usuario',email=email).first()
    print(user)
    if user:
        flash('Já existe esse email. Tente logar!')
        return redirect(url_for('auth.signup'))
    elif senha!=confirmacao:
        flash('Senha e confirmação são diferentes!')
        return render_template('signup.html')
    elif not login or not nome or not senha or not empresa or not confirmacao:
        flash('Preencha todos os campos!')
        return render_template('signup.html')
    novo_usuario = Usuario(email=email, nome=nome, senha=generate_password_hash(senha, method='sha256'),empresa=empresa)
    db.graph.push(novo_usuario)
    return redirect(url_for('auth.login'))
@auth.route('/logout')
def logout():
    logout_user()
    flash("Deslogou de profile")
    return redirect(url_for('main.home'))
