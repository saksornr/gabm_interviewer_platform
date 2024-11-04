import threading
import queue
import io
import openai

from pydub import AudioSegment
from google.cloud import speech

from global_methods import *
from interviewer_agent.interviewer_utils.settings import * 

openai.api_key = get_open_api_keyset()["key"]


def jsp_log(message): 
  from datetime import datetime
  formatted_time = datetime.now().strftime("%H:%M:%S")
  print (f'[transcribe.py] {formatted_time} -- {message}')


def transcribe_voice(audio_buffer, optional_key_phrases=["my name is Joon"]):
  """
  Transcribes voice from an audio buffer using Google Speech-to-Text and 
  OpenAI's Whisper.

  The function first converts the audio buffer to an AudioSegment object to 
  determine its duration. If the audio is shorter than 20 seconds, it uses 
  Google's Speech-to-Text API for transcription, leveraging a service account 
  for authentication and enabling automatic punctuation.

  (Note: even when we use Google API, we still run this through Whisper, 
  which is more accurate. This is to compensate for Whisper's downside, which
  is that it is weak against empty audio as it hallucinates.)

  In case there are no results from Google's API, or if the audio is longer 
  than 20 seconds, the function then utilizes OpenAI's Whisper model. The 
  model is provided with the language setting and optional key phrases to 
  assist in the transcription process.

  Args:
    audio_buffer (BytesIO): A buffer containing the audio data.
    optional_key_phrases (list of str, optional): A list of key phrases that
      may be present in the audio. Useful for improving the accuracy of 
      transcription in case of specific or hard-to-spell words. 
      Defaults to ["my name is Joon"].

  Returns:
      str: The transcribed text.
  """
  duration_seconds = len(AudioSegment.from_file(audio_buffer)) / 1000.0  
  jsp_log("Starting to actually transcribe user's voice")
  jsp_log(f"Audio duration: {duration_seconds} seconds")

  if duration_seconds < 20: 
    # Use service account credentials by specifying the private key file
    g_client = speech.SpeechClient.from_service_account_json(GOOGLE_CRED_PATH)

    # The buffer's bytes can be directly used as the content
    content = audio_buffer.getvalue()
    audio = speech.RecognitionAudio(content=content)

    # Configure the request with the desired parameters
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True  # Enable automatic punctuation
    )
    # Transcribe the audio file
    response = g_client.recognize(config=config, audio=audio)

    jsp_log(f"From Google API: {response.results}")
    if not response.results: 
      jsp_log("Ending transcription with an empty str")
      return ""

  # For capturing hard to spell words, like names
  optional_key_phrases = ', '.join(optional_key_phrases)
  audio_buffer.name = "file.wav"
  whisper_completion = openai.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_buffer,
    language="en",
    prompt=optional_key_phrases)
  user_speech = whisper_completion.text

  jsp_log(f"Whisper API keyword: {optional_key_phrases}")
  jsp_log(f"From Whisper API: {user_speech}")
  return user_speech


def threaded_transcribe_voice(audio_buffer, 
                              optional_key_phrases=["my name is Joon"], 
                              timeout=8, 
                              max_retries=3):
  """
  Transcribes voice from an audio buffer using a threaded approach with 
  retries and timeout handling.

  This function creates a thread to handle the transcription process. It 
  retries the transcription up to a specified number of times if it fails or 
  times out. The function uses the `transcribe_voice` function for the actual 
  transcription.

  Args:
    audio_buffer (BytesIO): A buffer containing the audio data.
    optional_key_phrases (list of str, optional): A list of key phrases 
      that may be present in the audio. Useful for improving the accuracy 
      of transcription in case of specific or hard-to-spell words.
      Defaults to ["my name is Joon"].
    timeout (int, optional): The maximum number of seconds to wait for a 
      transcription to complete before timing out. Defaults to 8 seconds.
    max_retries (int, optional): The maximum number of times to retry the 
      transcription in case of failure or timeout. Defaults to 3 retries.

  Returns:
    str: The transcribed text, or a placeholder string "..." if 
      transcription fails after maximum retries.
  """
  # def worker():
  #   try:
  #     result = transcribe_voice(audio_buffer, optional_key_phrases)
  #     q.put(result)
  #   except Exception as e:
  #     q.put(e)

  # jsp_log("Starting the thread for transcribing voice")
  # jsp_log(f"Timeout is {timeout}, and max retries is {max_retries}")

  # for count in range(max_retries):
  #   jsp_log(f"Current thread try: {count}")

  #   q = queue.Queue()
  #   transcribe_thread = threading.Thread(target=worker)
  #   transcribe_thread.start()
  #   transcribe_thread.join(timeout)

  #   if transcribe_thread.is_alive():
  #     # Stop the thread if it's still running after the timeout
  #     # Note: This is not a safe way to stop a thread, better alternatives 
  #     # should be considered
  #     jsp_log(f"Transcription timed out, retrying...")
  #     transcribe_thread._stop()
  #   else:
  #     # Check if queue has a result or an exception
  #     result = q.get()
  #     if isinstance(result, Exception):
  #       jsp_log(f"Error occurred: {result}")
  #     else:
  #       jsp_log(f'Transcribed as follows: "{result}')
  #       return result

  # jsp_log(f"Max retries reached, transcription failed.")
  # return "..."


  def worker(stop_event):
    try:
      result = transcribe_voice(audio_buffer, optional_key_phrases)
      if not stop_event.is_set():
        q.put(result)
    except Exception as e:
      if not stop_event.is_set():
        q.put(e)

  jsp_log("Starting the thread for transcribing voice")
  jsp_log(f"Timeout is {timeout}, and max retries is {max_retries}")

  for count in range(max_retries):
    jsp_log(f"Current thread try: {count}")
    
    q = queue.Queue()
    stop_event = threading.Event()
    transcribe_thread = threading.Thread(target=worker, args=(stop_event,))
    transcribe_thread.start()
    transcribe_thread.join(timeout)

    if transcribe_thread.is_alive():
      # Signal the thread to stop and wait a bit for cleanup
      stop_event.set()
      transcribe_thread.join(1)
      jsp_log(f"Transcription timed out, retrying...")
    else:
      result = q.get()
      if isinstance(result, Exception):
        jsp_log(f"Error occurred: {result}")
      else:
        jsp_log(f'Transcribed as follows: "{result}"')
        return result

  jsp_log(f"Max retries reached, transcription failed.")
  return "..."



























