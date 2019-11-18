<%
from bottle import request
if not request.urlparts[2] == "/":
%>
<p><a href="/">Home</a></p>
% end
<hr>

<a href="/feedback">Report a Problem</a>
