from flask import Flask

app = Flask(__name__)

def register_bp():
    from .Matrix import matrix_bp
    from .PI import pi_bp

    app.register_blueprint(matrix_bp)
    app.register_blueprint(pi_bp)
    #app.register_blueprint(dcx_bp)

def get_app():
    register_bp()
    return app