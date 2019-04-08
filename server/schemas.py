from clear_my_record_backend.server import ma
from clear_my_record_backend.server.models import *


class ChargeSchema(ma.ModelSchema):
    conviction = ma.Nested('ConvictionSchema', exclude=('charges', ))

    class Meta:
        model = Charge
        fields = (
            'id',
            'conviction_id',
            'charge',
            'citation',
            'sentence',
            'class_type',
            'charge_type',
            'eligible'
        )

class ConvictionSchema(ma.ModelSchema):
    charges = ma.Nested(ChargeSchema, many=True)
    client = ma.Nested('ClientSchema', exclude=('convictions', ))

    class Meta:
        model = Conviction
        fields = (
            'id',
            'client_id',
            'client',
            'case_number',
            'agency',
            'court_name',
            'court_city_county',
            'judge',
            'record_name',
            'release_status',
            'release_date',
            'charges',
        )

class ClientSchema(ma.Schema):
    convictions = ma.Nested(ConvictionSchema, many=True, exclude=('client', ))
    # exclude clients to avoid recursion issues lmao
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
            'user',
            'user_id',
            'convictions',
        )

class UserSchema(ma.ModelSchema):
    clients = ma.Nested(ClientSchema, many=True, exclude=('user', 'user_id', ))

    class Meta:
        model = User
        fields = ('id', 'username', 'clients')

# schema instantiation for routes.py
user_schema = UserSchema()
users_schema = UserSchema(many=True)
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
conviction_schema = ConvictionSchema()
convictions_schema = ConvictionSchema(many=True)
charge_schema = ChargeSchema()
charges_schema = ChargeSchema(many=True)
