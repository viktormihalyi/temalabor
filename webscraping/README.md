# Usage
## with Docker
```bash
docker-compose up -d
```

## without Docker (on Ubuntu)
### install
```bash
sudo apt-get install python3 python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### run
You will need to run Elasticsearch on port 9200. (This can be changed in `src/settings.py`)
```bash
python3 src/main.py
```

# TODO
- struktúrált adatok
    - ahol van, ott csak hozzákerül a description-höz
- előre beállított tulajdonságokat keressen
    - működik úgy, hogy a honlapon beállítom a keresést, és a scrapelést arról az URL-ről indítom
- dinamikusan töltődő oldalak
    - Selenium: https://www.seleniumhq.org/
    - plugin pythonhoz: https://selenium-python.readthedocs.io/
