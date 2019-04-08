from clear_my_record_backend.server import ma
from clear_my_record_backend.server.models import *

class ClientSchema(ma.Schema):
    class Meta:
        model = Client
        fields = (
            'id',
            'full_name',
            'phone',
            'email',
            'sex',
            'race',
            'dob',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'zip_code',
            'license_number',
            'license_issuing_state',
            'license_expiration_date',
            'status',
            'active',
        )

class UserSchema(ma.ModelSchema):
    clients = ma.Nested(ClientSchema, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'clients')


# class ConvictionSchema(ma.ModelSchema):
#     class Meta:
#         model = Conviction
#         fields = ()
