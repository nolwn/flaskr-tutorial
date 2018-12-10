import os # used for operating system operations (filepath, etc)

from flask import Flask # importing Flask itself

from . import db # import our own db module

# Application factory function. Sets up the app somehow. test_config=None is a
# default parameter, NOT a kwarg related thing. In a testing environment, a
# configuration file will get passed in here.
def create_app(test_config=None):

    # "creates an instance of flask. __name__ is the name of the current Python
    # module. The app needs to know where it's located to set up some paths, and
    # __name__ is a convinient way to tell it that." – Flask documentation
    app = Flask(__name__, instance_relative_config=True)

    # Makes file paths relative to instance. The instance is "/flaskr_tutorial."
    app.config.from_mapping(

        # This is a secret key used for signing. Get a better one in production
        SECRET_KEY='thisisasecretkeyusedforsigning.Getabetteroneinproduction',

        # This takes us to our sqlite file. Obviously a more serious database
        # is going to need a different kind of configuration...
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # i.e., if we are not in a testing environment, and have not recieved a
    # testing config.
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True) # load our config.py
    else: # i.e., we did recieve a testing config.
        app.config.from_mapping(test_config) # load that!

    # create app isntance path... I don't understand this yet.
    # "ensure the instance folder exists" – Flask documentation
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Do nothing?

    # A function and a function decorator. Tells flask to load the hello
    # into a route "/hello". When that route is triggered, app.route will run
    # with a callback, `hello`.
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.init_app(app) #

    return app # We returned a configured instance of flask!
