# 🌟 SkinVision AI Backend
**AI-based Facial Skin Analysis for Personalized Skincare Recommendation**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python)](https://www.python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg?style=flat&logo=opencv)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10+-red.svg?style=flat&logo=google)](https://mediapipe.dev)

---

## 📝 Introduction  
SkinVision AI เป็นระบบ **วิเคราะห์ภาพผิวหน้าด้วย AI** ที่ช่วยตรวจจับและจำแนกปัญหาผิว เช่น สิว ริ้วรอย ความมัน/รูขุมขน และจุดด่างดำ พร้อมทั้งแนะนำแนวทางการดูแลผิวเฉพาะบุคคล โดยผสานการทำงานของ **Computer Vision** และ **Deep Learning**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/skinvision-ai-backend.git
   cd skinvision-ai-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env
   # Edit .env file with your configuration
   ```

5. **Run the development server**
   ```bash
   fastapi dev app/main.py
   ```

The API will be available at `http://localhost:8000`

- **API Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

---

## 🏗️ Project Structure

```
skinvision-ai-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py       # Health check endpoints
│   │       ├── skin_analysis.py # Skin analysis endpoints
│   │       └── recommendations.py # Recommendation endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── skin_analysis.py    # Pydantic models for analysis
│   │   └── recommendations.py  # Pydantic models for recommendations
│   └── services/
│       ├── __init__.py
│       ├── image_processor.py  # Image processing service
│       ├── skin_analyzer.py    # Skin analysis service
│       └── recommendation_engine.py # Recommendation engine
├── uploads/                    # Directory for uploaded images
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md               # This file
```

---

## 🔧 API Endpoints

### Health Check
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed system health

### Skin Analysis
- `POST /api/v1/upload-image` - Upload image for analysis
- `POST /api/v1/analyze` - Analyze uploaded image
- `GET /api/v1/analysis/{analysis_id}` - Get analysis result
- `GET /api/v1/supported-conditions` - Get supported skin conditions

### Recommendations
- `POST /api/v1/recommend` - Get skincare recommendations
- `GET /api/v1/recommend/{analysis_id}` - Get recommendations by analysis ID
- `GET /api/v1/products/categories` - Get product categories
- `GET /api/v1/products/ingredients` - Get ingredient information
- `GET /api/v1/routines/templates` - Get routine templates
- `GET /api/v1/advice/general` - Get general skincare advice

---

## 🧪 Usage Examples

### 1. Upload and Analyze Image

```bash
# Upload image
curl -X POST "http://localhost:8000/api/v1/upload-image" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/your/image.jpg"

# Response will include upload_id
{
  "upload_id": "123e4567-e89b-12d3-a456-426614174000",
  "filename": "123e4567-e89b-12d3-a456-426614174000.jpg",
  "file_size": 2048000,
  "image_url": "/uploads/123e4567-e89b-12d3-a456-426614174000.jpg"
}

# Analyze uploaded image
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "upload_id=123e4567-e89b-12d3-a456-426614174000&detailed_analysis=true"
```

### 2. Get Recommendations

```bash
# Get recommendations for analysis
curl -X POST "http://localhost:8000/api/v1/recommend" \
     -H "Content-Type: application/json" \
     -d '{
       "analysis_id": "analysis_123",
       "budget_preference": "medium",
       "routine_complexity": "beginner"
     }'
```

### 3. Python Client Example

```python
import requests
import json

# Upload image
with open("face_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/api/v1/upload-image", files=files)
    upload_data = response.json()

# Analyze image
analyze_data = {
    "upload_id": upload_data["upload_id"],
    "detailed_analysis": True
}
response = requests.post("http://localhost:8000/api/v1/analyze", data=analyze_data)
analysis_result = response.json()

# Get recommendations
recommend_data = {
    "analysis_id": analysis_result["analysis_id"],
    "routine_complexity": "beginner"
}
response = requests.post("http://localhost:8000/api/v1/recommend", json=recommend_data)
recommendations = response.json()

print(json.dumps(recommendations, indent=2))
```

---

## 🎯 Skin Conditions Detected

The system can detect and analyze the following skin conditions:

- **Acne** - Various types of acne and breakouts
- **Wrinkles** - Fine lines and aging signs
- **Dark Spots** - Hyperpigmentation and age spots
- **Oiliness** - Excess sebum production
- **Dryness** - Dehydrated or dry skin
- **Pores** - Large or visible pores
- **Pigmentation** - Uneven skin tone and discoloration

---

## 💡 Features

### Current Features (Phase 1)
- ✅ Image upload and validation
- ✅ Face detection using MediaPipe
- ✅ Basic image preprocessing
- ✅ Mock skin condition analysis
- ✅ Rule-based skincare recommendations  
- ✅ RESTful API with FastAPI
- ✅ Interactive API documentation
- ✅ Comprehensive error handling

### Future Features (Roadmap)
- 🔲 **Phase 2**: Integration with trained ML models
- 🔲 **Phase 3**: User profiles and personalization
- 🔲 **Phase 4**: Database integration
- 🔲 **Phase 5**: Real-time skin tracking
- 🔲 **Phase 6**: Mobile app integration

---

## 🛠️ Development

### Running in Development Mode
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
fastapi dev app/main.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests
```bash
# Install pytest
pip install pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

### Code Quality
```bash
# Format code
black app/

# Check code style
flake8 app/

# Type checking
mypy app/
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `true` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `MAX_FILE_SIZE` | Max upload size (bytes) | `10485760` |
| `MODEL_CONFIDENCE_THRESHOLD` | AI model confidence threshold | `0.7` |
| `FACE_DETECTION_CONFIDENCE` | Face detection confidence | `0.5` |

### Supported File Types
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)

