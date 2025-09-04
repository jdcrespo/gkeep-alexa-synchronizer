import gkeepapi
import websockets
import asyncio
import json
from dotenv import load_dotenv
import os
from aiohttp import web
import aiohttp

load_dotenv()

token = os.getenv('GOOGLE_KEEP_TOKEN')
google_keep_email = os.getenv('GOOGLE_KEEP_EMAIL')
google_keep_note_id = os.getenv('GOOGLE_KEEP_NOTE_ID')
websocket_uri = os.getenv('WEBSOCKET_URI')
clear_checked = os.getenv('CLEAR_CHECKED', 'false').lower() == 'true'


async def get_items_from_alexa(websocket):
    try:
        await websocket.send(json.dumps({"command": "get_list", "args": {}}))
        response = await websocket.recv()
        result = json.loads(response)
        if "result" in result and result["error"] is None:
            return result.get("result", [])
    except Exception as e:
        print(f"Error getting items from Alexa: {e}")
    return []

async def remove_item_from_alexa(websocket, item):
    try:
        await websocket.send(json.dumps({"command": "remove_item", "args": {'item': item}}))
        await websocket.recv()
    except Exception as e:
        print(f"Error removing item from Alexa: {e}")


async def process_items_common(websocket, webhook_url=None):
    try:
        print("Getting items from Alexa...")
        alexa_items = await get_items_from_alexa(websocket)
        print(f"Items obtained: {len(alexa_items)} items")

        print("Getting note from Google Keep...")
        keep = gkeepapi.Keep()
        keep.authenticate(google_keep_email, token)

        note = keep.get(google_keep_note_id)
        if note is None:
            print("Note not found, exiting...")
            response = {"status": "error", "message": "Note not found"}
            if webhook_url:
                await send_webhook_response(webhook_url, response)
            return web.json_response(response, status=404) if not webhook_url else None

        alexa_main_item = next((item for item in note.unchecked if item.text == "Alexa"), None)
        if alexa_main_item is None:
            print("No Alexa item found.")
            response = {"status": "error", "message": "No Alexa item found"}
            if webhook_url:
                await send_webhook_response(webhook_url, response)
            return web.json_response(response, status=404) if not webhook_url else None

        old_items = [item for item in note.unchecked if item.parent_item is not None and item.parent_item.text == 'Alexa']
        print(f"Old Alexa items: {len(old_items)} found")
        current_items = []
        for old_item in old_items:
            if old_item.text not in alexa_items:
                old_item.delete()
            else:
                current_items.append(old_item.text)
        
        print("Adding Alexa items to Google Keep...")
        alexa_items_to_delete = []
        for alexa_item in alexa_items:
            if alexa_item not in current_items:
                alexa_main_item.add(alexa_item)
                alexa_items_to_delete.append(alexa_item)
        
        if clear_checked:
            print("Removing checked items from Google Keep...")
            for checked_item in note.checked:
                checked_item.delete()

        print("Syncing Google Keep...")
        keep.sync()

        print("Removing items from Alexa...")
        for alexa_item in alexa_items_to_delete:
            await remove_item_from_alexa(websocket, alexa_item)

        print("Finished processing items.")
        response = {
            "status": "success",
            "message": f"{len(alexa_items_to_delete)} items synchronized"
        }
        if webhook_url:
            await send_webhook_response(webhook_url, response)
        return web.json_response(response) if not webhook_url else None
    except Exception as e:
        print(f"Error processing items: {e}")
        response = {"status": "error", "message": f"Error: {e}"}
        if webhook_url:
            await send_webhook_response(webhook_url, response)
        return web.json_response(response, status=500) if not webhook_url else None

async def process_items():
    async with websockets.connect(websocket_uri) as websocket:
        return await process_items_common(websocket)

async def process_items_async(webhook_url):
    async with websockets.connect(websocket_uri) as websocket:
        await process_items_common(websocket, webhook_url)

async def send_webhook_response(webhook_url, response):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(webhook_url, json=response) as resp:
                print(f"Webhook response sent. Status: {resp.status}")
        except Exception as e:
            print(f"Error sending webhook response: {e}")

async def handle_sync(request):
    return await process_items()

async def handle_async(request):
    try:
        data = await request.json() if request.can_read_body else {}
        webhook_url = data.get("webhook") if data else None
        
        asyncio.create_task(process_items_async(webhook_url))
        return web.json_response({"status": "success", "message": "Processing started"})
    except Exception as e:
        print(f"Error handling async request: {e}")
        return web.json_response({"status": "error", "message": f"Error: {e}"}, status=500)

async def main():
    app = web.Application()
    app.router.add_get('/sync', handle_sync)
    app.router.add_post('/async', handle_async)
    print("Starting server on port 5000...")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()
    print("Server started. Listening on http://0.0.0.0:5000")
    while True:
        await asyncio.sleep(3600)

asyncio.run(main())

