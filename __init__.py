# __init__.py

import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    # Configuração da aplicação
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Carrega a configuração do arquivo config.py, se existir
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Carrega a configuração de teste se fornecida
        app.config.from_mapping(test_config)

    # Garante que a pasta de instância exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Registro do blueprint
    from . import json_handler  # Renomeado de json.py
    app.register_blueprint(json_handler.bp)

    return app
