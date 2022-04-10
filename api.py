from flask import Blueprint, render_template, redirect, url_for, request,flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import Usuario,db
from sistema_recomendacao import Recomendar
import pandas as pd
api = Blueprint('api',__name__,url_prefix="/api")
#rotas da aplicação
@api.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
@api.route('/recomendar',methods=['GET','POST'])
@login_required
def recomendar():
    if request.method=='POST':
        arquivo=request.form.get('arquivo')
        compression=request.form.get('compression')
        feature=request.form.get('feature')
        target=request.form.get('target')
        target_count=request.form.get('target_count')
        r=Recomendar(arquivo,compression,feature,target,target_count)
        #response=pd.read_json(r,typ='series',orient='ranking')
        res=r.to_json()
        return res
    return render_template('recomendar.html')
@api.route('/minhas',methods=['GET','POST'])
@login_required
def minhas():
    if request.method=='POST':
        nome=request.form.get('nome')
        return render_template('recomendacao.html')
    return render_template('minhas.html')
