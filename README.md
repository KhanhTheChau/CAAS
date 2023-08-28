# CAAS: CHAT-VOICE ADMISSIONS ADVISORY SUPPORT USING CHATGPT AND MACHINE LEARNING
# By Truong-Thanh Ma, The-Khanh Chau, Thien-Phuc Nguyen, Gia-Khuong Huynh, Viet-Chau Tran


### Introduction:
`ABSTRACT— Admissions consultation has consistently remained a prominent topic throughout the years. This activity aims to address the inquiries of parents and students, enabling a clearer understanding of the various career paths available for their plans. Depending on the institution, the consultation system has distinct datasets tailored to cater to each institution's and field's specific requirements. Recognizing the prowess of ChatGPT and the potential of machine learning algorithms, we have proposed a chat-voice framework to enhance admissions advisory within the realm of Information Technology disciplines. The central idea involves implementing a hierarchical model for selecting responses using ChatGPT or a trained model with Rasa. Specifically, the system executes binary classification at the initial level before routing it to the response generation layer. Here, the method leverages the 'Google Assistance API' to facilitate auditory communication between the system and users. Experimental results showcase an approximate 99% accuracy rate for the classification model employing PhoBERT, while the Rasa-based response model achieves accuracy rates of 98% and above. A web application has also been developed for deploying the proposed framework.`

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
rasa train --config config
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
