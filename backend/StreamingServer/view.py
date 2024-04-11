from revproxy.views import ProxyView

class TorrentsView(ProxyView):
    upstream = 'http://localhost:9091/transmission/web'

class TorrentsRPCView(ProxyView):
    upstream = 'http://localhost:9091/transmission/rpc'

class TorrentsUploadView(ProxyView):
    upstream = 'http://localhost:9091/transmission/upload'