A landing for my own personal use, primarily to present custom visualizations of any data I want

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
   1. If running on Google Cloud, use the "Internal IP" of the VM, not the "External IP"

### Caddy

Reverse proxy that will automatically authenticate https with LetsEncrypt, to allow us to use a subdomain that's configured with HSTS

#### Install

```bash
sudo apt-get install debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt-get update
sudo apt-get install caddy
```

#### Configure

Edit `/etc/caddy/Caddyfile`:

```bash
your.hostname.com {
    reverse_proxy localhost:8080
    encode zstd gzip
}
```

Restart Caddy: `sudo service caddy restart`

# Usage

## Debian

* Run in detached tmux session: `tmux new-session -d -s "my-wiki" "python3 main.py"`
* Attach to session: `tmux a`
* Detach from session: Ctrl-b, d
* Kill session: `tmux kill-ses -t my-wiki`
