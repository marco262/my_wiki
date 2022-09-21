
<!-- https://github.com/sachinchoolur/lightGallery -->
<link rel="stylesheet" href="/static/css/lightgallery-bundle.min.css">

<div id="lightgallery">
  % for path in glob_file_list:
    <a class="light_gallery_thumbnail" href="{{ path }}">
        <img src="{{ path }}" />
    </a>
  % end
</div>

<script src="/static/js/common/lightgallery.umd.js"></script>
<script type="text/javascript">
    lightGallery(document.getElementById('lightgallery'));
</script>
