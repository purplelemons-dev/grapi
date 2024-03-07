# Example GRAPI server setup

import grapi

server = grapi.Server()


@server("/hello")
def GET(request, response):
    return response.text("Hello, world!")

server.run()
