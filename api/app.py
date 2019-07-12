import json

from flask import Flask, request, make_response, jsonify

from api.config import load_config
from extensions import migrate, db, celery
from api.resources import BLUEPRINTS

config = load_config()


def create_app(app_name='api', blueprints=BLUEPRINTS):
    app = Flask(app_name)
    config = load_config()
    app.config.from_object(config)
    blueprints_resister(app, blueprints)
    extensions_load(app)

    @app.before_request
    def verify_user():
        if request.path in (
            '/v1/child_photo/like',
        ):
            open_id = request.args.get('openid')
            if not open_id:
                if 'MicroMessenger' in request.user_agent.to_header():
                    # 说明是微信客户端
                    wx_callback = request.args.get('event_path')
                    wx_callback = '{}&openid=1'.format(wx_callback)
                    if wx_callback is not None:
                        wx_callback_api_url = "https://}".format(
                            callback_url=wx_callback)
                        resp = make_response(jsonify({'data': {'code': 999, 'wx_callback': wx_callback_api_url}}))
                        print('wx_callxxxxx: {}'.format(wx_callback_api_url))
                        # resp.headers['location'] = wx_callback_api_url
                        return resp

    return app


def blueprints_resister(app, blueprints):
    for bp in blueprints:
        app.register_blueprint(bp)


def extensions_load(app):
    db.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)
