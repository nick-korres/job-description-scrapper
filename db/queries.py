from inspect import getmembers
from typing import Type
from db.db_connect import run_query
from utils.general.list_actions import get_class_attributes

class GenericClass:
    def __init__(self, value):
        self.value = value


def insert_one(db_class: Type[GenericClass],options = {"insert_or_ignore": True}):
    columns = get_class_attributes(db_class)
    values = [getattr(db_class,column) for column in columns]
    placeholder_values = ["?" for _ in range(len(values))]
    table_name = db_class.__class__.__name__
    insert = "INSERT OR IGNORE"if options["insert_or_ignore"] else "INSERT"

    query_string = f'{insert} INTO {table_name} ({",".join(columns)}) VALUES ({",".join(placeholder_values)}) ;'
    result = run_query(query_string,values)
    return result

def find_where(db_class: GenericClass,attribute,value,operator="="):
    table_name = db_class.__name__
    columns = get_class_attributes_without_instance(db_class)
    query_string = f'SELECT {",".join(columns)} FROM {table_name} where {table_name}.{attribute} {operator} "{value}"'
    result = run_query(query_string)
    return serialize_db_response(result,db_class)

    
def get_class_attributes_without_instance(db_class: GenericClass):
    return list(db_class.__annotations__.keys())

def serialize_db_response(result: list[tuple[str]],db_class: GenericClass) -> list[GenericClass]:
    if result is None: return None
    # column names are the same as class attribute names
    columns = get_class_attributes_without_instance(db_class)
    serialized_result = [] 
    for res in result:
        row = dict()
        # query must select in same order as they are defined in the class
        index = 0 
        for column in res:
            row[columns[index]] = column
            index+=1

        serialized_result.append(db_class(**row))
    return serialized_result

def delete_where(db_class: GenericClass,attribute,value,operator="="):
    table_name = db_class.__name__
    query_string = f'DELETE FROM {table_name} where {table_name}.{attribute} {operator} ? ;'
    run_query(query_string,[value])