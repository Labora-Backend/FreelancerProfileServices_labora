# FreelancerProfileServices - Labora Backend

A comprehensive Django REST API service for managing freelancer profiles in the Labora platform. This microservice handles profile creation, updates, retrieval, and deletion with support for skills, ratings, and availability management.

## 🚀 Overview

FreelancerProfileServices is a dedicated microservice that provides complete profile management for freelancers in the Labora ecosystem. It enables freelancers to create and maintain professional profiles with detailed information including skills, experience, rates, and portfolio information.

## 📋 Features

### Profile Management
- ✅ Create freelancer profiles with comprehensive information
- ✅ Update existing profiles with partial or full data
- ✅ Retrieve profile information by user ID
- ✅ Delete profiles securely
- ✅ Profile image uploads with media storage

### Skills & Expertise
- ✅ Add multiple skills to profiles
- ✅ Manage skill database
- ✅ Filter freelancers by skills
- ✅ Skills with unique constraints

### Professional Information
- ✅ Professional title and bio
- ✅ Years of experience tracking
- ✅ Hourly rate management with multiple currencies
- ✅ Availability status (Full-time, Part-time, Freelance)
- ✅ Languages spoken
- ✅ Portfolio URL integration

### Profile Statistics & Verification
- ✅ Job completion tracking
- ✅ Average rating system
- ✅ Verification badge system
- ✅ Active/Inactive status
- ✅ Last seen timestamp
- ✅ Profile creation and update tracking

### Authentication & Authorization
- ✅ JWT authentication support
- ✅ User ID linkage from Auth Service
- ✅ Permission-based access control
- ✅ Flexible permission settings for profile visibility

## 📦 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Django | 5.2+ |
| API | Django REST Framework | 3.14+ |
| Authentication | Simple JWT | 5.2+ |
| Environment Management | python-dotenv | 1.0+ |
| Database | SQLite (dev) / MySQL/PostgreSQL (prod) | - |
| HTTP Server | Gunicorn | 21+ |
| Image Processing | Pillow | 10.0+ |

## 🛠 Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Labora-Backend/FreelancerProfileServices_labora.git
   cd FreelancerProfileServices_labora
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt python-dotenv pillow
   ```

4. **Create .env file**
   ```bash
   cat > .env << EOF
   # Django Settings
   DJANGO_SECRET_KEY=your-super-secret-key-change-in-production
   DEBUG=True
   
   # JWT Configuration
   JWT_ALGORITHM=HS256
   JWT_SIGNING_KEY=your-jwt-signing-key
   
   # Database (Optional - for production)
   # DB_ENGINE=django.db.backends.mysql
   # DB_NAME=freelancer_db
   # DB_USER=root
   # DB_PASSWORD=password
   # DB_HOST=localhost
   # DB_PORT=3306
   EOF
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t labora/freelancer-profile-service:latest .
```

### Run Container
```bash
docker run -d \
  --name freelancer-profile-service \
  -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  -v /path/to/media:/app/media \
  labora/freelancer-profile-service:latest
```

### Docker Compose Example
```yaml
version: '3.8'
services:
  freelancer-profile-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}
      DEBUG: "False"
      JWT_ALGORITHM: HS256
      JWT_SIGNING_KEY: ${JWT_SIGNING_KEY}
    volumes:
      - ./media:/app/media
    command: >
      sh -c "python manage.py migrate &&
             gunicorn freelancer_profile_service.wsgi:application --bind 0.0.0.0:8000"
