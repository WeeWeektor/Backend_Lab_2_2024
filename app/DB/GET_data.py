def get_users_from_db(cur):
    cur.execute('''SELECT json_build_object(
                   'id', id,
                   'user_name', "user_name",
                   'currency_id',currency_id
                   ) AS data FROM "User"''')
    get_users_data = cur.fetchall()
    cur.close()
    return {'Users': get_users_data}

def get_user_from_db(cur, user_id):
    cur.execute('''SELECT * FROM "User" WHERE id = %s''', (user_id,))
    result = cur.fetchone()
    cur_name = get_currency_name(cur, result[1])
    cur.close()
    return {f'User - {result[0]}': {'id = ': result[2], 'currency id = ': result[1], 'currency = ': cur_name}}


def get_currency_name(cur, currency_id):
    cur.execute('''SELECT currency_name AS data FROM "Currency" WHERE id = %s''',
                (currency_id,))
    name_currency = cur.fetchone()
    return name_currency[0]

def get_all_categories(cur):
    cur.execute('''SELECT json_build_object(
                   'id', id,
                   'category_name', "category_name"
                   ) AS data FROM "Category"''')
    get_category_data = cur.fetchall()
    cur.close()
    return {'Categories': get_category_data}

def get_record_by_id(cur, identifier, another_id=None, identifier_2=None, another_id_2=None):
    if identifier_2 is None and another_id_2 is None:
        column_name = 'id' if another_id is None else another_id
        cur.execute(f'''SELECT json_build_object(
            'user_id', user_id,
            'category_id', category_id,
            'date', date,
            'total_price', total_price,
            'currency_id', currency_id,
            'id', id
            ) AS data FROM "Record" WHERE "{column_name}" = %s''', (identifier,))
    else:
        cur.execute(f'''SELECT json_build_object(
                    'user_id', user_id,
                    'category_id', category_id,
                    'date', date,
                    'total_price', total_price,
                    'currency_id', currency_id,
                    'id', id
                    ) AS data FROM "Record" 
                    WHERE "{another_id}" = %s AND "{another_id_2}" = %s''', (identifier, identifier_2))
    get_record_data = cur.fetchone()
    cur.close()
    return {'Record': get_record_data}

def get_currency_from_db(cur):
    cur.execute('''SELECT json_build_object(
                'currency_name', "currency_name",
                'id', id
                ) AS data FROM "Currency"''')
    get_currency_data = cur.fetchall()
    cur.close()
    return {'Currency': get_currency_data}

def get_user_id(cur, name):
    cur.execute(f'''SELECT id FROM "User" WHERE "user_name" = %s''', (name,))
    result = cur.fetchone()
    cur.close()
    return result[0]
