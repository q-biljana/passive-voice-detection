Project structure looks like:
```
├── logs                   # Training logs
├── models                 # Trained models
├── trainer                # Source for Cloud ML training
│   ├── __init__.py              # Table of contents
│   ├── cloudml-gpu.yaml         # Frequently asked questions
│   ├── keras_spell.py           # Miscellaneous information
├── gcloud.sh                    # Script starting Cloud training
├── requirements.txt       # Requirements for local training
├── setup.py               # Config for Cloud training
├── download_data.sh	   # Download data for local training
├── predict.sh	           # Script for predict
├── deepspell_local.py     # Script for local training
├── predict.py             # Code for predict
└── README.md              
```
