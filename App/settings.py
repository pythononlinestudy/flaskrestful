def get_db_uri(dbinfo):
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")
    db = dbinfo.get("DB")
    driver = dbinfo.get("DRIVER")

    return "{}+{}://{}:{}@{}:{}/{}".format(db, driver, user, password, host, port, name)


class Config():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "110"


class DevelopConfig(Config):
    DEBUG = True
    DATABASE = {
        "USER": "root",
        "PASSWORD": "rock1204",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskDay55",
        "DB": "mysql",
        "DRIVER": "pymysql"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


envs = {
    "develop": DevelopConfig,
}

