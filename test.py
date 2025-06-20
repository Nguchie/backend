import smtplib

try:
    server = smtplib.SMTP_SSL('smtpout.secureserver.net', 465)  # For SSL
    # server = smtplib.SMTP('smtpout.secureserver.net', 587)  # For TLS
    # server.starttls()  # Uncomment if using TLS
    server.login('samuel@stagefx.us', 'Cira@37065698')
    print("✅ SMTP login successful!")
    server.quit()
except Exception as e:
    print(f"❌ SMTP error: {e}")