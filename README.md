# Restaurant Backend & Frontend

A full-stack restaurant management application with a FastAPI backend and a React (Vite) frontend.

## Project Structure

- `/app`: FastAPI backend application logic, models, and API routes.
- `/frontend`: Vite-based React frontend.
- `/Dataset`: CSV data files for initial data loading.
- `main.py`: Entry point for the FastAPI server.
- `load_data.py`: Script to load CSV data into the SQLite database.

## Setup & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/minaiytalati95/Restaurant-system.git
cd Restaurant-system
```

### 2. Backend Setup
1. **Create and activate a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database**:
   Before running the server for the first time, you must load the initial data from the CSV files in the `Dataset` folder.
   ```bash
   python load_data.py
   ```

4. **Run the FastAPI server**:
   ```bash
   python main.py
   ```
   The backend will now be running at `http://127.0.0.1:8000`.

### 3. Frontend Setup
1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```
   The frontend will typically be available at `http://localhost:5173`.

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
