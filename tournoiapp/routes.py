from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, JoueurDB
from tournoiapp import db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('home.html')

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


@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
        return redirect(url_for('main.login'))
    from tournoiapp.models import JoueurDB
    joueurs = JoueurDB.query.all()
    return render_template('dashboard.html', pseudo=session['pseudo'], joueurs=joueurs)
 
@bp.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('main.home'))

@bp.route('/ajouter_joueur', methods=['POST'])
def ajouter_joueur():
    nom = request.form.get('nom')
    niveau = request.form.get('niveau')

    if not nom or not niveau:
        return jsonify({'error': 'Nom ou niveau manquant'}), 400

    try:
        niveau = int(niveau)
    except ValueError:
        return jsonify({'error': 'Niveau invalide'}), 400

    joueur = JoueurDB(nom=nom, niveau=niveau)
    db.session.add(joueur)
    db.session.commit()

    return jsonify({'nom': joueur.nom, 'niveau': joueur.niveau})

@bp.route('/supprimer_joueur/<int:joueur_id>', methods=['POST'])
def supprimer_joueur(joueur_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Non autorisé'}), 401

    joueur = JoueurDB.query.get(joueur_id)
    if not joueur:
        return jsonify({'error': 'Joueur non trouvé'}), 404

    db.session.delete(joueur)
    db.session.commit()
    return jsonify({'success': True}), 200

@bp.route('/modifier_joueur/<int:joueur_id>', methods=['POST'])
def modifier_joueur(joueur_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Non autorisé'}), 401

    joueur = JoueurDB.query.get(joueur_id)
    if not joueur:
        return jsonify({'error': 'Joueur non trouvé'}), 404

    data = request.form
    nom = data.get('nom')
    niveau = data.get('niveau')

    if nom:
        joueur.nom = nom
    if niveau:
        try:
            joueur.niveau = int(niveau)
        except ValueError:
            return jsonify({'error': 'Niveau invalide'}), 400

    db.session.commit()
    return jsonify({
        'id': joueur.id,
        'nom': joueur.nom,
        'niveau': joueur.niveau
    }), 200

