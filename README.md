# Data Analytics Platform

A comprehensive platform for data analytics and insights, built with FastAPI and Python.

## Features

- **Data Ingestion**: Collect data from multiple sources including News API and Twitter
- **Data Storage**: Store raw data in SQLite database with structured schemas
- **REST API**: FastAPI-based API for data access and ingestion
- **Configurable Sources**: Easy configuration for different data sources

## Project Structure

```
DataAnalPlatform/
├── app/
│   ├── api/
│   │   ├── endpoints/          # API endpoint definitions
│   │   └── routes.py          # Main API router
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   └── database.py        # Database configuration
│   ├── models/
│   │   └── data_models.py     # SQLAlchemy models
│   ├── schemas/
│   │   ├── data_schemas.py    # Pydantic schemas for data
│   │   └── ingestion_schemas.py # Ingestion request/response schemas
│   ├── services/
│   │   ├── ingestion_service.py # Main ingestion logic
│   │   ├── news_service.py    # News API integration
│   │   └── twitter_service.py # Twitter API integration
│   └── main.py               # FastAPI application
├── scripts/
│   ├── init_db.py           # Database initialization
│   └── ingest_sample_data.py # Sample data ingestion
├── requirements.txt         # Python dependencies
├── env.example             # Environment variables template
└── README.md              # This file
```

## Setup Instructions

### 1. Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration

1. Copy the environment template:
```bash
cp env.example .env
```

2. Edit `.env` file and add your API keys:
   - Get a News API key from [newsapi.org](https://newsapi.org/)
   - Get Twitter API credentials from [developer.twitter.com](https://developer.twitter.com/)

### 3. Database Setup

Initialize the database:
```bash
python scripts/init_db.py
```

### 4. Run the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. API Documentation

- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Usage

### Ingest Data

#### News Data
```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/news" \
     -H "Content-Type: application/json" \
     -d '{"query": "artificial intelligence", "language": "en", "page_size": 100}'
```

#### Twitter Data
```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/twitter" \
     -H "Content-Type: application/json" \
     -d '{"query": "AI OR artificial intelligence", "page_size": 100}'
```

### Retrieve Data

#### Get all data
```bash
curl "http://localhost:8000/api/v1/data/?limit=10"
```

#### Get data by source
```bash
curl "http://localhost:8000/api/v1/data/?source=news&limit=10"
```

#### Get specific data entry
```bash
curl "http://localhost:8000/api/v1/data/1"
```

## Data Sources

### News API
- **Source**: [News API](https://newsapi.org/)
- **Data**: News articles with title, content, author, URL, and metadata
- **Rate Limits**: 1000 requests per day (free tier)

### Twitter API
- **Source**: [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api)
- **Data**: Tweets with text, author, timestamps, and engagement metrics
- **Rate Limits**: Varies by endpoint and plan

## Development

### Running Sample Data Ingestion

```bash
python scripts/ingest_sample_data.py
```

### Database Management

The application uses SQLite for development. The database file will be created at `./data_analytics.db`.

### Adding New Data Sources

1. Create a new service in `app/services/`
2. Add the service to `IngestionService`
3. Create new API endpoints in `app/api/endpoints/`
4. Update the database models if needed

## Next Steps

- [ ] Add data preprocessing and cleaning
- [ ] Implement data analysis and insights
- [ ] Add visualization endpoints
- [ ] Set up data export functionality
- [ ] Add authentication and authorization
- [ ] Implement data source monitoring
- [ ] Add data quality checks
