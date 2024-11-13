def delete_data_from_db(cur, identifier, table):
    cur.execute(f'''DELETE FROM "{table}" WHERE id = %s''', (identifier,))
    cur.connection.commit()
    cur.close()
    return {'Successful': f'{table} with id = {identifier} deleted!'}
