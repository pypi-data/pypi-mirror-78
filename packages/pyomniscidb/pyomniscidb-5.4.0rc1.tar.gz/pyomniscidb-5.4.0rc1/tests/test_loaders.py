import datetime
from omnisci._loaders import _build_input_rows
from omnisci._parsers import ColumnDetails
from omnisci.thrift.OmniSci import (
    TStringRow,
    TStringValue,
)
import numpy as np


def get_col_types(col_properties: dict):
    common_col_params = dict(
        nullable=True,
        precision=0,
        scale=0,
        comp_param=0,
        encoding='NONE',
        # is_array=True,
    )

    return [
        ColumnDetails(**properties, **common_col_params)
        for properties in col_properties
    ]


class TestLoaders:
    @staticmethod
    def check_empty_insert(result, expected):
        assert len(result) == 3
        assert expected[0][0] == result[0][0]
        assert expected[0][2] == result[0][2]
        assert abs(expected[0][1] - result[0][1]) < 1e-7  # floating point

    def test_build_input_rows(self):
        dt_microsecond_format = '%Y-%m-%d %H:%M:%S.%f'

        def get_dt_nanosecond(v):
            return np.datetime64('201{}-01-01 01:01:01.001001001'.format(v))

        def get_dt_microsecond(v):
            return datetime.datetime.strptime(
                '201{}-01-01 01:01:01.001001'.format(v), dt_microsecond_format
            )

        data = [
            (1, 'a', get_dt_nanosecond(1), get_dt_microsecond(1)),
            (2, 'b', get_dt_nanosecond(2), get_dt_microsecond(2)),
        ]
        result = _build_input_rows(data)
        # breakpoint
        expected = [
            TStringRow(
                cols=[
                    TStringValue(str_val='1', is_null=None),
                    TStringValue(str_val='a', is_null=None),
                    TStringValue(
                        str_val=get_dt_nanosecond(1).astype(str), is_null=None
                    ),
                    TStringValue(
                        str_val=get_dt_microsecond(1).strftime(
                            dt_microsecond_format
                        ),
                        is_null=None,
                    ),
                ]
            ),
            TStringRow(
                cols=[
                    TStringValue(str_val='2', is_null=None),
                    TStringValue(str_val='b', is_null=None),
                    TStringValue(
                        str_val=get_dt_nanosecond(2).astype(str), is_null=None
                    ),
                    TStringValue(
                        str_val=get_dt_microsecond(2).strftime(
                            dt_microsecond_format
                        ),
                        is_null=None,
                    ),
                ]
            ),
        ]

        assert result == expected

    def test_build_input_rows_with_array(self):
        data = [(1, 'a'), (2, 'b'), (3, ['c', 'd', 'e'])]
        result = _build_input_rows(data)
        expected = [
            TStringRow(
                cols=[
                    TStringValue(str_val='1', is_null=None),
                    TStringValue(str_val='a', is_null=None),
                ]
            ),
            TStringRow(
                cols=[
                    TStringValue(str_val='2', is_null=None),
                    TStringValue(str_val='b', is_null=None),
                ]
            ),
            TStringRow(
                cols=[
                    TStringValue(str_val='3', is_null=None),
                    TStringValue(str_val='{c,d,e}', is_null=None),
                ]
            ),
        ]

        assert result == expected

    def test_load_empty_table(self, con):

        con.execute("drop table if exists baz;")
        con.execute("create table baz (a int, b float, c text);")

        data = [(1, 1.1, 'a'), (2, 2.2, '2'), (3, 3.3, '3')]
        con.load_table_rowwise("baz", data)
        result = sorted(con.execute("select * from baz"))
        self.check_empty_insert(result, data)
        con.execute("drop table if exists baz;")

    def test_select_null(self, con):
        con.execute("drop table if exists pymapd_test_table;")
        con.execute("create table pymapd_test_table (a int);")
        con.execute("insert into pymapd_test_table VALUES (1);")
        con.execute("insert into pymapd_test_table VALUES (null);")
        # the test

        c = con.cursor()
        result = c.execute("select * from pymapd_test_table")
        expected = [(1,), (None,)]
        assert result.fetchall() == expected

        # cleanup
        con.execute("drop table if exists pymapd_test_table;")

    def test_array_in_result_set(self, con):

        # text
        con.execute("DROP TABLE IF EXISTS test_lists;")
        con.execute(
            "CREATE TABLE IF NOT EXISTS test_lists \
                    (col1 TEXT, col2 TEXT[]);"
        )

        row = [
            ("row1", "{hello,goodbye,aloha}"),
            ("row2", "{hello2,goodbye2,aloha2}"),
        ]

        con.load_table_rowwise("test_lists", row)
        ans = con.execute("select * from test_lists").fetchall()

        expected = [
            ('row1', ['hello', 'goodbye', 'aloha']),
            ('row2', ['hello2', 'goodbye2', 'aloha2']),
        ]

        assert ans == expected

        # int
        con.execute("DROP TABLE IF EXISTS test_lists;")
        con.execute(
            "CREATE TABLE IF NOT EXISTS test_lists \
                    (col1 TEXT, col2 INT[]);"
        )

        row = [("row1", "{10,20,30}"), ("row2", "{40,50,60}")]

        con.load_table_rowwise("test_lists", row)
        ans = con.execute("select * from test_lists").fetchall()

        expected = [('row1', [10, 20, 30]), ('row2', [40, 50, 60])]

        assert ans == expected

        # timestamp
        con.execute("DROP TABLE IF EXISTS test_lists;")
        con.execute(
            "CREATE TABLE IF NOT EXISTS test_lists \
                    (col1 TEXT, col2 TIMESTAMP[], col3 TIMESTAMP(9));"
        )

        row = [
            (
                "row1",
                "{2019-03-02 00:00:00,2019-03-02 00:00:00,2019-03-02 00:00:00}",  # noqa
                "2010-01-01T01:01:01.001001001",
            ),
            (
                "row2",
                "{2019-03-02 00:00:00,2019-03-02 00:00:00,2019-03-02 00:00:00}",  # noqa
                "2011-01-01T01:01:01.001001001",
            ),
        ]

        con.load_table_rowwise("test_lists", row)
        ans = con.execute("select * from test_lists").fetchall()

        expected = [
            (
                'row1',
                [
                    datetime.datetime(2019, 3, 2, 0, 0),
                    datetime.datetime(2019, 3, 2, 0, 0),
                    datetime.datetime(2019, 3, 2, 0, 0),
                ],
                np.datetime64("2010-01-01T01:01:01.001001001"),
            ),
            (
                'row2',
                [
                    datetime.datetime(2019, 3, 2, 0, 0),
                    datetime.datetime(2019, 3, 2, 0, 0),
                    datetime.datetime(2019, 3, 2, 0, 0),
                ],
                np.datetime64("2011-01-01T01:01:01.001001001"),
            ),
        ]
        assert ans == expected

        # date
        con.execute("DROP TABLE IF EXISTS test_lists;")
        con.execute(
            "CREATE TABLE IF NOT EXISTS test_lists \
                    (col1 TEXT, col2 DATE[]);"
        )

        row = [
            ("row1", "{2019-03-02,2019-03-02,2019-03-02}"),
            ("row2", "{2019-03-02,2019-03-02,2019-03-02}"),
        ]

        con.load_table_rowwise("test_lists", row)
        ans = con.execute("select * from test_lists").fetchall()

        expected = [
            (
                'row1',
                [
                    datetime.date(2019, 3, 2),
                    datetime.date(2019, 3, 2),
                    datetime.date(2019, 3, 2),
                ],
            ),
            (
                'row2',
                [
                    datetime.date(2019, 3, 2),
                    datetime.date(2019, 3, 2),
                    datetime.date(2019, 3, 2),
                ],
            ),
        ]

        assert ans == expected

        # time
        con.execute("DROP TABLE IF EXISTS test_lists;")
        con.execute(
            "CREATE TABLE IF NOT EXISTS test_lists \
                    (col1 TEXT, col2 TIME[]);"
        )

        row = [
            ("row1", "{23:59:00,23:59:00,23:59:00}"),
            ("row2", "{23:59:00,23:59:00,23:59:00}"),
        ]

        con.load_table_rowwise("test_lists", row)
        ans = con.execute("select * from test_lists").fetchall()

        expected = [
            (
                'row1',
                [
                    datetime.time(23, 59),
                    datetime.time(23, 59),
                    datetime.time(23, 59),
                ],
            ),
            (
                'row2',
                [
                    datetime.time(23, 59),
                    datetime.time(23, 59),
                    datetime.time(23, 59),
                ],
            ),
        ]

        assert ans == expected
        con.execute("DROP TABLE IF EXISTS test_lists;")

    def test_insert_unicode(self, con):

        """INSERT Unicode using bind_params"""

        c = con.cursor()
        c.execute('drop table if exists text_holder;')
        create = 'create table text_holder (the_text text);'
        c.execute(create)
        first = {"value": "我和我的姐姐吃米饭鸡肉"}
        second = {"value": "El camina a case en bicicleta es relajante"}

        i1 = "INSERT INTO text_holder VALUES ( :value );"

        c.execute(i1, parameters=first)
        c.execute(i1, parameters=second)

        c.execute('drop table if exists text_holder;')

    def test_execute_leading_space_and_params(self, con):

        # https://github.com/omnisci/pymapd/issues/263

        """Ensure that leading/trailing spaces in execute statements
           don't cause issues
        """

        c = con.cursor()
        c.execute('drop table if exists test_leading_spaces;')
        create = 'create table test_leading_spaces (the_text text);'
        c.execute(create)
        first = {"value": "我和我的姐姐吃米饭鸡肉"}
        second = {"value": "El camina a case en bicicleta es relajante"}

        i1 = """

                    INSERT INTO test_leading_spaces


                    VALUES ( :value );

                            """

        c.execute(i1, parameters=first)
        c.execute(i1, parameters=second)

        c.execute('drop table if exists test_leading_spaces;')
