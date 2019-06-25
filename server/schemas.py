from server import ma
from server.models import *
from marshmallow import ValidationError

class ChargeSchema(ma.ModelSchema):
    conviction = ma.Nested('ConvictionSchema', exclude=('charges', 'client', ))

    class Meta:
        model = Charge
        fields = (
            'id',
            'conviction_id',
            'charge',
            'citation',
            'sentence',
            'eligible',
            'conviction_charge_type',
            'conviction_class_type',
            'eligible',
            'please_expunge',
            'notes',
            'conviction_description',
            'to_print',
            'convicted',
        )

class ConvictionSchema(ma.ModelSchema):
    # need to figure out good way to exclude convictions.charges.convictions.users, etc etc
    charges = ma.Nested(ChargeSchema, many=True, exclude=('convictions', ))
    client = ma.Nested('ClientSchema', exclude=('convictions', ))

    class Meta:
        model = Conviction
        fields = (
            'id',
            'client_id',
            'case_number',
            'agency',
            'court_name',
            'court_city_county',
            'judge',
            'record_name',
            'release_status',
            'release_date',
            'notes',
            'name',
            'arrest_date',
            'charges',
            'approximate_date_of_charge',
        )

def non_empty_field(data):
    if not data:
        raise ValidationError('Data not provided.')

class ClientSchema(ma.ModelSchema):
    convictions = ma.Nested(ConvictionSchema, many=True, exclude=('client', ))
    # exclude clients to avoid recursion issues lmao
    user = ma.Nested('UserSchema', exclude=('clients', ))
    full_name = ma.Str(validate=non_empty_field)

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
            'full_license_issuing_state',
            'license_expiration_date',
            'status',
            'active',
            'user_id',
            'notes',
            'filing_court',
            'judicial_circuit_number',
            'county_of_prosecutor',
            'judge_name',
            'division_name',
            'division_name',
            'petitioner_name',
            'division_number',
            'city_name_here',
            'county_name',
            'arresting_county',
            'arresting_municipality',
            'other_agencies_name',
            'cms_case_number',
            'previous_expungements'
        )

class UserSchema(ma.ModelSchema):
    clients = ma.Nested(ClientSchema, many=True, only=('id', 'full_name'))

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
