from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from tournoiapp import db
bp = Blueprint('main', __name__)

# ----------------------------
# PAGE D’ACCUEIL
# ----------------------------
@bp.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('home.html')


# ----------------------------
# INSCRIPTION
# ----------------------------
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']

        # Vérifie si le pseudo existe déjà
        existing_user = User.query.filter_by(pseudo=pseudo).first()
        if existing_user:
            flash('Ce pseudo est déjà pris.', 'warning')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(pseudo=pseudo, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Inscription réussie, vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


# ----------------------------
# CONNEXION
# ----------------------------
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']

        user = User.query.filter_by(pseudo=pseudo).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['pseudo'] = user.pseudo
            flash(f'Bienvenue {user.pseudo} !', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Identifiants incorrects.', 'danger')
            return redirect(url_for('main.login'))

    return render_template('login.html')


# ----------------------------
# DASHBOARD UTILISATEUR
# ----------------------------
@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
        return redirect(url_for('main.login'))
    return render_template('dashboard.html', pseudo=session['pseudo'])


# ----------------------------
# DÉCONNEXION
# ----------------------------
@bp.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('main.home'))