```

## 📡 API Endpoints

All endpoints are prefixed with `/api/`

### 1. Create Freelancer Profile

**Endpoint:** `POST /api/profile/add/`

**Permission:** AllowAny

**Request Body:**
```json
{
  "user_id": 101,
  "full_name": "John Doe",
  "title": "Senior Web Developer",
  "bio": "Experienced full-stack developer with 5+ years in web development",
  "location": "San Francisco, CA",
  "experience_years": 5,
  "hourly_rate": "75.00",
  "currency": "USD",
  "availability": "freelance",
  "languages": "English, Spanish",
  "portfolio_url": "https://johndoe.portfolio.com",
  "profile_image": "<image_file>",
  "skills": [1, 2, 3]
}
```

**Response:** `201 Created`
```json
{
  "message": "Profile added"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "full_name": ["This field is required."],
  "hourly_rate": ["This field is required."]
}
```

### 2. Update Freelancer Profile

**Endpoint:** `PUT /api/profile/update/` or `PATCH /api/profile/update/`

**Permission:** AllowAny

**Request Body (Partial Update):**
```json
{
  "user_id": 101,
  "title": "Senior Full-Stack Developer",
  "hourly_rate": "85.00",
  "average_rating": "4.8"
}
```

**Response:** `200 OK`
```json
{
  "message": "profile updated"
}
```

**Error Response:** `404 Not Found`
```json
{
  "error": "Profile not found"
}
```

### 3. Retrieve Freelancer Profile

**Endpoint:** `GET /api/profile/view/`

**Permission:** AllowAny

**Query Parameters:**
```
user_id (required): Integer - The user ID of the freelancer
```

**Example Request:**
```bash
curl "http://localhost:8000/api/profile/view/?user_id=101"
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 101,
  "full_name": "John Doe",
  "title": "Senior Web Developer",
  "bio": "Experienced full-stack developer with 5+ years in web development",
  "location": "San Francisco, CA",
  "profile_image": "http://localhost:8000/media/freelancer_profiles/johndoe.jpg",
  "experience_years": 5,
  "hourly_rate": "75.00",
  "currency": "USD",
  "skills": [
    {
      "id": 1,
      "name": "Python"
    },
    {
      "id": 2,
      "name": "Django"
    }
  ],
  "availability": "freelance",
  "languages": "English, Spanish",
  "portfolio_url": "https://johndoe.portfolio.com",
  "total_jobs_completed": 24,
  "average_rating": "4.8",
  "is_verified": true,
  "is_active": true,
  "last_seen": "2024-01-15T14:30:00Z",
  "created_at": "2024-01-10T10:00:00Z",
  "updated_at": "2024-01-15T14:30:00Z"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "error": "user_id is required"
}
```

### 4. Delete Freelancer Profile

**Endpoint:** `DELETE /api/profile/delete/`

**Permission:** AllowAny

**Request Body:**
```json
{
  "user_id": 101
}
```

**Response:** `204 No Content`

**Error Response:** `404 Not Found`
```json
{
  "error": "Profile not found"
}
```

## 🗄️ Database Schema

### FreelancerProfile Model

```python
class FreelancerProfile(models.Model):
    # User Reference
    user_id: IntegerField(unique=True)  # Comes from Auth Service
    
    # Basic Information
    full_name: CharField(max_length=150)
    title: CharField(max_length=150, blank=True)
    bio: TextField(blank=True)
    location: CharField(max_length=100, blank=True)
    
    # Profile Image
    profile_image: ImageField(upload_to="freelancer_profiles/")
    
    # Professional Details
    experience_years: PositiveIntegerField(default=0)
    hourly_rate: DecimalField(max_digits=10, decimal_places=2)
    currency: CharField(max_length=10, default="INR")
    
    # Skills & Expertise
    skills: ManyToManyField(Skill, related_name="freelancers", blank=True)
    
    # Availability
    availability: CharField(
        choices=[
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("freelance", "Freelance")
        ]
    )
    
    # Languages
    languages: CharField(max_length=200)
    
    # Portfolio
    portfolio_url: URLField(blank=True)
    
    # Profile Statistics
    total_jobs_completed: PositiveIntegerField(default=0)
    average_rating: DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    # Status
    is_verified: BooleanField(default=False)
    is_active: BooleanField(default=True)
    
    # Timestamps
    last_seen: DateTimeField(null=True, blank=True)
    created_at: DateTimeField(auto_now_add=True)
    updated_at: DateTimeField(auto_now=True)
```

### Skill Model

```python
class Skill(models.Model):
    name: CharField(max_length=100, unique=True)
    
    # Relations
    freelancers: ManyToManyField(FreelancerProfile, related_name="skills")
```

## 🔐 Authentication

This service uses JWT (JSON Web Token) authentication via Simple JWT.

### Token Configuration
Set these environment variables to match your Auth Service:

```bash
JWT_ALGORITHM=HS256  # Algorithm used (HS256, RS256, etc.)
JWT_SIGNING_KEY=your-secret-key  # Secret key for signing/verification
```

### Token Structure
```json
{
  "user_id": 101,
  "username": "johndoe",
  "email": "john@example.com",
  "iat": 1642345600,
  "exp": 1642349200
}
```

### Using Tokens in Requests
```bash
curl -H "Authorization: Bearer <your_jwt_token>" \
  "http://localhost:8000/api/profile/view/?user_id=101"
