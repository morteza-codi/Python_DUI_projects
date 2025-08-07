#!/usr/bin/env python
"""
Basic tests for Real-Time Chat Application
"""
import unittest
import json
import tempfile
import os
from main import app, socketio
from database import ChatDatabase

class ChatApplicationTest(unittest.TestCase):
    """Test cases for chat application"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.app.config['DATA_FILE'] = self.temp_db.name
        
        self.client = self.app.test_client()
        self.socketio_client = socketio.test_client(self.app)
    
    def tearDown(self):
        """Clean up after tests"""
        os.unlink(self.temp_db.name)
    
    def test_index_redirect(self):
        """Test that index redirects to login when not authenticated"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_register_page(self):
        """Test register page loads"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'register', response.data.lower())
    
    def test_login_page(self):
        """Test login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())
    
    def test_user_registration(self):
        """Test user registration functionality"""
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'email': 'test@example.com'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Should redirect to login page
        self.assertIn(b'login', response.data.lower())
    
    def test_api_users_unauthorized(self):
        """Test API users endpoint requires authentication"""
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 401)
    
    def test_database_initialization(self):
        """Test database initialization"""
        db = ChatDatabase(':memory:')  # Use memory database for testing
        
        # Check that default rooms are created
        rooms = db.get_all_rooms()
        self.assertIn('general', rooms)
        self.assertIn('tech', rooms)
        self.assertIn('random', rooms)
        
        # Test user creation
        user_data = {
            'username': 'testuser',
            'password': 'hashed_password',
            'email': 'test@example.com',
            'join_date': '2024-01-01T00:00:00',
            'last_seen': '2024-01-01T00:00:00',
            'is_admin': False
        }
        
        success = db.create_user('testuser', user_data)
        self.assertTrue(success)
        
        # Test user retrieval
        retrieved_user = db.get_user('testuser')
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user['username'], 'testuser')
    
    def test_message_operations(self):
        """Test message operations"""
        db = ChatDatabase(':memory:')
        
        # Test message addition
        message_data = {
            'id': 'test-message-1',
            'username': 'testuser',
            'message': 'Hello, world!',
            'timestamp': '2024-01-01T00:00:00',
            'room': 'general',
            'type': 'text'
        }
        
        success = db.add_message(message_data)
        self.assertTrue(success)
        
        # Test message retrieval
        messages = db.get_recent_messages(10)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['message'], 'Hello, world!')
        
        # Test message search
        results = db.search_messages('Hello')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['message'], 'Hello, world!')
    
    def test_file_share_operations(self):
        """Test file sharing operations"""
        db = ChatDatabase(':memory:')
        
        file_data = {
            'filename': 'test_file.txt',
            'original_name': 'test_file.txt',
            'uploaded_by': 'testuser',
            'upload_time': '2024-01-01T00:00:00',
            'file_size': 1024,
            'downloads': 0
        }
        
        success = db.add_file_share('test-file-id', file_data)
        self.assertTrue(success)
        
        retrieved_file = db.get_file_share('test-file-id')
        self.assertIsNotNone(retrieved_file)
        self.assertEqual(retrieved_file['filename'], 'test_file.txt')
        
        # Test download count update
        success = db.update_file_downloads('test-file-id')
        self.assertTrue(success)
        
        updated_file = db.get_file_share('test-file-id')
        self.assertEqual(updated_file['downloads'], 1)
    
    def test_user_stats(self):
        """Test user statistics tracking"""
        db = ChatDatabase(':memory:')
        
        # Create user first
        user_data = {
            'username': 'testuser',
            'password': 'hashed_password'
        }
        db.create_user('testuser', user_data)
        
        # Test stats retrieval
        stats = db.get_user_stats('testuser')
        self.assertEqual(stats['message_count'], 0)
        self.assertEqual(stats['login_count'], 0)
        
        # Test stats update
        db.update_user_stats('testuser', {'login_count': 1})
        updated_stats = db.get_user_stats('testuser')
        self.assertEqual(updated_stats['login_count'], 1)
        
        # Test message count increment
        db.increment_message_count('testuser')
        final_stats = db.get_user_stats('testuser')
        self.assertEqual(final_stats['message_count'], 1)
    
    def test_room_operations(self):
        """Test room management operations"""
        db = ChatDatabase(':memory:')
        
        room_data = {
            'name': 'Test Room',
            'description': 'A test room',
            'created_by': 'testuser',
            'created_at': '2024-01-01T00:00:00',
            'members': ['testuser']
        }
        
        success = db.create_room('test_room', room_data)
        self.assertTrue(success)
        
        room = db.get_room('test_room')
        self.assertIsNotNone(room)
        self.assertEqual(room['name'], 'Test Room')
        
        # Test duplicate room creation
        duplicate_success = db.create_room('test_room', room_data)
        self.assertFalse(duplicate_success)
    
    def test_database_stats(self):
        """Test database statistics"""
        db = ChatDatabase(':memory:')
        
        stats = db.get_database_stats()
        self.assertIn('total_users', stats)
        self.assertIn('total_messages', stats)
        self.assertIn('total_rooms', stats)
        self.assertIn('total_files', stats)
        
        # Should have default rooms
        self.assertEqual(stats['total_rooms'], 3)

