% rebase("common/base.tpl", title="Mutations Generator")

<p>This page will let you randomly generate a combination of mutations. Pick your template from the dropdown below.<br/>
    You can view more details of each mutation on the <a href="/numenera/Mutants">Mutants</a> page.</p>

<table class="no-border">
    <tr>
        <td>Search Key:</td>
        <td>
            <select id="selected_mutation">
                <option value="2 Beneficial">2 Beneficial</option>
                <option value="3 Beneficial and 1 Harmful">3 Beneficial and 1 Harmful</option>
                <option value="1 Powerful and 1 Harmful">1 Powerful and 1 Harmful</option>
                <option value="1 Powerful, 1 Distinctive, 1 Harmful">1 Powerful, 1 Distinctive, 1 Harmful</option>
            </select>
            <input type="button" value="Generate" id="generate_button"/>
        </td>
    </tr>
</table>

<p>

<div id="generator_results"><i>Your generated mutations will appear here</i></div>

<script type="module">
    import {generate, on_key_press} from "/js/numenera/mutations_generator.js";
    document.getElementById("selected_mutation").onkeypress = on_key_press;
    document.getElementById("generate_button").onclick = generate;
</script>
