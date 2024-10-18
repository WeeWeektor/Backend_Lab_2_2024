import uuid
import datetime
import pytz


class User:
    def __init__(self):
        self.users = []

    def new_user(self, user_name):
        user_id = uuid.uuid4().hex

        user = {
            'id': user_id,
            'name': user_name
        }

        self.users.append(user)
        return user


class Category:
    def __init__(self):
        self.categories = []

    def new_categories(self, category_name, category_description):
        category_id = uuid.uuid4().hex

        category = {
            'id': category_id,
            'name': category_name,
            'description': category_description
        }

        self.categories.append(category)
        return category


class Record:
    def __init__(self):
        self.records = []

    def new_record(self, user_id, category_id, amount_of_expenses):
        record_id = uuid.uuid4().hex
        date = datetime.datetime.now(pytz.timezone('Europe/Kyiv')).strftime("%d-%m-%Y %H:%M:%S")

        record = {
            'id': record_id,
            'user id': user_id,
            'category id': category_id,
            'time of record creation': date,
            'amount of expenses': amount_of_expenses
        }

        self.records.append(record)
        return record
