class Config:
    SECRET_KEY = 'hard to guess string' or os.environ.get('SECRET_KEY') 

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    mailto_list = 'ai131416@126.com'
    mail_host = 'mailsh.tct.tcl.com'
    mail_user = 'ta-cd/li.ai' 
    mail_pass = 'Arno141516'
    mail_postfix='tcl.com'
    DATABASE = 'user'

class TestingConfig(Config):
    TESTING = True
    DATABASE = 'user'

class ProductionConfig(Config):
    DATABASE = 'user'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    
    'default': DevelopmentConfig
}