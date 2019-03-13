from clear_my_record_backend.server import cmr, dbs
from clear_my_record_backend.server.models import Users


@cmr.shell_context_processor
def make_shell_ctx():
    return {'dbs': dbs, 'User': Users}
