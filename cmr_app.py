from server import create_app, dbs, ma
from server.models import User, Qualifying_Answer, User, Client, Conviction, Charge, charge_types, class_types, user_types
from server.schemas import UserSchema, ClientSchema

cmr = create_app()


@cmr.shell_context_processor
def make_shell_ctx():
    return {
        'dbs': dbs,
        'User': User,
        'Qualifying_Answer': Qualifying_Answer,
        'User': User,
        'Client': Client,
        'Conviction': Conviction,
        'Charge': Charge,
        'charge_types': charge_types,
        'class_types': class_types,
        'user_types': user_types,
        'UserSchema': UserSchema,
        'ClientSchema': ClientSchema
    }