### File Size Limits
- Maximum file size: 10MB
- Recommended resolution: 1024x1024 or smaller

---

## 🚀 Deployment

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
# Dockerfile (create this file)
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t skinvision-ai-backend .
docker run -p 8000:8000 skinvision-ai-backend
```

---

## 🧩 Technical Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for serving the application
- **Pydantic** - Data validation using Python type annotations

### Computer Vision & AI
- **OpenCV** - Computer vision and image processing
- **MediaPipe** - Face detection and landmark extraction
- **NumPy** - Numerical computing
- **scikit-image** - Image processing algorithms
- **Pillow** - Image handling and manipulation

### Future ML Integration
- **PyTorch** - Deep learning framework (ready for integration)
- **TensorFlow** - Alternative deep learning framework
- **scikit-learn** - Machine learning algorithms

---

## 📊 Development Workflow

### Phase 1: Foundation ✅
- [x] Project setup and structure
- [x] Basic API endpoints
- [x] Image processing pipeline  
- [x] Mock analysis system
- [x] Rule-based recommendations

### Phase 2: AI Integration (Next)
- [ ] Dataset preparation and preprocessing
- [ ] Model training for skin condition detection
- [ ] Model integration and optimization
- [ ] Advanced image processing techniques

### Phase 3: Enhancement
- [ ] User authentication and profiles
- [ ] Database integration (PostgreSQL)
- [ ] Advanced recommendation algorithms
- [ ] API rate limiting and security

### Phase 4: Production
- [ ] Frontend integration
- [ ] Mobile app support
- [ ] Performance optimization
- [ ] Monitoring and logging

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 API Documentation

The API provides comprehensive documentation accessible at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Response Format
All API responses follow a consistent format:

```json
{
  "status": "success|error",
  "data": {},
  "message": "Description",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Error Handling
The API provides detailed error responses:

```json
{
  "detail": "Error description",
  "status_code": 400,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## 🔒 Security Considerations

- File upload validation and sanitization
- Image size and type restrictions
- Rate limiting (to be implemented)
- Input validation using Pydantic models
- Secure file storage practices

---

## 📈 Performance

- **Image Processing**: Optimized OpenCV operations
- **Face Detection**: MediaPipe for efficient detection
- **API Response**: Average response time < 500ms
- **Concurrent Requests**: Supports multiple concurrent uploads
- **Memory Management**: Efficient image handling

---

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're in the project directory and virtual environment is activated
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **OpenCV Installation Issues**
   ```bash
   # Install OpenCV with specific version if needed
   pip install opencv-python==4.8.0.74
   ```

3. **MediaPipe Issues**
   ```bash
   # Reinstall MediaPipe
   pip uninstall mediapipe
   pip install mediapipe
   ```

4. **File Upload Errors**
   - Check file size (max 10MB)
   - Ensure supported file format (JPEG, PNG)
   - Verify uploads directory exists and is writable

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/skinvision-ai-backend/issues)
- **Documentation**: This README and API docs
- **Email**: support@skinvision-ai.com

---

## 📄 License  
MIT License © 2024 SkinVision AI Team

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [MediaPipe](https://mediapipe.dev/) for face detection capabilities
- [OpenCV](https://opencv.org/) for computer vision tools
- Open source skincare datasets and research community