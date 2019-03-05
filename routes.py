from cmr_backend import cmr


@cmr.route('/')
@cmr.route('/index')
def index():
    return "Hello, World!"
