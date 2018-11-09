pip install -r requirements.txt
sudo cp ./rbl.service /etc/systemd/system/rbl.service
sudo systemctl enable /etc/systemd/system/rbl.service
