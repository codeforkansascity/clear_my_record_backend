from clear_my_record_backend.server import ma
from clear_my_record_backend.server.models import *

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ('username', 'email', 'user_type', 'clients')
