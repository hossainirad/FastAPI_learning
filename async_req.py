import time
import asyncio
import httpx


class Reqer():
	def __init__(self):
		self.url = 'http://127.0.0.1:8000/users/'

	async def send_request(self, url):
		async with httpx.AsyncClient(timeout=60.0) as client:
			response = await client.get(url)
			return response.status_code

	async def start_crawl(self):
		req = await self.send_request(self.url)
		print(req)
		return req


start = time.time()


async def main():
	crowl_list = []
	for i in range(1000):
		a = Reqer()
		crowl_list.append(a.start_crawl())
	await asyncio.gather(*crowl_list)

asyncio.run(main())
end = time.time()
print(end - start)
