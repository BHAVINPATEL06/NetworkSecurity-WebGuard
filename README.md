# 🛡️ Network Security (WebGuard) ML Project 🛡️

## 📋 Overview
This project is a complete end-to-end machine learning pipeline for network security analysis built during Krish Naik's Machine Learning Bootcamp. It uses advanced ML techniques to detect and classify network security threats from network data.

## 🛠️ Tech Stack
- **🐍 Programming Language**: Python 3.10
- **🚀 Web Framework**: FastAPI
- **🗄️ Database**: MongoDB
- **📊 ML Libraries**:
  - scikit-learn
  - pandas
  - numpy
- **⚙️ MLOps Tools**:
  - MLflow (for experiment tracking)
  - DagsHub (for versioning and collaboration)
- **☁️ Cloud Services**: AWS S3 (for artifact and model storage)
- **🐳 Container**: Docker
- **📚 Other Libraries**:
  - pymongo
  - python-dotenv
  - dill (for object serialization)

## 📁 Project Structure

### 📂 Root Directory
- `app.py`: FastAPI application for serving predictions
- `main.py`: Entry point to run the complete pipeline
- `push_data.py`: Script to push data from CSV to MongoDB
- `setup.py`: Package installation and setup file
- `requirements.txt`: Project dependencies
- `Dockerfile`: Docker containerization configuration

### 📦 Core Directories
- `network_security/`: Main package containing all modules
  - `components/`: Core components of the ML pipeline
    - `data_ingestion.py`: 📥 Data collection from MongoDB
    - `data_validation.py`: ✅ Validate the quality of ingested data
    - `data_transformation.py`: ⚗️ Feature engineering and preprocessing
    - `model_trainer.py`: 🧠 Model training and selection
  - `entity/`: 📝 Data classes for config and artifacts
  - `pipeline/`: 🔄 Pipeline orchestration code
  - `utils/`: 🔧 Utility functions for ML and operations
  - `cloud/`: ☁️ Cloud integration code (S3 syncing)
  - `constants/`: 📋 Project constants
  - `exception/`: ⚠️ Custom exception handling
  - `logging/`: 📝 Logging configuration

### 💾 Data and Artifacts
- `Network_Data/`: 📊 Raw data directory
- `Artifacts/`: 📦 Stores artifacts from each pipeline run
- `final_model/`: 🏆 Contains the final trained model and preprocessor
- `logs/`: 📜 Application logs
- `templates/`: 🖥️ HTML templates for web interface

## 🚀 How to Run the Project

### 📋 Prerequisites
1. 🐍 Python 3.10 or higher
2. 🗄️ MongoDB instance
3. ☁️ AWS account (optional, for S3 storage)

### 🔧 Environment Setup
1. 📥 Clone the repository
   ```bash
   git clone <repository-url>
   cd Network-Security-Machine-Learning-Project
   ```

2. 🔑 Create a `.env` file in the root directory with the following:
   ```
   MONGO_URI=<your-mongodb-connection-string>
   AWS_ACCESS_KEY_ID=<your-aws-access-key>
   AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
   ```

3. 📦 Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install using setup.py:
   ```bash
   pip install -e .
   ```

### 📤 Data Ingestion
1. Push data to MongoDB:
   ```bash
   python push_data.py
   ```

### 🧠 Model Training
Run the complete training pipeline:
```bash
python main.py
```

This will:
1. 📥 Ingest data from MongoDB
2. ✅ Validate the data
3. 🔄 Transform and prepare features
4. 🧪 Train multiple models and select the best one
5. 💾 Save the model artifacts
6. ☁️ Upload artifacts to S3 (if configured)

### 🚀 Running the Prediction Service
Start the FastAPI service:
```bash
python app.py
```

The API will be available at http://localhost:8000 with the following endpoints:
- 📚 `/`: Documentation (redirects to `/docs`)
- 🧠 `/train`: Endpoint to trigger model training
- 🔮 `/predict`: Endpoint to make predictions (requires file upload)

### 🐳 Using Docker
Build and run with Docker:
```bash
docker build -t network-security-ml .
docker run -p 8000:8000 -d network-security-ml
```

## 📊 MLflow Integration
The project integrates with MLflow and DagsHub for experiment tracking:

```python
# Access the experiment tracking interface
# MLflow UI will be available through DagsHub
```

## 🔄 Project Workflow
1. 📤 Data is loaded from a CSV file into MongoDB
2. 📥 Data is ingested from MongoDB
3. ✅ Data is validated against a schema
4. ⚗️ Features are transformed and preprocessed
5. 🧪 Multiple ML models are trained and evaluated:
   - 🌳 Random Forest
   - 🌲 Decision Tree
   - 📈 Gradient Boosting
   - 📊 Logistic Regression
   - 🔋 AdaBoost
6. 🏆 The best model is selected based on performance metrics
7. 💾 The model is saved for deployment
8. 🚀 The model is served via a FastAPI application

