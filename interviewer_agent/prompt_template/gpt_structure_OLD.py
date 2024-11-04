import json
import random
import openai
import time 
import threading

from interviewer_agent.interviewer_utils.settings import * 

openai.api_key = get_open_api_keyset()["key"]


def jsp_log(message): 
  from datetime import datetime
  formatted_time = datetime.now().strftime("%H:%M:%S")
  print (f'[gpt_structure.py] {formatted_time} -- {message}')


# ============================================================================
# #######################[SECTION 0: HELPER FUNCTIONS] #######################
# ============================================================================

def temp_sleep(seconds=0.1):
  """
  Pause the program's execution for a specified number of seconds.
  ARGS:
    seconds (float, optional): The duration for which the program should 
      sleep, in seconds. Default is 0.1 seconds.
  RETURNS:
    None
  Example:
    To pause the program for 2.5 seconds, you can call the function like this:
    >>> temp_sleep(2.5)
  """
  time.sleep(seconds)


def generate_prompt(curr_input, prompt_lib_file): 
  """
  Takes in the current input (e.g. comment that you want to classifiy) and 
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this 
  function replaces this substr with the actual curr_input to produce the 
  final promopt that will be sent to the GPT3 server. 
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file. 
  RETURNS: 
    a str prompt that will be sent to OpenAI's GPT server.  
  """
  if type(curr_input) == type("string"): 
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):   
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt: 
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()


# ============================================================================
# ################## [SECTION 1: SAFE GENERATE (Original)] ###################
# ============================================================================

def ChatGPT_simple_request(prompt, system_prompt=""): 
  try: 
    if system_prompt: 
      completion = openai.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": prompt}
        ]
      )
    else: 
      completion = openai.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}])
    output = completion.choices[0].message.content
    return output
  except Exception as e:
    return "GENERATION ERROR"


def chat_safe_generate(prompt, 
                       gpt_version="ChatGPT",
                       repeat=3,
                       fail_safe_response="error",
                       func_validate=None,
                       func_clean_up=None,
                       verbose=False): 
  if verbose: 
    print (f"CURRENT PROMPT\n{prompt}")

  for i in range(repeat): 
    try:
      curr_gpt_response = ChatGPT_simple_request(prompt).strip()

      if curr_gpt_response == "GENERATION ERROR": 
        time.sleep(2**i)
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)

      print (f"---- REPEAT COUNT: {i}")
      print (f"Current response: ")
      print (curr_gpt_response)
      print (f"---- DEBUG CASE ^: {i}")

    except:
      pass

  print ("FAIL SAFE TRIGGERED") 
  return fail_safe_response


# ============================================================================
# ################## [SECTION 2: SAFE GENERATE (Threading)] ##################
# ============================================================================


def threaded_ChatGPT_simple_request(prompt, system_prompt=""):
  """
  Sends a prompt to OpenAI's ChatGPT and retrieves a response using a threaded
  approach with retries.

  This function creates a thread to send a prompt to the ChatGPT model and 
  waits for a response. It retries the request up to a maximum number of times 
  if it fails to get a response within a specified timeout.

  Args:
    prompt (str): The user's prompt to send to the ChatGPT model.
    system_prompt (str, optional): An additional system-level prompt to 
      provide context or instructions to the model. Useful for setting up a 
      specific scenario or providing guidelines for the response.
      Defaults to an empty string.

  Returns:
    str: The response from ChatGPT, or an error message if the request 
      fails or the thread hangs.
  """
  def target():
    nonlocal output
    try:
      if system_prompt:
        completion = openai.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
          ]
        )
      else:
        completion = openai.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "user", "content": prompt}]
        )
      output = completion.choices[0].message.content
    except Exception as e:
      output = "GENERATION ERROR"

  max_retries = 3
  retries = 0

  while retries < max_retries:
    output = None
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout=8)

    if thread.is_alive():
      # Thread is still running after 5 seconds, retrying
      retries += 1
      jsp_log(f"Attempt {retries} failed, retrying...")
    else:
      # Function completed within the timeout
      return output

  return "THREAD HANGING"


def threaded_chat_safe_generate(prompt, 
                                gpt_version="ChatGPT",
                                repeat=3,
                                fail_safe_response="error",
                                func_validate=None,
                                func_clean_up=None,
                                verbose=False): 
  """
  Generates responses to a prompt using ChatGPT with safety and validation 
  checks, retrying if necessary.

  This function sends a prompt to ChatGPT and retrieves a response. It 
  includes additional mechanisms for validation and cleanup of the generated 
  response. The function retries the generation process a specified number of 
  times if the initial attempts are not successful or do not pass validation.

  Args:
    prompt (str): The prompt to be sent to the ChatGPT model.
    gpt_version (str, optional): The version of the GPT model to use. 
      Defaults to "ChatGPT".
    repeat (int, optional): The number of times to retry generating a 
      response if validation fails. Defaults to 3.
    fail_safe_response (str, optional): The response to return if all 
      retries fail or an error occurs. Defaults to "error".
    func_validate (callable, optional): A function to validate the generated 
      response. It should take two arguments: the response and the original 
      prompt, and return a boolean.
    func_clean_up (callable, optional): A function to clean up or modify the 
      generated response before returning it. It should take two arguments: 
      the response and the original prompt, and return a modified response.
    verbose (bool, optional): If True, enables additional logging for 
      debugging. Defaults to False.

  Returns:
    str: The generated and processed response from ChatGPT, or the fail-safe 
      response if generation fails.
  """
  if verbose: 
    jsp_log(f"Current prompt:\n {prompt}")

  for i in range(repeat): 
    try:
      curr_gpt_response = threaded_ChatGPT_simple_request(prompt).strip()

      if curr_gpt_response == "GENERATION ERROR": 
        time.sleep(2**i)

      if curr_gpt_response == "THREAD HANGING": 
        break
      
      if func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt)

      jsp_log(f"Error occurred in generating.")
      jsp_log(f"Current repeat count is {i}.")
      jsp_log(f"Current erred response is {curr_gpt_response}.")

    except:
      pass

  jsp_log(f"We failed to generate: {curr_gpt_response}")
  jsp_log(f"Following failsafe is triggered: {fail_safe_response}")
  return fail_safe_response


# ============================================================================
# #################### [SECTION 3: OTHER API FUNCTIONS] ######################
# ============================================================================

def get_embedding(text, model="text-embedding-ada-002"):
  """
  Generates an embedding for a given text using OpenAI's specified embedding 
  model.

  This function creates a numerical representation (embedding) of the provided 
  text. It is useful for various natural language processing tasks like 
  semantic analysis, similarity comparison, etc. The function uses OpenAI's 
  Embedding API to generate the embedding.

  Args:
    text (str): The text for which the embedding is to be generated.
    model (str, optional): The model to be used for generating the embedding. 
      Defaults to "text-embedding-ada-002".

  Returns:
    list: A list of numerical values representing the embedding of the given 
      text.
  """
  text = text.replace("\n", " ")
  if not text: 
    text = "this is blank"
  return openai.Embedding.create(
    input=[text], model=model)['data'][0]['embedding']









































