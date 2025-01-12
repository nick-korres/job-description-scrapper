CREATE TABLE IF NOT EXISTS 'job_post' (
        linkedin_id TEXT PRIMARY KEY,
        outer_html TEXT,
        inner_html TEXT,
        'description' TEXT,
        title TEXT,
        'size' TEXT,
        sector TEXT,
        'name' TEXT,
        'location' TEXT,
        age_number TEXT,
        age_type TEXT,
        applicants TEXT,
        'remote' TEXT,
        full TEXT,
        'level' TEXT,
        skills_required TEXT,
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_date TIMESTAMP DEFAULT NULL,
        expired_date TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS 'search_strings' (
        id TEXT PRIMARY KEY,
        search TEXT
);

CREATE TABLE IF NOT EXISTS 'search_to_job' (
        linkedin_id TEXT,
        search_id TEXT,
        FOREIGN KEY(linkedin_id) REFERENCES  job_post(linkedin_id) ON DELETE CASCADE,
        FOREIGN KEY(search_id) REFERENCES  search_strings(id) ON DELETE CASCADE,
        PRIMARY KEY ( linkedin_id , search_id )
);


CREATE TABLE IF NOT EXISTS  'user' (
	id TEXT PRIMARY KEY,
	linkedin_url TEXT UNIQUE	
) ;


CREATE TABLE IF NOT EXISTS 'user_saw_job_post' (
	user_id TEXT ,
	job_post_id TEXT ,
        user_chose_it boolean,
	PRIMARY KEY (user_id,job_post_id),
	FOREIGN KEY(user_id) REFERENCES 'user'(id) ON DELETE CASCADE,
	FOREIGN KEY(job_post_id) REFERENCES 'job_post'(linkedin_id) ON DELETE CASCADE
);
