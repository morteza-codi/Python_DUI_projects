# Real-Time Chat Application (چت ریل تایم)

A modern, feature-rich real-time chat application built with Flask-SocketIO, featuring Persian/Farsi language support, file sharing, user management, and comprehensive admin panel.

## 🌟 Features

### Core Features
- **Real-time messaging** with Socket.IO
- **User authentication** (registration/login)
- **Persian/Farsi language support** with RTL design
- **Multiple chat rooms** support
- **Private messaging** between users
- **File sharing** with upload/download functionality
- **User profiles** with customizable settings
- **Admin panel** with comprehensive user management

### Advanced Features
- **Message reactions** (emoji reactions to messages)
- **Typing indicators** (shows when users are typing)
- **Online user tracking** (real-time user status)
- **Message search** functionality
- **User blocking/unblocking** system
- **Rate limiting** (prevents spam)
- **User statistics** tracking
- **Polls and voting** system
- **Theme customization** (light/dark/blue/green themes)
- **Sound notifications** and preferences

### Security Features
- **Password hashing** with Werkzeug
- **Rate limiting** for login attempts and messages
- **Session management** with secure tokens
- **File upload validation** and security
- **Admin role management**
- **User banning** system
- **Input validation** and XSS prevention

### Technical Features
- **Responsive design** (mobile-friendly)
- **Error handling** with custom 404/500 pages
- **Logging system** for debugging and monitoring
- **Data persistence** with JSON storage
- **Extensible architecture** for future enhancements

## 📋 Requirements

- Python 3.7+
- Flask 3.1.1
- Flask-SocketIO 5.5.1
- All dependencies listed in `requirements.txt`

## 🚀 Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd real_time_chat
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   
   **Windows:**
   ```bash
   .venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables (optional):**
   ```bash
   # Windows
   set SECRET_KEY=your-secret-key-here
   set DEBUG=False
   set PORT=5000
   
   # macOS/Linux
   export SECRET_KEY=your-secret-key-here
   export DEBUG=False
   export PORT=5000
   ```

6. **Run the application:**
   ```bash
   python main.py
   ```

7. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## 📝 Usage

### First Time Setup
1. Register the first user account (will automatically become admin)
2. Login with your credentials
3. Start chatting!

### User Features
- **Register/Login:** Create an account or login with existing credentials
- **Send Messages:** Type in the message box and press Enter or click Send
- **Change Rooms:** Use the room selector to switch between different chat rooms
- **Private Messages:** Click on a user to send private messages
- **Upload Files:** Use the file upload button to share documents, images, etc.
- **React to Messages:** Click on messages to add emoji reactions
- **Search Messages:** Use the search feature to find specific messages
- **Customize Profile:** Update your profile information and preferences

### Admin Features
- **User Management:** Ban/unban users, promote to admin
- **System Statistics:** View real-time statistics and user activity
- **Room Management:** Create and manage chat rooms
- **Message Monitoring:** Monitor chat activity and user behavior

## 🏗️ Project Structure

```
real_time_chat/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── chat_data.json         # Data storage (auto-generated)
├── templates/             # HTML templates
│   ├── index.html         # Main chat interface
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── profile.html       # User profile page
│   ├── admin.html         # Admin panel
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── uploads/              # File upload directory (auto-created)
└── .venv/                # Virtual environment
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Secret key for sessions (auto-generated if not set)
- `DEBUG`: Enable/disable debug mode (True/False)
- `PORT`: Port number for the application (default: 5000)

### File Upload Settings
- Maximum file size: 16MB
- Allowed file types: png, jpg, jpeg, gif, pdf, doc, docx, txt, mp3, mp4, zip
- Upload directory: `uploads/`

### Rate Limiting
- Messages: 30 per minute per user
- File uploads: 5 per 5 minutes per user
- Login attempts: 5 per 5 minutes per IP

## 🚀 Deployment

### Production Deployment
1. Set environment variables for production:
   ```bash
   export SECRET_KEY=your-strong-secret-key
   export DEBUG=False
   export PORT=80
   ```

2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn eventlet
   gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:80 main:app
   ```

3. Consider using a reverse proxy (Nginx) for better performance
4. Set up SSL/TLS certificates for HTTPS

### Docker Deployment (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
```

## 🛡️ Security Considerations

- Change the default secret key in production
- Use HTTPS in production
- Regularly update dependencies
- Monitor logs for suspicious activity
- Implement additional security measures as needed
- Regular backups of chat_data.json

## 🔍 API Endpoints

### Public Endpoints
- `GET /` - Main chat interface
- `GET /login` - Login page
- `GET /register` - Registration page
- `POST /login` - User authentication
- `POST /register` - User registration

### Authenticated Endpoints
- `GET /profile` - User profile page
- `POST /update_profile` - Update user profile
- `GET /api/users` - Get user statistics
- `GET /api/rooms` - Get available rooms
- `GET /api/history` - Get message history
- `POST /api/upload_file` - Upload files
- `GET /api/download_file/<file_id>` - Download files
- `GET /api/search_messages` - Search messages

