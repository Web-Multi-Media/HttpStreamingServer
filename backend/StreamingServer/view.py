from revproxy.views import ProxyView

class TorrentsView(ProxyView):
    upstream = 'http://localhost:9091/transmission/web'
    add_x_forwarded = True

class TorrentsRPCView(ProxyView):
    upstream = 'http://localhost:9091/transmission/rpc'
    add_x_forwarded = True

class TorrentsUploadView(ProxyView):
    upstream = 'http://localhost:9091/transmission/upload'
    add_x_forwarded = True