```

## 📊 Project Structure

```
FreelancerProfileServices_labora/
├── freelancer_profile_service/     # Django project settings
│   ├── __init__.py
│   ├── settings.py                 # Django configuration
│   ├── urls.py                     # Project URL routing
│   ├── asgi.py                     # ASGI configuration
│   └── wsgi.py                     # WSGI configuration
├── profiles/                        # Main application
│   ├── migrations/                 # Database migrations
│   ├── __init__.py
│   ├── admin.py                    # Django admin setup
│   ├── apps.py                     # App configuration
│   ├── models.py                   # Database models
│   ├── views.py                    # API views
│   ├── serializers.py              # DRF serializers
│   ├── urls.py                     # App URL routing
│   └── tests.py                    # Unit tests
├── media/                          # User uploaded files
│   └── freelancer_profiles/        # Profile images
├── manage.py                       # Django management script
├── db.sqlite3                      # SQLite database (dev)
├── .env                            # Environment variables
├── .gitignore                      # Git exclusions
└── README.md                       # This file
```

## 🔄 Profile Workflow

### 1. Creating a Profile
1. Client sends POST request to `/api/profile/add/`
2. Server validates the input data
3. Profile is created in database
4. Skills are associated if provided
5. Profile image is stored in media directory
6. Success response with message is returned

### 2. Viewing a Profile
1. Client sends GET request with `user_id` parameter
2. Server retrieves profile from database
3. Related skills are included in response
4. Profile image URL is generated
5. Complete profile data is returned

### 3. Updating a Profile
1. Client sends PATCH/PUT request with `user_id` and data to update
2. Server finds the profile
3. Specified fields are updated (partial update supported)
4. Updated timestamp is automatically set
5. Confirmation message is returned

### 4. Deleting a Profile
1. Client sends DELETE request with `user_id`
2. Server finds and deletes the profile
3. Associated media files can be cleaned up
4. Success response is returned

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test profiles
```

### Run Specific Test Class
```bash
python manage.py test profiles.tests.FreelancerProfileTestCase
```

### Run with Verbose Output
```bash
python manage.py test profiles -v 2
```

## 🐛 Troubleshooting

### Issue: Image Upload Returns 400 Error
**Solution:** Ensure Pillow is installed and media directory exists:
```bash
pip install pillow
mkdir -p media/freelancer_profiles
python manage.py collectstatic
```

### Issue: Profile Not Found When Creating
**Solution:** Verify user_id is unique and correctly formatted:
```bash
# Check database for existing profiles
python manage.py shell
>>> from profiles.models import FreelancerProfile
>>> FreelancerProfile.objects.filter(user_id=101).exists()
```

### Issue: JWT Authentication Failed
**Solution:** Verify JWT_SIGNING_KEY matches your Auth Service:
```bash
# Check environment variables
echo $JWT_SIGNING_KEY
echo $JWT_ALGORITHM
```

### Issue: Permission Denied on Media Upload
**Solution:** Check file permissions and media directory:
```bash
chmod -R 755 media/
ls -la media/freelancer_profiles/
```

### Issue: Database Migration Errors
**Solution:** Reset migrations in development:
```bash
# Backup database first!
python manage.py migrate profiles zero
python manage.py migrate
```

## 🚀 Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure strong `DJANGO_SECRET_KEY`
- [ ] Use environment variables for sensitive data
- [ ] Set up proper database (MySQL/PostgreSQL)
- [ ] Configure media file storage (AWS S3 recommended)
- [ ] Set up logging and monitoring
- [ ] Configure CORS if needed
- [ ] Set up database backups
- [ ] Use HTTPS/SSL in production
- [ ] Configure proper file permissions
- [ ] Test JWT integration with Auth Service

## 📝 Environment Variables

### Required
- `DJANGO_SECRET_KEY`: Django secret key (min 50 chars for production)
- `JWT_SIGNING_KEY`: JWT signing key (should match Auth Service)

### Recommended
- `DEBUG`: Set to "False" for production
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Optional (Production Database)
- `DB_ENGINE`: Database backend (default: sqlite3)
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port

### Optional (Media Storage)
- `MEDIA_URL`: URL prefix for media files (default: /media/)
- `MEDIA_ROOT`: File system path to media (default: ./media)

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Pillow Image Library](https://pillow.readthedocs.io/)
- [Django File Uploads](https://docs.djangoproject.com/en/stable/topics/files/)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add new feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## 📄 License

This project is part of the Labora Backend platform. All rights reserved.

## 📧 Support

For issues, questions, or suggestions, please:
1. Check existing GitHub issues
2. Create a new issue with detailed information
3. Contact the development team

## 🔗 Related Services

- **MessageService**: Real-time messaging between users
- **JobService**: Job posting and management
- **AuthService**: User authentication and authorization
- **NotificationService**: Event-based notifications

---

**Last Updated:** May 2024  
**Version:** 1.0.0  
**Maintained by:** Labora Backend Team
