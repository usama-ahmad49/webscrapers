import time
from abc import abstractmethod

from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import NoResultFound
import logging.config
from scraping import settings
# from logging_config import set_up_logging

from db import (Base, db_session_bbi)

# logging.config.dictConfig(settings.LOGGING)
# logger = logging.getLogger(__file__)
# set_up_logging(logger)


class classproperty(object):
    def __init__(self, getter_func):
        self.getter_func = getter_func

    def __get__(self, instance, owner_class):
        return self.getter_func(owner_class)


def create_table(engine):
    Base.metadata.create_all(engine)


class QueryMixinBase(Base, object):
    __abstract__ = True

    query = None

    @classproperty
    @abstractmethod
    def session(cls):
        pass

    @classmethod
    def get(cls, pk_id):
        """
        This method gets object from database against given id.
        If that object is already in session, this method will not get that
        object from database.
        This function will raise NoResultFound exception if no record found in
        database against given primary key.
        """
        try:
            obj = cls.query.get(pk_id)
        except Exception as e:
            cls.session.rollback()
            obj = cls.query.get(pk_id)
            # logger.info('Exception: ', e)
        return obj

    @classmethod
    def get_by_id(cls, pk_id):
        """
        This method gets the latest object from database against given id.
        """
        primary_key = cls.__mapper__.primary_key[0].key
        filter_string = '%s = :value' % primary_key
        return cls.query.filter(filter_string).params(value=pk_id).one()

    @classmethod
    def get_all(cls):
        """Return all records of calling class."""
        return cls.query.all()

    @classmethod
    def save(cls, instance):
        """
        Take object of model class and save that object in database.
        """
        try:
            cls.session.add(instance)
            cls.session.flush()
        except OperationalError:
            # In case of deadlock we will rollback add a delay and then retry the transaction
            cls.session.rollback()
            time.sleep(2)
            try:
                cls.session.add(instance)
                cls.session.commit()
            except:
                raise
        except Exception as e:
            cls.session.rollback()
            # logger.info('Exception: ', e)
        else:
            cls.session.commit()

    @classmethod
    def save_with_ignore(cls, data):
        """
        Take object of model class and save that object in database and ignore if it already exists.
        """
        try:
            cls.session.execute(insert(cls.__table__, values=data, prefixes=['IGNORE']))
        except Exception as e:
            cls.session.rollback()
            # logger.info('Exception: ', e)
        else:
            cls.session.commit()

    @classmethod
    def delete(cls, pk_id):
        """
        This method gets object against given primary key and delete it from
        database.
        """
        primary_key = cls.__mapper__.primary_key[0].key
        filter_string = '%s = :value' % primary_key
        rows_deleted = cls.query.filter(filter_string).params(value=pk_id).delete('fetch')

        if rows_deleted:
            cls.session.commit()
        return rows_deleted

    def update(self, **args):
        """
        1) This method gets primary key of table of current object.
        2) Make filter string using that primary key.
        3) Finally update current record with given values in args dictionary.

        Note:
        'fetch' string is passed in update function so that it will also update
        object in current session.
        """
        assert args, "No argument given to update method to update this object"
        primary_key = self.__mapper__.primary_key[0].key
        filter_string = '%s = :value' % primary_key  # We used this to avoid Sql injection
        rows_updated = self.query.filter(filter_string).params(value=getattr(self, primary_key)).update(args, 'fetch')
        if rows_updated:
            self.session.commit()
        return rows_updated

    @classmethod
    def bulk_save(cls, instances=None):
        """
        This method takes list of objects and save them to database
        :param instances: list
        :return:
        """
        if isinstance(instances, list):
            try:
                cls.session.add_all(instances)
                cls.session.flush()
            except OperationalError:
                # In case of deadlock we will rollback add a delay and then retry the transaction
                cls.session.rollback()
                time.sleep(2)
                try:
                    cls.session.add_all(instances)
                    cls.session.commit()
                except:
                    raise
            except IntegrityError:
                cls.session.rollback()
                raise
            else:
                cls.session.commit()

    @classmethod
    def bulk_add(cls, instance=None):
        """
        This method would take an instance and add it to session only and by flushing we would get
        the next id before actually saving it in db
        :param instance: model object
        """
        try:
            cls.session.add(instance)
            cls.session.flush()
        except OperationalError:
            # In case of deadlock we will rollback add a delay and then retry the transaction
            cls.session.rollback()
            time.sleep(2)
            try:
                cls.session.add(instance)
                cls.session.flush()
            except:
                raise
        except IntegrityError:
            cls.session.rollback()
            raise

    @classmethod
    def bulk_add_with_ignore(cls, data, postgres=False):
        """
        This method would take list of data dictionaries and add it to session with INSERT IGNORE option.
        >>> NOTE:
        Make sure each item in the list have same schema (keys) otherwise it will raise error

        "INSERT value for column table.column is explicitly rendered as a boundparameter in the VALUES clause;
        a Python-side value or SQL expression is required"

        :param list data: List of data dictionaries
        """
        if isinstance(data, list) and data:
            if postgres:
                cls.session.execute(postgres_insert(cls.__table__).values(data).on_conflict_do_nothing())
            else:
                try:
                    cls.session.execute(insert(cls.__table__, values=data, prefixes=['IGNORE']))
                except Exception as e:
                    cls.session.rollback()
                    # logger.info('Exception: ', e)
            cls.bulk_commit()
            cls.buffer_add_ignore = list()

    @classmethod
    def bulk_update(cls, instance, data, columns=None):
        """
        This method would take an instance and add it to session only and by flushing we would get
        the next id before actually saving it in DB

        >> NOTE: Data must contain valid column names, otherwise it will break the update

        :param instance: model object
        :param dict data: Data to update given object
        :param list|None columns: Columns to save data for
        """
        if not columns:
            columns = instance.__table__.columns.keys()
        for key in data.keys():
            assert key in columns, '`{}` is not a valid column for model `{}`'.format(key, instance.__table__.name)
        for key, value in data.items():
            if value:
                # We only need to update data if is updating to some non-null value
                setattr(instance, key, value)
        try:
            cls.session.flush()
        except Exception as e:
            cls.session.rollback()
            cls.session.flush()
            # logger.info('Exception: ', e)

    @classmethod
    def bulk_commit(cls):
        """
        This method would take an instance write it to database
        """
        try:
            cls.session.commit()
        except:
            cls.session.rollback()


class QueryMixinBBI(QueryMixinBase):
    __abstract__ = True

    query = db_session_bbi.query_property()

    @classproperty
    def session(cls):
        return db_session_bbi
