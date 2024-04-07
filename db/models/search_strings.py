import uuid

from db.queries import find_where, insert_one


class search_strings:
    id :str
    search: str
    def __init__(self, search:str,id:str=None):
        self.id:str = id or str(uuid.uuid4())
        self.search:str = search
        # TODO add created at and updated at

def find_or_create_search(string:str):
    existing_search: search_strings | None =  find_existing_search(string)
    if (existing_search is None):
        new_search_string =  search_strings(search=string)
        insert_one(new_search_string)
        return new_search_string
    else:
        return existing_search


def find_existing_search(search:str):
    existing_search: list[search_strings] | None =  find_where(search_strings,"search",search)
    if (existing_search is None or len(existing_search) == 0):
        return None
    elif len(existing_search) > 1 :
        raise Exception(f'more than id for {search}')
    else:
        return existing_search[0]
