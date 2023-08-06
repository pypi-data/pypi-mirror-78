#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The following client is used to read data to and write data from the postgres
Meter Management System which includes TimescaleDB for meter metric data.
"""

# Built-in Modules

# Third Party Modules
import pandas as pd
import psycopg2
from psycopg2 import sql
from mms.helpers import get_db_client_kwargs


class MMSClient:
    def __init__(self, **kwargs):
        if kwargs.get('dbname') is None:
            self.kwargs = get_db_client_kwargs()
        else:
            self.kwargs = kwargs

    def get_device_ids_for_codes(self, codes):
        """

        :param codes: A list of device codes (strings) to return the
        device id's for.
        :return: A 1 to 1 dictionary with key (device code)
        and value (device id) (All strings)
        """
        query = sql.SQL("SELECT code, id FROM devices WHERE code IN ({})")\
            .format(sql.SQL(', ').join(sql.Placeholder() * len(codes)))
        with psycopg2.connect(**self.kwargs) as conn:
            df = pd.read_sql(query,
                             con=conn,
                             index_col='code',
                             params=codes)
        df['id'] = df['id'].apply(str)
        return dict(zip(list(df.index.values), list(df['id'].values)))

    def device_inverted(self, device_id):
        """
            :param device_id: A device codes (string) to return the
            device id for.
            :return: A single integer (device id)
            """
        if device_id is None:
            return 0

        query = "SELECT is_inverted " \
                "FROM meters " \
                "WHERE device_id = %s"
        with psycopg2.connect(**self.kwargs) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (device_id,))
                if cur.fetchone:
                    return int(cur.fetchone()[0])
                else:
                    # No device record returned
                    raise LookupError("No meter found for device {0}"
                                      .format(device_id))
