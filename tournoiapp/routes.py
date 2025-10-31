from flask import Blueprint, render_template, request, redirect, url_for, flash, session

main_routes = Blueprint('main_routes', __name__)

# Page d'accueil
@main_routes.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)


# Page de connexion
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Auth très simple (juste pour tester)
        if email == 'admin@example.com' and password == '1234':
            session['user'] = {'email': email}
            flash('Connexion réussie ! Bienvenue Michel 👋', 'success')
            return redirect(url_for('main_routes.index'))
        else:
            flash('Identifiants incorrects. Réessaie.', 'danger')
            return redirect(url_for('main_routes.login'))

    return render_template('login.html')


# Déconnexion
@main_routes.route('/logout')
def logout():
    session.pop('user', None)
    flash('Déconnexion réussie 👋', 'info')
    return redirect(url_for('main_routes.index'))
