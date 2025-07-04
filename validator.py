from google import genai
from google.genai import types
import json
import re

class Validator:
    def __init__(self):
        open_key = self._load_key('./keys.json')
        self.key = open_key
        self.client = genai.Client(api_key=open_key)
        self.system = """
        You are part of an access to information system that is intended to make sure people get access to credible
        information. Users want to check the credibility of claims, stories or rumors through you and your responsibility
        is to do fact-checking on the claims. You are required to do a google search to get results relavant to the claim
        and then generate a fact-check validity report. The report contains 3 things: 1. summary of sources reporting on
        the claim if any, 2. credibility summary on the 3 most credible and 3 least credible of the sources if any and 3.
        A conclusion considering all the 2 things above.

        Here is the user's claim/question/story/story:
        """

    def _load_key(self, key_path):
        with open(key_path, 'r') as f:
            keys = json.load(f)
            return keys.get("google") # Assuming your key is stored under "api_key"

    def search(self, claim):
        grounding_tool = types.Tool(google_search=types.GoogleSearch())
        config = types.GenerateContentConfig(tools=[grounding_tool])
        response = self.client.models.generate_content(model="gemini-2.5-flash", contents=self.system + claim, config=config)
        return response.text