from app import create_app
from app.routes.views import ruta as routes
from app.ajax.views import ruta as ajax
from app.login.views import ruta as login


app = create_app()
app.register_blueprint(routes)
app.register_blueprint(ajax)
app.register_blueprint(login)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)


