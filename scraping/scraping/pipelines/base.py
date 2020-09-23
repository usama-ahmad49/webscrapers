import csv
import io
import logging.config
import os
from datetime import datetime
from os.path import dirname

import six
from scrapy.exporters import CsvItemExporter

from scraping import settings
# from scraping.models import zip_msa
# from logging_config import set_up_logging, configure_logging
#
# logging.config.dictConfig(settings.LOGGING)
# logger = logging.getLogger(__file__)
#
# configure_logging(logger, 'base_pipeline.log')
# slack_client = slack.WebClient(token=settings.SLACK_BOT_ACCESS_TOKEN)


class CustomCsvItemExporter(CsvItemExporter):
    """
    scrapy's csv pipeline
    """
    def __init__(self, file, include_headers_line=True, join_multivalued=',', **kwargs):
        self._configure(kwargs, dont_fail=True)
        if not self.encoding:
            self.encoding = 'utf-8'
        self.include_headers_line = include_headers_line
        self.stream = io.TextIOWrapper(
            file,
            line_buffering=False,
            write_through=True,
            encoding=self.encoding,
            newline=''  # Windows needs this https://github.com/scrapy/scrapy/issues/3034
        ) if six.PY3 else file
        self.csv_writer = csv.writer(self.stream, **kwargs)
        self._headers_not_written = True
        self._join_multivalued = join_multivalued


def make_dirs(path):
    """
    created directory on given path
    :param path: path of directory
    :return:
    """
    path = path.rstrip("/")
    cwd = os.getcwd()  # Remember the current working dir
    try:
        os.chdir(path)
    except (IOError, FileNotFoundError):
        # Directory `path` does not exist yet.
        make_dirs(dirname(path))  # Make parent directories
        os.mkdir(path)  # Make directory
    os.chdir(cwd)  # Restore the original working directory.


class CSVPipeline(object):
    """
    This pipeline saves data in CSV, we use it while running scraper on local
    """
    def process_item(self, item, spider):
        """
        save item in CSV
        :param item:
        :param spider:
        :return:
        """
        self.exporter.export_item(item)
        return item

    def open_spider(self, spider):
        """
        This function executes on spider open, it creates a csv file on given path and start exporting data.
        """
        file_path = '%s_%s.csv' % (spider.name, datetime.now().strftime("%Y%m%d%H%M%S"))
        spider.file_name = spider.get_index(file_path.split('_'), 1)
        csv_path = os.path.join(settings.PROJECT_DIR, 'csv', spider.name)
        make_dirs(csv_path)
        self.file = open(os.path.join(csv_path, file_path), 'w+b')
        self.exporter = CustomCsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        """
        Finish exporting data when spider closed
        """
        self.exporter.finish_exporting()
        self.file.close()


