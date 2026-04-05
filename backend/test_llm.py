import urllib.request
from app.core.config import settings

try:
    print(f"Key: {settings.GROQ_API_KEY[:5]}...")
    url = "https://api.groq.com/openai/v1/models"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"})
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        body = response.read().decode('utf-8')
        print("Body:", body[:200])
except Exception as e:
    print("Failed requests:")
    print(str(e))
