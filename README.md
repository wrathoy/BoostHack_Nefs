❗ Problem Being Solved In Algeria, many cancer patients travel long distances from other Wilayas to CAC Batna just to request an appointment, often waiting hours or even sleeping outside the hospital.

NEFS solves this by:

Allowing patients to book online for next-day appointments

Helping admins schedule and assign time slots based on queue

Displaying a live countdown and generating PDF receipts

Making the system more human, efficient, and accessible

## 🧪 Tech Stack :
Python 3 /
Html / Css / JavaScriot

Flask — Web framework

Flask-Session — Session management

SQLite3 (raw) — Lightweight database

ReportLab — PDF receipt generation

Jinja2 — Templating engine (rendering pages)

## ⚙️ Setup & Run Instructions

Clone the project bash Copy Edit git clone https://github.com/your-username/nefs-backend.git cd nefs-backend
Create virtual environment (optional but recommended) bash Copy Edit python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate
Install requirements bash Copy Edit pip install -r requirements.txt
Run the server bash Copy Edit ## **python run.py** Server will start on http://127.0.0.1:5000

## Future Improvements:

Add email/SMS notifications upon approval

Allow appointment cancellation or rescheduling

Build full React frontend connected to this backend (API mode)

Track no-shows and reassign time slots (auto-waitlist)

Add multi-day queue (plan for next 3–5 days in advance)

Include QR code on PDF receipts for easy scanning ⬇
⬇
