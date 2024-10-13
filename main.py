import uvicorn
import psycopg2
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
   "http://127.0.0.1:5500"
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

class Yetimhane:
   def __init__(self,id,ad,adres):
      self.id = id
      self.ad = ad
      self.adres = adres
      

   def to_dict(self):
        return {
            "id": self.id,
            "ad": self.ad,
            "adres": self.adres
         }   


@app.get("/veri")
async def index():
   return {"message": "Hello World"}

@app.get("/yetimhaneler")
async def index():
   connection = psycopg2.connect(user="postgres",
                                 password="1907",
                                 host="127.0.0.1",
                                 port="5434",
                                 database="dbyetimhane")
   cursor = connection.cursor()
   cursor.execute("Select * From yetimhane")
   result = cursor.fetchall()
   cursor.close()
   connection.close()

   yetimhane_list = []
   for row in result:
      yetimhane = Yetimhane(row[0],row[1],row[2])
      yetimhane_list.append(yetimhane.to_dict())

   return JSONResponse(content=yetimhane_list)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)