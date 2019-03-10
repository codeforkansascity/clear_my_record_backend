from clear_my_record_backend.server import cmr


@cmr.route('/')
@cmr.route('/index')
def index():
    return "Hello, World!"

@cmr.route('/qualifying_question', methods=['GET'])
def qualifying_question():
    pass

@cmr.route('/qualifying_questions', methods=['GET'])
def qualifying_questions():
    pass

@cmr.route('/qualifying_answer', methods=['POST'])
def qualifying_answer():
    pass