class BasePipeline(object):
    """
    This is base pipeline for storing data in database
    """
    buffer = []
    buffer_add_ignore = []
    max_buffer_size = 1
    postgres = False
    required_fields = []    # fields to check errors and send slack notifications on
    bucket = {}
    threshold = 50      # min errors required to send slack notifications
    runDate = datetime.today().date()

    def open_spider(self, spider):
        """
        fields to check errors and send slack notifications if these fields are not available
        """
        for field in self.required_fields:
            self.bucket[field] = 0

    def process_item(self, item, spider):
        """
        This method cleans values of item that is scraped by spider
        :param item: item scraped
        :return:
        """
        item['runDate'] = self.runDate
        item['item_time_csv'] = datetime.now().strftime("%Y-%m-%d %H:%M:%Sms")
        if self.postgres:
            return item
        for key, value in item.items():
            if value and isinstance(value, bytes):
                item[key] = value.decode('utf-8')
            if hasattr(self, 'clean_%s' % key):
                item[key] = getattr(self, 'clean_%s' % key)(value)
            if item[key] and isinstance(item[key], str):
                item[key] = item[key].strip().encode('utf-8')

    def close_spider(self, spider):
        """
        Save the remaining items in the buffer and send slack error message if number of missing required fields cross
        threshold
        """
        self.bulk_commit()
        self.bulk_commit_add_with_ignore()

    def enqueue_item(self, item, update=False, data=None, columns=None, _class=None):
        """
        Here we add/update the DB objects in the session only and add them to self.buffer.
        Once buffer size is equal to MAX_BUFFER_SIZE, we commit all the changes in the session.
        :param item: Object from DB
        :param bool update: If true, it will update the given object with given data
        :param dict data: Data to update the given object
        :param list|None columns: Columns to save data for
        :param class|None _class: Class to call save/update on
        """
        if _class:
            self._class = _class
        if len(self.buffer) >= self.max_buffer_size:
            self.bulk_commit(_class)
        if update:
            self._class.bulk_update(item, data, columns)
        else:
            self._class.bulk_add(item)
        self.buffer.append(item)
        return item

    def enqueue_add_with_ignore(self, data, _class=None, buffer=None):
        """
        Here we add the DB objects in the session with INSERT IGNORE option and add them to self.buffer_add_ignore.
        Once buffer size is equal to MAX_BUFFER_SIZE, we commit all the changes in the session.
        :param dict data: Data for the new object
        :param class _class: Class to call enqueue for
        :param list buffer: List to store the buffer data
        """
        if buffer is not None:
            self.buffer_add_ignore = buffer
        if len(self.buffer_add_ignore) >= self.max_buffer_size:
            self.bulk_commit_add_with_ignore(_class)
        self.buffer_add_ignore.append(data)
        return data

    def bulk_commit(self, _class=None):
        """
        save data that is in buffer on exceeding buffer size
        """
        if _class:
            _class.bulk_commit()
        else:
            self._class.bulk_commit()
        self.buffer = list()

    def bulk_commit_add_with_ignore(self, _class=None, buffer=None):
        """
        added buffer item in db with add ignore option
        """
        if _class:
            self._class = _class
        if buffer is not None:
            self.buffer_add_ignore = buffer
        self._class.bulk_add_with_ignore(self.buffer_add_ignore, self.postgres)
        self._class.bulk_commit()
        self.buffer_add_ignore = list()

    def clean_zip(self, value):
        """
        This function cleans zip value
        :param value: zip value
        :return: cleaned zip value
        """
        try:
            cleaned = int(value)
        except (ValueError, TypeError):
            cleaned = None
        else:
            cleaned = str(cleaned).zfill(5) if len(str(cleaned)) == 4 else cleaned
        return cleaned

    @staticmethod
    def clean_state(value):
        """
        This method will get full state name and return its abbreviation
        :param value: Full state name
        :return: state abbreviation
        """
        return []

    @staticmethod
    def create_data(data, model, excluded_columns, columns=None):
        """
        Here we create dict of data using keys from the model columns
        :param dict data: data obtained from spider
        :param model: (SQLAlchemy class) Model to get data for
        :param list excluded_columns: Columns to exclude
        :param list|None columns: Columns in model
        """
        item = {}
        if not columns:
            columns = model.__table__.columns.keys()
        columns = [column for column in columns if column not in excluded_columns]
        for column in columns:
            item[column] = data.get(column)
        return item


