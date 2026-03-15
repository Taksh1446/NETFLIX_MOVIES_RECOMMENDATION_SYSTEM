# 🎬 Netflix Movie Recommendation System using Machine Learning

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-brightgreen)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-orange?logo=numpy)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-red?logo=scikitlearn)
![TMDB API](https://img.shields.io/badge/API-TMDB-blue)

A **Machine Learning-based Movie Recommendation System** that suggests movies similar to the one selected by the user.

The system uses **Content-Based Filtering** and calculates **movie similarity** to recommend the most relevant movies.

The project also includes a **Netflix-style interactive web application built with Streamlit**.

---

# 🌐 Live Web Application

🚀 **Try the deployed application here**

https://ai-ml-and-ds-projects-ne3p2sm3mnlgcovc8gxzza.streamlit.app/

---

# 📌 Project Overview

Movie recommendation systems are widely used by platforms like **Netflix, Amazon, and YouTube** to improve user experience.

This project builds a **content-based movie recommendation system** that recommends movies based on **similarity between movie features**.

The system analyzes movie attributes such as:

- Genres
- Keywords
- Cast
- Crew
- Movie overview

and recommends movies that are **most similar to the selected movie**.

---

# 🧠 Machine Learning Pipeline

```mermaid
graph TD

A[Load Dataset] --> B[Data Preprocessing]
B --> C[Feature Engineering]
C --> D[Vectorization]
D --> E[Cosine Similarity Calculation]
E --> F[Recommendation System]
F --> G[Streamlit Web Application]
