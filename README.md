# research_collaboration-platform
# Research Collaboration Platform

Django-based platform for researchers to collaborate, find problems, and manage projects.

## Quick Setup

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Create Database
In MySQL:
```sql
CREATE DATABASE research_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Database
Edit `research_fb/settings.py` - Update MySQL password:
```python
DATABASES = {
    'default': {
        'PASSWORD': 'your_mysql_password_here',  # Change this
    }
}
```

### 4. Setup Database
```bash
python manage.py migrate
python manage.py generate_data
```

### 5. Run Server
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000/

## Features
- Simple Login (dropdown selection)
- User Profiles & Search
- World Feed & Posts
- Problem Search (color-coded severity)
- Project Management
- Collaboration Requests & Notifications

## Team
- Muwafiq Khan Josh (23201414)
- Ahmed Rahman (23201501)
- Sadia Akter (23201645)

CSE370 Database Systems Project - Fall 2025
