# Integrity Challenge - Django Blog

Welcome to our coding challenge! A simple, modern blog application built with Django 5.0 and Bootstrap 5. This project includes user authentication, blog post creation/management, and a responsive design.

This challenge is intended to take under 4 hours. Use your best judgment and document any decisions and assumptions you make a long the way.

We will do a group review once complete.

## Getting Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager


### Installation
1. Fork this repository
2. Clone your forked repository
3. Create and activate a virtual environment:
   - ```python -m venv env```
   - ```source env/bin/activate  # On Windows: .\env\Scripts\activate```
4. Configure environment variables:
    - Create .env file in the project root
    ```
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```
> For internal users, check our password manager for the Encrypto Key labeled "Encrypto for Shell/Citgo" to decrypt the `.env.crypto` file.`
5. Install dependencies:
    - ```pip install -r requirements.txt```
6. Run migrations:
    - ```cd blog_project```
    - ```python manage.py makemigrations```
    - ```python manage.py migrate```

6. Create a superuser (this will be the user you use to access the admin and/or post blogs directly on the frontend):
    - ```python manage.py createsuperuser```

7. Start the development server:
    - ```python manage.py runserver```
    - The application will be available at http://127.0.0.1:8000

## The Challenge

### Tasks

1. **Add Comment Functionality Under Blog Posts:** Please use the current code base and add comment functionality to the blog entries. For bonus credit, make the comments reviewable on the django admin and allowed to be removed at any point. 
2. **Code Documentation:** Add detailed docstrings to all classes and functions explaining what they do and why they are needed.

### Requirements

- Write clean, maintainable code
- Follow SOLID principles where applicable
- Make meaningful git commits

### Bonus Points

- Add additional features that you think would be valuable
- Improve the UI/UX
- Add comprehensive test coverage
- Implement performance optimizations
- Add proper error handling
- Implement proper form validation

### Evaluation Criteria

- Code quality and organization
- Problem-solving approach
- Git commit history
- Test coverage
- Documentation
- UI/UX quality
- Performance quality

### Submission

1. Push your changes to your forked repository
2. Create a Pull Request to the original repository
3. Include a description of your changes and any decisions you made
