import os
import json
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel
from together import Together
from fastapi import FastAPI, HTTPException
from Prompts.Browse import BROWSING_PROMPT_TEMPLATE
load_dotenv(override=True)
app = FastAPI()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))


class Listing(BaseModel):
    name: str
    description: str
    value: float


class BrowsingRequest(BaseModel):
    request: str
    listings: list[Listing]


class BrowsingResponse(BaseModel):
    top_listings: list[Listing]



@app.post("/browse", response_model=BrowsingResponse)
async def browse_endpoint(request: BrowsingRequest):
    try:
        listings_text = "\n\n".join([
            f"Item name: {item.name}\n"
            f"Item description: {item.description}\n"
            f"Price: {item.value}"
            for item in request.listings
        ])
        
        updated_prompt = BROWSING_PROMPT_TEMPLATE.format(
            request=request.request,
            listings=listings_text
        )
        
        messages = [{"role": "user", "content": updated_prompt}]
        
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            messages=messages,
            max_tokens=1024,
            temperature=0,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
        )
        ai_response = completion.choices[0].message.content
        cleaned_response = ai_response.strip()

        if not (cleaned_response.startswith('[') and cleaned_response.endswith(']')):
            cleaned_response = cleaned_response.split('[', 1)[-1].rsplit(']', 1)[0]
            cleaned_response = f"[{cleaned_response}]"
        
        parsed_response = json.loads(cleaned_response)
        top_listings = [Listing(**item) for item in parsed_response]
        return BrowsingResponse(top_listings=top_listings)
    
    except json.JSONDecodeError as json_error:
        raise HTTPException(status_code=500, detail=f"Invalid JSON response from AI: {str(json_error)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)