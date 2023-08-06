__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '0.2.0'
__all__ = [
    'DF',
    'SDF',
    'CONTEXT',
    'build_dataframe',
    'filter_rows',
    'filter_range_rows',
    'select_columns',
    'spark_to_pandas'
]

import typing as tp
import operator as op
import functools as ft
import warnings as wn

import pandas as pd
with wn.catch_warnings():
    wn.simplefilter('ignore')
    import pyspark as ps


DF = pd.DataFrame
SDF = ps.sql.DataFrame
CONTEXT = ps.SQLContext


def build_dataframe(sql_context: CONTEXT, database: str, table: str) -> SDF:
    """Build Pyspark DataFrame from Spark SQL context.

    :param sql_context: Pyspark SQL context to connect to database and table.
    :type sql_context: ``pyspark.SQLContext``
    :param database: Database name.
    :type database: ``str``
    :param table: Table name.
    :type table: ``str``
    :return: Pyspark DataFrame pointing to specified table.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return sql_context.table(f'{database}.{table}')


def filter_rows(df: SDF, *column_value: tp.Tuple[str, tp.Any]) -> SDF:
    """Filter rows of pyspark dataframe by each pair of (column, value).

    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param column_value: Pairs of column and value to be filtered.
    :type column_value: (``str``, ``any``)
    :return: Filtered spark dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.filter(ft.reduce(op.and_, [df[column] == value for column, value in column_value]))


def filter_range_rows(df: SDF, column: str, lower: tp.Any, upper: tp.Any) -> SDF:
    """Filter rows of pyspark dataframe within the range of lower and upper value (inclusive).

    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param column: Column to be filtered.
    :type column: ``str``
    :param lower: Lower value to be filtered.
    :type lower: ``any``
    :param upper: Upper value to be filtered.
    :type upper: ``any``
    :return: Filtered spark dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.filter((df[column] >= lower) & (df[column] <= upper))


def select_columns(df: SDF, *columns: str) -> SDF:
    """Select columns of pyspark dataframe.

    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param columns: Columns to be selected.
    :type columns: ``str``
    :return: Filtered spark dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.select(*columns)


def spark_to_pandas(df: SDF) -> DF:
    """Query spark dataframe getting pandas dataframe.

    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :return: Pandas dataframe with the data.
    :rtype: ``pandas.DataFrame``
    """
    return df.toPandas()
