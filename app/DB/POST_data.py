from passlib.handlers.pbkdf2 import pbkdf2_sha256
from .PATCH_data import get_currency_from_db
import datetime
import pytz


def create_new_user(cur, user_name, currency_name, user_password):
    try:
        if currency_name is None:
            currency_name = "USD"
        currency_id_ = get_currency_from_db(cur, str(currency_name))
        sha256_user_password = pbkdf2_sha256.hash(user_password)
        cur.execute('''INSERT INTO "User" ("user_name", currency_id, "password") VALUES (%s, %s, %s)''',
                    (user_name, currency_id_, sha256_user_password))
        cur.connection.commit()
        return {'Successful': f'New user with name - {user_name} create with default currency {currency_name}'}, 201
    except Exception as e:
        cur.connection.rollback()
        return {'error': str(e)}, 500


def create_new_category(cur, category_name, category_description):
    try:
        cur.execute('''INSERT INTO "Category" ("category_name", "category_description") VALUES (%s, %s)''',
                    (category_name, category_description))
        cur.connection.commit()
        cur.close()
        return {'Successful': f'New category {category_name} created!'}, 201
    except Exception as e:
        cur.connection.rollback()
        return {'error': str(e)}, 500

def create_new_record(cur, user_id, category_id, price, currency_id):
    try:
        adding_time = datetime.datetime.now(pytz.timezone('Europe/Kyiv')).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(f'''INSERT INTO "Record" (user_id, category_id, date, total_price, currency_id) 
                    VALUES (%s, %s, %s, %s, %s)''', (user_id, category_id, adding_time, price, currency_id))
        cur.connection.commit()
        cur.close()
        return {'Successful': f'New record created!'}, 201
    except Exception as e:
        cur.connection.rollback()
        return {'error': str(e)}, 500

def create_new_currency(cur, currency_name):
    try:
        cur.execute('''INSERT INTO "Currency" ("currency_name") VALUES (%s)''', (currency_name, ))
        cur.connection.commit()
        cur.close()
        return {'Successful': f'New currency {currency_name} created!'}, 201
    except Exception as e:
        cur.connection.rollback()
        return {'error': str(e)}, 500
