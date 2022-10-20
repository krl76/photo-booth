def main():
    db_session.global_init('db/photo-booth.sqlite')
    app.run()
