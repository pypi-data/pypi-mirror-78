import mysql.connector

from RDS_Cognito_attribute_alignment.rds_cognito_pkg.settings import QUERY_STRING


def connect_to_db(db_user, db_password, db_host, db_port, db_database):
    """
    Use this function to connect to your RDS instance
    """
    print('Connecting to DB')
    connection = mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_database
    )
    return connection


def get_db_data(conn):
    """
    This function will take the connection object returned by the connect_to_db function and gather
    the required attribute data from your RDS instance.
    """
    db_data = []

    cursor = conn.cursor()

    # Set this variable to the query you intend to execute in your RDS instance.
    # query = f'SELECT user_id, {rds_table_column} FROM app_users WHERE org_id != 0 LIMIT 5'

    cursor.execute(QUERY_STRING)

    for (user_id, org_id) in cursor:
        db_data.append([user_id, org_id])

    conn.close()
    return db_data