# Title Fix - Complete Web Application

A comprehensive monorepo containing both the **Title Fix Python package** and a **modern web application** that provides an intuitive interface for intelligent title case conversion and text formatting.

## 🌟 Features

### Python Package (`title_fix/`)
- Multiple case conversion options (Title, Sentence, UPPERCASE, lowercase, etc.)
- Citation style support (APA, Chicago, AP, MLA, NYT)
- Intelligent handling of Roman numerals, acronyms, and hyphenated words
- Headline scoring and text analysis
- Comprehensive text formatting utilities

### Web Application
- **Modern React Frontend** with real-time conversion
- **FastAPI Backend** providing RESTful API
- **Responsive Design** that works on all devices
- **Real-time Processing** with 300ms debouncing
- **Copy to Clipboard** functionality
- **Text Statistics** (word count, character count, headline score)
- **Multiple Citation Styles** with dynamic UI
- **SEO Optimized** for search engines

## 🏗️ Project Structure

```
title-fix-suite/
├── title_fix/                 # Python package (core engine)
│   ├── __init__.py
│   ├── core.py               # Main processing logic
│   ├── constants.py          # Citation styles and constants
│   └── utils.py              # Utility functions
├── backend/                  # FastAPI web API
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/                 # React web application
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Base styles
│   ├── public/
│   │   └── index.html       # HTML template
│   └── package.json         # Node.js dependencies
├── build.sh                 # Build script for deployment
├── start.sh                 # Start script for production
├── render.yaml              # Render.com configuration
├── Dockerfile               # Docker containerization
├── pyproject.toml           # Python package configuration
└── README.md                # Python package documentation
```

## 🚀 Quick Start

### Local Development

#### 1. Install Python Dependencies
```bash
# Install the title_fix package in development mode
pip install -e .

# Install backend dependencies
pip install -r backend/requirements.txt
```

#### 2. Start the Backend (Terminal 1)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### 3. Start the Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🌐 Deployment on Render

### Prerequisites
- GitHub account with your code pushed to a repository
- Render account (free tier available)

### Step-by-Step Deployment

#### 1. **Prepare Your Repository**
```bash
# Add all files and commit
git add .
git commit -m "Initial web app setup"
git push origin main
```

#### 2. **Create New Web Service on Render**
1. Go to [render.com](https://render.com) and sign up/log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `title_fix` repository

#### 3. **Configure the Service**
```yaml
Name: title-fix-app
Environment: Python 3
Build Command: ./build.sh
Start Command: ./start.sh
```

#### 4. **Set Environment Variables** (Optional)
```
PYTHON_VERSION=3.11.0
NODE_VERSION=18.17.0
PYTHONUNBUFFERED=true
```

#### 5. **Deploy**
- Click **"Create Web Service"**
- Render will automatically build and deploy your app
- Build process takes ~5-10 minutes
- Your app will be live at `https://your-app-name.onrender.com`

### Alternative: Manual Configuration
If you prefer manual configuration over `render.yaml`:

```yaml
Build Command: pip install --upgrade pip && pip install -r backend/requirements.txt && pip install -e . && cd frontend && npm ci && npm run build
Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 🐳 Docker Deployment

For containerized deployment:

```bash
# Build the Docker image
docker build -t title-fix-app .

# Run the container
docker run -p 8000:8000 title-fix-app
```

## 📡 API Usage

The backend provides a RESTful API that can be used independently:

### Convert Text
```bash
curl -X POST "https://your-app.onrender.com/api/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "this is a test title",
    "case_type": "title",
    "style": "apa"
  }'
```

### Get Available Options
```bash
curl "https://your-app.onrender.com/api/options"
```

### Health Check
```bash
curl "https://your-app.onrender.com/api/health"
```

## 🎨 Customization

### Frontend Styling
The React app uses custom CSS classes in `frontend/src/App.css`. You can:
- Modify colors by changing CSS variables
- Update the gradient background
- Customize component spacing and layout
- Add new UI components

### Backend Extensions
To add new API endpoints:
1. Edit `backend/main.py`
2. Add new Pydantic models for request/response
3. Implement the endpoint logic using the `title_fix` package

### Python Package Features
The core `title_fix` package can be extended with:
- New citation styles in `constants.py`
- Additional case types in `core.py`
- Enhanced text analysis features

## 🔧 Development Tools

### Local Testing
```bash
# Test the Python package
python -m pytest tests/

# Test the API endpoints
cd backend
python -m pytest  # (if you add API tests)

# Build and test the React app
cd frontend
npm test
npm run build
```

### Code Quality
```bash
# Format Python code
black title_fix/ backend/

# Lint Python code
flake8 title_fix/ backend/

# Format JavaScript/React code
cd frontend
npm run lint  # (if you add ESLint)
```

## 📊 Performance

The application is optimized for performance:
- **Python Package**: Uses compiled regex patterns and LRU caching
- **Backend**: FastAPI with async support and singleton pattern
- **Frontend**: React with debounced input and optimized re-renders
- **Deployment**: Multi-stage Docker build for minimal image size

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (both package and web app)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for the backend
- Frontend powered by [React](https://reactjs.org/)
- Icons from [Lucide React](https://lucide.dev/)
- Deployed on [Render](https://render.com/)

---

**Live Demo**: [Your App URL Here](https://your-app.onrender.com)  
**API Documentation**: [Your App URL Here](https://your-app.onrender.com/docs) 