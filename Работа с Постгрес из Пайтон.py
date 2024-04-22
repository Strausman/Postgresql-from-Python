import psycopg2

def create_db(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
            )
            """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL,
            phone TEXT NOT NULL,
            FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE
            )
            """)


def add_client(conn, first_name, last_name, email):
    cur.execute(
    "INSERT INTO  clients(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;",
        (first_name, last_name, email))
    client_id = cur.fetchone()[0]
    return client_id


def add_phone(conn, client_id, phone):
    cur.execute(
    "INSERT INTO phones(client_id, phone) VALUES(%s, %s);",
        (client_id, phone))


def update_client(conn, first_name=None, last_name=None, email=None):
    values = []
    columns = []
    if first_name:
        columns.append('first_name = %s')
        values.append(first_name)
    if last_name:
        columns.append('last_name = %s')
        values.append(last_name)
    if email:
        columns.append('email = %s')
        values.append(email)
    values.append(client_id)
    cur.execute(
        'UPDATE clients SET' + ','.join(columns) + 'WHERE id = %s;',
        values)

def remove_phone(conn, phone):
    cur.execute('DELETE FROM phones WHERE phone = %s;', (phone,))

def remove_client(conn, client_id):
    cur.execute("DELETE FROM clients WHERE id = %s;", (client_id,))


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    conditions = []
    values = []
    if first_name:
        conditions.append("clients.first_name = %s")
        values.append(first_name)
    if last_name:
        conditions.append("clients.last_name = %s")
        values.append(last_name)
    if email:
        conditions.append("clients.email = %s")
        values.append(email)
    if phone:
        conditions.append("phones.phone = %s")
        values.append(phone)
    query = sql.SQL("""
        SELECT DISTINCT clients.* FROM clients
        LEFT JOIN phones ON clients.id = phones.client_id
        WHERE {}
        """.format("OR".join(conditions))) if conditions else sql.SQL("SELECT * FROM clients;")
    cur.execute(query, values)
    return cur.fetchall()


with psycopg2.connect(database="clients_db", user="postgres", password="qwerty1995") as conn:
    with conn.cursor() as cur:
        create_db(conn)
        add_client(conn, 'Polina', 'Strausman', 'strausmanpol@gmail.com')
        add_phone(conn, 1, '999')
        update_client(conn, first_name = 'Johns')
        remove_phone(conn, '999')
        find_client(conn, last_name = 'Johns')
        remove_client(conn, 1)

conn.close()