Project structure looks like:
```
├── logs                   # Training logs
├── models                 # Trained models
├── trainer                # Source for Cloud ML training
│   ├── __init__.py              # Table of contents
│   ├── cloudml-gpu.yaml         # Specify number and type of machines used
│   ├── keras_spell.py           # Deep-spell model & output
|   ├── credential.json
├── gcloud.sh                    # Script starting Cloud training
├── requirements.txt       # Requirements for local training
├── setup.py               # Config for Cloud training
├── download_data.sh	     # Download data for local training
├── predict.sh	           # Script for prediction
├── deepspell_local.py     # Script for local training
├── predict.py             # Code for local prediction
└── README.md              
```
