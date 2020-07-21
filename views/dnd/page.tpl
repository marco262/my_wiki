% include("common/header.tpl", title=title)

<div id="content">
    <div id="banner-image">
        <a id="wiki-title" href="/">My Wiki</a>
        % include("common/top_bar.tpl")
    </div>
    <div id="page-content">
        <h1 id="page-title">{{title}}</h1>
        <hr>

        % include("common/toc.tpl")

        {{!text}}
        <br>
    </div>

    % include("common/footer.tpl")
</div>

