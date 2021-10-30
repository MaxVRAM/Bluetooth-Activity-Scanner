# Bluetooth Activity Scanner with Prometheus Node

Hardware: Raspberry Pi 4

Reports surrounding Bluetooth devices and aggregated change of individual BLE device signal each scan.
It then sends the values to a local Prometheus server via push gateway.


1. Clone the Repo:

```bash
git clone https://github.com/MaxVRAM/Bluetooth-Activity-Scanner.git && cd Bluetooth-Activity-Scanner
```

2. Install the Python modules:
```bash
pip3 install -r requirements.txt
```

3. Open ports: 
```bash
sudo ufw allow 9090, 9091, 9100 proto tcp
```

4. Deploy the Promethus stack:
```bash
docker-compose up -d
```

5. Run the Python script:
```bash
python3 bt_counter.py
```

The server can be accessed via web brower, or as a datasource in Grafana: [http://localhost:9090](http://localhost:9090)
