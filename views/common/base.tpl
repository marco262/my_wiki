<!DOCTYPE html>
<head>
    <title>{{title}} - Private 5e Wiki</title>
    <link rel="stylesheet" type="text/css" href="/static/css/stylesheet.css">
</head>
<body>
<div id="content">
    <div id="banner-image">
        <a id="wiki-title" href="/">My Wiki</a>
        % include("common/top_bar.tpl")
    </div>
    <article id="page-content">
        <h1 id="page-title">{{title}}</h1>
        <hr>
        {{ !base }}
        <hr>
        <div class="footer">
            <a href="https://docs.google.com/forms/d/e/1FAIpQLScvmgZcJHNDEs_Zp0hMveXWwlO6ggKuMO7FygE1pN4ijL5Uyw/viewform?usp=sf_link" target="_blank">Submit Feeback/Bug Report</a>
        </div>
        <br>
    </article>
</div>
</body>