from cmr_backend.server import cmr


@cmr.route('/')
@cmr.route('/index')
def index():
    return "Hello, World!"
