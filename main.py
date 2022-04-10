from flask import Flask,render_template,Blueprint
from flask_login import login_required,current_user
from app import create_app,db
main= Blueprint("main",__name__,url_prefix="/main")
@main.route('/home')
def home():
    return render_template('base.html')
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',nome=current_user.nome)
if __name__=="__main__":
    ap=create_app()
    ap.run(debug =True,host='0.0.0.0')