from server.models import User


def test_add_user(_dbs, new_user):
    _dbs.session.add(new_user)
    _dbs.session.commit()
    u = _dbs.session.query(User).filter_by(username=new_user.username).first()
    assert u.username == "John Doe"
