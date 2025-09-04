from aiohttp import web
import json

async def handle_webhook_test(request):
    try:
        body = await request.json()
        print("Received body:", json.dumps(body, indent=2))
        return web.json_response({"status": "success", "message": "Body received"})
    except Exception as e:
        print(f"Error processing request: {e}")
        return web.json_response({"status": "error", "message": "Invalid JSON"}, status=400)

async def main():
    app = web.Application()
    app.router.add_post('/webhook-test', handle_webhook_test)
    print("Starting server on port 5050...")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5050)
    await site.start()
    print("Server started. Listening on http://0.0.0.0:5050")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
