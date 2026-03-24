# Phishing Website Detection Web App

## Problem Statement

Phishing websites are malicious websites designed to trick users into sharing sensitive information such as passwords, banking details, and personal data. These websites often look similar to legitimate websites, which makes manual identification difficult for normal users.

The main goal of this project is to build an end-to-end web application that can analyze a website URL and detect whether it is **legitimate** or **phishing**. This system uses machine learning along with URL-based and webpage-based feature extraction to classify websites.

This project is useful because phishing attacks are one of the most common cybersecurity threats, and an automated detection system can help users identify risky websites quickly.

---

## Dataset Source

The dataset used in this project is the **Phishing Websites Dataset** from the **UCI Machine Learning Repository**.

The dataset contains handcrafted phishing-related website features and a target column named **Result**, where:

- `1` = Legitimate website
- `-1` = Phishing website

The original dataset file used in this project was:

- `Training Dataset.arff`

The dataset contains:

- **11055 rows**
- **31 columns**
- **30 input features**
- **1 target column**

---

## Top 21 Features Used in This Project

For practical real-time prediction, a deployable subset of **21 features** was used. These features were selected because they can be extracted from the URL and webpage during runtime.

### Final 21 Features

1. having_IP_Address  
2. URL_Length  
3. Shortining_Service  
4. having_At_Symbol  
5. double_slash_redirecting  
6. Prefix_Suffix  
7. having_Sub_Domain  
8. SSLfinal_State  
9. Favicon  
10. HTTPS_token  
11. Request_URL  
12. URL_of_Anchor  
13. Links_in_tags  
14. SFH  
15. Submitting_to_email  
16. Abnormal_URL  
17. Redirect  
18. on_mouseover  
19. RightClick  
20. popUpWidnow  
21. Iframe  

These features were chosen because they are more suitable for a real-world phishing detection web app than some other dataset features such as Page Rank, DNS record, web traffic, or domain age, which are harder to extract reliably during live prediction.

---

## Models Used

### 1. Logistic Regression
Logistic Regression is a simple and widely used classification algorithm. It works well when the relationship between input features and output is relatively linear. It is often used as a strong baseline model in machine learning classification tasks.

### 2. Decision Tree
Decision Tree is a rule-based model that splits data into branches based on feature values. It is easy to understand, easy to explain, and works well with categorical or encoded feature values. It was one of the strongest models in this project.

### 3. Random Forest
Random Forest is an ensemble model that combines multiple decision trees. It improves stability and reduces overfitting compared to a single decision tree. It produced very strong performance on this phishing detection dataset.

---

## Model Performance

### Full Feature Model Performance

| Model | Accuracy |
|------|----------|
| Random Forest | 0.9742 |
| Decision Tree | 0.9711 |
| Logistic Regression | 0.9290 |

### Practical 21-Feature Model Performance

| Model | Accuracy |
|------|----------|
| Decision Tree | 0.9561 |
| Random Forest | 0.9557 |
| Logistic Regression | 0.9249 |

### Final Observation

The full feature model achieved the highest accuracy, but not all features were practical for real-time deployment.  
For deployment, the 21-feature subset was selected because it allows live feature extraction from the given URL and webpage.  
The Decision Tree model was chosen for the deployed application because it gave strong performance and was simple to integrate into the end-to-end system.

---

## How the 21 Features Are Extracted

The final prediction system does not depend on manual user entry of all 21 features. Instead, the user only enters a website URL, and the backend automatically extracts the required features.

These 21 features are extracted in **three categories**:

---

## 1. URL-Based Features

These features are extracted directly from the URL string without opening the webpage.

### Features:
- having_IP_Address  
- URL_Length  
- Shortining_Service  
- having_At_Symbol  
- double_slash_redirecting  
- Prefix_Suffix  
- having_Sub_Domain  
- HTTPS_token  
- Abnormal_URL  

### Explanation

These features help identify suspicious patterns in the URL itself. For example, a phishing URL may use an IP address instead of a domain name, may contain an `@` symbol, may use shortened URLs, or may contain unusual subdomains and prefix-suffix patterns.

This type of feature extraction is fast and useful because it does not require webpage loading. It provides the first layer of phishing detection.

---

## 2. Webpage-Based Features

These features are extracted after fetching and parsing the webpage content.

### Features:
- Favicon  
- Request_URL  
- URL_of_Anchor  
- Links_in_tags  
- SFH  
- Submitting_to_email  
- on_mouseover  
- RightClick  
- popUpWidnow  
- Iframe  

### Explanation

These features are based on the HTML structure and webpage behavior. For example, phishing pages may use external favicon sources, suspicious anchor links, unusual form actions, hidden iframes, popup windows, or scripts that disable right-click.

This layer improves detection because some phishing signals cannot be identified from the URL alone. It helps capture suspicious webpage design and behavior.

---

## 3. Request / Security / Response-Based Features

These features depend on the final request response and website security behavior.

### Features:
- SSLfinal_State  
- Redirect  

### Explanation

These features are related to how the website responds when accessed. For example, the system checks whether the final page uses HTTPS and whether multiple redirects occur during access.

These signals are important because phishing websites often have poor SSL behavior or unusual redirect patterns. This provides another useful layer of live detection.

---

## Project Workflow

1. Load and understand the phishing dataset  
2. Clean the dataset and convert feature values to integer format  
3. Map the target column into machine learning friendly labels  
4. Train multiple classification models  
5. Compare model performance  
6. Select a practical 21-feature subset for deployment  
7. Save the trained model and feature names  
8. Build feature extraction modules for URL and webpage analysis  
9. Build a Python ML service for prediction  
10. Connect Node.js backend to the Python ML service  
11. Connect React frontend to the Node backend  
12. Display phishing prediction and extracted feature analysis in the web app  

---

## Technologies Used

### Machine Learning and Backend Logic
- Python
- Pandas
- Scikit-learn
- Joblib
- Requests
- BeautifulSoup

### Python ML Service
- Flask
- Flask-CORS

### Node Backend
- Node.js
- Express.js
- Axios
- dotenv
- CORS

### Frontend
- React.js
- JavaScript
- Vite
- CSS

---

## Web Application Overview

The web application allows the user to enter a website URL and receive a phishing prediction. The system automatically extracts phishing-related features from the URL and webpage, passes them to the machine learning model, and returns the result.

The frontend displays:

- entered URL
- prediction result
- risk level
- confidence score
- extracted security signals

This makes the application practical, interactive, and suitable for real-time phishing website analysis.

---

## Project Structure

```text
phishing_website_detection/
│
├── client/
├── server/
├── ml_service/
├── notebooks/
└── .gitignore
