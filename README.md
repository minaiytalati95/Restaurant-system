# Restaurant Backend & Frontend

A full-stack restaurant management application with a FastAPI backend and a React (Vite) frontend.

## Project Structure

- `/app`: FastAPI backend application logic, models, and API routes.
- `/frontend`: Vite-based React frontend.
- `/Dataset`: CSV data files for initial data loading.
- `main.py`: Entry point for the FastAPI server.
- `load_data.py`: Script to load CSV data into the SQLite database.

## Setup

### Backend

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`
