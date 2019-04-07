from clear_my_record_backend.server import dbs


def save_to_dbs(entity):
    dbs.session.add(entity)
    dbs.session.commit()
