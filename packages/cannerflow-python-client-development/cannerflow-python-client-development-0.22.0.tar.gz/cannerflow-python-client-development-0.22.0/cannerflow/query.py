from cannerflow.utils import *

__all__ = ["Query"]


class Query(object):
    def __init__(
        self,
        workspace_id,
        request,
        sql,
        cache_refresh,
        cache_ttl,
        data_format
    ):
        self.workspace_id = workspace_id
        self.request = request
        self.sql = sql
        self.data_format = data_format
        self.offset = 0
        self.limit = 500
        self._columns = None
        self.create_sql_query_payload = gen_create_sql_query_payload(
            workspace_id=workspace_id,
            cache_refresh=cache_refresh,
            cache_ttl=cache_ttl,
            sql=sql)
        self.data = []
        self.row_count = 0
        self.id = None
        self.status = None
        self.error = None
        self.statement_id = None
        self.create_sql_query()

    def __ensure_row_count(self):
        if self.row_count is None:
            self.get_first()

    def __ensure_columns(self):
        if self._columns is None:
            self.get_first()

    def __iter__(self):
        index = 0
        page = 1
        page_size = 50000
        self.get_first() # initial columns and row count

        # fetch first page
        result = self.request.post(gen_sql_result_payload(self.id, page_size, 0)).get(
            'sqlResultPagination')
        data = result['result']

        while (page - 1) * page_size + index < self.row_count:
            if index == page_size:
                # fetch new page
                result = self.request.post(gen_sql_result_payload(self.id, page_size, page_size * page)).get('sqlResultPagination')
                data = result['result']
                index = 0
                page += 1
            if len(data) > index:
                rtn_data = data_factory(data_format=self.data_format, columns=self.columns, data=[data[index]])
                yield rtn_data
                index += 1
            else:
                break


    @property
    def columns(self):
        self.__ensure_columns()
        return self._columns

    def create_sql_query(self):
        result = self.request.post(self.create_sql_query_payload).get('createSqlQuery')
        if result['status'] == 'FAILED':
            print(result)
            raise RuntimeError('Execute sql failed')
        self.update_info(result)

    def get_sql_query(self):
        result = self.request.post(gen_sql_query_payload(self.id)).get('sqlQuery')
        self.update_info(result)

    def delete_statement(self):
        if self.statement_id is None:
            return
        self.request.post(gen_delete_statement_payload(self.statement_id))
        # update info
        self.get_sql_query()

    def get_sql_result(self, limit, offset):
        limit = limit or self.limit
        offset = offset or self.offset
        result = self.request.post(gen_sql_result_payload(self.id, limit, offset)).get('sqlResultPagination')
        self._columns = result['columns']
        self.data = result['result']
        self.row_count = result['rowCount']

    def wait_for_finish(self, timeout=120, period=1):
        def check_status_and_update_info():
            if self.status != 'FINISHED':
                self.get_sql_query()
                return False
            else:
                return True
        wait_until(check_status_and_update_info, timeout, period)

    def update_info(self, result):
        self.id = result['id']
        self.status = result['status']
        self.error = result['error']
        self.row_count = result['rowCount']
        self.statement_id = result['statementId']

    def get_data(self):
        try:
            return data_factory(data_format=self.data_format, columns=self.columns, data=self.data)
        except Exception:
            raise RuntimeError(
                'Cannot get data correctly, please run query.wait_for_finish(timeout=seconds,period=seconds) first')

    def get_all(self):
        self.__ensure_row_count()
        self.get_sql_result(self.row_count, 0)
        return self.get_data()

    def get_first(self, limit=1):
        self.get_sql_result(limit, 0)
        return self.get_data()

    def get_last(self, limit=1):
        self.__ensure_row_count()
        offset = self.row_count - limit
        self.get_sql_result(limit, offset)
        return self.get_data()

    def get(self, limit, offset):
        self.get_sql_result(limit, offset)
        return self.get_data()

    def kill(self):
        self.delete_statement()

    def get_iterrows(self):
        return self

