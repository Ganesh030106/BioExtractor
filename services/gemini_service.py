"""
Gemini AI Service
-----------------
Uses Google Gemini API to intelligently extract structured profile data
from free-form text. Falls back to the regex-based extractor if the API
key is missing or a request fails.
"""

import json
from datetime import datetime

import google.generativeai as genai

from config.settings import GEMINI_API_KEY, GEMINI_MODEL, is_gemini_configured

# ------------------------------------------------------------------ #
#  Prompt template
# ------------------------------------------------------------------ #
_SYSTEM_PROMPT = """You are an expert data extraction engine. 
Given a free-form text (bio, self-introduction, profile description, or any paragraph), 
extract ALL possible structured information and return ONLY a valid JSON object.

Rules:
1. Extract every field you can find. If a field is not mentioned, set it to null.
2. Return ONLY the JSON — no markdown fences, no explanation.
3. For tech_stacks and education, return arrays. For interests, return an array.
4. Be smart about context — infer company names, roles, locations even if phrased indirectly.
5. For experience, always format as "<N> years" (e.g., "7 years").
6. Normalize technology names (e.g., "js" → "JavaScript", "react" → "React").

Required JSON schema:
{
    "name": "<string or null>",
    "role": "<string or null>",
    "experience": "<string like '7 years' or null>",
    "company": "<string or null>",
    "tech_stacks": ["<tech1>", "<tech2>"] or null,
    "education": ["<degree1>", "<field1>"] or null,
    "location": "<string or null>",
    "email": "<string or null>",
    "phone": "<string or null>",
    "linkedin": "<string or null>",
    "github": "<string or null>",
    "interests": ["<interest1>", "<interest2>"] or null
}"""


def _configure_client(api_key):
    """Configure the Gemini client with the API key."""
    genai.configure(api_key=api_key)


def extract_with_gemini(text, api_key=None):
    """
    Send the text to Google Gemini and parse the structured JSON response.

    Returns:
        dict  – extracted profile data (same schema as regex extractor)
        None  – if the API call fails (caller should fall back to regex)
    """
    if not api_key or not api_key.strip():
        print("[Gemini Service] Warning: No API key provided from user.")
        return None

    try:
        _configure_client(api_key)

        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": 0.1,
                "top_p": 0.95,
                "max_output_tokens": 2048,
            },
        )

        prompt = f"{_SYSTEM_PROMPT}\n\nText to extract from:\n\"\"\"\n{text}\n\"\"\""

        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Strip markdown fences if Gemini wraps it
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3].strip()
        if raw.startswith("json"):
            raw = raw[4:].strip()

        extracted = json.loads(raw)

        # Ensure consistent schema — fill missing keys with None
        fields = [
            "name", "role", "experience", "company", "tech_stacks",
            "education", "location", "email", "phone",
            "linkedin", "github", "interests",
        ]
        for field in fields:
            if field not in extracted:
                extracted[field] = None

        # Attach metadata
        extracted["raw_text"] = text
        extracted["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        extracted["extracted_by"] = "gemini"

        return extracted

    except Exception as e:
        print(f"[Gemini Service] Error: {e}")
        return None
