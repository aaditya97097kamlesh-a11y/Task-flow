# Task Flow

Task Flow is a simple task management application built using FastAPI, SQLite, HTML, CSS and JavaScript.

## Features

- Create a task
- View tasks
- Edit tasks
- Delete tasks
- Set task priority
- Set due date
- Create and view projects
- Project statistics
- REST API using FastAPI
- Swagger API documentation

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript

## How to Run Backend

Open terminal in the backend folder.

Activate virtual environment:

venv\Scripts\activate

Run the FastAPI server:

uvicorn main:app --reload

Backend will run at:

http://127.0.0.1:8000

## API Documentation

Open:

http://127.0.0.1:8000/docs

## How to Run Frontend

Open the frontend/index.html file using Live Server.

The frontend will connect with the FastAPI backend.

## Project Structure

backend/
- database.py
- main.py
- models.py
- schemas.py
- taskflow.db

frontend/
- index.html
- script.js
- style.css

## Conclusion

Task Flow provides basic task and project management functionality with a FastAPI backend and a simple web frontend.