"""
Inicialización de la aplicación Flask para el Sistema de Detección de Placas

Este módulo contiene la función factory para crear la aplicación Flask.
Aquí se configura la aplicación, se registran las rutas y se definen
parámetros iniciales.

La estructura modular permite una mejor organización y mantenimiento del código.
"""

from flask import Flask

def create_app():
    """
    Factory function que crea y configura la aplicación Flask.
    
    Esta función permite la creación modular de la aplicación Flask, lo que
    facilita las pruebas y el mantenimiento. Registra los blueprints
    necesarios para el funcionamiento de las rutas.
    
    Returns:
        Flask: La aplicación Flask configurada y lista para usar
    """
    app = Flask(__name__)
    
    # Registrar las rutas a través del blueprint principal
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app 