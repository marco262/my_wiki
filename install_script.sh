sudo apt-get update
sudo apt-get install -y git python3-pip tmux

git config --global init.defaultBranch master
git config --global pull.rebase true

git init my_wiki
cd my_wiki
git remote add -f origin https://github.com/marco262/my_wiki.git
git branch --set-upstream-to=origin/master master

git sparse-checkout set \
  "data/" \
  "src/" \
  "static/" \
  "views/" \
  ".gitignore" \
  "config.ini.dist" \
  "main.py" \
  "makefile" \
  "requirements.txt" \
  "startup_script.sh" \
  "swagger.json"

git pull origin master

python3 -m pip install -r requirements.txt
cp config.ini.dist config.ini
