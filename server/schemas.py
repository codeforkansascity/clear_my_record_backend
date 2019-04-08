from clear_my_record_backend.server import ma
from clear_my_record_backend.server.models import *


class ChargesSchema(ma.ModelSchema):
    class Meta:
        model = Charge
        fields = ()

class ConvictionSchema(ma.ModelSchema):
    charge = ma.Nested(ChargesSchema, many=True)

    class Meta:
        model = Conviction
        fields = ()

class ClientSchema(ma.Schema):
    convictions = ma.Nested(ConvictionSchema, many=True)
    user = ma.Nested('UserSchema', exclude=('clients', ))

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
            'user'
        )

class UserSchema(ma.ModelSchema):
    clients = ma.Nested(ClientSchema, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'clients')
