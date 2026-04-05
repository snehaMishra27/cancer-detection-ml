# cancer-detection-ml
# 🧬 Cervical Cancer Detection using Machine Learning

A machine learning-based web application that predicts the risk of cervical cancer based on user inputs. The system integrates a trained ML model with a Flask backend and an interactive frontend UI.

---

## 🚀 Features

- Predicts cervical cancer risk using input parameters
- End-to-end ML pipeline (data preprocessing + model)
- Flask backend for API handling
- Interactive frontend (HTML, CSS, JavaScript)
- Reproducible model training script
- Handles missing data and feature scaling
- Option to handle class imbalance

---

## 🛠️ Tech Stack

- **Machine Learning:** scikit-learn (Logistic Regression)
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Libraries:** pandas, numpy, joblib
- **Environment:** Python Virtual Environment (.venv)

---

## 📁 Project Structure
cancerDetectionCode/
│
├── backend/
│ ├── app.py # Flask API
│ ├── train_model.py # Model training script
│ ├── model.pkl # Trained ML model
│
├─ frontend/
│ ├── index.html # UI
│ ├── script.js # API integration
│ ├── style.css # Styling
│
├── requirements.txt # Dependencies
├── cervical-cancer_csv.csv # Dataset
└── README.md


---

## ⚙️ How to Run the Project (Windows)


git clone https://github.com/snehaMishra27/cancer-detection-ml.git
cd cancer-detection-ml/cancerDetectionCode
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python backend\app.py
Backend will start at: http://127.0.0.1:5000
Frontend will run using Live Server

Sample Workflow
User enters input in UI
Frontend sends request to Flask API
Backend loads model.pkl
Prediction is generated
Result displayed on UI

### 🔹 Prediction Output
![Prediction](assets/prediction.png)
![Prediction](assets/prediction2.png)
![Prediction](assets/prediction3.png)

