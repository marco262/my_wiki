A landing for my own personal use, primarily to present custom visualizations of any data I want.

# Installation

## Debian

1. Update system, clone repo, and install requirements:  
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip tmux
   git clone https://github.com/marco262/my_wiki.git
   cd my_wiki
   python3 -m pip install -r requirements.txt
   ```
2. Make a copy of `config.ini.dist` and rename it to `config.ini`.
   1. Alternately, run the server briefly to auto-create it.
3. Update `config.ini` so `host` is the egress IP of the machine you're on, assuming you want this instance to host external traffic.
   1. If running on Google Cloud, use the "Internal IP" of the VM, not the "External IP".

### Nginx and Certbot

These are basic instructions about how to use Nginx and certbot to allow the server to be hosted from a domain using HTTPS. 

#### Install

Install Nginx and certbot

```bash
sudo apt-get install nginx certbot python3-certbot-nginx
```

#### Configure

Create a new file nginx file at `/etc/nginx/sites-available/my_wiki` with the following configuration:

```bash
server {
    listen 80;
    server_name subdomain.your-domain.com;

    location / {
        proxy_pass http://localhost:8080;  # Change to your Bottle server's port
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then, create a symbolic link to this configuration in the sites-enabled directory:

```bash
sudo ln -s /etc/nginx/sites-available/your-app.conf /etc/nginx/sites-enabled/
```

Ensure there are no syntax errors in your Nginx configuration:

```bash
sudo nginx -t
```

Obtain SSL/TLS certificate using certbot

```bash
sudo certbot --nginx -d subdomain.your-domain.com --key-type ecdsa
```

After obtaining the certificate, Certbot should automatically update your Nginx configuration to handle HTTPS traffic. If not, you can update your server block in the Nginx configuration file to include the SSL settings:

```nginx
server {
    listen 80;
    server_name subdomain.your-domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name subdomain.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/subdomain.your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/subdomain.your-domain.com/privkey.pem;

    # Additional SSL settings go here

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Test your Nginx configuration again and restart Nginx:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

Update your `config.ini` file to host the Bottle server on `localhost:8080`:

```ini
host = localhost
port = 8080
```

## Terraform

Some initial setup is required to allow yourself to run terraform.

```bash
gcloud config set project upheld-setting-362218
gcloud auth application-default login
```

# Usage

## Debian

* Run in detached tmux session: `tmux new-session -d -s "my-wiki" "python3 main.py"`
* Attach to session: `tmux a`
* Detach from session: Ctrl-b, d
* Kill session: `tmux kill-ses -t my-wiki`
