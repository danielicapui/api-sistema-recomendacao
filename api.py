from flask import Blueprint, render_template, redirect, url_for, request,flash,send_file
from flask_login import login_required,current_user
from app import Usuario,db
from sistema_recomendacao import Recomendar, calcular_recomendacao
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
        arquivo=request.files['arquivo']
        #arquivo=open(arquivo,r)
        feature=request.form.get('feature')
        target=request.form.get('target')
        target_count=request.form.get('target_count')
        r=calcular_recomendacao(arquivo,feature,target,target_count)
        #response=pd.read_json(r,typ='series',orient='ranking')
        #res=r.to_json()
        nome_arquivo="resultado_"+str(current_user.id)+".csv"
        local='static/csv/'+nome_arquivo
        r.to_csv(local,encoding='utf-8',sep=';')
        return redirect(url_for('static', filename='csv/'+nome_arquivo))
    return render_template('index.html')
@api.route('/minhas',methods=['GET','POST'])
@login_required
def minhas():
    if request.method=='POST':
        nome=request.form.get('nome')
        return render_template('recomendacao.html')
    return render_template('minhas.html')
