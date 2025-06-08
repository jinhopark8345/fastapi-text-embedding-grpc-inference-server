from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import grpc
import tei_pb2
import tei_pb2_grpc

app = FastAPI()

TEI_GRPC_ADDRESS = "localhost:8080"

class TextInput(BaseModel):
    text: str

@app.post("/embed")
def embed_text(payload: TextInput):
    try:
        with grpc.insecure_channel(TEI_GRPC_ADDRESS) as channel:
            stub = tei_pb2_grpc.EmbedStub(channel)
            request = tei_pb2.EmbedRequest(inputs=payload.text)  # <-- not a list anymore
            response = stub.Embed(request)
            return {"embedding": list(response.embeddings)}  # note: flat float list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
