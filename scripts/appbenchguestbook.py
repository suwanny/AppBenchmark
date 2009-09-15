# The Grinder 3.2
# HTTP script recorded by TCPProxy at Jul 29, 2009 11:44:39 AM

from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from net.grinder.plugin.http import HTTPPluginControl, HTTPRequest
from HTTPClient import NVPair
connectionDefaults = HTTPPluginControl.getConnectionDefaults()
httpUtilities = HTTPPluginControl.getHTTPUtilities()

# To use a proxy server, uncomment the next line and set the host and port.
# connectionDefaults.setProxyServer("localhost", 8001)

# These definitions at the top level of the file are evaluated once,
# when the worker process is started.

url0 = 'http://appbench-guestbook.appspot.com:80'

connectionDefaults.defaultHeaders = \
  ( NVPair('Accept-Language', 'ko'),
    NVPair('Accept-Encoding', 'gzip, deflate'),
    NVPair('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'),
    NVPair('Accept', 'image/gif, image/x-xbitmap, image/jpeg, application/xaml+xml, */*'), )

headers0= ( )

# Create an HTTPRequest for each request, then replace the
# reference to the HTTPRequest with an instrumented version.
# You can access the unadorned instance using request101.__target__.
request101 = HTTPRequest(url=url0, headers=headers0)
request101 = Test(101, 'POST sign').wrap(request101)

request102 = HTTPRequest(url=url0, headers=headers0)
request102 = Test(102, 'GET /').wrap(request102)

class TestRunner:
  """A TestRunner instance is created for each worker thread."""

  # A method for each recorded page.
  def guestbook(self):
    result = request101.POST('/sign',
      ( NVPair('content', 'appscale 1'), ),
      ( NVPair('Content-Type', 'application/x-www-form-urlencoded'), ))
    request102.GET('/')
    return result

  def __call__(self):
    """This method is called for every run performed by the worker thread."""
    self.guestbook()      # POST sign (requests 101-102)

def instrumentMethod(test, method_name, c=TestRunner):
  """Instrument a method with the given Test."""
  unadorned = getattr(c, method_name)
  import new
  method = new.instancemethod(test.wrap(unadorned), None, c)
  setattr(c, method_name, method)

# Replace each method with an instrumented version.
# You can call the unadorned method using self.page1.__target__().
instrumentMethod(Test(100, 'guestbook'), 'guestbook')
