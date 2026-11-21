import asyncio
import websockets

ENDPOINT_ID = "YOUR_ENDPOINT_ID"

URLS = {
    "Instance A": f"ws://127.0.0.1:8000/api/ws/endpoints/13164d03-da73-485d-b84e-1f7623163d1f",
    "Instance B": f"ws://127.0.0.1:8001/api/ws/endpoints/13164d03-da73-485d-b84e-1f7623163d1f",
}


async def listen(name: str, url: str):
    try:
        async with websockets.connect(url) as websocket:
            print(f"[{name}] Connected!")

            while True:
                message = await websocket.recv()
                print(f"\n[{name}] Received: {message}")

    except Exception as exc:
        print(f"[{name}] Connection error: {exc}")


async def main():
    await asyncio.gather(
        *(listen(name, url) for name, url in URLS.items())
    )


if __name__ == "__main__":
    asyncio.run(main())
