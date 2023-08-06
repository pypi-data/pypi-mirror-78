__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '0.4.0'
__all__ = [
    'DF',
    'SDF',
    'SS',
    'CONTEXT',
    'build_dataframe',
    'build_from_jdbc',
    'difference_between_rows',
    'filter_rows',
    'filter_range_rows',
    'select_columns',
    'spark_to_pandas',
]

import typing as tp
import operator as op
import functools as ft
import warnings as wn

import pandas as pd
with wn.catch_warnings():
    wn.simplefilter('ignore')
    import pyspark as ps
    from pyspark.sql.window import Window
    import pyspark.sql.functions as f

DF = pd.DataFrame
SDF = ps.sql.DataFrame
CONTEXT = ps.SQLContext
SS = ps.sql.session.SparkSession


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


def build_from_jdbc(spark_session: SS, jdbc_url: str, table: str, user: str, password: str,
                    integrated_security: str) -> SDF:
    """Build PySpark DataFrame from spark connection with SQL Server driver.

    :param spark_session: Spark Session to connect to table.
    :type spark_session: ``pyspark.sql.session.SparkSession``
    :param jdbc_url: URL to connect to database.
    :type jdbc_url: ``str``
    :param table: Table name.
    :type table: ``str``
    :param user: User to access table.
    :type user: ``str``
    :param password: Password to access table.
    :type password: ``str``
    :param integrated_security: Flag to set integrated security.
    :type integrated_security: ``str``
    :return: Pyspark DataFrame pointing to specified table.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return spark_session.read.format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table) \
        .option("user", user) \
        .option("password", password) \
        .option("integratedSecurity", integrated_security) \
        .load()


def difference_between_rows(df: SDF, order_column: str, difference_column: str, result_column: str):
    """Calculate the difference between consecutive rows in specified column of dataframe.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.DataFrame``
    :param order_column: Column informing order of records.
    :type order_column: ``str``
    :param difference_column: Column for which the difference is calculated.
    :type difference_column: ``str``
    :param result_column: Column name in which the result is saved.
    :type result_column: ``str``
    :return: Spark dataframe with consecutive difference column.
    :rtype: ``pyspark.DataFrame``
    """
    order_window = Window.orderBy(order_column)
    prev_column = f'{difference_column}_prev'

    df = df.withColumn(prev_column, f.lag(df[difference_column]).over(order_window))
    df = df.withColumn(result_column, (df[difference_column] - df[prev_column]))
    
    # Replace null value with original column value
    df = df.withColumn(result_column, f.coalesce(df[result_column], df[difference_column]))
    return df.drop(prev_column)


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
