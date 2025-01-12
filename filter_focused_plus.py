from data_process.filter_search import Criteria, CriteriaConfigField, filter_search
from db.models.job_posts import  job_post
from show_and_choose import show_and_choose


# Example , each (?=) is one more "and" expression
# (?=match this expression)(?=match this too)(?=oh, and this)
# | is "or" so a python data engineer or a c++ embedded is:
# (?=.*python)(?=.*data engineer)|(?=.*c\+\+)(?=.*embedded)

# fullText = {
#     "or" : ["Athens|Attiki","hybrid|remote"],
#     "and" : ["back(-|\s)?end","node","remote|hybrid"],
#     "not" : [
#         "7.*years",
#         "front(-|\s)?end",
# ],
#     "ignore_case" : True, # Default is True
#     "use_regex" : True # Default is True
# }


# Refers to job title
title : CriteriaConfigField = {
    'field_name': "title",
    "criteria":  {  
        "not" : [
            "Front[ -]?end",
            "Senior",
            "Full(-|\s)?stack",
            "React"
            ]
    }
}



level = {
    "field_name": "level",
    "criteria":  {    
        "not" : [
            # "entry"
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


# Refers to company name
name = {
    "field_name": "name",
    "criteria":  {  
        "and" : [],  
        "not" : [
            # "EY",
            # "Viva",
            # "Accenture",
            # "Canonical"
        ]
    },
    "ignore_case" : False, 
}

description = {
    "field_name": "description",
    "criteria":  {
        "or" : [
            "node",
            "nodejs",
            "Typescript",
            "Javascript",
            "deno",
        ],
        "and" :[
            "back(-|\s)?end"
            ],
        "not" : [
                "angular"
            ]
    },
    "ignore_case" : True, 
}

skills = {
    "field_name": "skills_required",
    "criteria":  {    
        "and" : [
            # "C++",
            ]
    },
    "ignore_case" : True, 
}

criteria = Criteria()
criteria.full = None #fullText
criteria.fields = [
    title,
    # level,
    remote,
    # name,
    description,
    # skills
]


search=None # None to search in all posts
filter_name="focused_plus"
delete_cache = True # If True, it will delete the cache and start from scratch

job_list: list[job_post] = filter_search(search,criteria,filter_name)

show_and_choose(filter_name,job_list,delete_cache=delete_cache,save_selection_info=True,hide_viewed_jobs=True)
