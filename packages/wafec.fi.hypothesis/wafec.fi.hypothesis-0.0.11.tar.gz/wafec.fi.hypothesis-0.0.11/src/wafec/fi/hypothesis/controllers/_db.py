from . import app
from wafec.fi.hypothesis.models import db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
