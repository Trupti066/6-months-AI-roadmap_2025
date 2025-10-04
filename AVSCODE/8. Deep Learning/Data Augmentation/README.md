# Data Augmentation App
This project demonstrates Data Augmentation in Deep Learning with an interactive Streamlit Web App.\
You can upload one or more images, choose a fill_mode, and generate augmented samples for training deep learning models.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 📌 Features
Upload multiple images (JPG, PNG).\
Choose from 4 fill modes (nearest, reflect, wrap, constant) or use Mix Mode (all together).\
Set how many augmented images to generate per input image.\
Preview augmented samples instantly.\
Download all results as a ZIP file.\
Beautiful custom UI with background, glowing buttons, and floating cards.\
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 🚀 How to Run
1. Clone this repo or copy the code.
2. Install dependencies:
      pip install -r requirements.txt
3 . Run the app:
      streamlit run app.py
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📂 Project Structure
Data_Aurgumentaion/
│── app.py              # Streamlit app
│── bg.avif             # Background image
│── Output/             # Folder with screenshots
│── Day78_Data_Augmentation.ipynb  # Documentation notebook
│── requirements.txt    # Dependencies
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📸 Screenshots
1️⃣ Overall App Look
<img width="1920" height="1080" alt="Frontend_View" src="https://github.com/user-attachments/assets/795a6496-1c97-4b3e-a36c-572c9e680e47" />
2️⃣ Upload Images & Select Mode
<img width="1920" height="1080" alt="Screenshot (285)" src="https://github.com/user-attachments/assets/de4a08aa-c39d-402f-b2f6-477f162bad66" />
3️⃣ Augmented Images Generated
<img width="1920" height="1080" alt="Mix _all modes_output" src="https://github.com/user-attachments/assets/0fca08f7-b0bf-4e30-9cda-1c26ddb7793a" />
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 🧠 What is Data Augmentation?
Data Augmentation is the process of increasing the diversity of your training dataset by applying small, realistic transformations to existing data. This improves the robustness and generalization of machine learning models.\

Examples include:\

- Rotations, flips, zooms for images
- Synonym replacement or back-translation for text
- Adding noise or scaling for signals
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🙌 Acknowledgements
- TensorFlow/Keras for image augmentation tools.
- Streamlit for making interactive ML apps simple.

📌 Author
👤 Kompally Trupti 🎯 Learning Deep Learning & MLOps | Building daily projects
