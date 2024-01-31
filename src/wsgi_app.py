from gevent import monkey

monkey.patch_all()

from app import app


@app.route('/api/hello-world')
def hello_world():
    return 'Hello World!'
