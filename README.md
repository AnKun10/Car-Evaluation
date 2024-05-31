# Car - Evaluation

## Table of Contents
1. [Project Introduction](#1-project-introduction)
2. [Data Preprocessing](#2-data-preprocessing)
3. [Model Usage](#3-model-usage)
4. [Model Evaluation](#4-model-evaluation)

## 1. Project Introduction

### Overview
This project presents our comprehensive research on predicting car prices using a variety of machine learning models trained on data we meticulously crawled from diverse online sources. Our objective is to develop robust models that deliver precise price estimates based on given car specifications, thereby helping users navigate the market with confidence.

### Objectives
To achieve high accuracy and reliability in price estimation, we employed several machine learning techniques, including Support Vector Regression (SVR), K-Nearest Neighbors (KNN), XGBoost, and Decision Trees, ... Additionally, we used stacking models to further enhance the prediction performance. Each model's strengths and weaknesses were rigorously evaluated to provide a comprehensive understanding of their performance. Our innovative approach combines meticulous data crawling, feature engineering, and state-of-the-art algorithms, offering significant practical implications for consumers and other stakeholders in the automotive market. This report details our methodology, findings, and the potential impact of our research on enhancing price assessment and market transparency.

## 2. Data Preprocessing
- Original data path: `Dataset/Original/car_detail_en.csv`. This CSV file includes data crawled from the web and some other sites
- The folder `Dataset/Patial Preprocessing` includes our data after each processing step. There are 5 versions corresponding to our 5 steps of data preprocessing.
- The final version of the data is placed in this folder `Dataset/Final` and includes crawl, analysis, removal of noise, and encoding process.



## 3. Model Usage
Firstly, you must install the required libraries by running the following command:

```sh
pip install -r requirements.txt
```
We tried a total of 10 models in this project. Each of these notebooks includes 1 or 3 models as follows.
   - Bagging: `Model/Main/Bagging.ipynb`
   - Stacking: `Model/Main/Bagging.ipynb`
   - Polynomial Regression: `Model/Main/Polynomial_Regression.ipynb`
   - SVR: `Model/Main/SVR_train.ipynb`
   - Decision Tree, RandomForest and ADaBoost: `Model/Main/Tree Price Prediction.ipynb`

Our MLP Model is too large to push to github, therefore we upload them on this Google Drive link: https://drive.google.com/drive/folders/1JRflRayeU7jh90eTcRB7iSf2y_Q8wb78?usp=sharing

The MLP folder contains two parts: Data Preprocessing and Model, you can run code in every notebook file, all the other files is just data files.      
     
Each notebook file corresponds to one model, which is similar to the file name. Some models require large memory and a long time to train, so we have to train them on Google Colab and Kaggle in the following links:
   - [Stacking](https://www.kaggle.com/code/quangduc3122004/stacking-car-prediction)
   - [Bagging](https://www.kaggle.com/code/quangduc3122004/bagging-ensemble-learning)
   - [Polynomial Regression](https://colab.research.google.com/drive/1WNIX-HT5t7WoxDBkCCn3ygZqvikZrRhx?usp=sharing)
   - [MLP - Hyperparameter Optimization](https://www.kaggle.com/code/tranhuudao/hyperparameteroptimizing)
   - [MLP - Metaheuristic Initialization](https://www.kaggle.com/code/tranhuudao/metaheuristic-initialization)




## 4. Model Evaluation
![Result](https://github.com/AnKun10/Car-Evaluation/blob/main/result.png)


