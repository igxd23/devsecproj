AI-Based Real-Time Engine Health Monitoring System

A DevSecOps-enabled real-time engine telemetry monitoring system that uses Machine Learning for anomaly detection and fault prediction.

The project combines:

* Real-time telemetry simulation
* Isolation Forest anomaly detection
* Random Forest fault prediction
* Streamlit live dashboard
* FastAPI prediction API
* Docker containerization
* GitHub Actions CI/CD
* Security scanning using Bandit and pip-audit

⸻

Features

* Real-time engine monitoring dashboard
* Live Plotly telemetry graphs
* Manual engine parameter control
* Real-time anomaly detection
* Fault prediction system
* Synthetic telemetry data generation
* CI/CD pipeline automation
* Static security scanning
* Dependency vulnerability scanning
* Dockerized deployment
* Swagger API testing

⸻

Tech Stack

Layer	Technology
Frontend	Streamlit
Backend API	FastAPI
Machine Learning	scikit-learn
Visualization	Plotly
CI/CD	GitHub Actions
Security	Bandit, pip-audit
Containerization	Docker
Testing	Pytest
Data Processing	Pandas, NumPy

⸻

Machine Learning Models

Isolation Forest

Used for:

* anomaly detection
* unusual engine behavior detection

Random Forest

Used for:

* fault prediction
* operational condition classification

⸻

Features Used

* RPM
* Temperature
* Fuel Efficiency
* Vibration X/Y/Z
* Torque
* Power Output
* Operational Mode
* Vibration Magnitude
* Moving Average Features

⸻

Project Structure

devsecproj/
│
├── app.py
├── api.py
├── requirements.txt
├── Dockerfile
├── vehicle_pipeline.pkl
├── engine_failure_dataset.csv
├── main.ipynb
│
├── tests/
│   └── test_basic.py
│
├── .github/
│   └── workflows/
│       └── devsecops.yml
│
└── README.md

⸻

Installation

Clone Repository

git clone https://github.com/igxd23/devsecproj.git
cd devsecproj

⸻

Create Virtual Environment

python -m venv .venv

Activate environment:

source .venv/bin/activate

⸻

Install Dependencies

pip install -r requirements.txt

⸻

Run Streamlit Dashboard

streamlit run app.py

Open:

http://localhost:8501

⸻

Run FastAPI Server

uvicorn api:app --reload --port 8001

Open Swagger UI:

http://127.0.0.1:8001/docs

⸻

Run Tests

pytest

⸻

Run Security Scans

Bandit

bandit -r . --exclude ./tests

pip-audit

pip-audit

⸻

Docker Setup

Build Docker Image

docker build -t engine-monitor .

Run Docker Container

docker run -p 8501:8501 engine-monitor

⸻

CI/CD Pipeline

The GitHub Actions pipeline automatically performs:

* dependency installation
* testing using Pytest
* security scanning using Bandit
* dependency scanning using pip-audit
* Docker image build verification

Workflow file:

.github/workflows/devsecops.yml

⸻

Security Features

* Static Application Security Testing (SAST)
* Dependency vulnerability scanning
* Non-root Docker container
* Automated CI/CD validation

⸻

Real-Time Dashboard Features

* Live telemetry simulation
* Interactive engine controls
* RPM and temperature monitoring
* Anomaly detection alerts
* Fault prediction alerts
* Plotly live graphs
* Safe operating ranges

⸻

API Example

POST /predict

Example Request:

{
  "RPM": 2000,
  "Temperature": 60,
  "Fuel_Efficiency": 15,
  "Vibration_X": 0.5,
  "Vibration_Y": 0.5,
  "Vibration_Z": 0.5,
  "Torque": 200,
  "Power": 80,
  "Operational_Mode": 0
}

Example Response:

{
  "anomaly": 0,
  "fault": 0
}

⸻

Future Improvements

* Real sensor integration
* MQTT/Kafka telemetry streaming
* Deep Learning models
* Kubernetes deployment
* Cloud monitoring integration
* Predictive maintenance analytics

⸻

Author

Igxd

Engineering Student | Quant Developer & AI Systems Enthusiast

⸻

License

This project is for educational and research purposes.