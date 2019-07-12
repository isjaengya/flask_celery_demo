import os
import imp


def load_config():
    mode = os.environ.get('DATA')
    try:
        if mode == 'PRODUCTION':
            Production = imp.load_source('Production', '/apps/config/bp_thetestcom_conf.py')
            return Production.ProductionConfig
        elif mode == 'TESTING':
            from api.config.testing import TestConfig
            return TestConfig
        else:
            from api.config.development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError as e:
        print(e)
        from api.config.default import DefaultConfig
        return DefaultConfig
