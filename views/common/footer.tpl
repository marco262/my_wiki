<hr>
<%
from bottle import request
print(request.urlparts.path)
if not request.urlparts[2] == "/":
%>
<a href="/">Home</a><br>
% end
<a href="/feedback">Report a Problem</a>
