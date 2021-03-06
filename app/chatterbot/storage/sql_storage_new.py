from app.chatterbot.storage import StorageAdapterNew


class SQLStorageAdapterNew(StorageAdapterNew):
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

        if (not self.engine.dialect.has_table(self.engine, 'Statement')) or \
                (not self.engine.dialect.has_table(self.engine, 'StatementRules')):
            self.create_database()

        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

    def get_statement_model(self):
        """
        Return the statement model.
        """
        from app.chatterbot.ext.sqlalchemy_app.models import Statement
        return Statement

    def get_random(self):
        """
        Returns a random statement from the database.
        """
        import random

        Statement = self.get_model('statement')

        session = self.Session()
        count = self.count()
        if count < 1:
            raise self.EmptyDatabaseException()

        random_index = random.randrange(0, count)
        random_statement = session.query(Statement)[random_index]

        statement = self.model_to_object(random_statement)

        session.close()
        return statement

    def get_statement_object(self):
        from app.chatterbot.conversation import Statement

        StatementModel = self.get_model('statement')

        Statement.statement_field_names.extend(
            StatementModel.extra_statement_field_names
        )

        return Statement

    def get_tag_model(self):
        """
        Return the conversation model.
        """
        from app.chatterbot.ext.sqlalchemy_app.models import Tag
        return Tag

    def get_statementrules_model(self):
        """
        Return the rule model.
        """
        from app.chatterbot.ext.sqlalchemy_app.models import StatementRules
        return StatementRules

    def model_to_object(self, statement):
        from app.chatterbot.conversation import Statement as StatementObject

        return StatementObject(**statement.serialize())

    def statement_model_to_object(self, statement):
        from app.chatterbot.conversation import Statement as StatementObject

        return StatementObject(**statement.serialize())

    def statementrules_model_to_object(self, statement):
        from app.chatterbot.conversation import StatementRules as StatementObject
        return StatementObject(**statement.serialize())

    def count(self):
        """
        Return the number of entries in the database.
        """
        Statement = self.get_model('statement')

        session = self.Session()
        statement_count = session.query(Statement).count()
        session.close()
        return statement_count

    def count_by_name(self, search_table):
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

    def remove_text(self, **kwargs):
        """
        删除符合statements的对话
        """
        Statement = self.get_model('statement')
        session = self.Session()
        if len(kwargs) == 0:
            query = session.query(Statement).filter()
        else:
            query = session.query(Statement).filter_by(**kwargs)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def remove_text_by_text(self, statement_text):
        """
        删除符合statements的对话
        """
        Statement = self.get_model('statement')
        session = self.Session()
        query = session.query(Statement).filter_by(text=statement_text)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def remove_text_by_id(self, statement_id):
        """
        删除符合statements的对话
        """
        Statement = self.get_model('statement')
        session = self.Session()
        query = session.query(Statement).filter_by(id=statement_id)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def remove_rules(self, **kwargs):
        """
        删除对应的对话规则
        """
        Statement = self.get_model('statementrules')
        session = self.Session()
        if len(kwargs) == 0:
            query = session.query(Statement).filter()
        else:
            query = session.query(Statement).filter_by(**kwargs)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def remove_rules_by_id(self, rule_id):
        """
        删除对应的对话规则
        """
        Statement = self.get_model('statementrules')
        session = self.Session()
        query = session.query(Statement).filter_by(id=rule_id)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def remove_rules_by_text(self, rule_text):
        """
        删除对应的对话规则
        """
        Statement = self.get_model('statementrules')
        session = self.Session()
        query = session.query(Statement).filter_by(text=rule_text)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain all
        listed attributes and in which all values match
        for all listed attributes will be returned.
        """
        from sqlalchemy import or_

        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        page_size = kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        persona_not_startswith = kwargs.pop('persona_not_startswith', None)
        search_text_contains = kwargs.pop('search_text_contains', None)

        # Convert a single sting into a list if only one tag is provided
        if type(tags) == str:
            tags = [tags]

        if len(kwargs) == 0:
            statements = session.query(Statement).filter()
        else:
            statements = session.query(Statement).filter_by(**kwargs)

        if tags:
            statements = statements.join(Statement.tags).filter(
                Tag.name.in_(tags)
            )

        if exclude_text:
            statements = statements.filter(
                ~Statement.text.in_(exclude_text)
            )

        if exclude_text_words:
            or_word_query = [
                Statement.text.ilike('%' + word + '%') for word in exclude_text_words
            ]
            statements = statements.filter(
                ~or_(*or_word_query)
            )

        if persona_not_startswith:
            statements = statements.filter(
                ~Statement.persona.startswith('bot:')
            )

        if search_text_contains:
            or_query = [
                Statement.search_text.contains(word) for word in search_text_contains.split(' ')
            ]
            statements = statements.filter(
                or_(*or_query)
            )

        if order_by:

            if 'created_at' in order_by:
                index = order_by.index('created_at')
                order_by[index] = Statement.created_at.asc()

            statements = statements.order_by(*order_by)

        total_statements = statements.count()

        for start_index in range(0, total_statements, page_size):
            for statement in statements.slice(start_index, start_index + page_size):
                yield statement

        session.close()

    def filter_text(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain all
        listed attributes and in which all values match
        for all listed attributes will be returned.
        """
        from sqlalchemy import or_

        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        page_size = kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        persona_not_startswith = kwargs.pop('persona_not_startswith', None)
        search_text_contains = kwargs.pop('search_text_contains', None)

        # Convert a single sting into a list if only one tag is provided
        if type(tags) == str:
            tags = [tags]

        if len(kwargs) == 0:
            statements = session.query(Statement).filter()
        else:
            statements = session.query(Statement).filter_by(**kwargs)

        if tags:
            statements = statements.join(Statement.tags).filter(
                Tag.name.in_(tags)
            )

        if exclude_text:
            statements = statements.filter(
                ~Statement.text.in_(exclude_text)
            )

        if exclude_text_words:
            or_word_query = [
                Statement.text.ilike('%' + word + '%') for word in exclude_text_words
            ]
            statements = statements.filter(
                ~or_(*or_word_query)
            )

        if persona_not_startswith:
            statements = statements.filter(
                ~Statement.persona.startswith('bot:')
            )

        if search_text_contains:
            or_query = [
                Statement.search_text.contains(word) for word in search_text_contains.split(' ')
            ]
            statements = statements.filter(
                or_(*or_query)
            )

        if order_by:

            if 'created_at' in order_by:
                index = order_by.index('created_at')
                order_by[index] = Statement.created_at.asc()

            statements = statements.order_by(*order_by)

        total_statements = statements.count()

        # print("tags=",Statement.tags)
        for start_index in range(0, total_statements, page_size):
            for statement in statements.slice(start_index, start_index + page_size):
                yield statement

        session.close()

    def filter_rules(self, **kwargs):
        """
        对话规则查询
        """
        from sqlalchemy import or_
        Statement = self.get_model('statementrules')
        session = self.Session()
        page_size = kwargs.pop('page_size', 1000)
        search_text_contains = kwargs.pop('search_text_contains', None)

        if len(kwargs) == 0:
            statements = session.query(Statement).filter()
        else:
            statements = session.query(Statement).filter_by(**kwargs)

        if search_text_contains:
            or_query = [
                Statement.search_text.contains(word) for word in search_text_contains.split(' ')
            ]
            statements = statements.filter(
                or_(*or_query)
            )

        total_statements = statements.count()

        for start_index in range(0, total_statements, page_size):
            for statement in statements.slice(start_index, start_index + page_size):
                yield statement

        session.close()

    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        tags = set(kwargs.pop('tags', []))

        if 'search_text' not in kwargs:
            kwargs['search_text'] = self.tagger.get_text_index_string(
                kwargs['text'])

        if 'search_in_response_to' not in kwargs:
            in_response_to = kwargs.get('in_response_to')
            if in_response_to:
                kwargs['search_in_response_to'] = self.tagger.get_text_index_string(
                    in_response_to)

        statement = Statement(**kwargs)

        for tag_name in tags:
            tag = session.query(Tag).filter_by(name=tag_name).first()

            if not tag:
                # Create the tag
                tag = Tag(name=tag_name)

            statement.tags.append(tag)

        session.add(statement)

        session.flush()

        session.refresh(statement)

        statement_object = self.model_to_object(statement)

        self._session_finish(session)

        return statement_object

    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        create_statements = []
        create_tags = {}

        for statement in statements:

            statement_data = statement.serialize()
            tag_data = statement_data.pop('tags', [])

            statement_model_object = Statement(**statement_data)

            if not statement.search_text:
                statement_model_object.search_text = self.tagger.get_text_index_string(
                    statement.text)

            if not statement.search_in_response_to and statement.in_response_to:
                statement_model_object.search_in_response_to = self.tagger.get_text_index_string(
                    statement.in_response_to)

            new_tags = set(tag_data) - set(create_tags.keys())

            if new_tags:
                existing_tags = session.query(Tag).filter(
                    Tag.name.in_(new_tags)
                )

                for existing_tag in existing_tags:
                    create_tags[existing_tag.name] = existing_tag

            for tag_name in tag_data:
                if tag_name in create_tags:
                    tag = create_tags[tag_name]
                else:
                    # Create the tag if it does not exist
                    tag = Tag(name=tag_name)

                    create_tags[tag_name] = tag

                statement_model_object.tags.append(tag)
            create_statements.append(statement_model_object)

        session.add_all(create_statements)
        session.commit()

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        if statement is not None:
            session = self.Session()
            record = None

            if hasattr(statement, 'id') and statement.id is not None:
                record = session.query(Statement).get(statement.id)
            else:
                record = session.query(Statement).filter(
                    Statement.text == statement.text,
                    Statement.conversation == statement.conversation,
                ).first()

                # Create a new statement entry if one does not already exist
                if not record:
                    record = Statement(
                        text=statement.text,
                        conversation=statement.conversation,
                        persona=statement.persona
                    )

            # Update the response value
            record.in_response_to = statement.in_response_to

            record.created_at = statement.created_at

            record.search_text = self.tagger.get_text_index_string(
                statement.text)

            if statement.in_response_to:
                record.search_in_response_to = self.tagger.get_text_index_string(
                    statement.in_response_to)

            for tag_name in statement.get_tags():
                tag = session.query(Tag).filter_by(name=tag_name).first()

                if not tag:
                    # Create the record
                    tag = Tag(name=tag_name)

                record.tags.append(tag)

            session.add(record)

            self._session_finish(session)

    def create_text(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        tags = set(kwargs.pop('tags', []))

        if 'search_text' not in kwargs:
            kwargs['search_text'] = self.tagger.get_text_index_string(
                kwargs['text'])

        if 'search_in_response_to' not in kwargs:
            in_response_to = kwargs.get('in_response_to')
            if in_response_to:
                kwargs['search_in_response_to'] = self.tagger.get_text_index_string(
                    in_response_to)

        statement = Statement(**kwargs)

        for tag_name in tags:
            tag = session.query(Tag).filter_by(name=tag_name).first()

            if not tag:
                # Create the tag
                tag = Tag(name=tag_name)

            statement.tags.append(tag)

        session.add(statement)

        session.flush()

        session.refresh(statement)

        statement_object = self.statement_model_to_object(statement)

        self._session_finish(session)

        return statement_object

    def create_rule(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statementrules')

        session = self.Session()
        if 'search_text' not in kwargs:
            kwargs['search_text'] = self.tagger.get_text_index_string(
                kwargs['text'])

        if 'search_in_response_to' not in kwargs:
            kwargs['search_in_response_to'] = self.tagger.get_text_index_string(
                kwargs['in_response_to'])
        statement = Statement(**kwargs)

        session.add(statement)

        session.flush()

        session.refresh(statement)

        statement_object = self.statementrules_model_to_object(statement)

        self._session_finish(session)

        return statement_object

    def create_many_texts(self, statements):
        """
        Creates multiple statement entries.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        create_statements = []
        create_tags = {}

        for statement in statements:

            statement_data = statement.serialize()
            tag_data = statement_data.pop('tags', [])

            statement_model_object = Statement(**statement_data)

            if not statement.search_text:
                statement_model_object.search_text = self.tagger.get_text_index_string(
                    statement.text)

            if not statement.search_in_response_to and statement.in_response_to:
                statement_model_object.search_in_response_to = self.tagger.get_text_index_string(
                    statement.in_response_to)

            new_tags = set(tag_data) - set(create_tags.keys())

            if new_tags:
                existing_tags = session.query(Tag).filter(
                    Tag.name.in_(new_tags)
                )

                for existing_tag in existing_tags:
                    create_tags[existing_tag.name] = existing_tag

            for tag_name in tag_data:
                if tag_name in create_tags:
                    tag = create_tags[tag_name]
                else:
                    # Create the tag if it does not exist
                    tag = Tag(name=tag_name)

                    create_tags[tag_name] = tag

                statement_model_object.tags.append(tag)
            create_statements.append(statement_model_object)

        session.add_all(create_statements)
        session.commit()

    def create_many_rules(self, statements):
        """
        Creates multiple statement entries.
        """
        Statement = self.get_model('statementrules')

        session = self.Session()

        create_statements = []

        for statement in statements:

            statement_data = statement.serialize()

            statement_model_object = Statement(**statement_data)

            create_statements.append(statement_model_object)

        session.add_all(create_statements)
        session.commit()

    def update_text(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        if statement is not None:
            session = self.Session()
            record = None

            if hasattr(statement, 'id') and statement.id is not None:
                record = session.query(Statement).get(statement.id)
            else:
                record = session.query(Statement).filter(
                    Statement.text == statement.text,
                    Statement.conversation == statement.conversation,
                ).first()

                # Create a new statement entry if one does not already exist
                if not record:
                    record = Statement(
                        text=statement.text,
                        conversation=statement.conversation,
                        persona=statement.persona
                    )

            # Update the response value
            record.text = statement.text
            record.in_response_to = statement.in_response_to

            record.created_at = statement.created_at

            record.search_text = self.tagger.get_text_index_string(
                statement.text)

            if statement.in_response_to:
                record.search_in_response_to = self.tagger.get_text_index_string(
                    statement.in_response_to)

            for tag_name in statement.get_tags():
                tag = session.query(Tag).filter_by(name=tag_name).first()

                if not tag:
                    # Create the record
                    tag = Tag(name=tag_name)

                record.tags.append(tag)

            session.add(record)

            self._session_finish(session)

    def update_rule(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        Statement = self.get_model('statementrules')

        if statement is not None:
            session = self.Session()
            record = None
            if hasattr(statement, 'id') and statement.id is not None:
                record = session.query(Statement).get(statement.id)
                if statement.text is not None:
                    record.text = statement.text
                if statement.in_response_to is not None:
                    record.in_response_to = statement.in_response_to
                if statement.search_text is not None:
                    record.search_text = statement.search_text
                else:
                    record.search_text = self.tagger.get_text_index_string(
                        statement.text)
                if statement.search_in_response_to is not None:
                    record.search_in_response_to = statement.search_in_response_to
                elif statement.in_response_to is not None:
                    record.search_in_response_to = self.tagger.get_text_index_string(
                        statement.in_response_to)
            else:
                if statement.text is not None:
                    record = session.query(Statement).filter(
                        Statement.text == statement.text,
                    ).first()
            # if statement.search_in_response_to is not None:
            #    record.search_in_response_to=statement.search_in_response_to
            if not record:
                record = Statement(
                    text=statement.text,
                )
            if statement.in_response_to is not None:
                record.in_response_to = statement.in_response_to
            if statement.search_text is not None:
                record.search_text = statement.search_text
            else:
                record.search_text = self.tagger.get_text_index_string(
                    statement.text)
            if statement.search_in_response_to is not None:
                record.search_in_response_to = statement.search_in_response_to
            elif statement.in_response_to is not None:
                record.search_in_response_to = self.tagger.get_text_index_string(
                    statement.in_response_to)

            session.add(record)

            self._session_finish(session)

    def drop(self):
        """
        Drop the database.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')
        Statementrules = self.get_model('statementrules')

        session = self.Session()

        session.query(Statement).delete()
        session.query(Tag).delete()
        session.query(Statementrules).delete()

        session.commit()
        session.close()

    def create_database(self):
        """
        Populate the database with the tables.
        """
        from app.chatterbot.ext.sqlalchemy_app.models import Base
        Base.metadata.create_all(self.engine)

    def _session_finish(self, session, statement_text=None):
        from sqlalchemy.exc import InvalidRequestError
        try:
            session.commit()
        except InvalidRequestError:
            # Log the statement text and the exception
            self.logger.exception(statement_text)
        finally:
            session.close()
