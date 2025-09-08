    # nginx/nginx-full-ssl.conf
    # This is the FINAL Nginx configuration that will serve your app over HTTPS.
    user nginx;
    worker_processes auto;
    error_log /var/log/nginx/error.log notice;
    pid /var/run/nginx.pid;

    events {
        worker_connections 1024;
    }

    http {
        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';

        access_log /var/log/nginx/access.log main;

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;

        # Increase client max body size for file uploads
        client_max_body_size 10M;

        # HTTP server block: Redirects all HTTP traffic to HTTPS
        server {
            listen 80;
            listen [::]:80;
            server_name pre.ocr-pck.eu www.pre.ocr-pck.eu;

            # Certbot's challenge path - still needed for renewals!
            location /.well-known/acme-challenge/ {
                root /var/www/certbot;
            }

            # Redirect all other HTTP traffic to HTTPS
            return 301 https://$host$request_uri;
        }

        # HTTPS server block
        server {
            listen 443 ssl;
            listen [::]:443 ssl;
            server_name pre.ocr-pck.eu www.pre.ocr-pck.eu;

            # SSL certificate paths (Certbot will have created these)
            ssl_certificate /etc/letsencrypt/live/pre.ocr-pck.eu/fullchain.pem;
            ssl_certificate_key /etc/letsencrypt/live/pre.ocr-pck.eu/privkey.pem;

            # Recommended SSL settings for security
            ssl_session_cache shared:SSL:10m;
            ssl_session_timeout 10m;
            ssl_protocols TLSv1.2 TLSv1.3;
            ssl_prefer_server_ciphers on;
            ssl_ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384";
            ssl_stapling on;
            ssl_stapling_verify on;
            add_header X-Frame-Options DENY;
            add_header X-Content-Type-Options nosniff;
            add_header X-XSS-Protection "1; mode=block";

            location / {
                # Increase client max body size for this location
                client_max_body_size 10M;
                
                # Proxy requests to the Flask application
                proxy_pass http://app:5000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
    }
