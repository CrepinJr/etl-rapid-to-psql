def joke_exists(conn, setup, delivery):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 1 FROM jokes WHERE setup = %s AND delivery = %s
        """, (setup, delivery))
        return cur.fetchone() is not None
