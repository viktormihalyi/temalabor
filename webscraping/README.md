## with docker
```docker
docker-compose up -d
```

## without docker (on ubuntu)
#### install
```bash
sudo apt-get install python3 python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

#### run
You will need to run Elasticsearch on port 9200. (This can be changed in `src/settings.py`)
```bash
python3 src/main.py
```
