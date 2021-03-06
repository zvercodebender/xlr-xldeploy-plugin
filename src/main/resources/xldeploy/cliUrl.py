#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
import httplib
import re

from java.lang import Exception
from java.io import PrintWriter
from java.io import StringWriter

from xldeploy.LocalCLI import Localcliscript

print "Script URL = %s" % scriptUrl
host=scriptUrl.split('//')[1].split('/')[0]
print "Host       = %s" % host
regex='^.*%s' % host
uri=re.sub( regex, '', scriptUrl )
print "URI        = %s" % uri
try:
   if scriptUrl.startswith('https'):
       print "Make HTTPS connection"
       URLSource = httplib.HTTPSConnection( host )
   else:
       print "Make HTTP connection"
       URLSource = httplib.HTTPConnection( host )
   # End if
   URLSource.request('GET', uri, {}, {})
   response = URLSource.getresponse()
   print response.status, response.reason
   script = response.read()

   cliScript = Localcliscript(cli['cliHome'], cli['xldHost'], cli['xldPort'], cli['xldContext'], cli['xldProxyHost'], cli['xldProxyPort'], cli['xldSocketTimeout'], cli['xldUserName'], cli['xldPassword'], script, cli['cliExecutable'], options)
   exitCode = cliScript.execute()

   output = cliScript.getStdout()
   err = cliScript.getStderr()
except Exception, e:
      stacktrace = StringWriter()
      writer = PrintWriter(stacktrace, True)
      e.printStackTrace(writer)
      err = stacktrace.toString()
      exitCode = 1
finally:
      URLSource.close()
# End try

if exitCode == 0:
   print output
else:
   print
   print "### Exit code "
   print exitCode
   print
   print "### Output:"
   print output
   
   print "### Error stream:"
   print err
   print 
   print "----"

sys.exit(exitCode)
