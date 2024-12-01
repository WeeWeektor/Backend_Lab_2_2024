from passlib.handlers.pbkdf2 import pbkdf2_sha256


def user_log_in_app(cur, name, password):
    cur.execute(f'''SELECT json_build_object(
                'user_name', "user_name",
                'id', id,
                'password', "password"
                ) AS data FROM "User"  
                WHERE "user_name" = %s''', (name,))
    result = cur.fetchone()
    cur.close()
    if not result:
        return False, "User not found"
    else:
        if pbkdf2_sha256.verify(password, result[0]['password']):
            return True, result[0]['id']
        else:
            return False, "Wrong password!"
