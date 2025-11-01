# manage.py
from tournoiapp import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    from tournoiapp.models import User, JoueurDB
    return {'db': db, 'User': User, 'JoueurDB': JoueurDB}
