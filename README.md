# 📡 P2P Messaging System with STUN Server

این پروژه یک سیستم پیام‌رسان **همتا به همتا (Peer-to-Peer)** است که با استفاده از یک **STUN-like Server مرکزی** برای کشف همتاها و مدیریت اطلاعات شبکه پیاده‌سازی شده است.  
پروژه شامل سه بخش اصلی است:

1. **STUN Server (Django + SQLite)**
2. **Peer Application (Python CLI)**
3. **Dockerized STUN Server**

---

## 🧱 معماری کلی پروژه

```
NET_Project/
│
├── stun server/        # STUN Server (Django Backend)
│
└── peer/               # Peer Application (Python CLI)
```

- ارتباط **Peer ↔ Peer** از طریق **TCP Socket مستقیم**
- ارتباط **Peer ↔ STUN Server** از طریق **HTTP API**
- STUN Server فقط نقش **Directory + Message Storage** را دارد

---

## 🟢 بخش اول: STUN Server

### 🔧 تکنولوژی‌ها
- Python
- Django
- SQLite

### 📂 ساختار پوشه
```
stun server/
├── conf/
├── server/
├── db.sqlite3
└── manage.py
```

---

## 🗄️ ساختار دیتابیس

### Peer
```python
class Peer(models.Model):
    username = models.CharField(unique=True)
    ip = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    last_seen = models.DateTimeField(auto_now=True)
```

### Friendship
```python
class Friendship(models.Model):
    owner = ForeignKey(Peer)
    friend_username = CharField()
```

### Message
```python
class Message(models.Model):
    sender = ForeignKey(Peer)
    receiver = ForeignKey(Peer)
    content = TextField()
    timestamp = DateTimeField(auto_now_add=True)
```

---

## 🔌 API Endpoints

| Endpoint | Method | توضیح |
|--------|-------|------|
| `/register` | POST | ثبت Peer |
| `/peers` | GET | لیست کاربران |
| `/peerinfo` | GET | اطلاعات Peer |
| `/friend/start/` | POST | شروع دوستی |
| `/friend/get/` | GET | لیست دوستان |
| `/message/create/` | POST | ذخیره پیام |
| `/message/get/` | GET | دریافت پیام‌ها |

---

## 💬 بخش دوم: Peer Application

### فایل‌ها
```
peer/
├── main.py
├── com_server.py
└── utils.py
```

### ویژگی‌ها
- ارتباط مستقیم TCP
- ذخیره پیام‌ها
- message box
- error handling کامل
- CLI تعاملی

---

## 🐳 Docker

### Build
```bash
docker build -t stun-server .
```

### Run
```bash
docker run -p 8000:8000 stun-server
```

---

## 🚀 اجرا

### STUN Server
```bash
python manage.py runserver
```

### Peer
```bash
python main.py
```

---

✍️ Computer Networks Course Project
