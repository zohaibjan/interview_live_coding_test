# Live Coding Interview Platform

A HackerRank-like platform for conducting live coding interviews, built with FastAPI and designed for deployment on Snowflake Park Container Services (SPCS).

## Features

- **Real-time Code Execution**: Secure Python code execution with time and memory limits
- **Multiple Problems**: Pre-loaded coding problems with varying difficulty levels
- **User Authentication**: JWT-based authentication system
- **Role-based Access**: Separate access for candidates and interviewers
- **Test Case Validation**: Automatic validation against hidden and visible test cases
- **HackerRank-like Interface**: Clean, professional coding interface
- **Docker Ready**: Fully containerized for easy deployment

## Quick Start

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- PostgreSQL (for production) or SQLite (for development)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd interview_live_coding_test
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database:**
   ```bash
   python populate_sample_data.py
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application:**
   - Open http://localhost:8000 in your browser
   - Use these test credentials:
     - **Candidate**: username=`candidate`, password=`candidate123`
     - **Interviewer**: username=`admin`, password=`admin123`

## Docker Deployment

### Build and run locally:
```bash
docker build -t coding-interview-platform .
docker run -p 8000:8000 coding-interview-platform
```

### Using Docker Compose (with PostgreSQL):
```bash
docker-compose up -d
```

## Snowflake Park Container Services (SPCS) Deployment

### 1. Prepare for SPCS Deployment

Create the SPCS specification file:

```yaml
# spcs-spec.yaml
spec:
  containers:
  - name: coding-interview-app
    image: /your-database/your-schema/your-repository/coding-interview-platform:latest
    env:
      DATABASE_URL: postgresql://username:password@your-db-host:5432/coding_test
      SECRET_KEY: your-production-secret-key-here
      REDIS_URL: redis://your-redis-host:6379
    resources:
      requests:
        cpu: 1
        memory: 2Gi
      limits:
        cpu: 2
        memory: 4Gi
  endpoints:
  - name: app-endpoint
    port: 8000
    public: true
```

### 2. Build and Push to Snowflake Registry

```sql
-- Create image repository
CREATE IMAGE REPOSITORY your_database.your_schema.coding_interview_platform;

-- Build and push the image
-- (Use docker build and docker push commands with the Snowflake registry URL)
```

### 3. Create and Start the Service

```sql
-- Create the service
CREATE SERVICE your_database.your_schema.coding_interview_service
  IN COMPUTE POOL your_compute_pool
  FROM SPECIFICATION_FILE='spcs-spec.yaml';

-- Start the service
ALTER SERVICE your_database.your_schema.coding_interview_service RESUME;

-- Check service status
DESCRIBE SERVICE your_database.your_schema.coding_interview_service;
```

## Application Architecture

### Backend (FastAPI)
- **Authentication**: JWT-based user authentication with role management
- **API Endpoints**:
  - `/api/auth/*` - User registration, login, token management
  - `/api/problems/*` - Problem management and retrieval
  - `/api/submissions/*` - Code submission and execution
- **Code Execution**: Secure Python code execution in isolated environment
- **Database**: SQLAlchemy ORM with PostgreSQL/SQLite support

### Frontend
- **Problem List**: Browse available coding problems
- **Code Editor**: Syntax-highlighted code editor (with CodeMirror fallback)
- **Test Results**: Real-time feedback on code execution
- **Authentication UI**: Login and registration modals

### Security Features
- **Input Validation**: All inputs are validated and sanitized
- **Code Sandboxing**: Code execution runs in controlled environment
- **Time Limits**: Prevents infinite loops and long-running code
- **Authentication**: JWT tokens for secure API access
- **CORS Protection**: Configured for production deployment

## Sample Problems

The platform comes with three pre-loaded problems:

1. **Two Sum** (Easy) - Find indices of two numbers that add up to a target
2. **Valid Palindrome** (Easy) - Check if a string is a palindrome
3. **FizzBuzz** (Easy) - Classic FizzBuzz implementation

## API Usage Examples

### Authentication
```bash
# Register a new user
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User",
    "is_interviewer": false
  }'

# Login and get access token
curl -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

### Submit Code for Evaluation
```bash
curl -X POST "http://localhost:8000/api/submissions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "problem_id": 1,
    "code": "def two_sum(nums, target):\n    # Your solution here\n    pass",
    "language": "python"
  }'
```

## Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT signing secret (change in production!)
- `REDIS_URL`: Redis connection for caching (optional)
- `MAX_EXECUTION_TIME`: Maximum code execution time (seconds)
- `MAX_MEMORY_LIMIT`: Maximum memory limit (MB)

### Production Considerations
- Use a strong secret key for JWT signing
- Configure proper CORS origins
- Set up database connection pooling
- Enable logging and monitoring
- Configure rate limiting
- Use HTTPS in production

## Development

### Adding New Problems
1. Create problem entry in database
2. Add test cases with expected inputs/outputs
3. Optionally provide starter code

### Extending Language Support
1. Add language parser in `code_execution.py`
2. Update frontend language selector
3. Add language-specific security restrictions

## Testing

Run the test suite:
```bash
pytest tests/
```

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please create an issue in the GitHub repository.