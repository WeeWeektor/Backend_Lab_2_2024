from flask import jsonify, request
from .DB.GET_data import get_users_from_db, get_user_from_db, get_all_categories, get_record_by_id, get_currency_from_db
from .DB.DELETE_data import delete_data_from_db
from .DB.PATCH_data import patch_user_in_db
from .DB.POST_data import create_new_user, create_new_category, create_new_record, create_new_currency
from .valid_and_search import is_valid_uuid, search_data_in_db, if_currency_in_db
from .DB.connection import conn


def init_routes(app):
    @app.route('/user/<string:user_id>', methods=['GET', 'DELETE', 'PATCH'])
    def get_delete_or_patch_user(user_id):
        if not is_valid_uuid(user_id):
            return jsonify({'error': 'Invalid user_id format. Expected UUID.'}), 400

        with conn.cursor() as cur:
            found_user = search_data_in_db(cur, user_id, "User")
        if found_user is False:
            return jsonify({'Not found': 'User not found!'}), 404

        if request.method == 'GET':
            with conn.cursor() as cur:
                user_data = get_user_from_db(cur, user_id)
            return jsonify(user_data), 200

        elif request.method == 'DELETE':
            with conn.cursor() as cur:
                del_us = delete_data_from_db(cur, user_id, "User")
            return jsonify(del_us), 200

        elif request.method == 'PATCH':
            data = request.get_json()
            new_name = data.get('name')
            new_currency = data.get('new default currency')
            with conn.cursor() as cur:
                patch_us, status_code = patch_user_in_db(cur, user_id, new_name, new_currency)
            return jsonify(patch_us), status_code

    @app.post('/user')
    def create_user():
        user_data = request.get_json()
        request_user_name = user_data.get('name')
        request_currency_name = user_data.get('currency name')

        if request_user_name is not None:
            with conn.cursor() as cur:
                post_user, status_code = create_new_user(cur, request_user_name, request_currency_name)
            return jsonify(post_user), status_code
        else:
            return jsonify({'error': 'Missing values!'}), 400

    @app.get('/users')
    def get_users():
        with conn.cursor() as cur:
            users_data = get_users_from_db(cur)
        return jsonify(users_data), 200

    @app.get('/category')
    def get_category():
        with conn.cursor() as cur:
            categories_data = get_all_categories(cur)
        return jsonify(categories_data), 200

    @app.post('/category')
    def new_category():
        category_data = request.get_json()
        request_category_name = category_data.get('name')
        request_category_description = category_data.get('description')

        if request_category_name and request_category_description is not None:
            with conn.cursor() as cur:
                add_new_category, status_code = create_new_category(cur, request_category_name,
                                                                    request_category_description)
            return jsonify(add_new_category), status_code
        else:
            return jsonify({'error': 'Missing values!'}), 400

    @app.delete('/category')
    def delete_category():
        category_data = request.get_json()
        request_category_id = category_data.get('id')

        if request_category_id is None:
            return jsonify({'error': 'Missing category identifier id!'}), 400

        if not is_valid_uuid(request_category_id):
            return jsonify({'error': 'Invalid category_id format. Expected UUID.'}), 400

        with conn.cursor() as cur:
            found_category = search_data_in_db(cur, request_category_id, "Category")
        if found_category is False:
            return jsonify({'Not found': 'Category not found!'}), 404

        with conn.cursor() as cur:
            delete_category_ = delete_data_from_db(cur, request_category_id, "Category")
        return jsonify(delete_category_), 200

    @app.get('/record/<string:record_id>')
    def get_record(record_id):
        if not is_valid_uuid(record_id):
            return jsonify({'error': 'Invalid record_id format. Expected UUID.'}), 400

        with conn.cursor() as cur:
            found_record = search_data_in_db(cur, record_id, 'Record')
        if found_record is False:
            return jsonify({'Not found': 'Records not found!'}), 404

        with conn.cursor() as cur:
            get_record_data = get_record_by_id(cur, record_id)
        return jsonify(get_record_data), 200

    @app.get('/record')
    def ger_records():
        user_id = request.args.get('user id')
        category_id = request.args.get('category id')

        if user_id is None and category_id is None:
            return jsonify({'error': 'Missing query parameters: user id or category id!'}), 400

        if user_id and not is_valid_uuid(user_id):
            return jsonify({'error': 'Invalid user_id format. Expected UUID.'}), 400

        if category_id and not is_valid_uuid(category_id):
            return jsonify({'error': 'Invalid category_id format. Expected UUID.'}), 400

        if user_id and not category_id:
            with conn.cursor() as cur:
                found_record = search_data_in_db(cur, user_id, 'Record', "user_id")
                if not found_record:
                    return jsonify({'Not found': 'Records not found!'}), 404
            with conn.cursor() as cur:
                get_record_data = get_record_by_id(cur, user_id, "user_id")
            return jsonify(get_record_data), 200

        elif category_id and not user_id:
            with conn.cursor() as cur:
                found_record = search_data_in_db(cur, category_id, 'Record', "category_id")
                if not found_record:
                    return jsonify({'Not found': 'Records not found!'}), 404
            with conn.cursor() as cur:
                get_record_data = get_record_by_id(cur, category_id, "category_id")
            return jsonify(get_record_data), 200

        elif category_id and user_id:
            with conn.cursor() as cur:
                found_record = search_data_in_db(cur, category_id, 'Record', "category_id", "user_id", user_id)
                if not found_record:
                    return jsonify({'Not found': 'Records not found!'}), 404
            with conn.cursor() as cur:
                get_record_data = get_record_by_id(cur, user_id, "user_id", category_id, "category_id")
            return jsonify(get_record_data), 200

    @app.post('/record')
    def create_record():
        record_data = request.get_json()
        request_record_user_id = record_data.get('user id')
        request_record_category_id = record_data.get('category id')
        request_record_currency_id = record_data.get('currency id')
        request_record_amount_of_expenses = record_data.get('amount of expenses')

        if not is_valid_uuid(request_record_user_id) or not is_valid_uuid(request_record_category_id) \
                or not is_valid_uuid(request_record_currency_id):
            return jsonify({'error': 'Invalid id format. Expected UUID.'}), 400

        if request_record_category_id and request_record_user_id and request_record_amount_of_expenses \
                and request_record_currency_id:
            with conn.cursor() as cur:
                add_new_record, status_code = create_new_record(cur, request_record_user_id, request_record_category_id,
                                                                request_record_amount_of_expenses,
                                                                request_record_currency_id)
            return jsonify(add_new_record), status_code
        else:
            return jsonify({'error': 'Missing values!'}), 400

    @app.delete('/record/<string:record_id>')
    def delete_record(record_id):
        if not is_valid_uuid(record_id):
            return jsonify({'error': 'Invalid record id format. Expected UUID.'}), 400

        with conn.cursor() as cur:
            found_record = search_data_in_db(cur, record_id, "Record")
        if found_record is False:
            return jsonify({'Not found': 'Record not found!'}), 404

        with conn.cursor() as cur:
            delete_record_ = delete_data_from_db(cur, record_id, "Record")
        return jsonify(delete_record_), 200

    @app.get('/allCurrency')
    def get_currency():
        with conn.cursor() as cur:
            get_all_currency = get_currency_from_db(cur)
        return jsonify(get_all_currency), 200

    @app.post('/createCurrency')
    def create_currency():
        data = request.get_json()
        request_currency = data.get('currency name')

        if request_currency is None:
            return jsonify({'error': 'Missing values!'}), 400

        with conn.cursor() as cur:
            found_currency = if_currency_in_db(cur, request_currency)
        if found_currency:
            return jsonify({'error': f'The currency {request_currency} has already been created with id = '
                                     f'{found_currency[0]}'}), 400
        else:
            with conn.cursor() as cur:
                new_currency, status_code = create_new_currency(cur, request_currency)
            return jsonify(new_currency), status_code
