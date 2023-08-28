# Chatbot DD

### 1. Create NLU data

1.1 Edit data in `dataset/data.yaml`
1.2 Export data with command

```bash
python scripts/export_data.py
```

1.3 Edit `data/stories.yml` (optional)

### 2. Train rasa (NLU & Core)

#### 2.1 Train with **fasttext** pipeline (recommended)

- Download [cc.vi.300.bin](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.vi.300.bin.gz), move it to `.cache/fasttext`

```bash
rasa train --config config/fasttext.yml
```

#### 2.2 Train with other pipline

```bash
rasa train --config {config_file}
```

### 2.3 Train nlu only

```bash
rasa train nlu --config {config_file}
```

### 2.4 Test your assistant

```bash
rasa shell
# or
rasa shell nlu
```

### 3. Evaluate NLU

Example: 5 folds CV

```bash
rasa test nlu --config config.yml --cross-validation --runs 5 --fold 5 --out results/test1
```

or run all configs, see `test_models.bat`


Prettify and display test result from `results/` folder

```bash
python eval.py

```

### 4. Install rasa x local mode

#### 4.1 Upgrade pip

```bash
pip install --upgrade pip
```

#### 4.2 Install rasa x

```bash
pip3 install rasa-x==1.0.1 --extra-index-url https://pypi.rasa.com/simple --use-deprecated=legacy-resolver
```

### 5. Deploy rasa x

- Required trained model with **{config_file}** before
```bash
rasa x --config {config_file}

# Sample output
Starting Rasa X in local mode... >
...
The server is running at http://localhost:5002/login?username=me&password=xxxxxxxxx
```
This should open a browser tab to [http://localhost:5002](http://localhost:5002) and login automatically

### 6. Share rasa x

- Install [**ngrok**](https://ngrok.com/download), run and command

```bash
ngrok http 5002

# Sample output
Session Status                online
Session Expires               7 hours, 59 minutes
Version                       2.3.35
Region                        United States (us)
Web Interface                 http://127.0.0.1:4041
Forwarding                    http://831897ef2f98.ngrok.io -> http://localhost:5002
Forwarding                    https://831897ef2f98.ngrok.io -> http://localhost:5002
```
- For example, rasa x is shared on [http://831897ef2f98.ngrok.io](http://831897ef2f98.ngrok.io)
