def patch_user_in_db(cur, user_id, new_name, new_currency):
    try:
        return_message = None
        if new_name is None and new_currency is None:
            return {'Failures': 'You have not entered any parameters to change!'}, 400

        elif new_name is not None and new_currency is None:
            cur.execute('''UPDATE "User" SET user_name = %s WHERE id = %s''', (new_name, user_id))
            return_message = {'Successful': {f'User with id = {user_id} is modified:': f'new name = {new_name}'}}

        elif new_currency is not None and new_name is None:
            new_currency_id = get_currency_from_db(cur, new_currency)
            cur.execute('''UPDATE "User" SET currency_id = %s WHERE id = %s''', (new_currency_id, user_id))
            return_message = {
                'Successful': {f'User with id = {user_id} is modified:': f'new default currency = {new_currency}'}}

        elif new_name is not None and new_currency is not None:
            new_currency_id = get_currency_from_db(cur, new_currency)
            cur.execute('''UPDATE "User" SET user_name = %s, currency_id = %s WHERE id = %s''',
                        (new_name, new_currency_id, user_id))
            return_message = {'Successful': {
                f'User with id = {user_id} is modified:': {'new name = ': new_name,
                                                           'new default currency = ': new_currency}}}

        cur.connection.commit()
        cur.close()
        return return_message, 200
    except Exception as e:
        cur.connection.rollback()
        return {'error': str(e)}, 500

def get_currency_from_db(cur, new_currency):
    cur.execute('''SELECT * FROM "Currency" WHERE currency_name = %s''', (new_currency,))
    res = cur.fetchone()
    if res is None:
        try:
            cur.execute('''INSERT INTO "Currency" ("currency_name") VALUES (%s) RETURNING id''',
                        (new_currency,))
            new_id = cur.fetchone()[0]
            cur.connection.commit()
            return new_id
        except Exception as e:
            cur.connection.rollback()
            return {'error': str(e)}, 500
    else:
        return res[1]
