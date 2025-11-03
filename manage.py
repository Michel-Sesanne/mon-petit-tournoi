from tournoiapp import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    from tournoiapp.models import User, JoueurDB
    return {'db': db, 'User': User, 'JoueurDB': JoueurDB}

if __name__ == "__main__":
    with app.app_context():
        inspector = db.inspect(db.engine)
        print("Tables existantes :", inspector.get_table_names())
        if 'joueurs' in inspector.get_table_names():
            print("La table 'joueurs' existe !")
        else:
            print("La table 'joueurs' n'existe pas.")