import os
import asyncio
from google import genai

async def main():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyD_3RrnqFslKVJViR1hFBysbK7fjVk7I7U"))
    models = await client.aio.models.list()
    for m in models:
        print(f"Model: {m.name}")

if __name__ == "__main__":
    asyncio.run(main())
