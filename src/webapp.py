from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from db_management import MongoCRUD
from clip_user import ClipUser
from clip_object import ClipObject
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

db = MongoCRUD()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = db.get_user(username, password)
    if user:
        return jsonify({
            'success': True,
            'user_id': user.get_id(),
            'username': user.get_username()
        })
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@app.route('/api/register', methods=['POST'])
def register():
    """Register new user endpoint"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    try:
        user = ClipUser(username, password, email)
        db.insert_user(user)
        return jsonify({
            'success': True,
            'user_id': user.get_id(),
            'username': user.get_username()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400


@app.route('/api/clipboard', methods=['POST'])
def add_clipboard():
    """Add a new clipboard entry (text or image)"""
    data = request.json
    user_id = data.get('user_id')
    content = data.get('content')
    content_type = data.get('content_type', 'text')
    image_data = data.get('image_data')

    if not user_id or not content:
        return jsonify({
            'success': False,
            'message': 'Missing user_id or content'
        }), 400

    try:
        # Create ClipObject with type and image data
        clip_obj = ClipObject(
            content=content,
            content_type=content_type,
            image_data=image_data
        )
        db.insert_transaction(user_id, clip_obj)

        # Notify all connected clients for this user
        socketio.emit('clipboard_update', {
            'user_id': user_id,
            'content': content,
            'content_type': content_type,
            'image_data': image_data,
            'timestamp': datetime.now().isoformat()
        }, room=str(user_id))

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/clipboard/<int:user_id>', methods=['GET'])
def get_clipboard_history(user_id):
    """Get clipboard history for a user"""
    limit = request.args.get('limit', 50, type=int)

    try:
        transactions = db.get_n_last_user_transaction(user_id, limit)
        result = []
        for trans in transactions:
            result.append({
                'content': trans.get('content'),
                'content_type': trans.get('content_type', 'text'),
                'image_data': trans.get('image_data'),
                'timestamp': trans.get('timestamp')
            })
        return jsonify({'success': True, 'history': result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


@socketio.on('join')
def handle_join(data):
    """Join a room based on user_id for targeted updates"""
    user_id = data.get('user_id')
    if user_id:
        join_room(str(user_id))
        print(f'User {user_id} joined their room')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)