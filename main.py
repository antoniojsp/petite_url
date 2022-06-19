from PetiteURL import create_app
from PetiteURL.ajax import ruta as ajax
from PetiteURL.routes import ruta as routes

app = create_app()
app.register_blueprint(ajax)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)


