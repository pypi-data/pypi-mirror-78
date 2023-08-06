import math
import pickle
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from littleutils import retry
from sqlalchemy import Column, DateTime, Integer, Text, func, LargeBinary, ForeignKey
from sqlalchemy.exc import (
    InterfaceError,
    InternalError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

from fn_station.utils import rows_to_dicts
from .queries import QueryStore


class FilePickleBlobStoreMixin(QueryStore):
    def __init__(self, root):
        self.root = Path(root)

    def store(self, query_id, path, obj):
        storage_path = self.root / str(query_id) / path
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(storage_path, "wb") as f:
            pickle.dump(obj, f)

    def get(self, query_id, path):
        storage_path = self.root / str(query_id) / path
        with open(storage_path, "rb") as f:
            return pickle.load(f)

    def store_parameters(self, query_id, parameters):
        return self.store(query_id, "parameters.pkl", parameters)

    def get_parameters(self, query_id):
        return self.get(query_id, "parameters.pkl")

    def store_signatures(self, query_id, signatures):
        return self.store(query_id, "signatures.pkl", signatures)

    def get_signatures(self, query_id):
        return self.get(query_id, "signatures.pkl")

    def store_result(self, query_id, result_name, result):
        return self.store(query_id, f"results/{result_name}.pkl", result)

    def get_result(self, query_id, result_name):
        return self.get(query_id, f"results/{result_name}.pkl")

    def store_definitions(self, query_id, definitions):
        return self.store(query_id, "definitions.pkl", definitions)

    def get_definitions(self, query_id):
        return self.get(query_id, "definitions.pkl")


class _Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__dict__.get("__name__", cls.__name__).lower()


class BaseComposerQuery:
    id = Column("id", Integer, primary_key=True)
    client_id = Column(Text)
    composer_name = Column(Text)
    user = Column(Text)
    timestamp = Column(DateTime)


MinimalBase = declarative_base(cls=_Base)


class MinimalComposerQuery(MinimalBase, BaseComposerQuery):
    pass


FullBase = declarative_base(cls=_Base)


class FullComposerQuery(FullBase, BaseComposerQuery):
    entry = Column(LargeBinary)


class ComposerQueryResult(FullBase):
    id = Column("id", Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey(FullComposerQuery.id))
    key = Column(Text)
    value = Column(LargeBinary)


# Based on https://docs.sqlalchemy.org/en/latest/errors.html#error-dbapi
retry_db = retry(3, (InterfaceError, OperationalError, InternalError, ProgrammingError))


class MinimalSQLAlchemyEntryStoreMixin(QueryStore):
    table_base = MinimalBase
    query_table = MinimalComposerQuery

    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)

        def session_scope():
            """Provide a transactional scope around a series of operations."""
            session = self.Session()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

        self.session_scope = contextmanager(session_scope)

    def setup(self):
        super().setup()
        self.table_base.metadata.create_all(self.engine)

    def store_query_entry(self, composer_name, client_id, entry, results):
        with self.session_scope() as session:
            query = MinimalComposerQuery(
                client_id=client_id,
                composer_name=composer_name,
                timestamp=datetime.now(),
            )
            session.add(query)
            session.commit()
            query_id = query.id

        self.store_parameters(query_id, entry.parameters)
        self.store_parameters(query_id, entry.definitions)
        self.store_parameters(query_id, entry.signatures)
        for key, result in results.items():
            self.store_result(query_id, key, result)

        return query_id

    def list_query_entries(
        self, page, id=None, composer_name=None, client_id=None, user=None, date=None
    ):
        cq = self.query_table
        with self.session_scope() as session:
            query = session.query(cq)
            if id:
                query = query.filter(cq.id == id)
            if composer_name:
                query = query.filter(cq.composer_name.ilike(f"%{composer_name}%"))
            if client_id:
                query = query.filter(cq.client_id.ilike(f"%{client_id}%"))
            if user:
                query = query.filter(cq.user.ilike(f"%{user}%"))
            if date:
                query = query.filter(func.date(cq.timestamp) == date)

            PAGE_SIZE = 30
            num_pages = math.ceil(query.count() / PAGE_SIZE)
            page = min(page, num_pages)
            return (
                rows_to_dicts(
                    query.order_by(-cq.id)
                    .limit(PAGE_SIZE)
                    .offset(max(0, (page - 1) * PAGE_SIZE))
                ),
                num_pages,
            )


class FullSQLAlchemyEntryStore(MinimalSQLAlchemyEntryStoreMixin):
    query_table = FullComposerQuery
    table_base = FullBase

    def store_query_entry(self, composer_name, client_id, entry, results):
        with self.session_scope() as session:
            query = FullComposerQuery(
                client_id=client_id,
                composer_name=composer_name,
                timestamp=datetime.now(),
                entry=pickle.dumps(entry),
            )
            session.add(query)
            session.commit()
            query_id = query.id

        with self.session_scope() as session:
            for key, value in results.items():
                session.add(
                    ComposerQueryResult(
                        key=key,
                        value=pickle.dumps(value),
                        query_id=query_id,
                    )
                )

        return query_id

    def get_result(self, query_id, result_name):
        with self.session_scope() as session:
            result_bytes = (
                session.query(ComposerQueryResult)
                    .filter_by(query_id=query_id, key=result_name)
                    .one()
                    .value
            )
        return pickle.loads(result_bytes)

    def get_query_entry(self, query_id):
        with self.session_scope() as session:
            result_bytes = (
                session.query(FullComposerQuery)
                    .filter_by(id=query_id)
                    .one()
                    .entry
            )
        return pickle.loads(result_bytes)
