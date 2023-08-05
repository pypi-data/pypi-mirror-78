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
        self.limit = 20
        self._columns = None
        self.create_sql_query_payload = gen_create_sql_query_payload(workspace_id=workspace_id, cache_refresh=cache_refresh, cache_ttl=cache_ttl, sql=sql);
        self.create_sql_query()
    @property
    def columns(self):
        self.ensure_columns()
        return self._columns
    def create_sql_query(self):
        result = self.request.post(self.create_sql_query_payload).get('createSqlQuery')
        if (result['status'] == 'FAILED'):
            print(result)
            raise RuntimeError('Execute sql failed')
        self.update_info(result)
    def get_sql_query(self):
        result = self.request.post(gen_sql_query_payload(self.id)).get('sqlQuery')
        self.update_info(result)
    def delete_statement(self):
        if (self.statement_id == None):
            return;
        self.request.post(gen_delete_statement_payload(self.statement_id))
        # update info
        self.get_sql_query();
    def get_sql_result(self, limit, offset):
        limit = limit or self.limit
        offset = offset or self.offset
        result = self.request.post(gen_sql_result_payload(self.id, limit, offset)).get('sqlResultPagination')
        self._columns = result['columns']
        self.data = result['result']
        self.row_count = result['rowCount']
    def wait_for_finish(self, timeout=120, period=1):
        def check_status_and_update_info():
            if (self.status != 'FINISHED'):
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
        return data_factory(data_format=self.data_format, columns=self.columns, data=self.data)
    def ensure_row_count(self):
        # hack: get rowCount by query first
        if (self.row_count == None):
            self.get_first()
    def ensure_columns(self):
          # hack: get columns by query first
        if (self._columns == None):
            self.get_first()
    def get_all(self):
        self.ensure_row_count()
        self.get_sql_result(self.row_count, 0)
        return self.get_data()
    def get_first(self, limit=1):
        self.get_sql_result(limit, 0)
        return self.get_data()
    def get_last(self, limit=1):
        self.ensure_row_count()
        offset = self.row_count - limit
        self.get_sql_result(limit, offset)
        return self.get_data()
    def get(self, limit, offset):
        self.get_sql_result(limit, offset)
        return self.get_data()
    def kill(self):
        self.delete_statement()