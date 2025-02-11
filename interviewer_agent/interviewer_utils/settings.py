import sys
import os
import random
import json
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", "")

def get_open_api_keyset(): 
  # open_api_keyset = []
  # open_api_keyset += [{"key": "",
  #                      "owner": "",
  #                      "id": 1,
  #                      "weight": 12}]

  # # Extracting weights
  # weights = [api["weight"] for api in open_api_keyset]
  # # Selecting one dictionary considering the weights
  # selected_api_key = random.choices(open_api_keyset, weights=weights, k=1)[0]
  # print (f"========== USING THE FOLLOWING: ", selected_api_key)

  selected_api_key = {'key': SECRET_KEY}
  return selected_api_key


# DEBUG = False
DEBUG = True

STORAGE_DIR = "storage"

# GOOGLE_CRED_PATH = "./google_cloud_credential.json"
GOOGLE_CRED_DICT = json.loads(os.environ.get("GCP_CREDS", "{}"))

INTERVIEW_AGENT_PATH = "interviewer_agent"



get_open_api_keyset()