# 🚚 Smart Shipping Quote App

**Smart Shipping Quote App** is a backend and web-based tool that calculates delivery fees dynamically based on cart value, delivery distance, item count, and time of day. Built with Python, FastAPI and Streamlit, it provides real-time shipping cost estimates for e-commerce platforms and logistics operations.

---

### 🔗 Live Demo

[![Live App](https://img.shields.io/badge/Try%20It%20Live-Streamlit-brightgreen?style=for-the-badge)](https://smart-shipping-quote-app-wgs5spspjd7k6g4tmcyzuu.streamlit.app/)

---

## 🛠️ Tech Stack

- **Python 3.10**
- **FastAPI** – backend API logic
- **Streamlit** – interactive web interface
- **Pydantic** – data validation
- **Docker** – deployment-ready containers
- **Pytest** – testing with 100% coverage

---

## 🚀 Features

- 📦 Calculates delivery fees based on:
  - Cart value
  - Delivery distance
  - Number of items
  - Time of day (e.g., rush hour)
- 🌐 Web interface + REST API
- 📄 Auto-generated Swagger UI
- ✅ 100% tested logic with `pytest`
- 🐳 Fully Dockerized for local development

---

## 📦 Sample API Request

```json
POST /delivery-fee

{
  "cart_value": 790,
  "delivery_distance": 2235,
  "amount_of_items": 4,
  "time": "2024-01-15T13:00:00Z"
}

## 👩🏻‍💻 Author
Maria Almeida
Machine Learning Engineer in training – turning code into real-world solutions.
