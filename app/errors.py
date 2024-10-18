from flask import jsonify


def init_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'error': 'The requested URL was not found on the server.'}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'error': 'Method Not Allowed. The method is not allowed for the requested URL.'}), 405

    @app.errorhandler(415)
    def unsupported_mediatype(e):
        return jsonify({'error': 'Unsupported Media Type. Expected application/json'}), 415
