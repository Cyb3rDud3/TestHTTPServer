
URLS = {}
from typing import List
from core.server import BaseServer




class TestServer:
    functions = {"get","post","put","delete","head"}
    cache = {}
    def __getattribute__(self,name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr,"__call__") and attr.__name__ in self.functions and attr not in URLS.values():
            def new_func(*args,**kwargs):
                url = args[0]
                def inner(func: object):
                    URLS.update({url: {"method": attr.__name__.upper(), "handler": func}})
                    print(URLS)
                    return func
                return inner
            return new_func
        return attr


    def validate_required_params(self,required_params: List):
        def inner(func: object):
            def _inner(request: BaseServer):
                request_params = request.query if request.method == "GET" else request.post_data
                for param in required_params:
                    if param not in request_params:
                        return request.send_error(code=400,message="Missing Params!")
                return func(request)
            return _inner
        return inner




    def post(self,*args,**kwargs):
        pass

    def get(self,*args,**kwargs):
        pass

    def head(self,*args,**kwargs):
        pass

    def put(self,*args,**kwargs):
        pass

    def delete(self,*args,**kwargs):
        pass


