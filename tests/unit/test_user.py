from werkzeug.security import check_password_hash


def test_new_user(new_user):
    assert new_user.email == "john.doe@example.com"
    assert new_user.username == "John Doe"
    assert (check_password_hash(new_user.pw_hash, "Password1234567890!") ==
            new_user.check_password("Password1234567890!"))
