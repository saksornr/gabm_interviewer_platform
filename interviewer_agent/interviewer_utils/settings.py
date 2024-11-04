import sys
import os
import random

def get_open_api_keyset(): 
  open_api_keyset = []
  open_api_keyset += [{"key": "",
                       "owner": "",
                       "id": 1,
                       "weight": 12}]

  # Extracting weights
  weights = [api["weight"] for api in open_api_keyset]
  # Selecting one dictionary considering the weights
  selected_api_key = random.choices(open_api_keyset, weights=weights, k=1)[0]
  print (f"========== USING THE FOLLOWING: ", selected_api_key)
  return selected_api_key


# DEBUG = False
DEBUG = True

STORAGE_DIR = "storage"

GOOGLE_CRED_PATH = ""

INTERVIEW_AGENT_PATH = "interviewer_agent"



get_open_api_keyset()