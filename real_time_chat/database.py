#!/usr/bin/env python
"""
Database module for Real-Time Chat Application
Provides abstraction layer for data storage and retrieval
"""
import json
import os
import time
import logging
from datetime import datetime
from threading import Lock
from typing import Dict, List, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

class ChatDatabase:
    """Database abstraction layer for chat application"""
    
    def __init__(self, data_file: str = 'chat_data.json'):
        self.data_file = data_file
        self.data_lock = Lock()
        self._data = {
            'users': {},
            'message_history': [],
            'private_messages': {},
            'rooms': {},
            'user_preferences': {},
            'user_stats': defaultdict(lambda: {
                'message_count': 0,
                'login_count': 0,
                'days_active': 0,
                'last_activity': None
            }),
            'file_shares': {},
            'message_reactions': defaultdict(list),
            'banned_users': [],
            'notifications': defaultdict(list)
        }
        self.load_data()
    
    def load_data(self) -> bool:
        """Load data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                # Update data with loaded values
                for key, value in loaded_data.items():
                    if key in self._data:
                        if key in ['user_stats', 'message_reactions', 'notifications']:
                            # Handle defaultdict types
                            if key == 'user_stats':
                                self._data[key] = defaultdict(
                                    lambda: {'message_count': 0, 'login_count': 0, 'days_active': 0, 'last_activity': None},
                                    value
                                )
                            else:
                                self._data[key] = defaultdict(list, value)
                        else:
                            self._data[key] = value
                
                # Initialize default rooms if not present
                if not self._data['rooms']:
                    self._initialize_default_rooms()
                
                logger.info(f"Data loaded successfully from {self.data_file}")
                return True
        except Exception as e:
            logger.error(f"Error loading data from {self.data_file}: {e}")
            self._initialize_default_rooms()
            return False
    
    def save_data(self) -> bool:
        """Save data to JSON file with thread safety"""
        try:
            with self.data_lock:
                # Convert defaultdicts to regular dicts for JSON serialization
                data_to_save = {}
                for key, value in self._data.items():
                    if isinstance(value, defaultdict):
                        data_to_save[key] = dict(value)
                    else:
                        data_to_save[key] = value
                
                # Create backup before saving
                if os.path.exists(self.data_file):
                    backup_file = f"{self.data_file}.backup"
                    os.replace(self.data_file, backup_file)
                
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=2)
                
                logger.debug("Data saved successfully")
                return True
        except Exception as e:
            logger.error(f"Error saving data to {self.data_file}: {e}")
            return False
    
    def _initialize_default_rooms(self):
        """Initialize default chat rooms"""
        self._data['rooms'] = {
            'general': {
                'name': 'عمومی',
                'description': 'اتاق چت عمومی',
                'created_by': 'system',
                'created_at': datetime.now().isoformat(),
                'members': []
            },
            'tech': {
                'name': 'فناوری',
                'description': 'بحث درباره فناوری',
                'created_by': 'system',
                'created_at': datetime.now().isoformat(),
                'members': []
            },
            'random': {
                'name': 'تصادفی',
                'description': 'گفتگو آزاد',
                'created_by': 'system',
                'created_at': datetime.now().isoformat(),
                'members': []
            }
        }
    
    # User management methods
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        return self._data['users'].get(username)
    
    def create_user(self, username: str, user_data: Dict[str, Any]) -> bool:
        """Create a new user"""
        try:
            if username in self._data['users']:
                return False
            
            self._data['users'][username] = user_data
            
            # Initialize user preferences
            self._data['user_preferences'][username] = {
                'theme': 'light',
                'notifications': True,
                'sound': True,
                'show_online': True,
                'allow_private': True
            }
            
            # Initialize user stats
            self._data['user_stats'][username] = {
                'message_count': 0,
                'login_count': 0,
                'days_active': 0,
                'last_activity': None
            }
            
            return self.save_data()
        except Exception as e:
            logger.error(f"Error creating user {username}: {e}")
            return False
    
    def update_user(self, username: str, updates: Dict[str, Any]) -> bool:
        """Update user data"""
        try:
            if username not in self._data['users']:
                return False
            
            self._data['users'][username].update(updates)
            return self.save_data()
        except Exception as e:
            logger.error(f"Error updating user {username}: {e}")
            return False
    
    def get_all_users(self) -> Dict[str, Dict[str, Any]]:
        """Get all users"""
        return self._data['users'].copy()
    
    def is_user_banned(self, username: str) -> bool:
        """Check if user is banned"""
        return username in self._data['banned_users']
    
    def ban_user(self, username: str) -> bool:
        """Ban a user"""
        try:
            if username not in self._data['banned_users']:
                self._data['banned_users'].append(username)
                return self.save_data()
            return True
        except Exception as e:
            logger.error(f"Error banning user {username}: {e}")
            return False
    
    def unban_user(self, username: str) -> bool:
        """Unban a user"""
        try:
            if username in self._data['banned_users']:
                self._data['banned_users'].remove(username)
                return self.save_data()
            return True
        except Exception as e:
            logger.error(f"Error unbanning user {username}: {e}")
            return False
    
    # Message management methods
    def add_message(self, message_data: Dict[str, Any]) -> bool:
        """Add a message to history"""
        try:
            self._data['message_history'].append(message_data)
            
            # Keep only last 1000 messages
            if len(self._data['message_history']) > 1000:
                self._data['message_history'] = self._data['message_history'][-1000:]
            
            return self.save_data()
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            return False
    
    def get_recent_messages(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent messages"""
        return self._data['message_history'][-limit:]
    
    def search_messages(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search messages by content"""
        query_lower = query.lower()
        results = []
        
        for msg in reversed(self._data['message_history'][-200:]):
            if query_lower in msg.get('message', '').lower():
                results.append(msg)
                if len(results) >= limit:
                    break
        
        return results
    
    def add_private_message(self, sender: str, recipient: str, message_data: Dict[str, Any]) -> bool:
        """Add a private message"""
        try:
            key = tuple(sorted([sender, recipient]))
            if key not in self._data['private_messages']:
                self._data['private_messages'][key] = []
            
            self._data['private_messages'][key].append(message_data)
            return self.save_data()
        except Exception as e:
            logger.error(f"Error adding private message: {e}")
            return False
    
    def get_private_messages(self, user1: str, user2: str) -> List[Dict[str, Any]]:
        """Get private messages between two users"""
        key = tuple(sorted([user1, user2]))
        return self._data['private_messages'].get(key, [])
    
    # Room management methods
    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get room by ID"""
        return self._data['rooms'].get(room_id)
    
    def get_all_rooms(self) -> Dict[str, Dict[str, Any]]:
        """Get all rooms"""
        return self._data['rooms'].copy()
    
    def create_room(self, room_id: str, room_data: Dict[str, Any]) -> bool:
        """Create a new room"""
        try:
            if room_id in self._data['rooms']:
                return False
            
            self._data['rooms'][room_id] = room_data
            return self.save_data()
        except Exception as e:
            logger.error(f"Error creating room {room_id}: {e}")
            return False
    
    # File sharing methods
    def add_file_share(self, file_id: str, file_data: Dict[str, Any]) -> bool:
        """Add a shared file"""
        try:
            self._data['file_shares'][file_id] = file_data
            return self.save_data()
        except Exception as e:
            logger.error(f"Error adding file share {file_id}: {e}")
            return False
    
    def get_file_share(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get shared file data"""
        return self._data['file_shares'].get(file_id)
    
    def update_file_downloads(self, file_id: str) -> bool:
        """Increment download count for a file"""
        try:
            if file_id in self._data['file_shares']:
                self._data['file_shares'][file_id]['downloads'] = \
                    self._data['file_shares'][file_id].get('downloads', 0) + 1
                return self.save_data()
            return False
        except Exception as e:
            logger.error(f"Error updating file downloads {file_id}: {e}")
            return False
    
    # User preferences methods
    def get_user_preferences(self, username: str) -> Dict[str, Any]:
        """Get user preferences"""
        return self._data['user_preferences'].get(username, {})
    
    def update_user_preferences(self, username: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences"""
        try:
            self._data['user_preferences'][username] = preferences
            return self.save_data()
        except Exception as e:
            logger.error(f"Error updating preferences for {username}: {e}")
            return False
    
    # User statistics methods
    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get user statistics"""
        return dict(self._data['user_stats'][username])
    
    def update_user_stats(self, username: str, updates: Dict[str, Any]) -> bool:
        """Update user statistics"""
        try:
            self._data['user_stats'][username].update(updates)
            return self.save_data()
        except Exception as e:
            logger.error(f"Error updating stats for {username}: {e}")
            return False
    
    def increment_message_count(self, username: str) -> bool:
        """Increment user message count"""
        try:
            self._data['user_stats'][username]['message_count'] += 1
            self._data['user_stats'][username]['last_activity'] = datetime.now().isoformat()
            return True  # Don't save immediately for performance
        except Exception as e:
            logger.error(f"Error incrementing message count for {username}: {e}")
            return False
    
    # Message reactions methods
    def add_message_reaction(self, message_id: str, username: str, reaction: str) -> bool:
        """Add a reaction to a message"""
        try:
            reaction_data = {
                'username': username,
                'reaction': reaction,
                'timestamp': datetime.now().isoformat()
            }
            self._data['message_reactions'][message_id].append(reaction_data)
            return self.save_data()
        except Exception as e:
            logger.error(f"Error adding reaction to message {message_id}: {e}")
            return False
    
    def remove_message_reaction(self, message_id: str, username: str, reaction: str) -> bool:
        """Remove a reaction from a message"""
        try:
            reactions = self._data['message_reactions'][message_id]
            for r in reactions[:]:  # Create a copy to iterate safely
                if r['username'] == username and r['reaction'] == reaction:
                    reactions.remove(r)
                    return self.save_data()
            return False
        except Exception as e:
            logger.error(f"Error removing reaction from message {message_id}: {e}")
            return False
    
    def get_message_reactions(self, message_id: str) -> List[Dict[str, Any]]:
        """Get reactions for a message"""
        return self._data['message_reactions'][message_id].copy()
    
    # Utility methods
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            'total_users': len(self._data['users']),
            'total_messages': len(self._data['message_history']),
            'total_rooms': len(self._data['rooms']),
            'total_files': len(self._data['file_shares']),
            'banned_users': len(self._data['banned_users']),
            'private_message_threads': len(self._data['private_messages']),
            'last_backup': os.path.getmtime(f"{self.data_file}.backup") if os.path.exists(f"{self.data_file}.backup") else None
        }
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """Clean up old data (messages, reactions, etc.)"""
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        cleaned_count = 0
        
        try:
            # Clean old messages
            original_count = len(self._data['message_history'])
            self._data['message_history'] = [
                msg for msg in self._data['message_history']
                if datetime.fromisoformat(msg.get('timestamp', '1970-01-01')).timestamp() > cutoff_time
            ]
            cleaned_count += original_count - len(self._data['message_history'])
            
            # Clean orphaned reactions
            message_ids = {msg['id'] for msg in self._data['message_history']}
            orphaned_reactions = [
                msg_id for msg_id in self._data['message_reactions']
                if msg_id not in message_ids
            ]
            for msg_id in orphaned_reactions:
                del self._data['message_reactions'][msg_id]
            cleaned_count += len(orphaned_reactions)
            
            if cleaned_count > 0:
                self.save_data()
                logger.info(f"Cleaned up {cleaned_count} old data entries")
            
            return cleaned_count
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return 0
