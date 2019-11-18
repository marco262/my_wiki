<%
from bottle import request
if not request.url.endswith(request.get_header("Host") + "/"):
%>
<p><a href="/">Home</a></p>
% end
<hr>

<a href="/feedback">Report a Problem</a>
