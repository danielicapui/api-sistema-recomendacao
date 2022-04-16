from flask import Flask, redirect,render_template,Blueprint,url_for
from flask_login import login_required,current_user,user_logged_in
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
    @ap.route('/')
    def index():
        return redirect(url_for("auth.login"))
    ap.run(debug=False,host='0.0.0.0')
