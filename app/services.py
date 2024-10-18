from app.data import user, record


def get_user_by_id(user_id):
    return next((u for u in user.users if u['id'] == user_id), None)

def get_record_by_id(record_id):
    return next((r for r in record.records if r['id'] == record_id), None)

def get_record_by_user_id(record_user_id):
    return [r for r in record.records if r['user id'] == record_user_id]

def get_record_by_category_id(record_category_id):
    return [r for r in record.records if r['category id'] == record_category_id]
