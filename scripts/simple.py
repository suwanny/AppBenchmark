# The Grinder 3.2
# HTTP script recorded by TCPProxy at Jul 11, 2009 3:31:40 PM

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

connectionDefaults.defaultHeaders = \
  ( NVPair('Accept-Language', 'ko'),
    NVPair('Accept-Encoding', 'gzip, deflate'),
    NVPair('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; SU 3.23; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'),
    NVPair('Accept', '*/*'), )

headers0= \
  ( )

url0 = 'http://appscale.cs.ucsb.edu:80'

# Create an HTTPRequest for each request, then replace the
# reference to the HTTPRequest with an instrumented version.
# You can access the unadorned instance using request101.__target__.
request101 = HTTPRequest(url=url0, headers=headers0)
request101 = Test(101, 'GET simple.html').wrap(request101)


class TestRunner:
  """A TestRunner instance is created for each worker thread."""

  # A method for each recorded page.
  def page1(self):
    """GET simple.html (request 101)."""
    result = request101.GET('/~spark2007/pages/simple.html', None, )
    return result

  def __call__(self):
    """This method is called for every run performed by the worker thread."""
    self.page1()      # GET simple.html (request 101)


def instrumentMethod(test, method_name, c=TestRunner):
  """Instrument a method with the given Test."""
  unadorned = getattr(c, method_name)
  import new
  method = new.instancemethod(test.wrap(unadorned), None, c)
  setattr(c, method_name, method)

# Replace each method with an instrumented version.
# You can call the unadorned method using self.page1.__target__().
instrumentMethod(Test(100, 'Page 1'), 'page1')
