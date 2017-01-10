from DataBaseConnections import connect
import psycopg2.extras

class Repository():
    ##
    # To store new App Name
    ##
    def store(self, tableName, params=None):
            cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            fields = ', '.join(params.keys())
            values = ', '.join(['%%(%s)s' % x for x in params])
            query = 'INSERT INTO %s (%s) VALUES (%s) RETURNING id;' % (tableName, fields, values)
            cursor.execute(query, params)
            connect.commit()
            return self.bind_column_name_with_data(cursor.fetchall())

    ##
    # To fetch app details
    ##
    def fetchDetailsWithJoin(self, fromTableName, withTableName, joinOn=None, params=None):
            cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
            fields = ', '.join(joinOn.keys())
            values = ', '.join(joinOn.values())
            fieldsMatch = ', '.join(params.keys())
            valuesMatch = ', '.join(['%%(%s)s' % x for x in params])
            if params:
                query = "SELECT %s.*, %s.* FROM %s LEFT OUTER JOIN %s ON (%s) = (%s) WHERE (%s)=(%s)" %(fromTableName, withTableName, fromTableName, withTableName, fields, values, fieldsMatch, valuesMatch)
            else:
                query = "SELECT %s.*, %s.* FROM %s LEFT OUTER JOIN %s ON (%s) = (%s)" %(fromTableName, withTableName, fromTableName, withTableName, fields, values)
            joinOn.update(params)
            cursor.execute(query, joinOn)
            connect.commit()
            return self.bind_column_name_with_data(cursor.fetchall())

    def fetchDetailsWithoutJoin(self, tableName, params=None):
        cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if params:
            fields = ', '.join(params.keys())
            values = ', '.join(['%%(%s)s' % x for x in params])
            query = 'SELECT * FROM %s WHERE (%s)=(%s)' %(tableName, fields, values)
        else:
            query = 'SELECT * FROM %s ' %(tableName)
        cursor.execute(query, params)
        connect.commit()
        return self.bind_column_name_with_data(cursor.fetchall())

    def nextVal(self, tableName):
        cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = 'SELECT * FROM %s ' %(tableName)
        cursor.execute(query, params)
        connect.commit()
        return cursor.fetch()

    ##
    # To bind data with column table name
    ##
    def bind_column_name_with_data(self,  data):
            result = []
            if len(data) == 1:
                return dict(data[0])
            for row in data:
                result.append(dict(row))
            return result