# Full DevOps CI/CD Pipeline: TodoManager

Welcome to the `PythonDevOpsProjects` repository! This project serves as a comprehensive, real-world example of an end-to-end DevOps CI/CD pipeline. The core application is a Python Flask "TodoManager" app that has been fully containerized and automated from development to AWS deployment.

## 🚀 Features
1. **Automated Continuous Integration (CI):** 
   - Code is automatically linted using `flake8` to ensure syntax formatting.
   - Every push triggers Python Unit Tests and Playwright browser tests.
2. **Containerization:** 
   - The application is securely packaged inside an isolated server environment using a `Dockerfile` and the lightweight `python:3.10-slim` image. It runs on a production-grade `gunicorn` web server on port 5000.
3. **Continuous Deployment (CD):** 
   - If tests pass, GitHub Actions automatically builds the Docker image and pushes it to the **GitHub Container Registry (GHCR)**.
   - The pipeline then securely SSHes into an **AWS EC2** instance, pulls the latest image, and spins it up live on the internet! 

## 📂 Project Structure
* `.github/workflows/ci-cd.yml`: The master GitHub Actions script directing the entire DevOps lifecycle.
* `TodoManager/app.py`: The core Python Flask application.
* `TodoManager/test_app.py` & `frontend_test.py`: The backend and frontend test suites.
* `TodoManager/Dockerfile`: The blueprint for building the production application container.
* `TodoManager/requirements.txt`: Master list of dependencies (Flask, Playwright, Gunicorn, etc).

## 🛠️ Running Locally
If you want to run or test the app directly on your laptop without Docker:

1. **Navigate to the App Folder:**
   ```bash
   cd TodoManager
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Flask App:**
   ```bash
   python app.py
   ```
   Open `http://localhost:5000` in your web browser!
4. **Run Tests:**
   ```bash
   python test_app.py
   python frontend_test.py
   ```

## ☁️ Connecting to AWS
This repository is configured to Automatically Deploy to AWS. To activate deployment, create an **EC2 Instance** on AWS (Ubuntu or Amazon Linux), enable HTTP and SSH traffic, and install Docker (`sudo apt install docker.io`).

Then, add these 3 Secrets in your GitHub Repository under **Settings > Secrets and Variables > Actions**:
* `EC2_HOST` : The public IPv4 address of your instance.
* `EC2_USERNAME` : Keep it as `ubuntu` or `ec2-user`.
* `EC2_SSH_KEY` : The raw text inside your `.pem` key file.

Any push to the `master` branch will now automatically build and ship to your server!
