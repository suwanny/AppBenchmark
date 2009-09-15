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

connectionDefaults.defaultHeaders = \
  ( NVPair('Accept-Language', 'ko'),
    NVPair('Accept-Encoding', 'gzip, deflate'),
    NVPair('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; SU 3.23; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'),
    NVPair('Accept', 'image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'), )

headers0= \
  ( )

headers1= \
  ( NVPair('Referer', 'http://128.111.55.209:8080/'), )

url0 = 'http://128.111.55.209:8080'

# Create an HTTPRequest for each request, then replace the
# reference to the HTTPRequest with an instrumented version.
# You can access the unadorned instance using request101.__target__.
request101 = HTTPRequest(url=url0, headers=headers0)
request101 = Test(101, 'GET /').wrap(request101)

request201 = HTTPRequest(url=url0, headers=headers1)
request201 = Test(201, 'POST sign').wrap(request201)

request202 = HTTPRequest(url=url0, headers=headers1)
request202 = Test(202, 'GET /').wrap(request202)

request301 = HTTPRequest(url=url0, headers=headers1)
request301 = Test(301, 'POST sign').wrap(request301)

request302 = HTTPRequest(url=url0, headers=headers1)
request302 = Test(302, 'GET /').wrap(request302)

request401 = HTTPRequest(url=url0, headers=headers1)
request401 = Test(401, 'POST sign').wrap(request401)

request402 = HTTPRequest(url=url0, headers=headers1)
request402 = Test(402, 'GET /').wrap(request402)

request501 = HTTPRequest(url=url0, headers=headers1)
request501 = Test(501, 'POST sign').wrap(request501)

request502 = HTTPRequest(url=url0, headers=headers1)
request502 = Test(502, 'GET /').wrap(request502)

request601 = HTTPRequest(url=url0, headers=headers1)
request601 = Test(601, 'POST sign').wrap(request601)

request602 = HTTPRequest(url=url0, headers=headers1)
request602 = Test(602, 'GET /').wrap(request602)


class TestRunner:
  """A TestRunner instance is created for each worker thread."""

  # A method for each recorded page.
  def page1(self):
    """GET / (request 101)."""
    result = request101.GET('/')

    return result

  def page2(self):
    """POST sign (requests 201-202)."""
    
    # Expecting 302 'Moved Temporarily'
    result = request201.POST('/sign',
      ( NVPair('content', 'appscale 1'), ),
      ( NVPair('Content-Type', 'application/x-www-form-urlencoded'), ))

    grinder.sleep(5054)
    request202.GET('/')

    return result

  def page3(self):
    """POST sign (requests 301-302)."""
    
    # Expecting 302 'Moved Temporarily'
    result = request301.POST('/sign',
      ( NVPair('content', 'appscale 2'), ),
      ( NVPair('Content-Type', 'application/x-www-form-urlencoded'), ))

    grinder.sleep(5035)
    request302.GET('/')

    return result

  def page4(self):
    """POST sign (requests 401-402)."""
    
    # Expecting 302 'Moved Temporarily'
    result = request401.POST('/sign',
      ( NVPair('content', 'appscale 3'), ),
      ( NVPair('Content-Type', 'application/x-www-form-urlencoded'), ))

    grinder.sleep(5021)
    request402.GET('/')

    return result

  def page5(self):
    """POST sign (requests 501-502)."""
    
    # Expecting 302 'Moved Temporarily'
    result = request501.POST('/sign',
      ( NVPair('content', 'appscale 4'), ),
      ( NVPair('Content-Type', 'application/x-www-form-urlencoded'), ))

    grinder.sleep(5021)
    request502.GET('/')

    return result

  def page6(self):
    """POST sign (requests 601-602)."""
    
    # Expecting 302 'Moved Temporarily'
    result = request601.POST('/sign',
      ( NVPair('content', 'appscale 5'), ),
      ( NVPair('Content-Type', 'application/x-www-form-urlencoded'), ))

    grinder.sleep(5046)
    request602.GET('/')

    return result

  def __call__(self):
    """This method is called for every run performed by the worker thread."""
    self.page1()      # GET / (request 101)

    grinder.sleep(21977)
    self.page2()      # POST sign (requests 201-202)

    grinder.sleep(8721)
    self.page3()      # POST sign (requests 301-302)

    grinder.sleep(8721)
    self.page4()      # POST sign (requests 401-402)

    grinder.sleep(11140)
    self.page5()      # POST sign (requests 501-502)

    grinder.sleep(20629)
    self.page6()      # POST sign (requests 601-602)


def instrumentMethod(test, method_name, c=TestRunner):
  """Instrument a method with the given Test."""
  unadorned = getattr(c, method_name)
  import new
  method = new.instancemethod(test.wrap(unadorned), None, c)
  setattr(c, method_name, method)

# Replace each method with an instrumented version.
# You can call the unadorned method using self.page1.__target__().
instrumentMethod(Test(100, 'Page 1'), 'page1')
instrumentMethod(Test(200, 'Page 2'), 'page2')
instrumentMethod(Test(300, 'Page 3'), 'page3')
instrumentMethod(Test(400, 'Page 4'), 'page4')
instrumentMethod(Test(500, 'Page 5'), 'page5')
instrumentMethod(Test(600, 'Page 6'), 'page6')
