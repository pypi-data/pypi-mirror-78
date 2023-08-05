# coding=utf-8
import json
import logging
import posixpath
import urllib.parse

import configparser
import requests
import requests.auth
from collections import OrderedDict
import time

__author__ = 'ThucNC'

from ptoolbox.helpers.clog import CLog

_logger = logging.getLogger(__name__)


class AirtableAuth(requests.auth.AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        auth_token = {"Authorization": "Bearer {}".format(self.api_key)}
        request.headers.update(auth_token)
        return request


class Airtable(object):
    API_LIMIT = 1.0 / 5  # 5 per second
    API_URL = "https://api.airtable.com/v0"
    MAX_RECORDS_PER_REQUEST = 10

    def __init__(self, api_key, base_id, table_name, timeout=None):
        session = requests.Session()
        session.auth = AirtableAuth(api_key=api_key)
        self.session = session

        self.table_name = table_name
        url_safe_table_name = urllib.parse.quote(table_name, safe="")
        self.url_table = posixpath.join(self.API_URL, base_id, url_safe_table_name)
        self.timeout = timeout
        # print("url:", self.url_table)

    def _process_params(self, params):
        """
        Process params names or values as needed using filters
        """
        # new_params = OrderedDict()
        # for param_name, param_value in sorted(params.items()):
        #     param_value = params[param_name]
        #     ParamClass = AirtableParams._get(param_name)
        #     new_params.update(ParamClass(param_value).to_param_dict())
        # return new_params

        return params

    def _chunk(self, iterable, chunk_size):
        """Break iterable into chunks."""
        for i in range(0, len(iterable), chunk_size):
            yield iterable[i:i + chunk_size]

    def _build_batch_record_objects(self, records):
        return [{'fields': record} for record in records]

    def _process_response(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            err_msg = str(exc)

            # Reports Decoded 422 Url for better troubleshooting
            # Disabled in IronPython Bug:
            # https://github.com/IronLanguages/ironpython2/issues/242
            if response.status_code == 422:
                err_msg = err_msg.replace(response.url, urllib.parse.unquote(response.url))
                err_msg += " (Decoded URL)"

            # Attempt to get Error message from response, Issue #16
            try:
                error_dict = response.json()
            except ValueError:
                pass
            else:
                if "error" in error_dict:
                    err_msg += " [Error: {}]".format(error_dict["error"])
            raise requests.exceptions.HTTPError(err_msg)
        else:
            return response.json()

    def record_url(self, record_id):
        """ Builds URL with record id """
        return posixpath.join(self.url_table, record_id)

    def _request(self, method, url, params=None, json_data=None):
        response = self.session.request(
            method, url, params=params, json=json_data, timeout=self.timeout
        )
        return self._process_response(response)

    def _get(self, url, **params):
        processed_params = self._process_params(params)
        return self._request("get", url, params=processed_params)

    def _post(self, url, json_data):
        return self._request("post", url, json_data=json_data)

    def _put(self, url, json_data):
        return self._request("put", url, json_data=json_data)

    def _patch(self, url, json_data):
        return self._request("patch", url, json_data=json_data)

    def _delete(self, url):
        return self._request("delete", url)

    def _delete_batch(self, record_ids):
        return self._request("delete", self.url_table,
                             params={'records': record_ids})

    def get(self, record_id):
        record_url = self.record_url(record_id)
        return self._get(record_url)

    def get_iter(self, **options):
        """
        Record Retriever Iterator
        Returns iterator with lists in batches according to pageSize.
        To get all records at once use :any:`get_all`
        >>> for page in airtable.get_iter():
        ...     for record in page:
        ...         print(record)
        [{'fields': ... }, ...]
    Keyword Args:
            max_records (``int``, optional): The maximum total number of
                records that will be returned. See :any:`MaxRecordsParam`
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            page_size (``int``, optional ): The number of records returned
                in each request. Must be less than or equal to 100.
                Default is 100. See :any:`PageSizeParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.
            formula (``str``, optional): Airtable formula.
                See :any:`FormulaParam`.
        Returns:
            iterator (``list``): List of Records, grouped by pageSize
        """
        offset = None
        while True:
            data = self._get(self.url_table, offset=offset, **options)
            records = data.get("records", [])
            time.sleep(self.API_LIMIT)
            yield records
            offset = data.get("offset")
            if not offset:
                break

    def get_all(self, **options):
        """
        Retrieves all records repetitively and returns a single list.
        >>> airtable.get_all()
        >>> airtable.get_all(view='MyView', fields=['ColA', '-ColB'])
        >>> airtable.get_all(maxRecords=50)
        [{'fields': ... }, ...]
    Keyword Args:
            max_records (``int``, optional): The maximum total number of
                records that will be returned. See :any:`MaxRecordsParam`
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.
            formula (``str``, optional): Airtable formula.
                See :any:`FormulaParam`.
        Returns:
            records (``list``): List of Records
        >>> records = get_all(maxRecords=3, view='All')
        """
        all_records = []
        for records in self.get_iter(**options):
            all_records.extend(records)
        return all_records

    def insert(self, fields, typecast=False):
        """
        Inserts a record
        >>> record = {'Name': 'John'}
        >>> airtable.insert(record)
        Args:
            fields(``dict``): Fields to insert.
                Must be dictionary with Column names as Key.
            typecast(``boolean``): Automatic data conversion from string values.
        Returns:
            record (``dict``): Inserted record
        """
        return self._post(
            self.url_table, json_data={"fields": fields, "typecast": typecast}
        )

    def batch_insert(self, records, typecast=False):
        """
        Breaks records into chunks of 10 and inserts them in batches.
        Follows the set API rate.
        To change the rate limit use ``airtable.API_LIMIT = 0.2``
        (5 per second)
        >>> records = [{'Name': 'John'}, {'Name': 'Marc'}]
        >>> airtable.batch_insert(records)
        Args:
            records(``list``): Records to insert
            typecast(``boolean``): Automatic data conversion from string values.
        Returns:
            records (``list``): list of added records
        """
        inserted_records = []
        for chunk in self._chunk(records, self.MAX_RECORDS_PER_REQUEST):
            new_records = self._build_batch_record_objects(chunk)
            response = self._post(self.url_table, json_data={
                "records": new_records, "typecast": typecast})
            inserted_records += response['records']
            time.sleep(self.API_LIMIT)
        return inserted_records

    def __repr__(self):
        return "<Airtable table:{}>".format(self.table_name)

    @staticmethod
    def read_credential(credential_file):
        config = configparser.ConfigParser()
        config.read(credential_file)
        if not config.has_section('AIRTABLE'):
            CLog.error(f'Section `AIRTABLE` should exist in {credential_file} file')
            return None, None
        if not config.has_option('AIRTABLE', 'api_key') \
                or not config.has_option('AIRTABLE', 'base_id') \
                or not config.has_option('AIRTABLE', 'table'):
            CLog.error(f'api_key, base_id and table are required in {credential_file} file')
            return None, None

        api_key = config.get('AIRTABLE', 'api_key')
        base_id = config.get('AIRTABLE', 'base_id')
        table = config.get('AIRTABLE', 'table')

        return api_key, base_id, table


if __name__ == "__main__":
    at = Airtable(api_key="key7AsmElRf7gYGLD", base_id="appjq5RyjSUAAbFwZ", table_name="cs_raw_log")

    rec = {
        "date": "2020-08-13T08:32:45",
        "username": "thucnguyen1",
        "A": 100,
        "rank": 2,
        "B": 100,
        "C": 300,
        "D": 300,
        "E": 300,
        "time": 111,
        "XP": 2200,
        "tournament": "https://app.codesignal.com/tournaments/vRPK5SKeXSPHPn9qg",
        "score": 1100,
        "check": True,
        "name": "Nguyễn Chí Thức"
    }
    res = at.batch_insert([rec])
    print("Inserted:", len(res), res)
    data = at.get_all()

    print(len(data), json.dumps(data))