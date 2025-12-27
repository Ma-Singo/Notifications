# 📣 Notifications  
### A Multi-Channel Notification Platform by **Notif**

**Notifications** is a production-ready Django application that delivers **Email, SMS, Push, and Webhook notifications** asynchronously using **Celery + Redis**.  
It follows **SOLID principles**, supports **subscription-based access with Stripe**, and provides **exactly-once delivery guarantees** through **idempotency and rate-limiting**.

---

## 🚀 Features

### 🔔 Notification Channels
- 📧 Email
- 📱 SMS
- 🔔 Push notifications
- 🌐 Webhook notifications (signed & retryable)

### ⚙️ Architecture
- Django (API & Admin)
- Celery + Redis (async delivery)
- SOLID-compliant service & provider layers
- Dockerized for production

### 🔐 Authentication
- Django authentication
- `django-allauth` integration
- Custom account emails
- Account event triggers (failed login, password reset, signup)

### 💳 Subscriptions & Billing
- Stripe-based subscription plans
- Free / Pro / Enterprise tiers
- Channel & quota enforcement
- Webhook-driven billing state

### 🧠 Reliability
- Exactly-once delivery (idempotency)
- Redis-backed rate limiting
- Automatic retries with exponential backoff
- Provider isolation

### 📊 Observability
- Metrics hooks (Prometheus-ready)
- Delivery success/failure tracking
- Provider health visibility

---

## 🏗️ System Architecture

```
Client Request
     ↓
NotificationService
     ↓
Idempotency Check
     ↓
Rate Limit Check
     ↓
Subscription Policy
     ↓
Celery Task (Redis)
     ↓
Provider Adapter
     ↓
Email / SMS / Push / Webhook
```

---

## 📁 Project Structure

```bash
notifications/
├── config/
├── accounts/
├── notifications/
│   ├── services/
│   ├── providers/
│   ├── tasks.py
│   └── observability/
├── subscriptions/
├── core/
├── templates/account/
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

---

## ⚙️ Tech Stack

- Python 3.12
- Django
- Celery
- Redis
- Stripe
- Docker
- Prometheus

---

## 🐳 Running the Project

```bash
docker-compose up --build
```

---

## 🔔 Sending a Notification

```python
NotificationService().send(user, payload, "unique-key")
```

---

## 🔐 Security
- Signed webhooks
- Idempotent Stripe events
- Rate-limited delivery
- Email verification enforced

---

## 🏢 About Notif

**Notif** builds scalable, reliable communication infrastructure so modern applications can deliver the right message at the right time.

---

## 📄 License
MIT License
