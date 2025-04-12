from datetime import datetime
from flask import render_template



def calculate_countdown(date_str):
    """Calculate countdown to a future date."""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        now = datetime.now()
        
        if target_date < now:
            return "حان موعد الزيارة!"
        
        delta = target_date - now
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{days} يوم {hours} ساعة {minutes} دقيقة"
    except (ValueError, TypeError):
        return "غير متاح"



#remvoe later
def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message))
