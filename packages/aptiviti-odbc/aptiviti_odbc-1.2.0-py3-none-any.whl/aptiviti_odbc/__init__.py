import pyodbc
import pandas
import math
import re

class aptiviti_odbc_connection:
    def __init__(self, host, username, password, database=None, driver='SQL Server Native Client 11.0', placeholder='mssqlserver', batch_limit=1000):
        self.BATCH_LIMIT = batch_limit
        self.driver = driver
        self.placeholders = { 'mssqlserver': '?' }
        self.placeholder = placeholder
        self.connection_string = f"Driver={{{driver}}};Server={host};UID={username};PWD={password};"

        if database != None:
            self.connection_string += f"database={database}"

        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()
    
    def get_placeholder(self):
        return self.placeholders[self.placeholder]

    def query(self, sql, parameters=None):
        return pandas.read_sql(sql, self.connection, params=parameters)

    def mutate(self, sql, parameters=None):
        if parameters == None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, parameters)            
        self.connection.commit()

    def get_batch_size(self, batch_number, max_batches, max_batch_size, record_count):
        return max_batch_size if batch_number < (max_batches-1) else record_count - max_batch_size*(max_batches-1)

    def get_placeholder_list(self, parameter_count, extra_parameters = []):
        return [self.get_placeholder() for i in range(0, parameter_count)] + extra_parameters

    def batch_insert(self, sql_template, values, extra_parameters = []):
        #expects sql template to contain a placeholder **values** for replacing with parameters        
        record_count = len(values)
        column_count = len(values[0])
        parameters = [value for record in values for value in record]
        parameters_length = len(parameters)
        max_batch_size = math.floor(self.BATCH_LIMIT / column_count)
        batches = math.ceil(parameters_length / self.BATCH_LIMIT)
        placeholder_list = self.get_placeholder_list(column_count, extra_parameters)
        for batch in range(0, batches):
            batch_size = self.get_batch_size(batch, batches, max_batch_size, record_count)
            batch_start = batch*max_batch_size
            record_list = [f'({",".join(placeholder_list)})' for i in range(0, batch_size)]            
            sql = sql_template.replace('**values**', ','.join(record_list))
            parameter_start = batch_start * column_count
            parameter_end = parameter_start + (batch_size * column_count)
            self.mutate(sql, parameters=parameters[parameter_start:parameter_end])

    def batch_query(self, sql_template, values, extra_parameters = []):
        item_count = len(values)
        batches = math.ceil(item_count / self.BATCH_LIMIT)
        combined_results = pandas.DataFrame([])        
        for batch in range(0, batches):
            batch_size = self.get_batch_size(batch, batches, self.BATCH_LIMIT, item_count)
            batch_start = batch*self.BATCH_LIMIT            
            placeholder_list = self.get_placeholder_list(batch_size)
            sql = sql_template.replace('**values**', ','.join(placeholder_list))
            parameter_start = batch_start
            parameter_end = parameter_start + batch_size
            parameters = values[parameter_start:parameter_end] + extra_parameters
            results = self.query(sql, parameters)
            combined_results = pandas.concat([combined_results, results])
        return combined_results

    def dynamic_update(self, sql_template, column_dictionary, extra_parameters = []):
        column_names = column_dictionary.keys()
        parameters = list(column_dictionary.values())        
        keyvalue_pair = []
        for key in column_names:
            keyvalue_pair.append(f'[{self.sanitize(key)}]=?')
        update_sql = sql_template.replace('**keyvalues**', ','.join(keyvalue_pair))
        parameters += extra_parameters
        self.mutate(update_sql, parameters=parameters)

    def sanitize(self, value):
        return re.sub(r"[^a-zA-Z0-9 ]", "", value)