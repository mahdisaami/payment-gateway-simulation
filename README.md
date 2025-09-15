# 💳 Payment Gateway Simulation Project

This project is a **Django-based payment gateway simulator**.  
It allows you to integrate multiple packages (e.g., subscription purchase, digital products, etc.) into a single system. Each purchase flows through the `Purchase` model, then generates a `Payment`, and finally connects to a simulated payment gateway.  

The project also supports **internationalization (i18n)** for multiple languages.

---

## 🔹 Features

- Create **purchases** for different packages (e.g., subscription plans).  
- Each purchase generates a related **payment record**.  
- Simulated **payment gateway connection to Zarinpal**.  
- **Signals**:  
  - After successful payment, the `is_paid` flag in the `Purchase` is set to `True`.  
- Basic **internationalization (i18n)** support for English and Persian.  

---

## 🔹 Tech Stack

- Python 3.x  
- Django 5.x  
- PostgreSQL (configurable)  
- Memcached

---