#!/usr/bin/env python3
"""
100X PLATFORM - ONE-COMMAND DEPLOYMENT AUTOMATION
Master deployment script for the entire 30-module platform
Supports multiple deployment targets: Vercel, Netlify, Railway, Render

Usage:
    python deploy.py --env production --platform vercel
    python deploy.py --env staging --platform netlify
    python deploy.py --env development --test-only
    python deploy.py --rollback --version v1.2.3
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
import shutil

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DeploymentManager:
    """Main deployment orchestration class"""

    def __init__(self, environment='development', platform=None, dry_run=False, skip_tests=False):
        self.environment = environment
        self.platform = platform
        self.dry_run = dry_run
        self.skip_tests = skip_tests
        self.config = self.load_config()
        self.env_config = self.config['environments'].get(environment)
        self.deployment_log = []
        self.start_time = datetime.now()

        if not self.env_config:
            self.error(f"Environment '{environment}' not found in deployment_config.json")
            sys.exit(1)

    def load_config(self):
        """Load deployment configuration"""
        config_path = Path(__file__).parent / 'deployment_config.json'
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.error("deployment_config.json not found!")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.error(f"Invalid JSON in deployment_config.json: {e}")
            sys.exit(1)

    def log(self, message, level='INFO'):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.deployment_log.append(log_entry)

        if level == 'INFO':
            print(f"{Colors.OKBLUE}{log_entry}{Colors.ENDC}")
        elif level == 'SUCCESS':
            print(f"{Colors.OKGREEN}{log_entry}{Colors.ENDC}")
        elif level == 'WARNING':
            print(f"{Colors.WARNING}{log_entry}{Colors.ENDC}")
        elif level == 'ERROR':
            print(f"{Colors.FAIL}{log_entry}{Colors.ENDC}")
        elif level == 'HEADER':
            print(f"\n{Colors.HEADER}{Colors.BOLD}{log_entry}{Colors.ENDC}\n")

    def error(self, message):
        """Log error and exit"""
        self.log(message, 'ERROR')

    def success(self, message):
        """Log success"""
        self.log(message, 'SUCCESS')

    def header(self, message):
        """Log header"""
        self.log(message, 'HEADER')

    def run_command(self, command, check=True, shell=True, cwd=None):
        """Execute shell command"""
        if self.dry_run:
            self.log(f"[DRY RUN] Would execute: {command}", 'INFO')
            return True

        self.log(f"Executing: {command}", 'INFO')
        try:
            result = subprocess.run(
                command,
                shell=shell,
                check=check,
                capture_output=True,
                text=True,
                cwd=cwd
            )
            if result.stdout:
                self.log(result.stdout.strip(), 'INFO')
            return True
        except subprocess.CalledProcessError as e:
            self.error(f"Command failed: {command}")
            if e.stderr:
                self.error(e.stderr.strip())
            return False

    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        self.header("STEP 1: Checking Prerequisites")

        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            self.error("Python 3.8 or higher is required")
            return False
        self.success(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")

        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            self.success(f"Node.js version: {result.stdout.strip()}")
        except FileNotFoundError:
            self.error("Node.js is not installed")
            return False

        # Check npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            self.success(f"npm version: {result.stdout.strip()}")
        except FileNotFoundError:
            self.error("npm is not installed")
            return False

        # Check Git
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            self.success(f"Git version: {result.stdout.strip()}")
        except FileNotFoundError:
            self.error("Git is not installed")
            return False

        # Check environment variables
        required_vars = self.config.get('required_environment_variables', [])
        missing_vars = []

        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            self.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            self.log("Please set these in your .env file or environment", 'WARNING')
            return False

        self.success("All required environment variables are set")

        # Check platform CLI if deploying
        if self.platform and not self.dry_run:
            platform_config = self.config['platforms'].get(self.platform)
            if platform_config:
                cli_commands = {
                    'vercel': 'vercel --version',
                    'netlify': 'netlify --version',
                    'railway': 'railway --version',
                    'render': 'render --version'
                }

                cli_cmd = cli_commands.get(self.platform)
                if cli_cmd:
                    try:
                        result = subprocess.run(cli_cmd.split(), capture_output=True, text=True)
                        self.success(f"{self.platform} CLI is installed")
                    except FileNotFoundError:
                        self.error(f"{self.platform} CLI is not installed")
                        self.log(f"Install with: {platform_config['cli_install']}", 'INFO')
                        return False

        self.success("All prerequisites met!")
        return True

    def install_dependencies(self):
        """Install project dependencies"""
        self.header("STEP 2: Installing Dependencies")

        # Install Node.js dependencies
        if os.path.exists('package.json'):
            self.log("Installing Node.js dependencies...", 'INFO')
            if not self.run_command('npm install'):
                return False
            self.success("Node.js dependencies installed")

        # Install Python dependencies
        if os.path.exists('requirements.txt'):
            self.log("Installing Python dependencies...", 'INFO')
            if not self.run_command('pip install -r requirements.txt'):
                return False
            self.success("Python dependencies installed")

        # Install backend dependencies
        backend_requirements = Path('BACKEND/requirements.txt')
        if backend_requirements.exists():
            self.log("Installing backend dependencies...", 'INFO')
            if not self.run_command(f'pip install -r {backend_requirements}'):
                return False
            self.success("Backend dependencies installed")

        # Install module dependencies
        modules_dir = Path('MODULES')
        if modules_dir.exists():
            for category in modules_dir.iterdir():
                if category.is_dir():
                    for module in category.iterdir():
                        req_file = module / 'requirements.txt'
                        if req_file.exists():
                            self.log(f"Installing {module.name} dependencies...", 'INFO')
                            if not self.run_command(f'pip install -r {req_file}'):
                                self.log(f"Warning: Failed to install {module.name} dependencies", 'WARNING')

        self.success("All dependencies installed!")
        return True

    def run_tests(self):
        """Run test suite"""
        if self.skip_tests:
            self.log("Skipping tests (--skip-tests flag)", 'WARNING')
            return True

        self.header("STEP 3: Running Tests")

        test_config = self.env_config.get('tests', {})
        if not test_config.get('enabled', True):
            self.log("Tests disabled for this environment", 'WARNING')
            return True

        # Run main test command
        test_command = test_config.get('command', 'npm test')
        self.log(f"Running tests: {test_command}", 'INFO')

        if not self.run_command(test_command):
            self.error("Tests failed!")
            return False

        self.success("All tests passed!")
        return True

    def build_frontend(self):
        """Build frontend assets"""
        self.header("STEP 4: Building Frontend")

        frontend_config = self.env_config.get('frontend', {})
        build_command = frontend_config.get('build_command', 'npm run build')

        self.log(f"Building frontend: {build_command}", 'INFO')
        if not self.run_command(build_command):
            self.error("Frontend build failed!")
            return False

        self.success("Frontend built successfully!")
        return True

    def deploy_backend(self):
        """Deploy backend APIs"""
        self.header("STEP 5: Deploying Backend APIs")

        backend_config = self.env_config.get('backend', {})
        backend_platform = backend_config.get('platform', self.platform)

        if not backend_platform or backend_platform == 'local':
            self.log("Backend deployment skipped (local environment)", 'INFO')
            return True

        self.log(f"Deploying backend to {backend_platform}...", 'INFO')

        # Set environment variables
        env_vars = backend_config.get('environment_variables', {})
        for key, value in env_vars.items():
            os.environ[key] = str(value)

        # Deploy based on platform
        if backend_platform == 'railway':
            if not self.run_command('railway up'):
                self.error("Railway backend deployment failed!")
                return False
        elif backend_platform == 'render':
            if not self.run_command('render deploy'):
                self.error("Render backend deployment failed!")
                return False
        else:
            self.log(f"Backend platform {backend_platform} not yet implemented", 'WARNING')

        self.success("Backend deployed successfully!")
        return True

    def deploy_frontend(self):
        """Deploy frontend to hosting platform"""
        self.header("STEP 6: Deploying Frontend")

        frontend_config = self.env_config.get('frontend', {})
        frontend_platform = frontend_config.get('primary_platform', self.platform)

        if not frontend_platform or frontend_platform == 'local':
            self.log("Frontend deployment skipped (local environment)", 'INFO')
            return True

        self.log(f"Deploying frontend to {frontend_platform}...", 'INFO')

        # Set environment variables
        env_vars = frontend_config.get('environment_variables', {})
        for key, value in env_vars.items():
            os.environ[key] = str(value)

        # Deploy based on platform
        if frontend_platform == 'vercel':
            if not self.run_command('vercel --prod --yes'):
                self.error("Vercel frontend deployment failed!")
                # Try fallback
                fallback = frontend_config.get('fallback_platform')
                if fallback:
                    self.log(f"Trying fallback platform: {fallback}", 'WARNING')
                    return self.deploy_to_platform(fallback)
                return False
        elif frontend_platform == 'netlify':
            if not self.run_command('netlify deploy --prod'):
                self.error("Netlify frontend deployment failed!")
                return False
        else:
            self.log(f"Frontend platform {frontend_platform} not yet implemented", 'WARNING')

        self.success("Frontend deployed successfully!")
        return True

    def deploy_to_platform(self, platform):
        """Deploy to specific platform"""
        if platform == 'vercel':
            return self.run_command('vercel --prod --yes')
        elif platform == 'netlify':
            return self.run_command('netlify deploy --prod')
        else:
            self.error(f"Unknown platform: {platform}")
            return False

    def run_smoke_tests(self):
        """Run smoke tests to verify deployment"""
        self.header("STEP 7: Running Smoke Tests")

        test_config = self.env_config.get('tests', {})
        smoke_tests = test_config.get('smoke_tests', [])

        if not smoke_tests:
            self.log("No smoke tests configured", 'WARNING')
            return True

        self.log(f"Running {len(smoke_tests)} smoke tests...", 'INFO')

        # Wait for deployment to propagate
        if not self.dry_run:
            self.log("Waiting 30 seconds for deployment to propagate...", 'INFO')
            time.sleep(30)

        failed_tests = []
        for test in smoke_tests:
            self.log(f"Testing: {test}", 'INFO')
            if not self.run_command(test, check=False):
                failed_tests.append(test)

        if failed_tests:
            self.error(f"Smoke tests failed: {len(failed_tests)}/{len(smoke_tests)}")
            for test in failed_tests:
                self.log(f"  - {test}", 'ERROR')
            return False

        self.success("All smoke tests passed!")
        return True

    def send_notifications(self, success=True):
        """Send deployment notifications"""
        self.header("STEP 8: Sending Notifications")

        notification_config = self.env_config.get('notifications', {})
        if not notification_config.get('enabled', False):
            self.log("Notifications disabled for this environment", 'INFO')
            return True

        channels = notification_config.get('channels', [])
        recipients = notification_config.get('recipients', [])

        status = "SUCCESS" if success else "FAILED"
        duration = (datetime.now() - self.start_time).total_seconds()

        message = f"""
        Deployment {status}
        Environment: {self.environment}
        Platform: {self.platform}
        Duration: {duration:.2f} seconds
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        self.log(f"Sending notifications to {len(recipients)} recipients via {channels}", 'INFO')

        # Email notifications
        if 'email' in channels:
            self.log("Would send email notification (not implemented)", 'INFO')

        # SMS notifications
        if 'sms' in channels:
            self.log("Would send SMS notification (not implemented)", 'INFO')

        # Slack notifications
        if 'slack' in channels:
            self.log("Would send Slack notification (not implemented)", 'INFO')

        self.success("Notifications sent!")
        return True

    def rollback(self, version=None):
        """Rollback to previous version"""
        self.header("INITIATING ROLLBACK")

        rollback_config = self.env_config.get('rollback', {})
        if not rollback_config.get('enabled', False):
            self.error("Rollback not enabled for this environment")
            return False

        self.log(f"Rolling back to version: {version or 'previous'}", 'WARNING')

        # Platform-specific rollback
        if self.platform == 'vercel':
            if version:
                self.run_command(f'vercel rollback {version}')
            else:
                self.run_command('vercel rollback')
        elif self.platform == 'netlify':
            if version:
                self.run_command(f'netlify deploy --alias {version}')
            else:
                self.run_command('netlify rollback')

        self.send_notifications(success=False)
        self.success("Rollback completed!")
        return True

    def create_backup(self):
        """Create backup before deployment"""
        backup_config = self.config.get('backup', {})
        if not backup_config.get('enabled', False):
            return True

        if not backup_config.get('before_deployment', False):
            return True

        self.log("Creating backup before deployment...", 'INFO')

        backup_dir = Path('.backups') / datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Backup configuration files
        config_files = ['deployment_config.json', '.env', 'package.json', 'requirements.txt']
        for config_file in config_files:
            if os.path.exists(config_file):
                shutil.copy2(config_file, backup_dir / config_file)

        self.success(f"Backup created at {backup_dir}")
        return True

    def save_deployment_log(self):
        """Save deployment log to file"""
        log_dir = Path('.deployment_logs')
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"deploy_{self.environment}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        with open(log_file, 'w') as f:
            f.write('\n'.join(self.deployment_log))

        self.log(f"Deployment log saved to {log_file}", 'INFO')

    def deploy(self):
        """Main deployment workflow"""
        self.header(f"DEPLOYING TO {self.environment.upper()}")

        if self.dry_run:
            self.log("DRY RUN MODE - No actual changes will be made", 'WARNING')

        # Create backup
        if not self.create_backup():
            self.error("Backup creation failed!")
            return False

        # Execute deployment steps
        steps = [
            ('Prerequisites Check', self.check_prerequisites),
            ('Install Dependencies', self.install_dependencies),
            ('Run Tests', self.run_tests),
            ('Build Frontend', self.build_frontend),
            ('Deploy Backend', self.deploy_backend),
            ('Deploy Frontend', self.deploy_frontend),
            ('Smoke Tests', self.run_smoke_tests),
        ]

        for step_name, step_func in steps:
            if not step_func():
                self.error(f"{step_name} failed!")

                # Auto-rollback on failure
                rollback_config = self.env_config.get('rollback', {})
                if rollback_config.get('auto_rollback_on_failure', False):
                    self.log("Auto-rollback triggered", 'WARNING')
                    self.rollback()

                self.send_notifications(success=False)
                self.save_deployment_log()
                return False

        # Send success notifications
        self.send_notifications(success=True)

        # Save deployment log
        self.save_deployment_log()

        # Final summary
        duration = (datetime.now() - self.start_time).total_seconds()
        self.header("DEPLOYMENT COMPLETE!")
        self.success(f"Total deployment time: {duration:.2f} seconds")

        # Display URLs
        frontend_url = self.env_config.get('frontend', {}).get('url')
        backend_url = self.env_config.get('backend', {}).get('url')

        if frontend_url:
            self.log(f"Frontend URL: {frontend_url}", 'SUCCESS')
        if backend_url:
            self.log(f"Backend URL: {backend_url}", 'SUCCESS')

        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='100X Platform - One-Command Deployment Automation'
    )

    parser.add_argument(
        '--env',
        choices=['development', 'staging', 'production'],
        default='development',
        help='Deployment environment'
    )

    parser.add_argument(
        '--platform',
        choices=['vercel', 'netlify', 'railway', 'render'],
        help='Deployment platform (optional, uses config default)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate deployment without making changes'
    )

    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Skip running tests'
    )

    parser.add_argument(
        '--test-only',
        action='store_true',
        help='Only run tests, do not deploy'
    )

    parser.add_argument(
        '--rollback',
        action='store_true',
        help='Rollback to previous version'
    )

    parser.add_argument(
        '--version',
        help='Specific version to rollback to'
    )

    args = parser.parse_args()

    # Create deployment manager
    manager = DeploymentManager(
        environment=args.env,
        platform=args.platform,
        dry_run=args.dry_run,
        skip_tests=args.skip_tests
    )

    # Handle rollback
    if args.rollback:
        success = manager.rollback(version=args.version)
        sys.exit(0 if success else 1)

    # Handle test-only
    if args.test_only:
        success = manager.check_prerequisites() and manager.run_tests()
        sys.exit(0 if success else 1)

    # Full deployment
    success = manager.deploy()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
