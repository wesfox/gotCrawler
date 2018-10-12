import sqlite3
from typing import List,Dict,Tuple

class MyDBConnection:
    """
        This class is aimed to handle every database calls, it use SQLite3
        in order to perform this. We may use one connection by Thread
    """
    def __init__(self,path_to_db):
        self.__db_connexion = sqlite3.connect(path_to_db, check_same_thread=False)
    
    def exec_mul(self, queries: List[str]) -> List[Dict[str,Tuple]]:
        """
            queries: the query list to be executed
            result: a list of dict which "result" key yield every rows from the 
            SQL result
            [{
                "query": query,
                "result": sql_result
            },...]
        """

        # this function is the same than exec_one but handle multiple queries
        # we made a copy past because the cursor must be create OUTSIDE the loop

        # we need to create a cursor to execute query(ies) and commit them (
        # to be sure they have been executed)
        cursor = self.__db_connexion.cursor()

        query_results = []

        for query in queries:
            # just checking that the query is a string
            if type(query) is not str :
                raise TypeError("query param is not a str")
            
            # we execute the query and fetch the result, for now, we do not
            # catch error waiting for an error handler.
            query_results.append({
                "query": query,
                "result": cursor.execute(query)
            })

        # once all the queries have been executed, we commit the result
        self.__db_connexion.commit()

        # we finaly return the result
        return query_results
    
    def exec_one(self, query: str):
        """
            query: the query to be executed
            result: an iterator which yield every rows from the SQL result
        """

        # just checking that the query is a string
        if type(query) is not str :
            raise TypeError("query param is not a str")
        # we need to create a cursor to execute query(ies) and commit them (
        # to be sure they have been executed)
        cursor = self.__db_connexion.cursor()
        
        # we execute the query and fetch the result
        query_result = cursor.execute(query)

        # the commit make sure that all the precedent executed query have been
        # properly executed (especially in multi-threaded context)
        self.__db_connexion.commit()

        # we finaly return the resule
        return query_result
