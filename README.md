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
upstream wiki {
    server localhost:8080;  # Change to your Bottle server's port
    keepalive 32;
}
server {
    listen 80;
    server_name subdomain.your-domain.com;

    location / {
        proxy_pass http://localhost:8080;  # Change to your Bottle server's port
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }    

    location /visual_aid_websocket {
        proxy_pass http://localhost:8080;  # Change to your Bottle server's port
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection $http_connection;
        proxy_set_header Upgrade $http_upgrade;
        proxy_connect_timeout 3600s;
        proxy_read_timeout 3600s;
    }
}
```

Then, create a symbolic link to this configuration in the sites-enabled directory:

```bash
sudo ln -s /etc/nginx/sites-available/my_wiki /etc/nginx/sites-enabled/
```

Ensure there are no syntax errors in your Nginx configuration:

```bash
sudo nginx -t
```

Obtain SSL/TLS certificate using certbot

```bash
sudo certbot --nginx -d subdomain.your-domain.com --key-type ecdsa
```

After obtaining the certificate, Certbot should automatically update your Nginx configuration to handle HTTPS traffic. Test your Nginx configuration again and restart Nginx:

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
gcloud config set project <project-id>
gcloud auth application-default login
```

# Configuration

## Externally hosted media files

The server supports either storing media files locally and hosting them from the same machine that the service is running on, or it can return a redirect an externally hosted file source, like a Google Cloud Bucket. If you wish to use an external file source, set the `media bucket` config setting to the URL of the root directory where all the media files are stored. e.g. https://storage.googleapis.com/<bucket-id>/media/

Note that this will not prevent the media files from being pulled down by a git clone. If you wish to avoid that, see the `startup_script.sh` for how to do a sparse checkout.

## Auto-update

The wiki supports automatically pulling down updates to the live server whenever a change is pushed to GitHub. To enable that, create a GitHub Respository Secret named `DOMAIN` with the domain where the server is hosted. e.g. https://your.server.com (no trailing slash)

Whenever a change is pushed to GitHub, a GitHub Action will fire that will hit the `/load_changes` endpoint at that domain, which should trigger the server to pull down any changes to the `master` branch and restart if needed.

# Usage

## Debian

* Run in detached tmux session: `tmux new-session -d -s "my-wiki" "python3 main.py"`
* Attach to session: `tmux a`
* Detach from session: Ctrl-b, d
* Kill session: `tmux kill-ses -t my-wiki`

## Media files

Media files are not pulled down from GitHub by the intended installation (see `startup_script.sh`). 
Instead, media files requests are redirected to the my-wiki cloud bucket, where all files should be manually copied.

To automatically sync your local media/ directory with the bucket:

```bash
gsutil -m rsync -r media/ gs://<bucket-id>/media/
```
