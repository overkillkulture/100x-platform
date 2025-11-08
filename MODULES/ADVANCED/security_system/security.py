"""MODULE #42: SECURITY SYSTEM - Authentication, encryption, validation"""
import hashlib
import secrets
import time
from typing import Dict, Optional

class SecuritySystem:
    def __init__(self):
        self.users: Dict[str, Dict] = {}
        self.sessions: Dict[str, Dict] = {}
        self.failed_attempts: Dict[str, int] = {}

    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${hashed.hex()}"

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password"""
        try:
            salt, hash_hex = hashed.split('$')
            verify_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return verify_hash.hex() == hash_hex
        except:
            return False

    def register_user(self, username: str, password: str) -> bool:
        """Register new user"""
        if username in self.users:
            return False
        self.users[username] = {
            'password': self.hash_password(password),
            'created': time.time(),
            'active': True
        }
        return True

    def login(self, username: str, password: str) -> Optional[str]:
        """Login and create session"""
        # Rate limiting
        if self.failed_attempts.get(username, 0) >= 5:
            return None

        user = self.users.get(username)
        if not user or not self.verify_password(password, user['password']):
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
            return None

        # Create session
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {
            'username': username,
            'created': time.time(),
            'expires': time.time() + 3600
        }
        self.failed_attempts[username] = 0
        return token

    def validate_session(self, token: str) -> Optional[str]:
        """Validate session token"""
        session = self.sessions.get(token)
        if not session:
            return None
        if time.time() > session['expires']:
            del self.sessions[token]
            return None
        return session['username']

    def sanitize_input(self, text: str) -> str:
        """Sanitize user input"""
        dangerous = ['<script>', 'javascript:', 'onerror=', 'onclick=']
        sanitized = text
        for dangerous_str in dangerous:
            sanitized = sanitized.replace(dangerous_str, '')
        return sanitized

if __name__ == "__main__":
    security = SecuritySystem()
    security.register_user("alice", "secure123")
    token = security.login("alice", "secure123")
    print(f"Login token: {token[:20]}...")
    print(f"Valid: {security.validate_session(token)}")
    print("✅ Security System working!")
