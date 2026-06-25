Heart Disease Prediction using Federated Learning
I have developed this Privacy-Preserving Federated Learning architecture to predict heart disease risk. Unlike centralized machine learning, I have designed this system to ensure that sensitive patient data remains local at the hospital level, while only the model insights (weights) are shared to train a robust global model.

🏗️ System Workflow
I have structured the workflow to simulate a real-world decentralized hospital network:

Local Data Partitioning (CSV Files): I have split the patient data into multiple CSV files (heart1ex.csv, heart2ex.csv, heart3ex.csv), representing different hospitals (clients).

Local Training (FederatedLearningClient.ipynb): Each client/hospital trains a local model on its private data without sharing it.

Global Aggregation (FederatedLearningCoordinator.ipynb): I have implemented the FedAvg (Federated Averaging) algorithm in the Coordinator to aggregate model weights from all clients and update the global model.

Validation (Accuracy.ipynb): I have validated the aggregated global model against test datasets to ensure high performance.

Deployment (app.py): I have deployed the final heart_disease_model.h5 using a secure Streamlit Web Portal.

🛠️ Tech Stack & Implementation
Federated Learning: I implemented FedAvg to ensure privacy-preserving distributed training.

Backend: I used Python with TensorFlow/Keras for the neural network architecture.

Database: I integrated SQLite3 for secure user authentication, storing encrypted credentials hashed with SHA-256.

Frontend: I built a professional-grade UI using Streamlit, featuring:

Secure Login/Signup portals.

Real-time heart disease risk prediction.

Password hashing for enhanced security.

User Session Management for access control.

🚀 How to Run the Project
Clone the Repository: git clone <your-repo-link>

Install Dependencies:
pip install streamlit tensorflow numpy

Initialize the Database:
Running the app will automatically create hospital_users.db for user management.

Launch the Portal:
streamlit run app.py

🔑 Key Features
Data Privacy: Raw patient data never leaves the hospital server.

Secure Access: I have restricted access to authorized users via a robust SQLite backend.

Modern UI/UX: I designed a clean, card-based interface with large, readable fonts.

Model Accuracy: My global model achieves high accuracy by learning from diverse distributed datasets.

💡 Motivation
In the healthcare sector, data privacy (HIPAA compliance) is critical. Through this project, I demonstrate how decentralized AI can solve the "Data Silos" problem, allowing hospitals to collaborate on better healthcare solutions without compromising patient confidentiality.

Ab yeh tere GitHub ke liye perfect hai! Isme ab tera ownership dikh raha hai. Kuch aur change karna ho toh bata, warna ise seedha GitHub par daal de!
