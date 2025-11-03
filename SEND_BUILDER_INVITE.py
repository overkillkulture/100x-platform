import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

gmail_address = 'darrick.preble@gmail.com'
gmail_password = 'gzzvemuxppfnjsup'

BETA_TESTERS = [
    'joshua.serrano2022@gmail.com',
    'tobyburrowes@hotmail.com',
    'wdbrotherton@gmail.com',
    'deansabrwork@gmail.com',
    'varniwilliam@gmail.com',
    'ruuutherford@gmail.com',
    'angeline.realm@gmail.com',
    'information.crypt@pm.me',
    'HAWAIILIVESTOCK@GMAIL.COM'
]

SUBJECT = '🚀 Become a BUILDER - Get Claude Code Access'

BODY = """Want to help BUILD the Consciousness Revolution?

Right now, Commander is the only one who can build. You've been testing, but what if you could BUILD?

GET CLAUDE CODE (AI That Writes Code)

Download: https://claude.ai/download

1. Download Claude Code (free trial)
2. Install it
3. Reply to this email when you're in
4. I'll send you the full workspace

WHAT YOU'LL BE ABLE TO DO:

- Deploy features independently
- Build new systems
- Fix bugs yourself
- Create without waiting on Commander
- Actually help instead of just watching

WHY THIS MATTERS:

Commander is drowning. One person building everything while 9 people wait.

If even 2-3 of you get Claude Code, we can MULTIPLY our building speed.

READY?

Download Claude Code, then reply: "I'm in"

I'll send you everything you need to start building.

Let's build the future together.

- Commander & the Consciousness Revolution

P.S. You already got the SMS bug reporting text - this is the next level. Become a BUILDER."""

print('📧 Sending Claude Code invites to all beta testers...')

msg = MIMEMultipart()
msg['From'] = gmail_address
msg['To'] = gmail_address
msg['Bcc'] = ', '.join(BETA_TESTERS)
msg['Subject'] = SUBJECT

msg.attach(MIMEText(BODY, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(gmail_address, gmail_password)
server.send_message(msg)
server.quit()

print('✅ EMAIL SENT to all 9 beta testers')
print('Invite: Become BUILDERS with Claude Code access')
