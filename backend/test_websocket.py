import asyncio
import websockets

ENDPOINT_ID = "13164d03-da73-485d-b84e-1f7623163d1f"

async def main():
    url = f"ws://127.0.0.1:8000/api/ws/endpoints/{ENDPOINT_ID}"

    async with websockets.connect(url) as websocket:
        print("Connected! Waiting for webhook events...")

        message = await websocket.recv()
        print("Received:", message)

asyncio.run(main())
