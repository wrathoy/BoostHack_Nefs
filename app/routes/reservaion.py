from flask import Blueprint, render_template, request, session, redirect, url_for, send_file
from app.database import get_db
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

reservation_bp = Blueprint('reservation', __name__)

# 1️⃣ Helper: Timer Logic for Tomorrow Appointments
def get_countdown(estimated_time_str):
    try:
        now = datetime.now()
        est_time = datetime.strptime(estimated_time_str, "%H:%M")
        today_with_est = datetime.combine(now.date(), est_time.time())

        # If appointment is for tomorrow
        if now.time() > est_time.time():
            today_with_est += timedelta(days=1)

        remaining = today_with_est - now
        return max(timedelta(0), remaining)
    except:
        return timedelta(0)


@reservation_bp.route('/', methods=['GET', 'POST'])
def reserve():
    user_id = session.get('user_id')


    conn = get_db()
    cursor = conn.cursor()

    # Check if user already submitted a reservation
    cursor.execute("""
        SELECT * FROM reservations
        WHERE user_id = ?
        ORDER BY id DESC LIMIT 1
    """, (user_id,))
    reservation = cursor.fetchone()

    # POST — form submitted
    if request.method == 'POST' and not reservation:
        age = request.form.get('age')
        reason = request.form.get('reason')
        tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

        cursor.execute("""
            INSERT INTO reservations (user_id, reason, requested_date)
            VALUES (?, ?, ?)
        """, (user_id, reason, tomorrow))
        conn.commit()
        return render_template("user/reservation.html", state='pending')

    # GET view — after submission
    if reservation:
        status = reservation['status']

        if status == 'pending':
            return render_template("user/reservation.html", state='pending')

        elif status == 'confirmed':
            countdown = get_countdown(reservation['estimated_time'])
            return render_template("user/reservation.html", state='confirmed',
                                   estimated_time=reservation['estimated_time'],
                                   countdown=str(countdown),
                                   reservation=reservation)

    # First visit — show form
    return render_template("user/reservation.html", state='new')


@reservation_bp.route('/download_receipt')
def download_receipt():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, u.name, u.last_name, u.phone
        FROM reservations r
        JOIN users u ON u.id = r.user_id
        WHERE r.user_id = ? AND r.status = 'confirmed'
        ORDER BY r.id DESC LIMIT 1
    """, (user_id,))
    res = cursor.fetchone()

    if not res:
        return "No confirmed reservation found."

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "🧾 NEFS - Appointment Confirmation")
    p.drawString(100, 780, f"Full Name: {res['name']}")
    p.drawString(100, 760, f"Last Name: {res['last_name']}")
    p.drawString(100, 760, f"Phone: {res['phone']}")
    p.drawString(100, 740, f"Reason: {res['reason']}")
    p.drawString(100, 720, f"Date: {res['requested_date']}")
    p.drawString(100, 700, f"Estimated Time: {res['estimated_time']}")
    p.drawString(100, 680, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="appointment_receipt.pdf", mimetype='application/pdf')
