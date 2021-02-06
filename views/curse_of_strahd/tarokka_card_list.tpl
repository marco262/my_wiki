% rebase("common/base.tpl", title=title)

<h1>Suits</h1>

% for suit in ["High Deck", "Swords Suit", "Stars Suit", "Coins Suit", "Glyphs Suit"]:
<h2>{{ suit }}</h2>

<p>{{ tarokka_deck[suit] }}</p>
% end

<h1>Cards</h1>

<table class="no-border">

% for card_name, description in tarokka_deck["cards"].items():
<tr>
    <td><img style="width: 15vw;" src="/static/img/tarokka/{{card_name}}.png" alt="{{card_name}}"></td>
    <td>
        <p><strong>{{card_name}}</strong></p>
        <p>{{description}}</p>
    </td>
</tr>
% end

</table>
