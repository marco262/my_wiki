A landing for my own personal use, primarily to present custom visualizations of any data I want.

# Installation

## Debian

1. Copy/paste the commands from [install_script.sh](install_script.sh) into the terminal.
   1. Alternately, upload the script and run it there.
2. Update `config.ini` so `host` is the egress IP of the machine you're on, assuming you want this instance to host external traffic.
   1. If running on Google Cloud, use the "Internal IP" of the VM, not the "External IP".
   2. If you are configuring an HTTPS connection via Certbot (see below), you can skip this step. 

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
    server 127.0.0.1:8080;  # Change to your Bottle server's port
    keepalive 32;
}
server {
    listen 80;
    server_name subdomain.your-domain.com;
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8080;  # Change to your Bottle server's port
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }    

    location /visual_aid_websocket {
        proxy_pass http://127.0.0.1:8080;  # Change to your Bottle server's port
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

Now is the time to set up your DNS to point at the running VM.

Next, obtain SSL/TLS certificate using certbot.

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

The server supports either storing media files locally and hosting them from the same machine that the service is running on, or it can return a redirect an externally hosted file source, like a Google Cloud Bucket. If you wish to use an external file source, set the `media bucket` config setting to the name of the bucket. The bucket must contain a top-level folder named `media` which contains all the media files.

Note that this will not prevent the media files from being pulled down by a git clone. If you wish to avoid that, see the `install_script.sh` for how to do a sparse checkout.

## Auto-update

The wiki supports automatically pulling down updates to the live server whenever a change is pushed to GitHub. To enable that, create a GitHub Respository Secret named `DOMAIN` with the domain where the server is hosted. e.g. https://your.server.com (no trailing slash)

Whenever a change is pushed to GitHub, a GitHub Action will fire that will hit the `/load_changes` endpoint at that domain, which should trigger the server to pull down any changes to the `master` branch and restart if needed.

# Usage

## Debian

* Run in detached tmux session: `tmux new-session -d -s "my-wiki" "venv/bin/python main.py"`
* Attach to session: `tmux a`
* Detach from session: Ctrl-b, d
* Kill session: `tmux kill-ses -t my-wiki`

## Media files

Media files are not pulled down from GitHub by the intended installation (see `install_script.sh`). 
Instead, media file requests are redirected to the my-wiki cloud bucket, where all files should be manually copied.

To automatically sync your local `media/` directory with the bucket:

```bash
gsutil -m rsync -ruc media/ gs://<bucket-id>/media/
```

# TARPIT

TARPIT is a useful Linux module that that will cause connections from certain IPs to be dropped without closing them, which can be inconvenient for malicious bots. Below is a brief summary of how to install it on a Google Cloud VM (Debian 12).

## Update Linux and load TARPIT module
Install the newest linux kernel.
```
sudo apt install linux-image-amd64
```
Edit the Grub config so the VM will boot with the non-cloud OS.
```
sudo vim /etc/default/grub
```
Edit the following line:
```diff
-GRUB_DEFAULT=0
+GRUB_DEFAULT="Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.1.0-37-amd64"
```
Regenerate GRUB and reboot
```
sudo update-grub
sudo reboot
```
After reboot, confirm that `uname -r` returns `6.1.0-37-amd64`
Next, load the TARPIT module
```
sudo apt install xtables-addons-dkms
sudo modprobe xt_TARPIT
```
## Test iptables
Log into another VM or a friend's computer and curl the IP of the target VM to confirm you get a valid reponse.
```
curl http://<ip-of-target-vm>:443
```
Add the external IP of the VM. Set `--dport` to the port you want to block.
```
sudo iptables -A INPUT -s 1.2.3.4 -p tcp --dport 443 -j TARPIT
```
In that other VM, curl the main VM again and confirm the connection times out.

After you're done testing, delete that rule:
```
sudo iptables -L INPUT -n --line-numbers
sudo iptables -D INPUT 1
```
## Create Deny List ipset
Create ipset and add blocked IPs
```
sudo ipset create deny_list hash:ip
sudo ipset add deny_list 1.2.3.4
sudo ipset add deny_list 11.22.33.44
```
Add logging and TARPIT rules, and remember to set `--dport`
```
sudo iptables -A INPUT -m set --match-set deny_list src -p tcp --dport 443 -j LOG --log-prefix "TARPIT IP: " --log-level 4
sudo iptables -A INPUT -m set --match-set deny_list src -p tcp --dport 443 -j TARPIT
```
Make iptables config persistent (you will have to select <Yes> to save your config during package installation)
```
sudo apt install iptables-persistent
sudo netfilter-persistent save
```
## Cheatsheet
* View TARPIT logs `sudo journalctl -k | grep "TARPIT IP:"`
* Add to ipset `sudo ipset add deny_list 11.22.33.44`
* Delete from ipset `sudo ipset del deny_list 11.22.33.44`
* List ipset `sudo ipset list deny_list`
* Save changes to ipset `sudo netfilter-persistent save`
* Save ipset to file `sudo ipset save > /path/to/file.conf`