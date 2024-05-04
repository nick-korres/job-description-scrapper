from db.queries import WhereClause, find_multiple_where, find_where, insert_one


class user_saw_job_post:
    user_id : str
    job_post_id : str
    user_chose_it : bool = False
    def __init__(self, user_id : str, job_post_id : str, user_chose_it : bool):
        self.user_id = user_id
        self.job_post_id = job_post_id
        self.user_chose_it = user_chose_it


def connect_user_to_job_post(user_id : str, job_post_id:str,chose_it:bool = False):
    new_user_saw_job_post = user_saw_job_post(user_id=user_id,job_post_id=job_post_id,user_chose_it=chose_it) 
    insert_one(new_user_saw_job_post)
    return new_user_saw_job_post

def connect_user_to_many_job_posts(user_id : str, job_post_ids:list[str],chose_all:bool = False):
    new_user_saw_job_post_list = []
    for job in job_post_ids :
        new_user_saw_job_post = user_saw_job_post(user_id=user_id,job_post_id=job,chose_it=chose_all) 
        insert_one(new_user_saw_job_post)
        new_user_saw_job_post_list.append(new_user_saw_job_post)
    return new_user_saw_job_post_list


def get_user_saw_job_post(user_id:str, job_post_id:str):
    first_clause =  WhereClause("user_id",user_id)
    second_clause = WhereClause("job_post_id",job_post_id)
    res = find_multiple_where(user_saw_job_post,[first_clause,second_clause])
    if len(res) == 0:
        return None
    return res[0]


def get_user_saw_job_posts(user_id:str):
    res = find_where(user_saw_job_post,"user_id",user_id)
    return res