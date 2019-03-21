from clear_my_record_backend.server import cmr, dbs
from clear_my_record_backend.server.models import User, Qualifying_Answer, Client, Conviction, Charge


@cmr.shell_context_processor
def make_shell_ctx():
    return {'dbs': dbs, 'User': User, 'Qualifying_Answer': Qualifying_Answer, 'Client': Client, 'Conviction': Conviction, 'Charge': Charge}
