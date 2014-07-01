Requirements:
	MySQL
	python2.7
	install pip
	pip install requests
Dump database:
	mysqldump -u root -p probe_db>probe_db.sql
Restore database:
	mysql -u root -p probe_db<probe_db.sql
Edit:
	script/config.py
Run:
	./install.sh
Execute:
	(in different shell)
	script/./run_loop.py
	script/./MASTER.py


