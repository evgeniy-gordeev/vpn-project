import pandas as pd
from sqlalchemy import text


def get_urls_from_db(eng, user_id, host_ids=[0]):
    
    q = f"""SELECT url FROM usr
            WHERE 1=1
                AND subs_id = {user_id} 
                AND host_id = ANY(ARRAY{host_ids})"""

    with eng.begin() as conn:
        df = pd.read_sql(q, conn)
    
    return df.url.tolist()


def add_url_to_db(eng, user_id, host_id, url):
    
    q = f"""INSERT INTO usr (subs_id, host_id, url)
            VALUES ({user_id}, {host_id}, '{url}');"""
    
    with eng.begin() as conn:
        conn.execute(text(q))
        conn.commit()
