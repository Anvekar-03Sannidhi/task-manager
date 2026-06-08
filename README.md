# TaskFlow

Manage tasks, stay productive, and achieve more every day.

## Overview

TaskFlow is a Django-based task management platform designed to help users organize their work, track goals, and improve productivity. It provides an intuitive interface for managing daily tasks, recurring activities, reminders, and long-term goals.

## Features

* Create, update, and delete tasks
* Organize and manage daily activities
* Recurring tasks support

  * Daily
  * Weekly
  * Monthly
  * Yearly
  * Custom recurrence
* Reminder system for important tasks
* Goal tracking and progress monitoring
* User authentication and profile management
* Admin dashboard for management
* PostgreSQL database support
* Responsive and user-friendly interface

## Tech Stack

### Backend

* Django
* Python

### Database

* PostgreSQL

### Frontend

* HTML
* CSS
* JavaScript

### Deployment

* Vercel

## Project Structure

```text
TaskFlow/
├── tasks/
├── task_manager/
├── static/
├── templates/
├── manage.py
└── requirements.txt
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/Anvekar-03Sannidhi/TaskFlow.git
```

2. Navigate to the project directory

```bash
cd TaskFlow
```

3. Create a virtual environment

```bash
python -m venv venv
```

4. Activate the virtual environment

```bash
venv\Scripts\activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Apply migrations

```bash
python manage.py migrate
```

7. Run the development server

```bash
python manage.py runserver
```

## Future Enhancements

* Email notifications
* Calendar integration
* Task analytics dashboard
* Mobile application support

## Live Demo

[Live Demo](https://taskflow-three-sable.vercel.app/)

## Author

Developed by Sannidhi Rajendrakumar Anvekar

GitHub: [Anvekar-03Sannidhi](https://github.com/Anvekar-03Sannidhi)
