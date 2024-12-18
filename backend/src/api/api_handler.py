# src/api/api_handler.py
import base64
import os
import random

from aiohttp import web
import time

from .model.azure_model import AzureModel
from .audio_converter import convert_webm_to_wav
from .vocab import NORMAL_VOCAB, DIALOG_VOCAB


# Define a cache with a TTL (in seconds)
NORMAL_CACHE = {}
NORMAL_CACHE_TTL = 10  # Cache duration of 10 seconds

DIALOGUE_CACHE = {}
DIALOGUE_CACHE_TTL = 10

# HTTP API handler
async def handle_send_input(request):
    # Simple API response (can be expanded based on your needs)
    return web.Response(text="Hello, World!")


async def get_normal_1v1_words(request):
    # return words based on topic in json format
    # get topic from request query
    topic = request.query.get("topic")
    # Check if we have a cached response for this topic that is still valid
    if topic in NORMAL_CACHE:
        cached_response, timestamp = NORMAL_CACHE[topic]
        if time.time() - timestamp < NORMAL_CACHE_TTL:
            # Return cached response if it's still valid
            return web.json_response(cached_response)

    # If no valid cache, generate a new random sample and cache it
    random_response = random.sample(NORMAL_VOCAB[topic], 3)
    NORMAL_CACHE[topic] = (random_response, time.time())  # Cache the response with the current timestamp

    return web.json_response(random_response)


async def get_dialogue_1v1_words(request):
    # return words based on topic in json format
    # get topic from request query
    print (request)
    print (request.query.get("topic"))

    topic = request.query.get("topic")

    if topic in DIALOGUE_CACHE:
        cached_response, timestamp = DIALOGUE_CACHE[topic]
        if time.time() - timestamp < DIALOGUE_CACHE_TTL:
            return web.json_response(cached_response)
        
    # random_response = random.sample
    # return web.json_response({"dialogues": random.sample(DIALOG_VOCAB[topic], 1)[0]})
    random_response = random.sample(DIALOG_VOCAB[topic], 1)[0]
    DIALOGUE_CACHE[topic] = (random_response, time.time())  # Cache the response with the current timestamp

    return web.json_response(random_response)

# API function to handle scoring logic (stub implementation)
async def return_topic_words_score(word: str, audio_input: bytes, client_id: str):
    # Convert the WebM audio input to WAV format (16kHz 16-bit)
    wav = convert_webm_to_wav(audio_input)

    # Make a request to the model server and get the scores
    am = AzureModel()
    response = am.run_assessment(word=word, audio=wav)
    # response = await make_grpc_request(word, wav)

    # Simulate scoring based on the word and audio input (to be replaced with actual logic)
    print(f"Scoring for word '{word}' with audio input of size {len(audio_input) / 1024 / 1024} megabytes")

    base64_audio = base64.b64encode(wav).decode('utf-8')

    json_data = {
        "question": word,
        "audio_file": base64_audio,
        "score": response,
        "sample_audio_file": base64_audio,
    }

    return json_data
