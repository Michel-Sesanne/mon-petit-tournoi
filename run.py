from tournoiapp import create_app, db

app = create_app()

if __name__ == "__main__":
    # Création de la base de données si elle n'existe pas
    with app.app_context():
        db.create_all()
    # Lancement du serveur en mode debug
    app.run(debug=True)
