
import grapi

server = grapi.Server()

@server("/hello")
def GET(request: grapi.Request, response: grapi.Response) -> grapi.Response:
    print(request.body)
    return response.text("Hello, world!")

server.run()