class BasePCPipeline(BasePipeline):
    """
    This base class can be used for all scrappers who have parent child relation between two tables
    using Foreign Key e.g all scrappers in multi_family, self_storage
    """
    parent_class = None
    parent = None
    child_class = None
    child_key_id = None
    child_unique_id = 'apartmentId'
    child_unique_columns = None

    def __init__(self, **kwargs):
        """
        initialize all instance level variables
        """
        self._class = self.parent_class
        self.existing_db_parent_items = {}
        self.existing_db_child_items = set()
        self.parent_key_id = kwargs.get('parent_key_id', 'communityId')
        self.queued_items = dict()
        self.unique_queued_items = set()
        self.child_key_name = kwargs.get('child_key_name', 'building')
        self.child_columns = kwargs.get('child_columns', self.child_class.__table__.columns.keys())
        self.parent_columns = kwargs.get('parent_columns', self.parent_class.__table__.columns.keys())
        excluded_columns = ['id', 'msa', 'createdDate', 'created', 'modified', self.child_key_id]
        self.excluded_columns = list(set(excluded_columns) | set(kwargs.get('excluded_columns', [])))
        self.all_msa = {}

    def open_spider(self, spider):
        """
        This function executes when spider opens and get existing parent db items,.
        """
        self.existing_db_parent_items = dict(self.parent_class.query.with_entities(
            getattr(self.parent_class, self.parent_key_id),
            getattr(self.parent_class, 'id')).all())

    def close_spider(self, spider):
        """
        Save the remaining items in the buffer
        """
        self.bulk_commit()
        self.bulk_commit_add_with_ignore(self.child_class)

    def process_item(self, item, spider):
        """
        This function create/update parent and child objects from scraped item and save them in database
        :return:
        """
        super().process_item(item, spider)
        for col in (self.parent_key_id, 'zip'):
            if isinstance(item[col], bytes):
                item[col] = item[col].decode('utf-8')
        if isinstance(item['zip'], int):
            item['zip'] = str(item['zip'])
        """
        id of parent object if parent object already exist
        """
        parent_id = self.existing_db_parent_items.get(item[self.parent_key_id])
        data = self.create_data(item, self.parent_class, self.excluded_columns, self.parent_columns)
        data['msa'] = self.all_msa.get(item['zip'])     # get msa from database against given zipcode
        if 'key' in self.parent_class.__table__.columns.keys():     # key is a column that uniquely identifies a record
            data['key'] = data[self.parent_key_id]
        if not parent_id:
            # When running scrapers in multi server need to check again before assuming parent is not present
            parent = self.parent_class.query.filter(
                getattr(self.parent_class, self.parent_key_id) == item[self.parent_key_id]).first()
            if parent:
                self.existing_db_parent_items.update({item[self.parent_key_id]: parent.id})
                parent_id = parent.id
        if parent_id:
            parent = self.parent_class.get(parent_id)
            self.enqueue_item(parent, update=True, data=data, columns=self.parent_columns)  # update parent object
        else:
            if 'key' in self.parent_class.__table__.columns.keys():
                data['key'] = data[self.parent_key_id]
            if 'finalDate' in self.parent_class.__table__.columns.keys():
                data['finalDate'] = datetime.today().date()     # finalDate is the latest date when this record came
            parent = self.parent_class(**data)
            try:
                self.parent_class.save(parent)      # create parent record if it is not already saved
            except Exception as e:
                print(f'Duplicate item found while saving for {item[self.parent_key_id]}')
                parent = self.parent_class.query.filter(
                    getattr(self.parent_class, self.parent_key_id) == item[self.parent_key_id]).first()
            self.existing_db_parent_items.update({item[self.parent_key_id]: parent.id})
        self.parent = parent
        data = {self.child_key_id: parent.id}       # adding foreign key
        """
        create_data receives a dictionary and created object of the given class from that dictionary 
        """
        apt_data = self.create_data(item, self.child_class, self.excluded_columns, self.child_columns)
        data.update(apt_data)
        self.post_processing(item, data)
        if hasattr(parent, 'key'):
            data['key'] = parent.key
        self.enqueue_add_with_ignore(data, self.child_class)
        for field in self.required_fields:
            if not item.get(field):
                self.bucket[field] = len(self.bucket[field]) + 1
                print(f'{field} is empty in {item}')
        return item

    def post_processing(self, item, data):
        """
        This method will be called before making the SQLAlchemy object to
        make any final changes before sending it for saving in the database
        :param dict item: Dictionary returned from the spider
        :param dict data: Dictionary that will be passed to session for saving
        :return:
        """
        pass


