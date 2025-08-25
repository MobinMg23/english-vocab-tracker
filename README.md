English Vocab Tracker
=====================

A comprehensive Django-based web application to help users track and improve their English vocabulary using daily missions, learning targets, and progress monitoring.

----------------------------
🚀 Features
----------------------------
- User Authentication (Login, Signup, Token-based auth)
- Vocabulary Management (Add, update, review words)
- Daily Missions (Auto-generated tasks to improve consistency)
- Learning Targets (Set personal learning goals)
- Activity Monitoring (Track user activity and learning progress)
- Asynchronous Tasks with Celery (e.g. reminders, daily mission creation)
- Dockerized development and deployment
- CI/CD Integration with GitHub Actions

----------------------------
🛠️ Tech Stack
----------------------------
- Backend: Django, Django REST Framework
- Task Queue: Celery + Redis
- Database: PostgreSQL
- Containerization: Docker, Docker Compose
- DevOps: GitHub Actions (CI/CD)
----------------------------
🧪 Getting Started
----------------------------
Prerequisites:
- Python 3.10+
- Docker & Docker Compose

Setup:
$ git clone https://github.com/MobinMg23/english-vocab-tracker.git
$ cd english-vocab-tracker
$ docker-compose up --build
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser

----------------------------
🧪 Run Tests
----------------------------
$ docker-compose exec web python manage.py test

----------------------------
🧠 API Endpoints (Sample)
----------------------------
| Method | Endpoint                  | Description                   |
|--------|---------------------------|-------------------------------|
| POST   | /api/auth/register/       | Register new user             |
| POST   | /api/auth/login/          | User login                    |
| GET    | /api/words/               | Get user words                |
| POST   | /api/words/               | Add new word                  |
| GET    | /api/missions/daily/      | Get today's daily mission     |
| POST   | /api/targets/             | Set learning target           |

----------------------------
📦 Deployment
----------------------------
This project is ready for production deployment using Docker. You may deploy it to services like:
- Heroku (with Docker)
- AWS ECS / EC2
- Render
- Railway

----------------------------
👤 Author
----------------------------
Mobin Goodarzian – mobin.1383.goodarziyan@gmail.com

