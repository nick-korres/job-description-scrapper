from db.models.job_posts import delete_orphan_jobs
from utils.files.delete_temp import delete_files_in_directory

def cleanup_temp():
    return delete_files_in_directory("./temp/")

def cleanup(cleanups=[delete_orphan_jobs,cleanup_temp]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            finally:
                for cleanup_func in cleanups:
                    if cleanup_func is not None: cleanup_func()
            return result
        return wrapper
    return decorator


