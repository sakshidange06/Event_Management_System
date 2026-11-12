# 🎉 Event Management System

A web application to create, organize and track events, built with **Python, Flask and Bootstrap**, with a modern dark UI. Event data is stored in an Excel file (OpenPyXL), so there is **no database setup** needed.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![Storage](https://img.shields.io/badge/Storage-Excel%20(OpenPyXL)-217346?logo=microsoftexcel&logoColor=white)
![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render&logoColor=white)

### 🌐 Live Demo: [https://event-management-system-71o9.onrender.com](https://event-management-system-71o9.onrender.com)

> Hosted on Render's free plan. If the site has been idle, the first load can take about a minute while it wakes up.

---

## 📌 Table of Contents
- [Live Demo](#-live-demo)
- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [How to Use](#-how-to-use)
- [Data Storage](#-data-storage)
- [Application Routes](#-application-routes)
- [Security](#-security)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Future Scope](#-future-scope)
- [Author](#-author)

---

## 🌐 Live Demo

**Try it here:** [https://event-management-system-71o9.onrender.com](https://event-management-system-71o9.onrender.com)

1. Open the link and click **Register** to create an account.
2. Log in and add, edit, search and delete events.

> ⚠️ **Demo note:** the free hosting plan has a temporary file system, so `data.xlsx` (users and events) can be reset when the service restarts or redeploys. Please treat the live site as a demo, and register again if your account is gone.

---

## 📖 About the Project

Organizing events with notebooks and spreadsheets is slow and error-prone. The **Event Management System** gives organizers one place to register, log in, and manage every event: its title, category, date, time, venue, organizer and capacity.

The storage layer is kept separate (`storage.py`), so the Excel file can later be replaced with **MySQL** without rewriting the routes.

---

## ✨ Features

| Feature | Status |
|---|---|
| User registration | ✅ |
| Login and logout (session based) | ✅ |
| Add new events | ✅ |
| View all events | ✅ |
| Update events | ✅ |
| Delete events (with confirmation) | ✅ |
| Search by keyword and filter by category | ✅ |
| Data storage in Excel (OpenPyXL) | ✅ |
| Dark, responsive UI (Bootstrap + custom CSS) | ✅ |
| Deployed online on Render | ✅ |
| Dashboard with event statistics | 🔜 |
| Report generation with CSV download | 🔜 |

> Mark 🔜 items as ✅ once you have built them.

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML, CSS, Bootstrap 5 |
| Fonts | Sora and Inter (Google Fonts) |
| Database | Excel using OpenPyXL |
| IDE | VS Code |
| Browser | Chrome |

---

## 📁 Project Structure

```
Event_Management/
├── app.py                # Flask routes (auth, event CRUD, search)
├── storage.py            # Excel read/write layer (OpenPyXL)
├── requirements.txt      # Python dependencies (includes gunicorn)
├── data.xlsx             # Created automatically on first run
├── README.md
├── templates/
│   ├── base.html         # Common layout (navbar, alerts)
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── events.html       # Event list with search and filter
│   └── event_form.html   # Shared add/edit form
└── static/
    └── style.css         # Dark theme styling
```

---

## ⚙️ Installation and Setup

**Prerequisites:** Python 3.10 or newer, and Google Chrome.

**1. Get the project**
```bash
git clone https://github.com/<your-username>/Event_Management.git
cd Event_Management
```
Or download the ZIP and extract it.

**2. Create and activate a virtual environment**
```powershell
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the application**
```bash
python app.py
```

**5. Open in the browser**

Go to **http://127.0.0.1:5000**

---

## 🚀 How to Use

1. Click **Register** and create an account.
2. **Log in** with your email and password.
3. Click **Add Event**, fill in the details and save.
4. On the **Events** page you can search, filter by category, **Edit** or **Delete** any event.
5. Click **Logout** when you are done.

---

## 🗄 Data Storage

Data lives in `data.xlsx`, which is created automatically the first time you run the app.

**Users sheet**

| Column | Description |
|---|---|
| id | Auto-increment number |
| name | Full name |
| email | Unique, used to log in |
| password | Hashed (never plain text) |

**Events sheet**

| Column | Description |
|---|---|
| id | Auto-increment number |
| title | Event name |
| category | Conference, Workshop, Seminar, Cultural, Sports, Wedding, Party, Other |
| date / time | When the event happens |
| venue | Location |
| organizer | Person or group in charge |
| capacity | Number of seats |
| description | Optional details |
| created_by | Name of the user who added it |

---

## 🔗 Application Routes

| Route | Method | Purpose |
|---|---|---|
| `/register` | GET, POST | Create an account |
| `/login` | GET, POST | Log in |
| `/logout` | GET | Log out |
| `/` | GET | Redirects to the events list |
| `/events` | GET | View, search and filter events |
| `/events/add` | GET, POST | Add a new event |
| `/events/<id>/edit` | GET, POST | Update an event |
| `/events/<id>/delete` | POST | Delete an event |

---

## 🔒 Security

- Passwords are hashed with Werkzeug (`generate_password_hash`), never stored as plain text.
- Pages are protected with a `@login_required` decorator.
- Delete actions use POST requests with a confirmation prompt.
- **Before deploying,** change `app.secret_key` in `app.py` to a long random value and set `debug=False` (Gunicorn on Render already ignores `debug`).

---

## ☁️ Deployment

The app is deployed on **Render** (free plan) and connected to this GitHub repository, so every push to the main branch triggers a new deploy.

| Setting | Value |
|---|---|
| Language | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Instance Type | Free |

**To deploy your own copy:**
1. Fork or push the project to your GitHub account.
2. Make sure `gunicorn` is listed in `requirements.txt`.
3. On [render.com](https://render.com), click **New → Web Service**, connect the repo and use the settings above.

**Limitations of the free plan:** the service sleeps after about 15 minutes without traffic, and files such as `data.xlsx` are not kept permanently. For lasting data, move storage to a database (see Future Scope).

---

## 📸 Screenshots

Add your screenshots to a `screenshots/` folder and link them here.

| Login | Events List |
|---|---|
| ![Login](screenshots/login.png) | ![Events](screenshots/events.png) |

| Add Event | Dashboard |
|---|---|
| ![Add Event](screenshots/add-event.png) | ![Dashboard](screenshots/dashboard.png) |

---

## 🔮 Future Scope

- Dashboard with totals, upcoming and past events, and category charts
- Report generation with filters and CSV download
- Migration from Excel to **MySQL or PostgreSQL** so data survives restarts on Render
- Attendee registration for events with seat limits
- Admin and user roles
- Event poster image upload
- Email confirmations and reminders

---

## 👤 Author

**Sakshi Dange**
GitHub: [@sakshidange06](https://github.com/sakshidange06)

---

⭐ If you found this project useful, consider giving it a star!
