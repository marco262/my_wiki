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
        <div class="footer no-float">
            <a href="https://docs.google.com/forms/d/e/1FAIpQLScvmgZcJHNDEs_Zp0hMveXWwlO6ggKuMO7FygE1pN4ijL5Uyw/viewform?usp=sf_link" target="_blank">Submit Feedback/Bug Report</a>
        </div>
        <br>
    </article>
</div>
</body>