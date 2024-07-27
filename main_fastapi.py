from webscraper import main
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class UrlInput(BaseModel):
    url:str

app=FastAPI()

@app.post("/scrape_content")
async def scrape_content(input:UrlInput):
    response=main(input.url)
    if response=="success":
        return {"status":"success"}
    else:
        return {"status":"failure"}
if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=5001)
