#!/bin/bash

# Останавливаем скрипт при любой ошибке
set -e

# ==========================================
# КОНФИГУРАЦИЯ
# ==========================================
PROJECT_NAME="mclean_project"
REPO_URL="https://oauth2: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@github.com/tashkhanov/m-clean-prod.git"
DOMAIN="new.m-clean.kz"
REPO_DIR="/var/www/$PROJECT_NAME"

# ==========================================

echo "====================================================="
echo "==> 1. Обновление системы и установка зависимостей..."
echo "====================================================="
sudo apt update
sudo apt upgrade -y
# Ubuntu 24.04 использует Python 3.12 по умолчанию (пакет python3)
sudo apt install -y python3-venv python3-pip python3-dev nginx git certbot python3-certbot-nginx pwgen

echo "====================================================="
echo "==> 2. Клонирование репозитория..."
echo "====================================================="
if [ -d "$REPO_DIR" ]; then
    echo "Директория $REPO_DIR уже существует. Обновляем репозиторий..."
    cd $REPO_DIR
    git reset --hard HEAD
    git pull
else
    sudo mkdir -p /var/www
    # Назначаем права текущему пользователю
    sudo chown -R $USER:$USER /var/www
    git clone $REPO_URL $REPO_DIR
    cd $REPO_DIR
fi

echo "====================================================="
echo "==> 3. Настройка файла .env..."
echo "====================================================="
if [ ! -f "$REPO_DIR/.env" ]; then
    echo "Генерация нового файла .env..."
    # Генерируем случайный SECRET_KEY
    SECRET_KEY=$(pwgen -s 50 1)
    
    cat > "$REPO_DIR/.env" <<EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,89.207.254.23,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN,http://89.207.254.23
EOF
    echo "Файл .env успешно создан."
else
    echo "Файл .env уже существует. Перезапись пропущена."
fi

echo "====================================================="
echo "==> 4. Создание виртуального окружения (Python 3.12) и установка зависимостей..."
echo "====================================================="
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn setuptools

echo "====================================================="
echo "==> 5. Применение миграций и сборка статики..."
echo "====================================================="
# ВАЖНО: Если локальный файл db.sqlite3 загружен, миграции просто проверят, что всё актуально, не затирая файлы.
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "====================================================="
echo "==> 6. Настройка Nginx..."
echo "====================================================="
NGINX_CONF_FILE="/etc/nginx/sites-available/$PROJECT_NAME"

sudo bash -c "cat > $NGINX_CONF_FILE" <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN 89.207.254.23;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    # Решение возможных проблем с загрузкой больших изображений
    client_max_body_size 50M;

    location /static/ {
        alias $REPO_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias $REPO_DIR/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn_${PROJECT_NAME}.sock;
    }
}
EOF

# Включаем конфигурацию Nginx
if [ ! -L /etc/nginx/sites-enabled/$PROJECT_NAME ]; then
    sudo ln -s /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
fi

# Удаляем дефолтный конфиг Nginx
sudo rm -f /etc/nginx/sites-enabled/default

# Проверка конфигурации Nginx
sudo nginx -t

echo "====================================================="
echo "==> 7. Настройка Gunicorn Systemd Сервиса..."
echo "====================================================="
GUNICORN_SERVICE_FILE="/etc/systemd/system/gunicorn_${PROJECT_NAME}.service"

sudo bash -c "cat > $GUNICORN_SERVICE_FILE" <<EOF
[Unit]
Description=gunicorn daemon for $PROJECT_NAME
Requires=gunicorn_${PROJECT_NAME}.socket
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$REPO_DIR
ExecStart=$REPO_DIR/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn_${PROJECT_NAME}.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

GUNICORN_SOCKET_FILE="/etc/systemd/system/gunicorn_${PROJECT_NAME}.socket"

sudo bash -c "cat > $GUNICORN_SOCKET_FILE" <<EOF
[Unit]
Description=gunicorn socket for $PROJECT_NAME

[Socket]
ListenStream=/run/gunicorn_${PROJECT_NAME}.sock

[Install]
WantedBy=sockets.target
EOF

sudo systemctl daemon-reload
sudo systemctl start gunicorn_${PROJECT_NAME}.socket
sudo systemctl enable gunicorn_${PROJECT_NAME}.socket
sudo systemctl restart gunicorn_${PROJECT_NAME}.service
sudo systemctl restart nginx

echo "====================================================="
echo "==> 8. Настройка SSL (HTTPS) через Certbot..."
echo "====================================================="
# Пытаемся выпустить сертификат, игнорируем ошибку (если DNS не делегирован)
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m admin@$DOMAIN || echo "Внимание: Запуск Certbot завершился с ошибкой. Проверьте A-записи домена."

echo "====================================================="
echo "==> Деплой успешно завершен!"
echo "База данных SQLite находится по пути: $REPO_DIR/db.sqlite3"
echo "Чтобы загрузить вашу базу с ПК - используйте SCP до запуска скрипта (или после с рестартом)."
echo "====================================================="
