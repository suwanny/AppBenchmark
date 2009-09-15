# The Grinder 3.2
# HTTP script recorded by TCPProxy at Aug 28, 2009 7:47:21 PM

from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from net.grinder.plugin.http import HTTPPluginControl, HTTPRequest
from HTTPClient import NVPair
connectionDefaults = HTTPPluginControl.getConnectionDefaults()
httpUtilities = HTTPPluginControl.getHTTPUtilities()

connectionDefaults.defaultHeaders = \
  ( NVPair('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),)

headers1= \
  ( NVPair('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
    NVPair('Accept-Language', 'ko'),
    NVPair('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB5; SU 3.23; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'),
    NVPair('Accept-Encoding', 'gzip, deflate'), )

headers2= \
  ( NVPair('Accept', '*/*'),
    NVPair('Accept-Encoding', 'gzip, deflate'),
    NVPair('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB5; SU 3.23; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'), )

url1 = 'http://appbench-petlog.appspot.com:80'

request101 = HTTPRequest(url=url1, headers=headers1)
request101 = Test(101, 'GET /').wrap(request101)

request102 = HTTPRequest(url=url1, headers=headers2)
request102 = Test(102, 'GET favicon.ico').wrap(request102)


class TestRunner:
  """A TestRunner instance is created for each worker thread."""
  def page1(self):
    result = request101.GET('/')
    request102.GET('/favicon.ico')
    return result

  def __call__(self):
    """This method is called for every run performed by the worker thread."""
    self.page1()      


def instrumentMethod(test, method_name, c=TestRunner):
  """Instrument a method with the given Test."""
  unadorned = getattr(c, method_name)
  import new
  method = new.instancemethod(test.wrap(unadorned), None, c)
  setattr(c, method_name, method)

# Replace each method with an instrumented version.
# You can call the unadorned method using self.page1.__target__().
instrumentMethod(Test(100, 'Page 1'), 'page1')
