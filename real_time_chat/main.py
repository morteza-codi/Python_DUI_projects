from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import json
import os
import uuid
import hashlib
import time
import secrets
import base64
from functools import wraps
import logging
from collections import defaultdict, deque
import re
from threading import Lock
import bleach
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Generate secure secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Data storage with thread safety
data_lock = Lock()
users = {}
active_users = {}  # Currently online users
message_history = []  # Store message history
private_messages = {}  # Store private messages
rooms = {
    'general': {'name': 'عمومی', 'description': 'اتاق چت عمومی', 'created_by': 'system', 'created_at': datetime.now().isoformat()},
    'tech': {'name': 'فناوری', 'description': 'بحث درباره فناوری', 'created_by': 'system', 'created_at': datetime.now().isoformat()},
    'random': {'name': 'تصادفی', 'description': 'گفتگو آزاد', 'created_by': 'system', 'created_at': datetime.now().isoformat()}
}
user_preferences = {}  # Store user preferences
banned_users = set()  # Store banned users
user_sessions = {}  # Track user sessions
rate_limiter = defaultdict(lambda: deque())  # Rate limiting
file_shares = {}  # Store shared files
user_stats = defaultdict(lambda: {'message_count': 0, 'login_count': 0, 'days_active': 0, 'last_activity': None})
message_reactions = defaultdict(list)  # Store message reactions
blocked_users = defaultdict(set)  # Users blocked by other users
notifications = defaultdict(list)  # Store user notifications
session_tokens = {}  # Store session tokens for better security

# File to persist data
DATA_FILE = 'chat_data.json'

def load_data():
    global users, message_history, private_messages, rooms, user_preferences, user_stats, file_shares, message_reactions
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                users = data.get('users', {})
                message_history = data.get('message_history', [])
                private_messages = data.get('private_messages', {})
                rooms = data.get('rooms', {
                    'general': {'name': 'عمومی', 'description': 'اتاق چت عمومی', 'created_by': 'system', 'created_at': datetime.now().isoformat()}
                })
                user_preferences = data.get('user_preferences', {})
                user_stats.update(data.get('user_stats', {}))
                file_shares = data.get('file_shares', {})
                message_reactions.update(data.get('message_reactions', {}))
                
                # Initialize missing user stats
                for username in users:
                    if username not in user_stats:
                        user_stats[username] = {'message_count': 0, 'login_count': 0, 'days_active': 0, 'last_activity': None}
                        
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            print(f"Error loading data: {e}")

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'users': users,
                'message_history': message_history,
                'private_messages': private_messages,
                'rooms': rooms,
                'user_preferences': user_preferences,
                'user_stats': dict(user_stats),
                'file_shares': file_shares,
                'message_reactions': dict(message_reactions)
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        print(f"Error saving data: {e}")

# Security and utility functions
def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        username = session['username']
        if not users.get(username, {}).get('is_admin', False):
            flash('دسترسی غیر مجاز!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def check_rate_limit(username, action='message', limit=10, window=60):
    """Rate limiting to prevent spam"""
    now = time.time()
    key = f"{username}_{action}"
    
    # Clean old entries
    while rate_limiter[key] and rate_limiter[key][0] < now - window:
        rate_limiter[key].popleft()
    
    # Check limit
    if len(rate_limiter[key]) >= limit:
        return False
    
    # Add current request
    rate_limiter[key].append(now)
    return True

def encrypt_message(message, key=None):
    """Simple message encryption for sensitive data"""
    if not key:
        key = app.config['SECRET_KEY'][:32]
    return base64.b64encode(message.encode()).decode()

def decrypt_message(encrypted_message, key=None):
    """Simple message decryption"""
    if not key:
        key = app.config['SECRET_KEY'][:32]
    try:
        return base64.b64decode(encrypted_message.encode()).decode()
    except:
        return encrypted_message

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'mp3', 'mp4', 'zip'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_message(message):
    """Sanitize user message to prevent XSS attacks"""
    # Allow basic HTML tags but sanitize dangerous content
    allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'br', 'p']
    allowed_attributes = {}
    
    clean_message = bleach.clean(message, tags=allowed_tags, attributes=allowed_attributes, strip=True)
    return clean_message.strip()

