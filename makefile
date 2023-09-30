start:
	tmux new-session -s "my-wiki" "python3 main.py"
view:
	tmux a
stop:
	tmux kill-ses -t my-wiki