### Admin Endpoints
- `GET /admin` - Admin panel
- `POST /api/ban_user` - Ban user
- `POST /api/unban_user` - Unban user
- `POST /api/toggle_admin` - Toggle admin status

## 🔌 Socket.IO Events

### Client to Server Events
- `message` - Send chat message
- `private_message` - Send private message
- `typing` - Typing indicator
- `join_room` - Join chat room
- `leave_room` - Leave chat room
- `file_share` - Share file
- `create_poll` - Create poll
- `vote_poll` - Vote on poll

### Server to Client Events
- `message` - Receive chat message
- `user_joined` - User joined notification
- `user_left` - User left notification
- `user_typing` - Typing indicator
- `message_reaction` - Message reaction update
- `poll_updated` - Poll results update

## 🐛 Troubleshooting

### Common Issues
1. **Port already in use:**
   - Change the PORT environment variable
   - Or kill the process using the port

2. **Permission errors on file upload:**
   - Check write permissions on the `uploads/` directory

3. **Database/JSON errors:**
   - Delete `chat_data.json` to reset (will lose all data)
   - Check file permissions

4. **Socket.IO connection issues:**
   - Check firewall settings
   - Verify network configuration

### Debugging
- Enable debug mode: `export DEBUG=True`
- Check application logs
- Use browser developer tools for client-side issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Developed with ❤️ for real-time communication needs.

## 🆕 Recent Improvements (Version 2.0)

### Enhanced Security
- **Input Sanitization**: XSS protection with `bleach` library
- **Enhanced Password Validation**: Stronger password requirements
- **File Security Checks**: Advanced file validation and malicious content detection
- **Thread-Safe Operations**: Improved data consistency with thread locks
- **Security Event Logging**: Comprehensive security monitoring
- **Session Management**: Improved session handling and cleanup

### Better Architecture
- **Database Abstraction**: Modular database layer with `database.py`
- **Configuration Management**: Centralized config with `config.py`
- **Docker Support**: Complete containerization with Docker and Docker Compose
- **Environment-based Configuration**: Support for development/production environments
- **Enhanced Error Handling**: Better error reporting and recovery

### Performance Improvements
- **Rate Limiting**: Advanced rate limiting for messages, uploads, and logins
- **Message Cleanup**: Automatic cleanup of old messages and data
- **File Upload Optimization**: Better file handling and validation
- **Memory Management**: Improved memory usage for large datasets

### Developer Experience
- **Type Hints**: Full type annotations for better code quality
- **Logging**: Comprehensive logging system
- **Testing Configuration**: Test environment setup
- **Documentation**: Enhanced code documentation

## 🐳 Docker Deployment

### Quick Start with Docker

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **Or build manually:**
   ```bash
   docker build -t real-time-chat .
   docker run -p 5000:5000 real-time-chat
   ```

3. **With Nginx reverse proxy:**
   ```bash
   docker-compose --profile with-nginx up -d
   ```

### Environment Variables
Create a `.env` file for production:
```env
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
DEBUG=False
PORT=5000
HOST=0.0.0.0
SESSION_COOKIE_SECURE=True
CORS_ORIGINS=https://yourdomain.com
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.11 or higher
- Node.js (optional, for frontend development)
- Docker (optional, for containerized development)

### Advanced Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd real_time_chat
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment:**
   ```bash
   cp .env.example .env  # Copy and modify as needed
   ```

5. **Run in development mode:**
   ```bash
   export FLASK_ENV=development
   python main.py
   ```

## 📊 Monitoring and Analytics

### Database Statistics
Access `/api/stats` (admin only) for:
- Total users and active users
- Message statistics
- File sharing metrics
- System performance data

### Logging
The application provides comprehensive logging:
- **Security Events**: Failed logins, suspicious activities
- **Performance Metrics**: Response times, error rates
- **User Activities**: Login/logout, message sending
- **System Events**: Startup, shutdown, errors

## 🔧 Advanced Configuration

### Custom Configuration
Modify `config.py` to customize:
- Rate limiting settings
- File upload restrictions
- Security policies
- Session management
- Database settings

### Production Optimization

1. **Use environment variables:**
   ```bash
   export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   export FLASK_ENV=production
   export DEBUG=False
   ```

2. **Set up reverse proxy (Nginx):**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Use production WSGI server:**
   ```bash
   pip install gunicorn eventlet
   gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 main:app
   ```

## 🔮 Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- Voice/Video calling with WebRTC
- End-to-end message encryption
- Push notifications
- Mobile app (React Native/Flutter)
- Advanced moderation tools
- Integration with external services (Slack, Discord)
- Better file preview capabilities
- Multi-language support
- AI-powered features (chatbots, translation)
- Analytics dashboard
- Load balancing and clustering

## 📞 Support

For support, questions, or suggestions, please create an issue in the repository or contact the development team.

---

**Happy Chatting! 💬**
