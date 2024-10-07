import httpx

class RESTClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def request(self, endpoint: str, method: str = "GET", json: dict = None):
        async with httpx.AsyncClient() as client:
            response = await client.request(method, f"{self.base_url}/{endpoint}", json=json)
            response.raise_for_status() 
            return response.json()


# Could be easier replaced for grpc client

# Example of usage: 

# client = RESTClient(base_url="https://anotherservice.localhost")
# data = await client.request("some_endpoint", method="POST", json={"key": "value"})
    