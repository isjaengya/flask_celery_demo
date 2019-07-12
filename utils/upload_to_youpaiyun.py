import upyun
from flask import current_app as app


def upload_to_cdn(path, file_path):
    try:
        if '.' not in path:
            str = path[-3:]
            path = path[:-3]+'.'+str
        up = upyun.UpYun(app.config['CDN_BUCKET'], username=app.config['CDN_USER_NAME'],
                         password=app.config['CDN_PASSWORD'], chunksize=131072)
        with open(file_path, 'rb') as f:
            up.put(path, f)
        return app.config['CDN_HOST'] + path
    except Exception as e:
        print(e)
        return None
