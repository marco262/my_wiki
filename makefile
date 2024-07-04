start:
	tmux new-session -s "my-wiki" "venv/bin/python main.py"
view:
	tmux a
stop:
	tmux kill-ses -t my-wiki
restart:
	tmux kill-ses -t my-wiki
	git pull origin master
	tmux new-session -s "my-wiki" "venv/bin/python main.py"