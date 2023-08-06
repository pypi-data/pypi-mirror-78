from sqlconnection import postgresql_queries, postgresql, logger


if __name__ == '__main__':
    psql = postgresql.Postgresql()
    conn = psql.connection
    #psql.close_connection()

    query = "SELECT * from  product limit 10;"
    x = postgresql_queries.execute_query(conn, query)
    for r in x:
        logger.info(r)
        logger.debug(r)
        logger.error(r)
        logger.critical(r)
    del conn
    y = 'u'
    z= psql.connection
    a = z
