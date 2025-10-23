from flask import Flask, render_template, request, redirect, url_for, flash
from requests import session, utils
from flask import session as login_session

def verificar_login():
    if not session:
        flash('Você deve estar logado para visualizar esta página', 'error')
        return redirect(url_for('login'))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form('email')
        password  = request.form('password')
        print(email, password, 'EMAILSENHA')
        usuario = utils.post_login(email, password)
        print(usuario)
        if 'access_token' in usuario:
            session['token'] = usuario['access_token']
            session['username'] = usuario['nome']
            session['papel'] = usuario['papel']

            if session['papel'] == 'admin':
                flash('Seja bem vind admistrador', 'success')
                return redirect(url_for('usuario'))
            elif session['papel'] == 'usuario':
                flash('Seja bem vind usuario', 'success')
                return redirect(url_for('usuario'))
            else:
                flash('Voce nao ter permissao para o acesso', 'error')
                print(flash)
                return redirect(url_for('login'))
        else:
            if usuario['erro'] == '401':
                flash('verefique o email e a senha', 'error')
            else:
                flash('Email ou senha incorretos', 'error')
            return render_template('login.html')
    else:
        return render_template('login.html')


