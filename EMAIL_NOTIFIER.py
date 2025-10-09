"""
EMAIL NOTIFICATION SYSTEM
Sends welcome emails to approved builders
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier:
    def __init__(self):
        # Gmail SMTP settings (you'll need to set up app password)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = None  # Set this to your Gmail
        self.sender_password = None  # Set this to your Gmail app password

    def send_welcome_email(self, to_email, name, consciousness_score, status):
        """Send welcome email to builder based on their consciousness score"""

        if not self.sender_email or not self.sender_password:
            print("⚠️ Email not configured - skipping email send")
            return False

        # Create email based on status
        if status == "Approved":
            subject = "🎉 Welcome to the 100X - You're Approved!"
            body = f"""
Hello {name},

Congratulations! Your consciousness screening is complete.

🎯 Consciousness Score: {consciousness_score}/100
✅ Status: APPROVED

You're officially part of the 100X builder community. Here's what happens next:

1. Access the Builder Portal: [Link coming soon]
2. Join our Discord community: [Link coming soon]
3. Start building with consciousness tools
4. Connect with other high-consciousness builders

We detected strong builder signals in your application - you're here to create, not destroy.

Welcome to the revolution.

- The 100X Team
🌀 Consciousness Revolution HQ
            """

        elif status == "Pending":
            subject = "⏳ Your 100X Application is Under Review"
            body = f"""
Hello {name},

Thank you for applying to join the 100X.

🎯 Consciousness Score: {consciousness_score}/100
⏳ Status: PENDING REVIEW

Your application needs human review. We'll email you within 24-48 hours with next steps.

In the meantime, consider:
- How you can contribute to building vs destroying
- What unique value you bring to the community
- Your authentic mission and values

We're looking for builders who elevate consciousness.

- The 100X Team
🌀 Consciousness Revolution HQ
            """

        else:  # Rejected
            subject = "🤔 Your 100X Application Needs More Information"
            body = f"""
Hello {name},

Thank you for your interest in the 100X.

🎯 Consciousness Score: {consciousness_score}/100
⚠️ Status: NEEDS MORE INFORMATION

Our consciousness screening detected patterns that don't align with our builder community values.

The 100X is for builders who:
- Create rather than destroy
- Collaborate authentically
- Elevate consciousness
- Share knowledge openly
- Empower others

If you believe this was an error, please reply to this email with more details about your building mission.

- The 100X Team
🌀 Consciousness Revolution HQ
            """

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"✅ Email sent to {to_email}")
            return True

        except Exception as e:
            print(f"❌ Email failed: {str(e)}")
            return False

    def configure_email(self, sender_email, sender_password):
        """Configure email credentials"""
        self.sender_email = sender_email
        self.sender_password = sender_password