def validate_username(username):
    """Enhanced username validation"""
    if not username or len(username) < 3 or len(username) > 20:
        return False, 'نام کاربری باید بین 3 تا 20 کاراکتر باشد.'
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, 'نام کاربری فقط می‌تواند شامل حروف، اعداد و خط زیر باشد.'
    
    # Check for reserved usernames
    reserved = ['admin', 'system', 'bot', 'moderator', 'support', 'help']
    if username.lower() in reserved:
        return False, 'این نام کاربری رزرو شده است.'
    
    return True, ''

def validate_password(password):
    """Enhanced password validation"""
    if len(password) < 6:
        return False, 'رمز عبور باید حداقل 6 کاراکتر باشد.'
    
    if len(password) > 100:
        return False, 'رمز عبور خیلی طولانی است.'
    
    # Check for at least one letter and one number
    if not re.search(r'[a-zA-Z]', password) or not re.search(r'\d', password):
        return False, 'رمز عبور باید حداقل شامل یک حرف و یک عدد باشد.'
    
    return True, ''

def generate_secure_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def is_valid_email(email):
    """Basic email validation"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def check_file_security(file_path):
    """Additional file security checks"""
    try:
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > 16 * 1024 * 1024:  # 16MB
            return False, 'File too large'
        
        # Basic file type validation
        with open(file_path, 'rb') as f:
            header = f.read(8)
            
        # Check for common malicious file signatures
        malicious_signatures = [
            b'\x4D\x5A',  # PE executable
            b'\x7F\x45\x4C\x46',  # ELF executable
        ]
        
        for sig in malicious_signatures:
            if header.startswith(sig):
                return False, 'File type not allowed'
        
        return True, ''
    except Exception as e:
        logger.error(f"File security check error: {e}")
        return False, 'File validation error'

def log_security_event(event_type, username, details):
    """Log security-related events"""
    logger.warning(f"SECURITY EVENT - {event_type}: User {username} - {details}")

def cleanup_old_sessions():
    """Clean up old inactive sessions"""
    current_time = datetime.now()
    expired_sessions = []
    
    for username, session_data in user_sessions.items():
        if isinstance(session_data, dict) and 'last_activity' in session_data:
            last_activity = datetime.fromisoformat(session_data['last_activity'])
            if current_time - last_activity > timedelta(hours=24):
                expired_sessions.append(username)
        elif username not in active_users:
            expired_sessions.append(username)
    
    for username in expired_sessions:
        if username in user_sessions:
            del user_sessions[username]
    
    return len(expired_sessions)

# Load data on startup
load_data()


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form.get('email', '').strip()
        
        # Enhanced validation
        error = None
        if len(username) < 3:
            error = 'نام کاربری باید حداقل 3 کاراکتر باشد.'
        elif len(username) > 20:
            error = 'نام کاربری نمی‌تواند بیش از 20 کاراکتر باشد.'
        elif not username.isalnum():
            error = 'نام کاربری فقط می‌تواند شامل حروف و اعداد باشد.'
        elif len(password) < 6:
            error = 'رمز عبور باید حداقل 6 کاراکتر باشد.'
        elif username in users:
            error = 'یوزر نیم از قبل وجود دارد.'
        elif not password == confirm_password:
            error = 'پسورد دوم مطابق با پسورد اول نیست'
        elif email and '@' not in email:
            error = 'ایمیل معتبر وارد کنید.'
        
        if not error:
            users[username] = {
                'username': username,
                'password': generate_password_hash(password),
                'email': email,
                'join_date': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat(),
                'is_admin': len(users) == 0,  # First user is admin
                'avatar': '',
                'status': 'آنلاین',
                'bio': '',
                'created_rooms': [],
                'blocked_users': []
            }
            user_preferences[username] = {
                'theme': 'light',
                'notifications': True,
                'sound': True,
                'show_online': True,
                'allow_private': True
            }
            user_stats[username] = {
                'message_count': 0,
                'login_count': 0,
                'days_active': 0,
                'last_activity': None
            }
            save_data()
            flash('ثبت نام با موفقیت انجام شد!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', error=error)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        # Check if user is banned
        if username in banned_users:
            error = 'حساب کاربری شما مسدود شده است!'
            return render_template('login.html', error=error)
        
        # Rate limiting for login attempts
        if not check_rate_limit(f"login_{request.remote_addr}", action='login', limit=5, window=300):
            error = 'تعداد تلاش‌های ورود زیاد است. لطفاً بعداً تلاش کنید.'
            return render_template('login.html', error=error)
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            session['session_id'] = str(uuid.uuid4())
            user_sessions[username] = session['session_id']
            
            # Update login stats
            user_stats[username]['login_count'] += 1
            user_stats[username]['last_activity'] = datetime.now().isoformat()
            users[username]['last_seen'] = datetime.now().isoformat()
            
            save_data()
            logger.info(f"User {username} logged in successfully")
            flash('با موفقیت وارد شدید!', 'success')
            return redirect(url_for('index'))
        
        error = 'پسورد یا نام کاربری اشتباه است!'
        logger.warning(f"Failed login attempt for username: {username}")
        return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    username = session.get('username')
    if username and username in active_users:
        del active_users[username]
        socketio.emit('user_left', {'username': username}, broadcast=True)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/profile')
@require_login
def profile():
    username = session['username']
    user_data = users.get(username, {})
    preferences = user_preferences.get(username, {})
    stats = user_stats.get(username, {})
    
    # Add stats to user data
    user_data.update(stats)
    
    return render_template('profile.html', user=user_data, preferences=preferences)

@app.route('/update_profile', methods=['POST'])
@require_login
def update_profile():
    username = session['username']
    email = request.form.get('email', '').strip()
    status = request.form.get('status', '').strip()
    bio = request.form.get('bio', '').strip()
    theme = request.form.get('theme', 'light')
    notifications = 'notifications' in request.form
    sound = 'sound' in request.form
    show_online = 'show_online' in request.form
    allow_private = 'allow_private' in request.form
    
    # Validate inputs
    if email and '@' not in email:
        flash('ایمیل معتبر وارد کنید.', 'error')
        return redirect(url_for('profile'))
    
    if len(status) > 100:
        flash('وضعیت نمی‌تواند بیش از 100 کاراکتر باشد.', 'error')
        return redirect(url_for('profile'))
    
    if len(bio) > 500:
        flash('بیوگرافی نمی‌تواند بیش از 500 کاراکتر باشد.', 'error')
        return redirect(url_for('profile'))
    
    if username in users:
        users[username]['email'] = email
        users[username]['status'] = status
        users[username]['bio'] = bio
        
    user_preferences[username] = {
        'theme': theme,
        'notifications': notifications,
        'sound': sound,
        'show_online': show_online,
        'allow_private': allow_private
    }
    
    save_data()
    flash('پروفایل با موفقیت بروزرسانی شد!', 'success')
    return redirect(url_for('profile'))

@app.route('/admin')
@require_admin
def admin_panel():
    return render_template('admin.html', 
                         users=users, 
                         active_users=active_users,
                         message_count=len(message_history),
                         rooms=rooms,
                         user_stats=dict(user_stats))

@app.route('/api/users')
def api_users():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'active_users': list(active_users.keys()),
        'total_users': len(users)
    })

@app.route('/api/rooms')
def api_rooms():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify(rooms)

@app.route('/api/history')
def api_history():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Return last 50 messages
    return jsonify(message_history[-50:])

# New API endpoints
@app.route('/api/ban_user', methods=['POST'])
@require_admin
def ban_user_api():
    data = request.get_json()
    username_to_ban = data.get('username')
    
    if username_to_ban and username_to_ban in users:
        banned_users.add(username_to_ban)
        # Disconnect banned user if online
        if username_to_ban in active_users:
            del active_users[username_to_ban]
            socketio.emit('user_banned', {'username': username_to_ban}, broadcast=True)
        
        save_data()
        logger.info(f"User {username_to_ban} banned by {session['username']}")
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'User not found'})

@app.route('/api/unban_user', methods=['POST'])
@require_admin
def unban_user_api():
    data = request.get_json()
    username_to_unban = data.get('username')
    
    if username_to_unban and username_to_unban in banned_users:
        banned_users.remove(username_to_unban)
        save_data()
        logger.info(f"User {username_to_unban} unbanned by {session['username']}")
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'User not in ban list'})

@app.route('/api/toggle_admin', methods=['POST'])
@require_admin
def toggle_admin_api():
    data = request.get_json()
    username_to_toggle = data.get('username')
    
    if username_to_toggle and username_to_toggle in users:
        # Don't allow removing admin from the first user
        if users[username_to_toggle].get('is_admin') and len([u for u in users.values() if u.get('is_admin')]) == 1:
            return jsonify({'success': False, 'error': 'Cannot remove last admin'})
        
        users[username_to_toggle]['is_admin'] = not users[username_to_toggle].get('is_admin', False)
        save_data()
        logger.info(f"Admin status toggled for {username_to_toggle} by {session['username']}")
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'User not found'})

@app.route('/api/create_room', methods=['POST'])
@require_login
def create_room_api():
    data = request.get_json()
    room_name = data.get('name', '').strip()
    room_description = data.get('description', '').strip()
    
    if not room_name or len(room_name) < 2:
        return jsonify({'success': False, 'error': 'Room name too short'})
    
    if len(room_name) > 50:
        return jsonify({'success': False, 'error': 'Room name too long'})
    
    room_id = room_name.lower().replace(' ', '_')
    
    if room_id in rooms:
        return jsonify({'success': False, 'error': 'Room already exists'})
    
    username = session['username']
    rooms[room_id] = {
        'name': room_name,
        'description': room_description,
        'created_by': username,
        'created_at': datetime.now().isoformat(),
        'members': [username]
    }
    
    # Add to user's created rooms
    if 'created_rooms' not in users[username]:
        users[username]['created_rooms'] = []
    users[username]['created_rooms'].append(room_id)
    
    save_data()
    logger.info(f"Room {room_name} created by {username}")
    
    # Notify all users about new room
    socketio.emit('new_room', {
        'room_id': room_id,
        'room_data': rooms[room_id]
    }, broadcast=True)
    
    return jsonify({'success': True, 'room_id': room_id})

@app.route('/api/upload_file', methods=['POST'])
@require_login
def upload_file_api():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if file and allowed_file(file.filename):
        # Check rate limit for file uploads
        username = session['username']
        if not check_rate_limit(username, action='upload', limit=5, window=300):
            return jsonify({'success': False, 'error': 'Upload rate limit exceeded'})
        
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(file_path)
            
            # Store file info
            file_id = str(uuid.uuid4())
            file_shares[file_id] = {
                'filename': filename,
                'original_name': file.filename,
                'uploaded_by': username,
                'upload_time': datetime.now().isoformat(),
                'file_size': os.path.getsize(file_path),
                'downloads': 0
            }
            
            save_data()
            logger.info(f"File {filename} uploaded by {username}")
            
            return jsonify({
                'success': True,
                'file_id': file_id,
                'filename': file.filename,
                'file_size': file_shares[file_id]['file_size']
            })
            
        except Exception as e:
            logger.error(f"File upload error: {e}")
            return jsonify({'success': False, 'error': 'File upload failed'})
    
    return jsonify({'success': False, 'error': 'File type not allowed'})

@app.route('/api/download_file/<file_id>')
@require_login
def download_file_api(file_id):
    if file_id not in file_shares:
        return jsonify({'error': 'File not found'}), 404
    
    file_info = file_shares[file_id]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_info['filename'])
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found on disk'}), 404
    
    # Update download count
    file_shares[file_id]['downloads'] += 1
    save_data()
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_info['filename'],
                               as_attachment=True, download_name=file_info['original_name'])

@app.route('/api/search_messages')
@require_login
def search_messages_api():
    query = request.args.get('q', '').strip().lower()
    if not query or len(query) < 2:
        return jsonify({'results': []})
    
    # Search in message history
    results = []
    for msg in message_history[-200:]:  # Search last 200 messages
        if query in msg.get('message', '').lower():
            results.append(msg)
    
    return jsonify({'results': results[-20:]})

@app.route('/api/react_to_message', methods=['POST'])
@require_login
def react_to_message_api():
    data = request.get_json()
    message_id = data.get('message_id')
    reaction = data.get('reaction')
    username = session['username']
    
    if not message_id or not reaction:
        return jsonify({'success': False, 'error': 'Missing data'})
    
    # Add or remove reaction
    if message_id not in message_reactions:
        message_reactions[message_id] = []
    
    # Check if user already reacted with this emoji
    existing_reaction = None
    for r in message_reactions[message_id]:
        if r['username'] == username and r['reaction'] == reaction:
            existing_reaction = r
            break
    
    if existing_reaction:
        # Remove reaction
        message_reactions[message_id].remove(existing_reaction)
        action = 'removed'
    else:
        # Add reaction
        message_reactions[message_id].append({
            'username': username,
            'reaction': reaction,
            'timestamp': datetime.now().isoformat()
        })
        action = 'added'
    
    save_data()
    
    # Notify all users about the reaction
    socketio.emit('message_reaction', {
        'message_id': message_id,
        'username': username,
        'reaction': reaction,
        'action': action,
        'total_reactions': len(message_reactions[message_id])
    }, broadcast=True)
    
    return jsonify({'success': True, 'action': action})

@app.route('/api/block_user', methods=['POST'])
@require_login
def block_user_api():
    data = request.get_json()
    user_to_block = data.get('username')
    username = session['username']
    
    if not user_to_block or user_to_block == username:
        return jsonify({'success': False, 'error': 'Invalid user'})
    
    if user_to_block not in users:
        return jsonify({'success': False, 'error': 'User not found'})
    
    blocked_users[username].add(user_to_block)
    save_data()
    
    return jsonify({'success': True})

@app.route('/api/unblock_user', methods=['POST'])
@require_login
def unblock_user_api():
    data = request.get_json()
    user_to_unblock = data.get('username')
    username = session['username']
    
    if user_to_unblock in blocked_users[username]:
        blocked_users[username].remove(user_to_unblock)
        save_data()
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'User not blocked'})

@app.route('/api/user_stats/<username>')
@require_login
def get_user_stats_api(username):
    if username not in users:
        return jsonify({'error': 'User not found'}), 404
    
    stats = user_stats.get(username, {})
    user_info = {
        'username': username,
        'join_date': users[username].get('join_date'),
        'last_seen': users[username].get('last_seen'),
        'is_admin': users[username].get('is_admin', False),
        'message_count': stats.get('message_count', 0),
        'login_count': stats.get('login_count', 0),
        'days_active': stats.get('days_active', 0)
    }
    
    return jsonify(user_info)


# Enhanced Socket.IO Events
@socketio.on('connect')
def on_connect():
    if 'username' in session:
        username = session['username']
        active_users[username] = {
            'username': username,
            'join_time': datetime.now().isoformat(),
            'room': 'general'
        }
        join_room('general')
        
        # Update user last seen
        if username in users:
            users[username]['last_seen'] = datetime.now().isoformat()
        
        emit('user_joined', {
            'username': username,
            'active_users': list(active_users.keys())
        }, broadcast=True)
        
        # Send recent messages to new user
        for msg in message_history[-20:]:
            emit('message', msg)

@socketio.on('disconnect')
def on_disconnect():
    if 'username' in session:
        username = session['username']
        if username in active_users:
            del active_users[username]
        leave_room('general')
        
        emit('user_left', {
            'username': username,
            'active_users': list(active_users.keys())
        }, broadcast=True)

@socketio.on('message')
def handle_message(data):
    if 'username' not in session:
        return
    
    username = session['username']
    message = data.get('message', '').strip()
    room = data.get('room', 'general')
    message_type = data.get('type', 'text')
    
    if not message:
        return
    
    # Check for banned users
    if username in banned_users:
        emit('error', {'message': 'شما ممنوع الارسال هستید!'})
        return
    
    # Rate limiting for messages
    if not check_rate_limit(username, action='message', limit=30, window=60):
        emit('error', {'message': 'پیام‌های زیاد! لطفاً کمی صبر کنید.'})
        return
    
    message_data = {
        'id': str(uuid.uuid4()),
        'username': username,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'room': room,
        'type': message_type,
        'reactions': [],
        'file_id': data.get('file_id') if message_type == 'file' else None
    }
    
    # Store message
    message_history.append(message_data)
    
    # Update user stats
    user_stats[username]['message_count'] += 1
    user_stats[username]['last_activity'] = datetime.now().isoformat()
    
    # Keep only last 1000 messages
    if len(message_history) > 1000:
        message_history.pop(0)
    
    save_data()
    
    emit('message', message_data, room=room)

@socketio.on('private_message')
def handle_private_message(data):
    if 'username' not in session:
        return
    
    sender = session['username']
    recipient = data.get('recipient')
    message = data.get('message', '').strip()
    
    if not message or not recipient or recipient not in users:
        return
    
    message_data = {
        'id': str(uuid.uuid4()),
        'sender': sender,
        'recipient': recipient,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'type': 'private'
    }
    
    # Store private message
    key = tuple(sorted([sender, recipient]))
    if key not in private_messages:
        private_messages[key] = []
    
    private_messages[key].append(message_data)
    save_data()
    
    # Send to both users if they're online
    if recipient in active_users:
        emit('private_message', message_data, room=request.sid)
        # Send to recipient's session
        for sid, user_data in active_users.items():
            if user_data.get('username') == recipient:
                emit('private_message', message_data, room=sid)

@socketio.on('join_room')
def handle_join_room(data):
    if 'username' not in session:
        return
    
    username = session['username']
    room = data.get('room', 'general')
    
    if room in rooms:
        join_room(room)
        if username in active_users:
            active_users[username]['room'] = room
        
        emit('room_joined', {
            'username': username,
            'room': room
        }, room=room)

@socketio.on('leave_room')
def handle_leave_room(data):
    if 'username' not in session:
        return
    
    username = session['username']
    room = data.get('room', 'general')
    
    leave_room(room)
    
    emit('room_left', {
        'username': username,
        'room': room
    }, room=room)

@socketio.on('typing')
def handle_typing(data):
    if 'username' not in session:
        return
    
    username = session['username']
    room = data.get('room', 'general')
    is_typing = data.get('typing', False)
    
    emit('user_typing', {
        'username': username,
        'typing': is_typing
    }, room=room, include_self=False)

@socketio.on('get_online_users')
def handle_get_online_users():
    emit('online_users', {
        'users': list(active_users.keys())
    })

# New Socket.IO events for enhanced features
@socketio.on('file_share')
def handle_file_share(data):
    if 'username' not in session:
        return
    
    username = session['username']
    file_id = data.get('file_id')
    room = data.get('room', 'general')
    
    if file_id and file_id in file_shares:
        file_info = file_shares[file_id]
        
        message_data = {
            'id': str(uuid.uuid4()),
            'username': username,
            'message': f"فایل به اشتراک گذاشته شد: {file_info['original_name']}",
            'timestamp': datetime.now().isoformat(),
            'room': room,
            'type': 'file',
            'file_id': file_id,
            'file_name': file_info['original_name'],
            'file_size': file_info['file_size']
        }
        
        message_history.append(message_data)
        save_data()
        
        emit('message', message_data, room=room)

@socketio.on('voice_call_request')
def handle_voice_call_request(data):
    if 'username' not in session:
        return
    
    username = session['username']
    target_user = data.get('target_user')
    
    if target_user and target_user in active_users:
        emit('voice_call_request', {
            'caller': username,
            'call_id': str(uuid.uuid4())
        }, room=active_users[target_user].get('session_id'))

@socketio.on('voice_call_response')
def handle_voice_call_response(data):
    if 'username' not in session:
        return
    
    username = session['username']
    caller = data.get('caller')
    accepted = data.get('accepted', False)
    call_id = data.get('call_id')
    
    if caller and caller in active_users:
        emit('voice_call_response', {
            'responder': username,
            'accepted': accepted,
            'call_id': call_id
        }, room=active_users[caller].get('session_id'))

@socketio.on('video_call_request')
def handle_video_call_request(data):
    if 'username' not in session:
        return
    
    username = session['username']
    target_user = data.get('target_user')
    
    if target_user and target_user in active_users:
        emit('video_call_request', {
            'caller': username,
            'call_id': str(uuid.uuid4())
        }, room=active_users[target_user].get('session_id'))

@socketio.on('screen_share_start')
def handle_screen_share_start(data):
    if 'username' not in session:
        return
    
    username = session['username']
    room = data.get('room', 'general')
    
    emit('screen_share_started', {
        'username': username,
        'room': room
    }, room=room, include_self=False)

@socketio.on('screen_share_stop')
def handle_screen_share_stop(data):
    if 'username' not in session:
        return
    
    username = session['username']
    room = data.get('room', 'general')
    
    emit('screen_share_stopped', {
        'username': username,
        'room': room
    }, room=room, include_self=False)

@socketio.on('user_status_change')
def handle_user_status_change(data):
    if 'username' not in session:
        return
    
    username = session['username']
    status = data.get('status', 'آنلاین')
    
    if username in users:
        users[username]['status'] = status
        save_data()
        
        emit('user_status_updated', {
            'username': username,
            'status': status
        }, broadcast=True)

@socketio.on('create_poll')
def handle_create_poll(data):
    if 'username' not in session:
        return
    
    username = session['username']
    question = data.get('question', '').strip()
    options = data.get('options', [])
    room = data.get('room', 'general')
    
    if not question or len(options) < 2:
        return
    
    poll_id = str(uuid.uuid4())
    poll_data = {
        'id': poll_id,
        'question': question,
        'options': {opt: [] for opt in options},
        'created_by': username,
        'created_at': datetime.now().isoformat(),
        'room': room,
        'active': True
    }
    
    # Store poll (you might want to add a polls storage)
    message_data = {
        'id': str(uuid.uuid4()),
        'username': username,
        'message': f"نظرسنجی ایجاد شد: {question}",
        'timestamp': datetime.now().isoformat(),
        'room': room,
        'type': 'poll',
        'poll_data': poll_data
    }
    
    message_history.append(message_data)
    save_data()
    
    emit('message', message_data, room=room)

@socketio.on('vote_poll')
def handle_vote_poll(data):
    if 'username' not in session:
        return
    
    username = session['username']
    poll_id = data.get('poll_id')
    option = data.get('option')
    
    # Find poll in message history and update votes
    for msg in reversed(message_history):
        if msg.get('type') == 'poll' and msg.get('poll_data', {}).get('id') == poll_id:
            poll_data = msg['poll_data']
            
            # Remove previous vote if exists
            for opt, voters in poll_data['options'].items():
                if username in voters:
                    voters.remove(username)
            
            # Add new vote
            if option in poll_data['options']:
                poll_data['options'][option].append(username)
                
            save_data()
            
            emit('poll_updated', {
                'poll_id': poll_id,
                'options': poll_data['options']
            }, room=poll_data['room'])
            break

@socketio.on('request_user_info')
def handle_request_user_info(data):
    if 'username' not in session:
        return
    
    requested_user = data.get('username')
    
    if requested_user and requested_user in users:
        user_data = users[requested_user]
        stats = user_stats.get(requested_user, {})
        
        # Don't send sensitive information
        safe_user_data = {
            'username': user_data['username'],
            'status': user_data.get('status', 'آنلاین'),
            'join_date': user_data.get('join_date'),
            'bio': user_data.get('bio', ''),
            'is_admin': user_data.get('is_admin', False),
            'message_count': stats.get('message_count', 0),
            'is_online': requested_user in active_users
        }
        
        emit('user_info_response', safe_user_data)

@socketio.on('mark_messages_read')
def handle_mark_messages_read(data):
    if 'username' not in session:
        return
    
    username = session['username']
    room = data.get('room', 'general')
    
    # Update user's last read timestamp for the room
    # This could be expanded to track read receipts
    if username in users:
        if 'last_read' not in users[username]:
            users[username]['last_read'] = {}
        users[username]['last_read'][room] = datetime.now().isoformat()
        save_data()


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal server error: {e}")
    return render_template('500.html'), 500

@app.errorhandler(413)
def file_too_large(e):
    flash('فایل انتخابی خیلی بزرگ است!', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Use environment variables for production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting chat application on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
