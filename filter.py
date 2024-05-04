from data_process.filter_search import Criteria, CriteriaConfigField, filter_search
from db.models.job_posts import  job_post
from show_and_choose import show_and_choose


# Example , each (?=) is one more "and" expression
# (?=match this expression)(?=match this too)(?=oh, and this)
# | is "or" so a python data engineer or a c++ embedded is:
# (?=.*python)(?=.*data engineer)|(?=.*c\+\+)(?=.*embedded)

fullText = {
    "or" : ["Athens|Attiki","hybrid|remote"],
    "and" : ["back(-|\s)?end","node","remote|hybrid"],
    "not" : [
        "7.*years",
        "front(-|\s)?end",
],
    "ignore_case" : True, # Default is True
    "use_regex" : True # Default is True
}

title :CriteriaConfigField = {
    'field_name': "title",
    "criteria":  {    
        "not" : ["Angular"]
    }
}

level = {
    "field_name": "level",
    "criteria":  {    
        "not" : [
            "entry"
        ]
    }
}

remote = {
    "field_name": "remote",
    "criteria":  {    
        "not" : [
            "on-site"
        ]
    }
}

name = {
    "field_name": "name",
    "criteria":  {    
        "not" : [
            "EY",
            "Intrasoft",
            "Viva"
        ]
    },
    "ignore_case" : False, 
}

description = {
    "field_name": "description",
    "criteria":  {    
        "or" : []
    },
    "ignore_case" : False, 
}

criteria = Criteria()
criteria.full = None #fullText
criteria.fields = [title,remote,name]


search=None # None to search in all posts
filter_name="test_filter"
delete_cache = False # If True, it will delete the cache and start from scratch

job_list: list[job_post] = filter_search(search,criteria,filter_name)

show_and_choose(filter_name,job_list,delete_cache=delete_cache,save_selection_info=True)
