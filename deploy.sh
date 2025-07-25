#!/bin/bash

# ===================================================================================
# Django Portfolio Auto-Deployment Script for Ubuntu 22.04
# ===================================================================================
# This script automates the deployment of a Django project using Gunicorn and Nginx.
# It should be run by a non-root user with sudo privileges.
# ===================================================================================

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Helper functions for colored output ---
info() { echo -e "\e[34m[INFO]\e[0m $1"; }
success() { echo -e "\e[32m[SUCCESS]\e[0m $1"; }
error() { echo -e "\e[31m[ERROR]\e[0m $1"; exit 1; }
prompt() { echo -n -e "\e[33m[PROMPT]\e[0m $1"; }

# --- Ensure the script is not run as root ---
if [ "$EUID" -eq 0 ]; then
  error "This script must be run as a non-root user with sudo privileges."
fi

# --- Step 1: Gather User Information ---
info "Gathering required information for deployment..."
prompt "Enter your Git repository URL: "
read GIT_REPO_URL

prompt "Enter your project's main directory name (e.g., my-portfoilo): "
read PROJECT_DIR_NAME

prompt "Enter your domain or server IP address (e.g., myportfolio.com or 12.34.56.78): "
read DOMAIN_OR_IP

prompt "Enter the desired URL for the admin page (e.g., my-secret-admin): "
read ADMIN_URL

prompt "Enter the username for the Django admin superuser: "
read SUPERUSER_USERNAME

prompt "Enter the password for the Django admin superuser: "
read -s SUPERUSER_PASSWORD
echo

prompt "Enter the email for the Django admin superuser: "
read SUPERUSER_EMAIL

# --- Step 2: System Update and Package Installation ---
info "Updating system packages and installing dependencies..."
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-dev python3-venv nginx git

# --- Step 3: Project Checkout and Setup ---
info "Cloning repository and setting up the project environment..."
if [ -d "$PROJECT_DIR_NAME" ]; then
    info "Project directory '$PROJECT_DIR_NAME' already exists. Skipping clone."
else
    git clone "$GIT_REPO_URL"
fi
cd "$PROJECT_DIR_NAME"

info "Creating and activating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

info "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# --- Step 4: Create Production .env file ---
info "Generating a new Django SECRET_KEY..."
NEW_SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

info "Creating production .env file..."
cat << EOF > .env
# Production Environment Variables
SECRET_KEY='$NEW_SECRET_KEY'
DEBUG=False
ADMIN_URL='$ADMIN_URL/'
ALLOWED_ADMIN_IPS='127.0.0.1,::1' # Add your public IP here if needed
SUPERUSER_USERNAME='$SUPERUSER_USERNAME'
SUPERUSER_EMAIL='$SUPERUSER_EMAIL'
SUPERUSER_PASSWORD='$SUPERUSER_PASSWORD'
EOF

success ".env file created successfully."

# --- Step 5: Django Management Commands ---
info "Running Django management commands..."
python3 manage.py migrate
python3 manage.py createsuperuser_from_env
python3 manage.py collectstatic --noinput

# --- Step 6: Configure Gunicorn Systemd Service ---
CURRENT_USER=$(whoami)
PROJECT_PATH=$(pwd)

info "Configuring Gunicorn systemd socket..."
sudo bash -c "cat << EOF > /etc/systemd/system/gunicorn.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF"

info "Configuring Gunicorn systemd service..."
sudo bash -c "cat << EOF > /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$CURRENT_USER
Group=www-data
WorkingDirectory=$PROJECT_PATH
ExecStart=$PROJECT_PATH/venv/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/run/gunicorn.sock \\
          portfolio.wsgi:application

[Install]
WantedBy=multi-user.target
EOF"

info "Starting and enabling Gunicorn socket..."
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
success "Gunicorn service configured."

# --- Step 7: Configure Nginx Reverse Proxy ---
info "Configuring Nginx as a reverse proxy..."

sudo bash -c "cat << EOF > /etc/nginx/sites-available/$PROJECT_DIR_NAME
server {
    listen 80;
    server_name $DOMAIN_OR_IP;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root $PROJECT_PATH;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF"

info "Enabling the new Nginx configuration..."
sudo ln -sf /etc/nginx/sites-available/$PROJECT_DIR_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

info "Testing Nginx configuration..."
sudo nginx -t

info "Restarting Nginx..."
sudo systemctl restart nginx

# --- Step 8: Configure Firewall ---
info "Configuring UFW firewall to allow Nginx traffic..."
sudo ufw allow 'Nginx Full'
sudo ufw status

# --- Final Success Message ---
echo
success "Deployment script finished successfully!"
echo
info "Your Django portfolio is now live at: http://$DOMAIN_OR_IP"
info "Your admin page is available at: http://$DOMAIN_OR_IP/$ADMIN_URL/"
info "To monitor Gunicorn logs, run: sudo journalctl -u gunicorn.service"
info "To monitor Nginx logs, run: sudo journalctl -u nginx.service"
echo 