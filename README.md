# Breast Cancer Diagnosis Prediction

This project is a Minimum Viable Product (MVP) and part of the "Qualidade de Software, Segurança e Sistemas Inteligentes" course, which is part of the Software Engineering Postgraduate Program at Pontifical Catholic University of Rio de Janeiro (PUC-Rio). It comprises:

- An API developed in Python using Flask, along with the creation of a database containing the **patients** table.
- The development of classification Machine Learning models to predict breast cancer.
- A frontend developed with Streamlit framework.

The dataset used in this project is the "Breast Cancer Wisconsin (Diagnostic)"

https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic

---
## Installation

### 1. Clone the repository:

```
git clone https://github.com/FernandoMiyazaki/puc-rio-mvp2-qualidade-seguranca-sistemas-inteligentes.git
```

### 2. Open the repository:

```
cd puc-rio-mvp2-qualidade-seguranca-sistemas-inteligentes
```

### 3. Create and activate a virtual environment

**Windows**

```
python -m venv venv
```
```
.\venv\Scripts\activate
```

**Mac/Linux**

```
python3 -m venv venv
```
```
source venv/bin/activate
```

### 4. Install the Python libraries listed in `requirements.txt`.

```
pip install -r requirements.txt
```

### 5. Run the API:

```
cd api
```
```
start python app.py
```

### 6. Access the application documentation:

Open [http://127.0.0.1:5000] in your browser.

### 5. Run the Streamlit app (frontend):

```
cd ..
```
```
streamlit run front/streamlit_app.py
```

The Streamlit UI runs on: [http://localhost:8501/]