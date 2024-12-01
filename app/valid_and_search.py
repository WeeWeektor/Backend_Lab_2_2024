import uuid

def is_valid_uuid(identifier):
    try:
        uuid_obj = uuid.UUID(str(identifier))
        return True
    except ValueError:
        return False

def search_data_in_db(cur, identifier, table, another_id=None, another_id_2=None, identifier_2=None):
    if another_id_2 is None and identifier_2 is None:
        column_name = 'id' if another_id is None else another_id
        cur.execute(f'''SELECT "{column_name}" FROM "{table}" WHERE "{column_name}" = %s''', (identifier,))
    else:
        cur.execute(f'''SELECT "{another_id}", "{another_id_2}" FROM "{table}" WHERE 
        "{another_id}" = %s AND "{another_id_2}" = %s''', (identifier, identifier_2))

    result = cur.fetchone()
    cur.close()
    return result if result else False

def if_currency_in_db(cur, name):
    cur.execute(f'''SELECT id FROM "Currency" WHERE "currency_name" = %s''', (name,))
    result = cur.fetchone()
    cur.close()
    return result if result else False

def if_user_name_in_db(cur, name):
    cur.execute(f'''SELECT 'user_name' FROM "User" WHERE "user_name" = %s''', (name,))
    result = cur.fetchone()
    cur.close()
    return result[0] if result else False
