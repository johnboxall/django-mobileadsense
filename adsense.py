import time
from UserDict import UserDict
from django.utils.http import urlencode


def adsense(request, client, ad_type="text_image", channel="", 
            format="mobile_single", markup="xhtml", oe="utf8", 
            output="xhtml", timeout=1, fail_silently=False):
    a = AdSense(request, client, ad_type, channel, format, markup, oe, output)
    return a.display(timeout, fail_silently)
    

class AdSense(UserDict):
    endpoint = '%s://pagead2.googlesyndication.com/pagead/ads?%s'

    def __init__(self, request, publisher_id, ad_type="text_image", channel="", 
                 format="mobile_single", markup="xhtml", encoding="utf8", 
                 output="xhtml"):
        self.request = request
        self.data = {
            "client": "ca-mb-%s" % publisher_id,
            "ad_type": ad_type,
            "channel": channel,
            "format": format,
            "markup": markup,
            "oe": encoding,
            "output": output,
            "dt": int(time.time() * 1000),
            "ip": self.request.META.get("REMOTE_ADDR", ""),
            "ref": self.get_header("REFERER"),
            "useragent": self.get_header("USER_AGENT"),
            "url": request.build_absolute_uri()
        }
        
        self.set_screen_size()
        self.set_muid()
        self.set_via_and_accept()
    
    def get_header(self, header, default=""):
        return self.request.META.get("HTTP_%s" % header, default)
    
    def set_screen_size(self):
        screen_res = self.get_header("UA_PIXELS") or \
                     self.get_header("X_UP_DEVCAP_SCREENPIXELS") or \
                     self.get_header("X_JPHONE_DISPLAY")
        try:
            self.data["u_w"], self.data["u_h"] = screen_res.split("[x,*]")
        except ValueError:
            pass
    
    def set_muid(self):
        self.data["muid"] = self.get_header("X_DCMGUID") or \
                            self.get_header("X_UP_SUBNO") or \
                            self.get_header("X_JPHONE_UID") or \
                            self.get_header("X_EM_UID")
    
    def set_via_and_accept(self):
        if self.data["useragent"] == "":
            self.data.update({
                "via": self.get_header("VIA"),
                "accept": self.get_header("ACCEPT")        
            })
    
    def build_url(self):        
        scheme = "http"
        if self.request.is_secure():
            scheme = "https"
        query = urlencode(self.data)
        return self.endpoint % (scheme, query)
    
    def fetch(self, url, timeout=1, fail_silently=False):
        import urllib2
        import socket
        
        default_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        try:
            return urllib2.urlopen(url).read()
        except urllib2.URLError:
            if fail_silently:
                return ""
            raise
        finally:
            socket.setdefaulttimeout(default_timeout)
    
    def display(self, timeout, fail_silently=False):
        return self.fetch(self.build_url(), timeout, fail_silently)