class SecurityTest(unittest.TestCase):
    """Test security features"""
    
    def test_password_validation(self):
        """Test password validation"""
        from main import validate_password
        
        # Test valid password
        is_valid, error = validate_password('TestPass123')
        self.assertTrue(is_valid)
        self.assertEqual(error, '')
        
        # Test short password
        is_valid, error = validate_password('12345')
        self.assertFalse(is_valid)
        self.assertIn('6', error)
        
        # Test password without numbers
        is_valid, error = validate_password('TestPassword')
        self.assertFalse(is_valid)
        self.assertIn('عدد', error)
        
        # Test password without letters
        is_valid, error = validate_password('123456789')
        self.assertFalse(is_valid)
        self.assertIn('حرف', error)
    
    def test_username_validation(self):
        """Test username validation"""
        from main import validate_username
        
        # Test valid username
        is_valid, error = validate_username('testuser123')
        self.assertTrue(is_valid)
        self.assertEqual(error, '')
        
        # Test short username
        is_valid, error = validate_username('ab')
        self.assertFalse(is_valid)
        self.assertIn('3', error)
        
        # Test long username
        is_valid, error = validate_username('a' * 25)
        self.assertFalse(is_valid)
        self.assertIn('20', error)
        
        # Test invalid characters
        is_valid, error = validate_username('test@user')
        self.assertFalse(is_valid)
        self.assertIn('حروف', error)
        
        # Test reserved username
        is_valid, error = validate_username('admin')
        self.assertFalse(is_valid)
        self.assertIn('رزرو', error)
    
    def test_message_sanitization(self):
        """Test message sanitization"""
        from main import sanitize_message
        
        # Test basic HTML sanitization
        clean_msg = sanitize_message('<script>alert("xss")</script>Hello')
        self.assertNotIn('<script>', clean_msg)
        self.assertIn('Hello', clean_msg)
        
        # Test allowed tags
        clean_msg = sanitize_message('<b>Bold text</b>')
        self.assertIn('<b>Bold text</b>', clean_msg)
    
    def test_email_validation(self):
        """Test email validation"""
        from main import is_valid_email
        
        # Test valid emails
        self.assertTrue(is_valid_email('test@example.com'))
        self.assertTrue(is_valid_email('user.name@domain.co.uk'))
        
        # Test invalid emails
        self.assertFalse(is_valid_email('invalid-email'))
        self.assertFalse(is_valid_email('@example.com'))
        self.assertFalse(is_valid_email('test@'))

if __name__ == '__main__':
    unittest.main()
