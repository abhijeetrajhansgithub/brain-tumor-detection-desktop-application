Brain Tumor Detection, Classification, and Segmentation Desktop Application
===========================================================================

Overview
--------
This project is a desktop-based medical imaging application developed to assist
in the detection, classification, and segmentation of brain tumors from MRI
images. The application integrates deep learning models with an interactive
PyQt5 graphical interface, allowing users to manage patient records, analyze
MRI scans, visualize results, and store prediction history securely.

Features
--------
- Brain Tumor Detection from MRI Images
- Brain Tumor Classification using Deep Learning Models
- Tumor Segmentation and Visualization
- Patient Record Management
- User Authentication and Authorization
- MRI Image Upload and Processing
- Prediction History Storage
- SQLite Database Integration
- Interactive PyQt5 Desktop Interface

Technology Stack
----------------
- Python
- PyQt5
- TensorFlow / Keras
- CNN
- Xception
- SQLite
- bcrypt
- SHA-512

Project Structure
-----------------

API/
    Database and Model Communication Modules

Data/
    Application Configuration Files

Database/
    SQLite Database and Database Operations

Documentation/
    Project Documentation and UI References

Globals/
    Global Variables and Configuration Management

Image/
    Application Images, Icons, and Uploaded Images

ImageSegmentationModules/
    Image Processing and Segmentation Modules

Main/
    Main Application Entry Point and Utilities

Models/
    Deep Learning Models and Inference Logic
    - CNN Models
    - Xception Models

Screens/
    PyQt5 User Interface Screens and Dialogs

Temp/
    Temporary Testing and Utility Scripts

Model Capabilities
------------------
- Brain Tumor Detection
- Brain Tumor Classification
- MRI Image Segmentation
- Patient-Specific Prediction Analysis

Security Features
-----------------
- SHA-512 Password Hashing
- bcrypt Authentication
- Salted Password Storage
- Secure User Login System

Application Workflow
--------------------
1. User Login
2. Patient Selection / Registration
3. MRI Image Upload
4. Image Preprocessing
5. Model Inference
6. Tumor Detection
7. Tumor Classification
8. Tumor Segmentation
9. XAI Visualization
10. Result Storage and Retrieval

Key Highlights
--------------
- Developed a complete desktop application for medical image analysis.
- Integrated deep learning models with a user-friendly GUI.
- Implemented patient management and secure authentication systems.
- Combined detection, classification, segmentation, and explainability in a
  single application.
- Utilized SQLite for local patient and prediction data management.

Author
------
Abhijeet Rajhans

License
-------
For educational and research purposes only.