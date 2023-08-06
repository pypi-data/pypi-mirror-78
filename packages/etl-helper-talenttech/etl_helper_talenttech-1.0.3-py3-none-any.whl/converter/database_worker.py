from converter.config.config_converter import excluded_fields, base_converter_params
import logging
import sys
import warnings
import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData, Table

warnings.filterwarnings("ignore")

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s  %(name)s  %(levelname)s: %(message)s",
)
logging.basicConfig(
    stream=sys.stderr,
    level=logging.ERROR,
    format="%(asctime)s  %(name)s  %(levelname)s: %(message)s",
)
logging.captureWarnings(True)


def get_type_sql_alchemy(type):
    try:
        return str(type.nested_type.__visit_name__).lower()
    except BaseException:
        return str(type.__visit_name__).lower()


def get_length_type_sql_alchemy(type):
    try:
        return type.length
    except BaseException:
        None


def get_default_arg_sql_alchemy(column):
    if column.default is not None:
        return column.default.arg
    elif column.server_default is not None:
        return str(column.server_default.arg)


class DataBaseWorker:
    def __init__(
            self, sql_credentials, db, debug=True, tables=None, table_checker=True
    ):
        """
        :param sql_credentials:
        :param from_db:
        :param to_db:
        :param debug: show debug text
        :param tables: converter only for list of tables. Will process more rapidly
        """
        self.table_checker = table_checker
        self.tables = tables or []
        self.db = db
        self.debug = debug
        self.sql_credentials = sql_credentials
        self.cred = self.sql_credentials[self.db]
        if self.__check_dialect():
            uri_sql_alchemy = "{0}://{1}:{2}@{3}:{4}/{5}".format(
                self.dialect,
                self.cred["user"],
                self.cred["password"],
                self.cred["host"],
                self.cred["port"],
                self.cred["database"],
            )
        additional_args = {}
        for key in self.sql_credentials[self.db]:
            if key not in ["database", "schema", "user", "host", "password", "port"]:
                additional_args[key] = self.sql_credentials[self.db][key]
        self.engine = create_engine(uri_sql_alchemy, **additional_args)
        self.log("try to connect...")
        self.conn = self.engine.connect()
        self.schema = None
        self.meta = None
        self.init_meta()
        self.log("connecting is successfull")

    def init_meta(self, tables=None):
        """
        reinit meta objects
        :return:
        """
        if "schema" in self.cred:
            self.schema = self.cred["schema"]
            self.meta = MetaData(bind=self.engine, schema=self.schema)
        else:
            self.meta = MetaData(bind=self.engine)
            self.schema = self.cred["database"]

        tables = tables or self.tables
        if len(tables) > 0 and self.table_checker:
            try:
                self.meta.reflect(only=tables)
            except sqlalchemy.exc.InvalidRequestError:
                raise sqlalchemy.exc.InvalidRequestError(
                    "One or more file didn't find in database {}. Critical exception"
                )
        elif len(tables) > 0 and not self.table_checker:
            try:
                self.meta.reflect(only=tables)
            except sqlalchemy.exc.InvalidRequestError:
                self.log(
                    "One or more file didn't find in database {}. Load table later".format(
                        self.db
                    )
                )
                self.meta = None
        else:
            self.meta.reflect()

    def __check_dialect(self):
        if self.db not in base_converter_params.keys():
            raise ModuleNotFoundError(
                "Dialect for {} type of database was'nt found, should be in list {}".format(
                    self.db, list(base_converter_params.keys())
                )
            )
        return True

    @property
    def dialect(self):
        return base_converter_params[self.db]["dialect"]

    @property
    def quote_char(self):
        return base_converter_params[self.db]["quote"]

    @property
    def __str__(self):
        return "DataBaseWorker_{}".format(self.db)

    @property
    def __repr__(self):
        return "DataBaseWorker_{}".format(self.db)

    def __del__(self):
        self.conn.close()

    def log(self, text):
        if self.debug:
            logging.info(self.__str__ + ": " + text)

    def check_if_table_availible(self, table):
        if len(self.tables) > 0 and table not in self.tables:
            raise ModuleNotFoundError(
                "Table_name to convert {} should be in list {} or set tables param to default".format(
                    table, self.tables
                )
            )
        return True

    def get_table_schema(self, table_name):
        columns_name = [
            "column_name",
            "data_type",
            "character_maximum_length",
            "column_default",
        ]
        table_sql = Table(table_name, self.meta)
        columns = [c.name for c in table_sql.columns]
        types = [get_type_sql_alchemy(c.type) for c in table_sql.columns]
        length = [get_length_type_sql_alchemy(c.type) for c in table_sql.columns]
        default = [get_default_arg_sql_alchemy(c) for c in table_sql.columns]
        fields = list(zip(columns, types, length, default))
        fields = [dict(zip(columns_name, f)) for f in fields]
        return fields

    def get_columns(self, table_name):
        """get column:type dict"""
        if self.check_if_table_availible(table_name):
            fields = self.get_table_schema(table_name)

        columns = [
            f["column_name"] for f in fields if f["column_name"] not in excluded_fields
        ]
        types = [
            f["data_type"] for f in fields if f["column_name"] not in excluded_fields
        ]
        return dict(zip(columns, types))
