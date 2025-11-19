import psycopg2

def get_connection():
    return psycopg2.connect (
        host="localhost",
        database="project_db",
        user="postgres",
        password=""
    )

def fetch_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

def display_stats():
    files = fetch_query("SELECT file_id, file_name, file_size, upload_date FROM files ORDER BY upload_date DESC;")
    total_files = len(files)
    total_size = sum(f[2] for f in files) // (1024*1024)
    return files , total_files , total_size
