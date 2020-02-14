<hr>
<%
from bottle import request
path = request.urlparts.path
%>
% if not path == "/dnd/" and path.startswith("/dnd/"):
<a href="/dnd/">D&D Home</a><br>
% elif not path == "/numenera/" and path.startswith("/numenera/"):
<a href="/numenera/">Numenera Home</a><br>
% end
% if not path == "/":
<a href="/">Home</a><br>
% end
<a href="/feedback">Report a Problem</a>
