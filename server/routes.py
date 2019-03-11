from flask import request, Response
from clear_my_record_backend.server import cmr, models, dbs
from datetime import datetime

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
    if not request.json:
        abort(400)

    qualifying_answer = {
        "user_session": request.json['user_session'],
        "question_id": request.json['question_id'],
        "answer": request.json['answer'],
        "qualifying_answer": request.json['qualifying_answer'],
        "question_version_number": request.json['question_version_number'],
        "timestamp": datetime.fromtimestamp(request.json['timestamp'])
    }

    answer = models.Qualifying_Answers(qualifying_answer)
    dbs.session.add(answer)
    dbs.session.commit()

    return Response('Success', status=200, mimetype='text/plain')
