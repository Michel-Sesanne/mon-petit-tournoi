from tournoiapp import create_app, db
from tournoiapp.models import User

app = create_app()

with app.app_context():
    # Vérifie que la table existe
    inspector = db.inspect(db.engine)
    if 'users' in inspector.get_table_names():
        print("Table 'users' existe !")
    else:
        print("Table 'users' n'existe pas...")

    # Affiche tous les utilisateurs
    users = User.query.all()
    if users:
        print("Utilisateurs présents :")
        for u in users:
            print(f"- {u.id}: {u.pseudo}")
    else:
        print("Aucun utilisateur dans la table.")
