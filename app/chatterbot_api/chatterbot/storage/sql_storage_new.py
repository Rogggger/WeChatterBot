from app.chatterbot_api.chatterbot.storage import StorageAdapter


class SQLStorageAdapterNew(StorageAdapter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        self.database_uri = kwargs.get('database_uri', False)

        # None results in a sqlite in-memory database as the default
        if self.database_uri is None:
            self.database_uri = 'sqlite://'

        # Create a file database if the database is not a connection string
        if not self.database_uri:
            self.database_uri = 'sqlite:///db.sqlite3'

        self.engine = create_engine(self.database_uri, convert_unicode=True)

        if self.database_uri.startswith('sqlite://'):
            from sqlalchemy.engine import Engine
            from sqlalchemy import event

            @event.listens_for(Engine, 'connect')
            def set_sqlite_pragma(dbapi_connection, connection_record):
                dbapi_connection.execute('PRAGMA journal_mode=WAL')
                dbapi_connection.execute('PRAGMA synchronous=NORMAL')

        if not self.engine.dialect.has_table(self.engine, 'Statement'):
            self.create_database()

        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

    def get_statement_model(self):
        """
        Return the statement model.
        """
        from app.chatterbot_api.chatterbot.ext.sqlalchemy_app.models import Statement
        return Statement

    def get_tag_model(self):
        """
        Return the conversation model.
        """
        from app.chatterbot_api.chatterbot.ext.sqlalchemy_app.models import Tag
        return Tag

    def get_statementrules_model(self):
        """
        Return the rule model.
        """

    def model_to_object(self, statement):
        from app.chatterbot_api.chatterbot.conversation import Statement as StatementObject

        return StatementObject(**statement.serialize())

    def count(self, search_table):
        """
        Return the number of entries in the database.
        """
        Statement = self.get_model(search_table)

        session = self.Session()
        statement_count = session.query(Statement).count()
        session.close()
        return statement_count

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        Statement = self.get_model('statement')
        session = self.Session()

        query = session.query(Statement).filter_by(text=statement_text)
        record = query.first()

        session.delete(record)

        self._session_finish(session)
