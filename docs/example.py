# Example GRAPI server setup

"""
Sample directory structure:
```
.
|-- server.py
|-- views
|   |-- .html
|   |-- .css
|   |-- .js
|   |-- about
|   |   |-- .html
|   |   |-- .css
|   |   |-- .js
|   |-- favicon.ico
```
Views are automatically served.
"""

import grapi

server = grapi.Server()


@server("/hello")
def GET(request: grapi.Request, response: grapi.Response) -> grapi.Response:
    return response.text("Hello, world!")


server.run()
