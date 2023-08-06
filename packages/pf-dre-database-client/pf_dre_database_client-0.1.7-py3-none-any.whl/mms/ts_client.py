#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The following client is used to read data to and write data from the postgres
Meter Management System which includes TimescaleDB for meter metric data.
"""

# Built-in Modules
import logging
import csv
from datetime import datetime, timedelta
from io import StringIO

# Third Party Modules
import pandas as pd
import psycopg2
from psycopg2 import sql, extras

# Project Specific Modules
from mms import helpers as h

# Logging
logger = logging.getLogger('timescale')


class TimescaleClient:
    def __init__(self, db_name, pk, standardized=True, **kwargs):
        self.db_name = db_name
        self.standardized = standardized
        if kwargs.get('dbname') is None:
            kwargs = h.get_db_client_kwargs()
        self.conn = psycopg2.connect(**kwargs)
        if kwargs.get('port') == "5000":
            read_only = False
        else:
            read_only = True
        self.conn.set_session(isolation_level="read uncommitted",
                              readonly=read_only,
                              autocommit=False)
        self.pk = pk
        self.allowed_aggs = ['first', 'last', 'avg']

    def rollback(self):
        self.conn.rollback()
        self.conn.close()

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def allowed_agg(self, agg):
        if agg not in self.allowed_aggs:
            raise ValueError("agg must be one of: {0}"
                             .format(self.allowed_aggs))
        return

    def query_to_df(self, query, params):
        try:
            df = pd.read_sql(query,
                             con=self.conn,
                             params=params)
            return df

        except psycopg2.Error as error:
            print("Error: %s".format(error))
            self.rollback()
            return None

    def execute_values(self, df, method='fail'):
        """
        Using psycopg2.extras.execute_values() to insert the Data Frame
        :param df: Data frame matching the schema of 'table' in the MMS.
        :param method: Action to perform when a duplicate row is
        encountered in the DB.
            - fail: Do not insert any rows in the transaction
            - update: Update the duplicate rows
            - ignore: Ignore the duplicate rows
        """
        # Comma-separated Data Frame columns, excluding index
        upsert_col_names = list(set(df.columns) - set(self.pk))
        upsert_setters = ', '.join(["{} = EXCLUDED.{}".format(a, a)
                                    for a in upsert_col_names])
        # Comma-separated Data Frame columns, including index
        cols = ','.join(list(df.columns))
        # Create a list of tuples from the Data Frame values
        tuples = [tuple(x) for x in df.to_numpy()]

        if method == 'fail':
            query = "INSERT INTO %s(%s) " \
                    "VALUES %%s " \
                    "RETURNING %s " % (self.db_name, cols, ','.join(self.pk))
        elif method == 'ignore':
            query = "INSERT INTO %s(%s) " \
                    "VALUES %%s " \
                    "ON CONFLICT (%s)" \
                    "DO NOTHING " \
                    "RETURNING %s " % (self.db_name, cols,
                                       ','.join(self.pk), ','.join(self.pk))
        elif method == 'update':
            query = "INSERT INTO %s(%s) " \
                    "VALUES %%s " \
                    "ON CONFLICT (%s)" \
                    "DO UPDATE SET %s " \
                    "RETURNING %s" % (self.db_name, cols,
                                      ','.join(self.pk), upsert_setters,
                                      ','.join(self.pk))
        else:
            raise ValueError("Param method must be one of 'fail', "
                             "'update', 'ignore'.")

        # SQL query to execute
        try:
            with self.conn.cursor() as cursor:
                extras.execute_values(cursor, query, tuples, page_size=1000)
                return cursor.fetchall()
        except psycopg2.IntegrityError as e:
            if e.pgcode == '23505':
                print("Cannot overwrite existing data in the MMS using "
                      "'fail' method")
            raise e
        except psycopg2.DatabaseError as error:
            print("Unexpected Error: %s" % error)
            self.rollback()
            raise error

    def copy_df_from_stringio(self, df):
        """
        Save the Data Frame in memory and use copy_from() to copy it to
        the table
        :param df: Data frame matching the schema of 'table' in the MMS.
        The index of the data frame will always be measurement_date
        :return: True if successful
        """
        s_buf = StringIO()
        cols = list(df.columns)
        df_idx = df.set_index('measurement_date', inplace=False)
        df_idx.to_csv(s_buf, sep='\t', quoting=csv.QUOTE_NONE, header=False)
        s_buf.seek(0)
        try:
            with self.conn.cursor() as cursor:
                cursor.copy_from(s_buf, self.db_name, columns=cols,
                                 sep='\t', size=8192)
                return cursor.rowcount
        except psycopg2.IntegrityError as e:
            if e.pgcode == '23505':
                print("Cannot overwrite existing data in the MMS using "
                      "'fail' method")
            raise e
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.rollback()
            raise error


class TimescaleClientNarrow(TimescaleClient):
    def __init__(self, db_name, standardized=True, **kwargs):
        pk = ['measurement_date', 'device_id', 'device_metric_type_id']
        TimescaleClient.__init__(self, db_name, pk, standardized, **kwargs)

    @staticmethod
    def get_agg_str(agg):
        if agg == 'avg':
            return "{0}(value)".format(agg)
        else:
            return "{0}(value, measurement_date)".format(agg)

    @staticmethod
    def standardize_df(df):
        """
        Convert narrow Data Frame format into the standard pandas DF
        result format by creating a multiIndex on
        device_id, device_metric_type_id, measurement_date.
        :param df: Raw query Data Frame with generic pandas index and the
        following columns:
        'device_id' (int), 'measurement_date' (string), '
        :return: Data frame in the format:
            - Index = ('measurement_date', 'device_id', 'device_metric_type_id')
            - Columns = ['value']
        """
        h.apply_standard_index(df)

        return df

    def get_all_metrics(self, device_ids, metrics, ts_start, ts_end):
        query = sql.SQL(
            "SELECT * "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND device_metric_type_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s ") \
            .format(sql.Identifier(self.db_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
        df = self.query_to_df(query,
                              device_ids +
                              metrics +
                              [ts_start, ts_end])
        if self.standardized:
            return self.standardize_df(df)
        else:
            return df

    def get_aggregated_metrics(self, res, device_ids, metrics,
                               ts_start, ts_end, agg='avg', fill=None):
        self.allowed_agg(agg)

        if fill == 'locf':
            # Linear interpolation between points
            value_str = "locf({0}) AS value".format(self.get_agg_str(agg))
        elif fill == 'interpolate':
            # Last Observation Carried Forward
            value_str = "interpolate({0}) AS value"\
                .format(self.get_agg_str(agg))
        else:
            value_str = "{0} AS value".format(self.get_agg_str(agg))
        query = sql.SQL(
            "SELECT "
            "time_bucket_gapfill({}, measurement_date) as time, "
            "device_id, device_metric_type_id, {} "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND device_metric_type_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s "
            "GROUP BY device_id, device_metric_type_id, time") \
            .format(sql.Literal(res),
                    sql.SQL(value_str),
                    sql.Identifier(self.db_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                    sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
        df = self.query_to_df(query,
                              device_ids + metrics + [ts_start, ts_end])
        df.rename(columns={'time': 'measurement_date'}, inplace=True)
        if self.standardized:
            return self.standardize_df(df)
        else:
            return df

    def get_latest_metrics(self, device_ids, metrics, window=None):
        """
        :param device_ids: A list of device_ids to be queried
        :param metrics: A list of metrics (Strings) to be queried for each
        device_id
        :param window: [Optional] The number of minutes prior to now that the
        latest values should be queried from.
        :return: Data Frame in standardized format:
        MultiIndex: (device_id <int64>,
                    device_metric_type_id <str>,
                    measurement_date <datetime64[ns])
        Columns: value <float64>
        """
        if window:
            ts_end = datetime.utcnow()
            ts_start = ts_end - timedelta(minutes=window)
            query = sql.SQL(
                "SELECT device_id, "
                "device_metric_type_id, "
                "last(measurement_date, measurement_date) AS measurement_date, "
                "last(value, measurement_date) AS value "
                "FROM {} "
                "WHERE device_id IN ({}) "
                "AND device_metric_type_id IN ({}) "
                "AND measurement_date BETWEEN %s AND %s "
                "GROUP BY device_id, device_metric_type_id") \
                .format(sql.Identifier(self.db_name),
                        sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                        sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
            df = self.query_to_df(query,
                                  device_ids +
                                  metrics +
                                  [ts_start, ts_end])
        else:
            query = sql.SQL(
                "SELECT device_id, "
                "device_metric_type_id, "
                "last(measurement_date, measurement_date) AS measurement_date, "
                "last(value, measurement_date) AS value "
                "FROM {} "
                "WHERE device_id IN ({}) "
                "AND device_metric_type_id IN ({}) "
                "GROUP BY device_id, device_metric_type_id")\
                .format(sql.Identifier(self.db_name),
                        sql.SQL(', ').join(sql.Placeholder() * len(device_ids)),
                        sql.SQL(', ').join(sql.Placeholder() * len(metrics)))
            df = self.query_to_df(query, device_ids + metrics)

        if self.standardized:
            return self.standardize_df(df)
        else:
            return df


class TimescaleClientJSON(TimescaleClient):
    def __init__(self, db_name, standardized=True, **kwargs):
        pk = ['measurement_date', 'device_id']
        TimescaleClient.__init__(self, db_name, pk, standardized, **kwargs)

    @staticmethod
    def get_agg_str(agg, m):
        if agg == 'avg':
            return "{0}((metrics->'{1}')::numeric)".format(agg, m)
        else:
            return "{0}((metrics->'{1}')::numeric, measurement_date)"\
                .format(agg, m)

    def standardize_df(self, df, metrics):
        """
        Convert JSON blob 'metrics' from query into the standard
        pandas DF
        result format.
        :param df:
        :param metrics: List fo metrics to be returned in the function
        :return: Data frame in the format:
            - Index = ('measurement_date', 'device_id', 'device_metric_type_id')
            - Columns = ['value']
        """

        # If the query returned raw rows (i.e. the metrics column), the JSON
        # data must be processed.
        if 'metrics' in list(df.columns):
            # Convert the JSON column to a pandas Series,
            # this creates columns for each key in the JSON
            df = pd.concat([df.drop(['metrics'], axis=1),
                                    df['metrics'].apply(pd.Series)], axis=1)
            # Filter the columns so only the requested metrics are stored
            df = df[[c for c in df.columns
                             if c in self.pk + metrics]]
        # Unpivot the DataFrame so the metric columns are compiled into
        # a single key value column pairing (number of DF rows increase)
        df = df.melt(
            id_vars=self.pk,
            var_name='device_metric_type_id',
            value_name='value'
        )
        h.apply_standard_index(df)

        return df

    def get_all_metrics(self, device_ids, metrics, ts_start, ts_end):
        query = sql.SQL(
            "SELECT * "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s") \
            .format(sql.Identifier(self.db_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)))
        df = self.query_to_df(query,
                              device_ids +
                              [ts_start, ts_end])
        if self.standardized:
            return self.standardize_df(df, metrics)
        else:
            return df

    def get_aggregated_metrics(self, res, device_ids, metrics,
                               ts_start, ts_end, agg='avg', fill=None):
        self.allowed_agg(agg)

        if fill == 'locf':
            # Last Observation Carried Forward
            values = ", ".join(["locf({0}) AS \"{1}\""
                               .format(self.get_agg_str(agg, m), m)
                                for m in metrics])
        elif fill == 'interpolate':
            # Linear interpolation between points
            values = ", ".join(["interpolate({0}) AS \"{1}\""
                               .format(self.get_agg_str(agg, m), m)
                                for m in metrics])
        else:
            values = ", ".join(["{0} AS \"{1}\""
                               .format(self.get_agg_str(agg, m), m)
                                for m in metrics])

        query = sql.SQL(
            "SELECT "
            "time_bucket_gapfill({}, measurement_date) AS time, "
            "device_id, {} "
            "FROM {} "
            "WHERE device_id IN ({}) "
            "AND measurement_date BETWEEN %s AND %s "
            "GROUP BY device_id, time")\
            .format(sql.Literal(res),
                    sql.SQL(values),
                    sql.Identifier(self.db_name),
                    sql.SQL(', ').join(sql.Placeholder() * len(device_ids)))
        df = self.query_to_df(query,
                              device_ids + [ts_start, ts_end])
        df.rename(columns={'time': 'measurement_date'}, inplace=True)
        if self.standardized:
            return self.standardize_df(df, metrics)
        else:
            return df

    def get_latest_metrics(self, device_ids, metrics, window=None):
        """
        :param device_ids: A list of device_ids to be queried
        :param metrics: A list of metrics (Strings) to be queried for
        each
        device_id
        :param window: [Optional] The number of minutes prior to now that the
        latest values
        should be queried from.
        :return: Data Frame in standardized format:
        MultiIndex: (device_id <int64>,
               device_metric_type_id <str>,
               measurement_date <datetime64[ns])
        Columns: value <float64>
        """
        if window:
            ts_end = datetime.utcnow()
            ts_start = ts_end - timedelta(minutes=window)
            query = sql.SQL(
                "SELECT device_id, "
                "last(measurement_date, measurement_date) AS measurement_date, "
                "last(metrics, measurement_date) AS metrics "
                "FROM {} "
                "WHERE device_id IN ({}) "
                "AND measurement_date BETWEEN %s AND %s "
                "GROUP BY device_id") \
                .format(sql.Identifier(self.db_name),
                        sql.SQL(', ').join(sql.Placeholder() * len(device_ids)))
            df = self.query_to_df(query,
                                  device_ids + [ts_start, ts_end])
        else:
            query = sql.SQL(
                "SELECT device_id, "
                "last(measurement_date, measurement_date) AS measurement_date, "
                "last(metrics, measurement_date) AS metrics "
                "FROM {} "
                "WHERE device_id IN ({}) "
                "GROUP BY device_id") \
                .format(sql.Identifier(self.db_name),
                        sql.SQL(', ').join(sql.Placeholder() * len(device_ids)))
            df = self.query_to_df(query, device_ids)
        if self.standardized:
            return self.standardize_df(df, metrics)
        else:
            return df
