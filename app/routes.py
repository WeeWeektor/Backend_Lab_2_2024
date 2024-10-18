from flask import jsonify, request
from app.data import user, category
from app.services import get_user_by_id


def init_routes(app):
    @app.route('/user/<string:user_id>', methods=['GET', 'DELETE', 'PATCH'])
    def get_delete_or_patch_user(user_id):
        found_user = get_user_by_id(user_id)
        if found_user is None:
            return jsonify({'error': 'User not found!'}), 404

        if request.method == 'GET':
            return jsonify(found_user), 200
        elif request.method == 'DELETE':
            user.users.remove(found_user)
            return jsonify({'message': f'User {user_id} deleted successfully!'}), 200
        elif request.method == 'PATCH':
            data = request.get_json()
            new_name = data.get('name')
            if new_name is not None:
                found_user['name'] = new_name
                return jsonify({'message': f'User {user_id} updated successfully', 'user': found_user}), 200
            else:
                return jsonify({'error': 'No name provided!'}), 400

    @app.post('/user')
    def create_user():
        user_data = request.get_json()
        request_user_name = user_data.get('name')

        if request_user_name is not None:
            user.new_user(request_user_name)
            return jsonify({'message': f"New user {request_user_name} created!"}), 201
        else:
            return jsonify({'error': 'Missing values!'}), 400

    @app.get('/users')
    def get_users():
        return user.users

    @app.get('/category')
    def get_category():
        return category.categories

    @app.post('/category')
    def new_category():
        category_data = request.get_json()
        request_category_name = category_data.get('name')
        request_category_description = category_data.get('description')

        if request_category_name and request_category_description is not None:
            category.new_categories(request_category_name, request_category_description)
            return jsonify({'message': f'New category {request_category_name} created!'}), 201
        else:
            return jsonify({'error': 'Missing values!'}), 400

    @app.delete('/category')
    def delete_category():
        category_data = request.get_json()
        request_category_name = category_data.get('name')
        request_category_id = category_data.get('id')

        if not request_category_name and request_category_id is None:
            return jsonify({'error': 'Missing category identifier (name or id)!'}), 400

        found_category = next((c for c in category.categories if c['id'] == request_category_id), None)
        if not found_category:
            found_category = next((c for c in category.categories if c['name'] == request_category_name), None)
        if not found_category:
            return jsonify({'error': 'Category not found!'}), 404

        category.categories.remove(found_category)
        return jsonify(
            {'message': f'Category {found_category["name"]}(id={found_category["id"]}) deleted successfully!'}), 200
