# Novella | Premium Book & Reading Hub

Novella is a cinematic web novel platform, bookstore, and reader community hub. Designed with modern aesthetics, vibrant dark ambient glows, elegant typography (Outfit and Playfair Display), and fluid micro-animations.

##  Getting Started

The backend is built in **Python** using the **Flask** microframework to render templates and serve static assets dynamically.

### Prerequisites

- Python 3.8+
- Pip (Python Package Installer)

### Installation & Run

1. Navigate to the `backend/` directory or run from the root:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Run the application:
   ```bash
   python backend/app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Repository Structure

```
novella/
├── backend/
│   ├── app.py                # Python Flask Application Server
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css      # Core premium design tokens and styles
│   │   ├── img/              # Image assets
│   │   └── js/
│   │       ├── alpine-store.js  # Global session, cart, and authentication state
│   │       └── reader-pref.js   # Interactive Web Reader settings store
│   └── templates/
│       ├── base.html         # Base layout with navbar, cart drawer, and login modal
│       ├── landing.html      # Immersive hero section, original works showcase
│       ├── library.html      # Bookstore catalog search, filters, and purchase triggers
│       ├── reader.html       # Web Reader engine with themes, fonts, and comment boards
│       ├── memberships.html  # Pricing tiers comparison, checkout modal, FAQ accordion
│       ├── community.html    # Discussion threads, reader voting polls, and author feeds
│       ├── contact.html      # Help center topics and support ticket validation form
│       └── dashboard/
│           └── author_admin.html # Analytics dashboard for both Readers and Authors
└── README.md                 # Project guide
```

---


