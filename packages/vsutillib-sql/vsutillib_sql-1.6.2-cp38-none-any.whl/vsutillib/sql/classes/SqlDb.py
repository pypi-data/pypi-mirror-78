"""
sql related classes
"""

import re
import sqlite3

from sqlite3 import Error as SQLiteError


class SqlDb:
    """
    class to manage connection to a sqllite database

    Raises:
        ValueError: when parametes don't match
    """

    def __init__(self, dbFile=None, autoCommit=False):

        self.__dbFile = dbFile
        self.__conn = None
        self.__lastError = None
        self.__autoCommit = autoCommit

        if self.__dbFile is not None:
            self.connect(dbFile)

    def __bool__(self):
        return bool(self.__conn)

    @property
    def connection(self):
        return self.__conn

    @property
    def error(self):
        return self.__lastError

    def close(self):
        self.connection.close()

    def connect(self, database, autoCommit=False):
        """
        connect connects to sqlite database

        Args:
            database (str, optional): database file. Defaults to None.
            autoCommit (bool, optional): execute commit after detection of
                SQL statement. Defaults to False.
        """

        rc = False

        self.__autoCommit = autoCommit
        self.__conn = None
        self.__lastError = None

        if isinstance(database, str):
            dbFile = database
        elif self.__dbFile is not None:
            dbFile = self.__dbFile

        if dbFile is not None:
            try:
                self.__conn = sqlite3.connect(database)
                rc = True
            except SQLiteError as e:
                self.__lastError = "SQLiteError: {}".format(e)

        return rc

    def sqlExecute(self, sqlStatement, *args, test=True):
        """
        sqlExecute execute sql statement

        Args:
            sqlStatement (str): sql statement to execute
            test (bool, optional): verify parameters pass to the method.
                Defaults to True.

        Raises:
            ValueError: raises error if the number of fields and values does not match

        Returns:
            sqlite3.cursor: cursor to point to the result of some operations
        """

        if test:
            regEx = re.compile(r"\?")
            regSelectEx = re.compile("SELECT")
            numExpectedVariables = 0
            numVariables = len(args)

            if match := regEx.findall(sqlStatement):
                numExpectedVariables = len(match)

            if numExpectedVariables != numVariables:
                if numExpectedVariables == 0:
                    msg = "Unexpected variables - {}".format(args)
                elif numVariables == 0:
                    msg = "Missing variables expected {}".format(numExpectedVariables)
                else:
                    msg = "Expected variables was {} received {}".format(
                        numExpectedVariables, numVariables
                    )
                raise ValueError(msg)

        cursor = None
        self.__lastError = None

        if match := regSelectEx.match(sqlStatement.strip().upper()):
            try:
                if len(args) > 0:
                    cursor = self.connection.execute(sqlStatement, args)
                else:
                    cursor = self.connection.execute(sqlStatement)
            except SQLiteError as e:
                self.__lastError = "SQLiteError: {}".format(e)
        else:
            try:
                with self.connection as conn:
                    if len(args) > 0:
                        cursor = conn.execute(sqlStatement, args)
                    else:
                        cursor = conn.execute(sqlStatement)
            except sqlite3.IntegrityError:
                self.__lastError = "Could not execute {}".format(sqlStatement)
            except SQLiteError as e:
                self.__lastError = "SQLiteError: {}".format(e)

        return cursor

    def sqlExecuteOriginal(self, sqlStatement, *args, test=True):
        """
        sqlExecute execute sql statement

        Args:
            sqlStatement (str): sql statement to execute
            test (bool, optional): verify parameters pass to the method.
                Defaults to True.

        Raises:
            ValueError: raises error if the number of fields and values does not match

        Returns:
            sqlite3.cursor: cursor to point to the result of some operations
        """

        if test:
            regEx = re.compile(r"\?")
            regDeleteEx = re.compile("DELETE")
            regInsertEx = re.compile("INSERT")
            regUpdateEx = re.compile("UPDATE")
            numExpectedVariables = 0
            numVariables = len(args)

            if match := regEx.findall(sqlStatement):
                numExpectedVariables = len(match)

            if numExpectedVariables != numVariables:
                if numExpectedVariables == 0:
                    msg = "Unexpected variables - {}".format(args)
                elif numVariables == 0:
                    msg = "Missing variables expected {}".format(numExpectedVariables)
                else:
                    msg = "Expected variables was {} received {}".format(
                        numExpectedVariables, numVariables
                    )
                raise ValueError(msg)

        cursor = None
        self.__lastError = None

        try:
            if len(args) > 0:
                cursor = self.connection.execute(sqlStatement, args)
            else:
                cursor = self.connection.execute(sqlStatement)
            if match := regDeleteEx.match(sqlStatement.strip().upper()):
                print("Delete commit")
                if self.__autoCommit:
                    print("select.connection.commit()")
            if match := regInsertEx.match(sqlStatement.strip().upper()):
                print("Insert commit")
                if self.__autoCommit:
                    print("select.connection.commit()")
            if match := regUpdateEx.match(sqlStatement.strip().upper()):
                print("Update commit")
                if self.__autoCommit:
                    print("select.connection.commit()")
        except SQLiteError as e:
            self.__lastError = "SQLiteError: {}".format(e)

        return cursor

    def transaction(self):
        sqlBeginTransaction = "BEGIN TRANSACTION;"
        cursor = self.connection.execute(sqlBeginTransaction)
        if cursor:
            return True
        return False

    def rollback(self):
        sqlRollback = "ROLLBACK;"
        cursor = self.connection.execute(sqlRollback)
        if cursor:
            return True
        return False

    def commit(self):
        sqlCommit = "COMMIT;"
        cursor = self.connection.execute(sqlCommit)
        if cursor:
            return True
        return False

    def tableExists(self, dbTable):
        """
        verify if table exists in the database
        """

        sqlTableCheck = """
            SELECT count(name)
              FROM sqlite_master
              WHERE type='table' AND name=?
            """

        cursor = self.connection.cursor()
        cursor.execute(sqlTableCheck, (dbTable, ))

        if cursor:
            row = cursor.fetchone()
            if row:
                return bool(row[0])

        return False
