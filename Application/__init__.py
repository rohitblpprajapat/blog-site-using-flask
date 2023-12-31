import os
from flask import Flask

def create_app(test_config=None):
    # creating and configuring app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'Application.sqlite'),
    )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    #database thing.......
    from . import db
    db.init_app(app)
    
    
    #blueprints thing for auth
    from . import auth
    app.register_blueprint(auth.bp)
    
    #Bluprints for blogs
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint= 'index')
    

    return app
