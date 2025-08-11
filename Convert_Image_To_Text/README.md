# 🚀 Image Text Processor

A modern, user-friendly GUI application for extracting text from images using OCR (Optical Character Recognition) and translating between multiple languages.

## ✨ Features

- **Multi-language OCR Support**: Extract text from images in multiple languages including English, Persian (Farsi), Arabic, French, German, Spanish, Russian, Chinese, and Japanese
- **Real-time Translation**: Translate extracted text between 9 different languages using Google Translate API
- **Modern GUI**: Beautiful, responsive interface with shadow effects and gradient styling
- **Multiple Processing Modes**:
  - Convert image to Persian text
  - Convert image to English text
  - Extract and translate text in one step
- **File Operations**: Save extracted/translated text to files, copy to clipboard
- **Image Preview**: View selected images before processing
- **Progress Tracking**: Real-time progress bars during OCR and translation
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 🖥️ Screenshots

The application features a modern interface with:
- Gradient backgrounds and shadow effects
- Language selection with flag emojis
- Drag-and-drop image upload areas
- Progress indicators
- Clean, readable text display areas

## 🔧 Requirements

- Python 3.7+
- Windows/Linux/macOS
- Tesseract OCR engine installed on your system

## 📦 Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd Convert_Image_To_Text
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

#### Windows:
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it (typically to `C:\Program Files\Tesseract-OCR\`)
3. The application will auto-detect common installation paths

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-fas  # For Persian support
sudo apt install tesseract-ocr-ara  # For Arabic support
```

#### macOS:
```bash
brew install tesseract
brew install tesseract-lang  # For additional language support
```

### 4. Install Language Packs (Optional)
For better OCR accuracy with specific languages, install additional Tesseract language packs:
- Persian (Farsi): `fas`
- Arabic: `ara`
- French: `fra`
- German: `deu`
- Spanish: `spa`
- Russian: `rus`
- Chinese (Simplified): `chi_sim`
- Japanese: `jpn`

## 🚀 Usage

### Starting the Application
```bash
python main.py
```

### Main Features:

#### 1. **Convert to Persian Text**
- Click "🇮🇷 Convert to Persian"
- Upload an image containing Persian/Farsi text
- Click "Process" to extract text
- Copy or save the results

#### 2. **Convert to English Text**
- Click "🇺🇸 Convert to English"
- Upload an image containing English text
- Click "Process" to extract text
- Copy or save the results

#### 3. **Translate Image Text**
- Click "🌐 Translate Image"
- Select source and target languages from dropdowns
- Upload an image
- Click "Translate" to extract and translate text
- View both original and translated text

### Supported File Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- BMP (.bmp)
- GIF (.gif)

### Language Support

| Language | OCR Code | Flag |
|----------|----------|------|
| English | eng | 🇺🇸 |
| Persian (Farsi) | fas | 🇮🇷 |
| Arabic | ara | 🇸🇦 |
| French | fra | 🇫🇷 |
| German | deu | 🇩🇪 |
| Spanish | spa | 🇪🇸 |
| Russian | rus | 🇷🇺 |
| Chinese (Simplified) | chi_sim | 🇨🇳 |
| Japanese | jpn | 🇯🇵 |

## 🏗️ Project Structure

```
Convert_Image_To_Text/
├── main_improved.py          # Main application file
├── convert.py               # UI definition (generated from Qt Designer)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── icon.ico                # Application icon (optional)
└── examples/               # Example images (optional)
```

## 🛠️ Technical Details

### Architecture
- **GUI Framework**: PyQt6
- **OCR Engine**: Tesseract via pytesseract
- **Translation**: Google Translate via deep-translator
- **Image Processing**: PIL (Python Imaging Library)
- **Threading**: QThread for non-blocking operations

### Key Components
- `BaseConvertDialog`: Base class for all conversion dialogs
- `PersianConvertDialog`: Specialized for Persian OCR
- `EnglishConvertDialog`: Specialized for English OCR  
- `TranslateImageDialog`: Combined OCR and translation
- `OCRWorker`: Background thread for OCR processing
- `TranslationWorker`: Background thread for translation
- Modern styling functions with gradient and shadow effects

### Performance Features
- **Multi-threading**: OCR and translation run in background threads to prevent UI freezing
- **Progress Tracking**: Real-time progress updates during processing
- **Memory Efficient**: Images are properly scaled for preview without loading full resolution
- **Error Recovery**: Graceful handling of network, file, and processing errors

## 🎨 Customization

### Styling
The application uses a modern design with customizable colors defined in the `COLORS` dictionary:
- Primary: `#2E86AB` (Blue)
- Secondary: `#A23B72` (Purple)
- Accent: `#F18F01` (Orange)
- Success: `#06FFA5` (Green)
- Warning: `#FFD23F` (Yellow)
- Danger: `#FF3366` (Red)

### Adding New Languages
To add support for new languages:
1. Install the Tesseract language pack
2. Add the language to the `languages` dictionary in `TranslateImageDialog`
3. Add the OCR language mapping in `ocr_lang_map`

## 🐛 Troubleshooting

### Common Issues:

1. **"Tesseract not found" error**
   - Solution: Install Tesseract OCR and ensure it's in your system PATH

2. **Poor OCR accuracy**
   - Solution: Use high-resolution, clear images with good contrast
   - Install language-specific Tesseract packs

3. **Translation errors**
   - Solution: Check internet connection (Google Translate requires internet)
   - Try shorter text segments

4. **UI elements not visible**
   - Solution: The recent update fixed text visibility issues with explicit color styling

### Debug Mode
For troubleshooting, check the console output for detailed logging information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for optical character recognition
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [deep-translator](https://github.com/nidhaloff/deep-translator) for translation services
- [PIL/Pillow](https://python-pillow.org/) for image processing

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information about your problem

---

**Made with ❤️ for text extraction and translation**
