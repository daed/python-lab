"""requestorama.py: A simple script to test the performance of some servers"""
import asyncio
import time
import subprocess
import requests

REQUESTS_PER_SECOND = 105
SECONDS = 10

results_second_total_time = []
results = {
    "aio": [],
    "flask": []
}

async def get_requests(second, port, results):
    """Send a request to the server"""
    url = f'http://localhost:{port}'
    start_time = time.time()
    requests.get(url, timeout=5)
    end_time = time.time()
    results[second].append(end_time - start_time)

async def start_requests(second, port, results):
    """Start the requests"""
    awaitables = []
    start_time = time.time()
    for _ in range(REQUESTS_PER_SECOND):
        awaitables.append(get_requests(second, port, results))
    await asyncio.gather(*awaitables)
    end_time = time.time()
    results_second_total_time.append(end_time - start_time)


def start_aio_server():
    """Start the server"""
    try:
        print("starting aiohttp server")
        return subprocess.Popen(['python3', 'aiohttp_server.py'])
    except OSError:
        print("cannot start server, will attempt to continue")

def start_flask_server():
    """Start the server"""
    try:
        print("starting flask server")
        return subprocess.Popen(['python3', 'flask_server.py'])
    except OSError:
        print("cannot start server, will attempt to continue")

def stop_server(p):
    """Stop the server"""
    if p:
        p.kill()

def print_stats(label, results):
    """Print the statistics"""
    print()
    print("Results for", label)
    for i, result in enumerate(results):
        if len(result) > 0:
            print(f"Second {i}: {len(result)} requests, total time {results_second_total_time[i]} | high {max(result)}, low {min(result)}, average {sum(result)/len(result)}")

async def hit_server(results, port):
    awaitables = []
    print(f"requesting {REQUESTS_PER_SECOND} requests per second for {SECONDS} seconds on port {port}")
    for i in range(SECONDS):
        results.append([])
        awaitables.append(start_requests(i, port, results))
        await asyncio.sleep(1)
        try:
            print(f"{i}: avg {sum(results[i])/len(results[i])}")
        except ZeroDivisionError:
            print(f"{i}: no requests")
    await asyncio.gather(*awaitables)


async def async_main():
    """Main function"""
    try:
        ps = []
        try:
            ps.append(start_aio_server())
            ps.append(start_flask_server())
            await asyncio.sleep(3)
            await hit_server(results.get("aio"), 8081)
            await hit_server(results.get("flask"), 8082)
        except KeyboardInterrupt:
            pass
        for p in ps:
            stop_server(p)
        for val in results:
            print_stats(val, results[val])
    except Exception as e: # pylint: disable=broad-except
        print(e)
        if p:
            for p in ps:
                stop_server(p)

if __name__ == '__main__':
    asyncio.run(async_main())
