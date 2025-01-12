from db.db_connect import run_query
from db.queries import WhereClause, find_multiple_where, find_where, get_class_attributes_without_instance, insert_one, serialize_db_response, upsert_one


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
    upsert_one(new_user_saw_job_post)
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


def get_user_saw_job_posts(user_id:str,show_expired:bool = False):
    if show_expired:
        res = find_where(user_saw_job_post,"user_id",user_id)
    else:
        columns = get_class_attributes_without_instance(user_saw_job_post)
        query = f'''
        SELECT {",".join(columns)} FROM user_saw_job_post 
        JOIN job_post ON user_saw_job_post.job_post_id = job_post.linkedin_id 
        WHERE user_saw_job_post.user_id = ? AND job_post.expired_date IS NULL
        '''
        escaped_query = query.replace('\n', ' ')
        res = run_query(escaped_query,[user_id])
        res = serialize_db_response(res,user_saw_job_post)
    return res