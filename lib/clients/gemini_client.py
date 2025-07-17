import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions, Part

# .env laden
load_dotenv()

# Vertex AI aktivieren?
USE_VERTEX_AI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False").lower() == "true"

# Authentifizierung: Dienstkonto-Credentials prüfen
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path or not os.path.isfile(credentials_path):
    raise EnvironmentError("Fehlende oder ungültige .json-Datei für GOOGLE_APPLICATION_CREDENTIALS.")

# Projektkonfiguration
project_id = os.getenv("GCP_PROJECT_ID")
location = os.getenv("GCP_LOCATION", "europe-west4")

if not project_id:
    raise EnvironmentError("GCP_PROJECT_ID ist nicht gesetzt. Bitte in der .env-Datei definieren.")

# Gemini-Client erstellen
client = genai.Client(
    http_options=HttpOptions(api_version="v1"),
    project=project_id,
    location=location
)

# Standardmodell
DEFAULT_MODEL = "gemini-2.5-flash"

def generate(input_type: str, prompt: str, model: str = DEFAULT_MODEL, image_path: str = None) -> str:
    if input_type == "text":
        return generate_text(prompt, model)
    elif input_type == "image":
        return generate_image_understanding(prompt, image_path, model)
    else:
        raise NotImplementedError(f"Input-Typ '{input_type}' ist in Gemini-Client noch nicht implementiert.")

def generate_text(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Textantwort mit Gemini über Vertex AI erzeugen"""
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Fehler bei der Generierung: {e}"

def generate_image_understanding(prompt: str, image_path: str, model: str = DEFAULT_MODEL) -> str:
    if not image_path or not os.path.isfile(image_path):
        return f"Bildpfad ungültig oder nicht gefunden: {image_path}"

    try:
        image_part = Part.from_bytes(
            data=open(image_path, "rb").read(),
            mime_type="image/jpeg"
        )

        response = client.models.generate_content(
            model=model,
            contents=[
                prompt,
                image_part
            ]
        )
        return response.text
    except Exception as e:
        return f"Fehler bei der Bildanalyse: {e}"