class BasePCPricingPipeline(BasePipeline):
    """
    This base class can be used for all scrappers who have parent child relation between three tables
    using Foreign Key e.g all scrappers in multi_family, self_storage
    ::NOTE::
        Each child class should have a `key` column which should uniquely identify each row
    """
    parent_class = None
    child_class = None
    pricing_class = None
    child_key_id = None
    pricing_key_id = 'apartmentId'
    child_unique_id = 'apartmentId'
    child_unique_columns = None

    def __init__(self, **kwargs):
        """
        This function initializes all instance level variables
        """
        self.parent = None
        self._class = self.parent_class
        self.existing_db_parent_items = {}
        self.existing_db_child_items = {}
        self.parent_key_id = kwargs.get('parent_key_id', 'communityId')
        self.queued_items = dict()
        self.unique_queued_items = set()
        self.child_key_name = kwargs.get('child_key_name', 'building')
        self.child_columns = kwargs.get('child_columns', self.child_class.__table__.columns.keys())
        self.parent_columns = kwargs.get('parent_columns', self.parent_class.__table__.columns.keys())
        excluded_columns = ['id', 'msa', 'createdDate', 'created', 'modified', 'key', self.child_key_id]
        self.excluded_columns = list(set(excluded_columns) | set(kwargs.get('excluded_columns', [])))
        self.all_msa = {}

    def open_spider(self, spider):
        """
        This function gets existing parent and child items and create dictionary, we are getting this in start so we
        won't have to query database every time
        """
        self.existing_db_parent_items = dict(self.parent_class.query.with_entities(
            getattr(self.parent_class, self.parent_key_id),
            getattr(self.parent_class, 'id')).all())
        self.existing_db_child_items = self.get_existing_db_child_items()

    def close_spider(self, spider):
        """
        Save the remaining items in the buffer
        """
        self.bulk_commit()
        self.bulk_commit(self.child_class)
        self.bulk_commit_add_with_ignore(self.pricing_class)

    def process_item(self, item, spider):
        """
        This function creates/update parent, child and pricing object from scraped item and save them in db(add pricing
        object in add_with_ignore buffer)
        """
        super().process_item(item, spider)
        for col in (self.parent_key_id, 'zip', self.child_unique_id):
            if isinstance(item[col], bytes):
                item[col] = item[col].decode('utf-8')
        if isinstance(item['zip'], int):
            item['zip'] = str(item['zip'])
        parent_id = self.existing_db_parent_items.get(item[self.parent_key_id])
        data = self.create_data(item, self.parent_class, self.excluded_columns, self.parent_columns)
        data['msa'] = self.all_msa.get(item['zip'])
        data['finalDate'] = datetime.today().date()
        if not parent_id:
            # When running scrapers in multi server need to check again before assuming parent is not present
            parent = self.parent_class.query.filter(
                getattr(self.parent_class, self.parent_key_id) == item[self.parent_key_id]).first()
            if parent:
                self.existing_db_parent_items.update({item[self.parent_key_id]: parent.id})
                parent_id = parent.id
        if parent_id:
            parent = self.parent_class.get(parent_id)
            self.enqueue_item(parent, update=True, data=data, columns=self.parent_columns)
        else:
            if 'key' in self.parent_class.__table__.columns.keys():
                data['key'] = data[self.parent_key_id]
            parent = self.parent_class(**data)
            self.parent_class.save(parent)
            self.existing_db_parent_items.update({item[self.parent_key_id]: parent.id})
        self.parent = parent
        data = {self.child_key_id: parent.id}
        apt_data = self.create_data(item, self.child_class, self.excluded_columns, self.child_columns)
        data.update(apt_data)
        self.post_processing(item, data)
        child_id = self.existing_db_child_items.get(self.get_child_key_column(parent, data))
        if not child_id:
            # When running scrapers in multi server need to check again before assuming child is not present
            child = self.child_class.query.filter_by(key=self.get_child_key_column(parent, data)).first()
            if child:
                self.existing_db_child_items.update({self.get_child_key_column(parent, data): child.id})
                child_id = child.id
        if child_id:
            child = self.child_class.get(child_id)
            self.enqueue_item(child, update=True, data=data, _class=self.child_class, columns=self.child_columns)
        else:
            if 'key' in self.child_class.__table__.columns.keys():
                data['key'] = self.get_child_key_column(parent, data)
            child = self.child_class(**data)
            self.child_class.save(child)
            self.existing_db_child_items.update({self.get_child_key_column(parent, data): child.id})
        data = self.create_data(item, self.pricing_class, self.excluded_columns)
        data[self.pricing_key_id] = child.id
        if hasattr(child, 'key'):
            data['key'] = child.key
        self.final_price_processing(item, data)
        self.enqueue_add_with_ignore(data, self.pricing_class)
        for field in self.required_fields:
            if not item.get(field):
                self.bucket[field] = len(self.bucket[field]) + 1
                print(f'{field} is empty in {item}')
        return item

    def post_processing(self, item, data):
        """
        This method will be called before making the SQLAlchemy object to
        make any final changes before sending it for saving in the database
        :param dict item: Dictionary returned from the spider
        :param dict data: Dictionary that will be passed to session for saving
        :return:
        """
        pass

    def final_price_processing(self, item, data):
        """
        This method will be called before making the SQLAlchemy object to
        make any final changes before sending it for saving in the database
        :param dict item: Dictionary returned from the spider
        :param dict data: Dictionary that will be passed to session for saving
        :return:
        """
        pass

    def get_existing_db_child_items(self):
        """
        This method will return distinct child items from the database
        :return dict:
        """
        return dict(self.child_class.query.with_entities(self.child_class.key, self.child_class.id))

    def get_child_key_column(self, parent, data):
        """
        This method will return combination of columns to be used as key column
        :return str: string containing data from combination of columns
        """
        return f'{parent.key};{data[self.child_unique_id]}'


class SingleTableBasePipeline(BasePipeline):
    """
    This base class can be used for all scrappers who have single table to check new entry.
    e.g. In AUTOMOTIVE.TSLA
    ::NOTE::
        Table will include final date column
    """
    model_class = None
    excluded_columns = ['id', 'createdDate', 'created', 'modified']

    def __init__(self, **kwargs):
        self._class = self.model_class
        self.excluded_columns = self.excluded_columns or kwargs.get('excluded_columns', [])

    def process_item(self, item, spider):
        """
        create instance of model_class from scraped item and save it with "add with ignore" option
        """
        super().process_item(item, spider)
        data = self.create_data(item, self._class, self.excluded_columns)
        self.post_processing(item, data)
        self.enqueue_add_with_ignore(data, self._class)
        for field in self.required_fields:
            if not item.get(field):
                self.bucket[field] = len(self.bucket[field]) + 1
                print(f'{field} is empty in {item}')
        return item

    def post_processing(self, item, data):
        """
        This method will be called before making the SQLAlchemy object to
        make any final changes before sending it for saving in the database
        :param dict item: Dictionary returned from the spider
        :param dict data: Dictionary that will be passed to session for saving
        :return:
        """
        pass
