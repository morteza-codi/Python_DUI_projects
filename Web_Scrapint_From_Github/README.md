# 🔍 GitHub Repository Finder

An advanced, feature-rich desktop application for discovering trending repositories on GitHub. Built with Python and PyQt6, this tool provides an intuitive interface for exploring GitHub's vast ecosystem of open-source projects.

![GitHub Repository Finder](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-red.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ✨ Features

### 🔍 **Smart Search**
- Search repositories by programming language
- Auto-complete with popular languages
- Advanced filtering options
- Multiple sorting criteria (stars, forks, updated)

### ⭐ **Advanced Filtering**
- Filter by minimum star count
- Exclude archived repositories
- Focus on recently updated projects
- Quality-focused results

### 📊 **Multiple Export Formats**
- **JSON**: Structured data for developers
- **CSV**: Spreadsheet-friendly format
- **Markdown**: Documentation-ready format
- **Plain Text**: Human-readable reports

### 🚀 **Enhanced GitHub Integration**
- Real-time API rate limit monitoring
- Support for GitHub API tokens
- Comprehensive repository metadata
- Activity indicators for project health

### 💾 **Smart Persistence**
- Automatic settings backup
- Search history tracking
- Persistent user preferences
- Resume where you left off

### 🎨 **Modern Interface**
- Clean, intuitive design
- Dark theme support
- Responsive layout
- Professional styling

## 🛠 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Quick Install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/github-repository-finder.git
   cd github-repository-finder
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

### Alternative Installation Methods

#### Using Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv github-finder-env

# Activate it
# On Windows:
github-finder-env\Scripts\activate
# On macOS/Linux:
source github-finder-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### Direct Dependencies Installation
```bash
pip install PyQt6>=6.6.0 requests>=2.31.0
python main.py
```

## 🚀 Usage

### Basic Search
1. Launch the application
2. Enter a programming language (e.g., "Python", "JavaScript")
3. Set the number of repositories to find (1-100)
4. Click "🔍 Search Repositories"

### Advanced Search
1. Check "Show Advanced Options"
2. Set minimum star count for quality filtering
3. Optionally add your GitHub API token for higher rate limits
4. Choose sorting method (stars/forks/updated)

### Working with Results
- **View**: Scroll through detailed repository information
- **Copy**: Copy all results to clipboard
- **Export**: Save in JSON, CSV, or Markdown format
- **Browse**: Click URLs to open repositories in your browser
- **Refresh**: Update results with latest data

## ⚙️ Configuration

### GitHub API Token (Optional)
To increase your rate limit from 60 to 5,000 requests per hour:

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `public_repo` scope
3. Add it in the Advanced Options section
4. The token is stored securely and encrypted

### Settings
All settings are automatically saved:
- Last used programming language
- Preferred number of results
- Sort preferences
- Advanced options state
- Search history (last 10 searches)

## 📊 Output Formats

### JSON Export
```json
{
  "name": "repository-name",
  "description": "Repository description",
  "html_url": "https://github.com/user/repo",
  "stargazers_count": 12345,
  "forks_count": 2345,
  "language": "Python",
  "owner": {"login": "username"},
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-12-01T00:00:00Z"
}
```

### CSV Export
Includes columns: Name, Description, URL, Stars, Forks, Language, Owner, Created, Updated, Size

### Markdown Export
```markdown
# Top 10 Python Repositories

## 1. [repository-name](https://github.com/user/repo)
**⭐ Stars:** 12,345 | **🍴 Forks:** 2,345 | **👤 Owner:** username
**Description:** Repository description
**Last Updated:** 2023-12-01
```

## 🧩 Technical Details

### Architecture
- **GUI Framework**: PyQt6 for modern, cross-platform interface
- **HTTP Client**: Requests library for GitHub API communication
- **Threading**: Asynchronous API calls to prevent UI blocking
- **Logging**: Comprehensive logging for debugging and monitoring
- **Settings**: QSettings for persistent configuration storage

### GitHub API Integration
- Uses GitHub Search API v3
- Implements rate limit monitoring
- Supports authenticated requests
- Handles error conditions gracefully
- Respects API best practices

### Data Enhancement
The application enhances raw GitHub data with:
- Popularity scores (stars + 2×forks)
- Activity indicators (🟢 active, 🟡 moderate, 🔴 stale)
- Formatted dates and time calculations
- Repository age metrics
- Quality indicators

## 🔧 Development

### Project Structure
```
github-repository-finder/
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
├── git.py              # Legacy UI file (can be removed)
└── logs/
    └── github_finder.log  # Application logs
```

### Code Quality
- Type hints throughout the codebase
- Comprehensive error handling
- Modular, object-oriented design
- Extensive documentation
- PEP 8 compliant formatting

### Extending the Application
The codebase is designed for easy extension:
- Add new export formats in `GitHubSearchDialog`
- Implement additional search filters in `GitHubSearchWorker`
- Customize UI themes in the main application setup
- Add new data sources beyond GitHub

## 🐛 Troubleshooting

### Common Issues

**"No module named 'PyQt6'"**
```bash
pip install PyQt6
```

**"API rate limit exceeded"**
- Add a GitHub API token in Advanced Options
- Wait for the rate limit to reset (shown in the UI)

**"Network error"**
- Check your internet connection
- Verify GitHub API accessibility
- Try again with a different network

**"Invalid search query"**
- Ensure the programming language is correctly spelled
- Try with more common language names
- Check for special characters in the input

### Logging
Check `github_finder.log` for detailed error information:
- API request details
- Error stack traces
- Performance metrics
- User actions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🙏 Acknowledgments

- **GitHub API** for providing comprehensive repository data
- **PyQt6** for the powerful GUI framework
- **Python Requests** for reliable HTTP communication
- **The Open Source Community** for inspiration and feedback

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information
4. Include logs and system information

---

**Happy coding! 🚀**

*Made with ❤️ for the developer community*
