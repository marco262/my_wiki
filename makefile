start:
	tmux new-session -d -s "my-wiki" "python3 main.py"
view:
	tmux a
stop:
	tmux kill-ses -t my-wiki