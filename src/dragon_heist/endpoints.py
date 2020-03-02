from bottle import Bottle, template, view
from src.common.utils import md_page


def init():
    pass


def popup_link(link, text):
    return """\n""".format(link=link, text=text)


def popup_list(pages):
    return "\n".join(["<li>{}</li>".format(popup_link(page[0], page[1])) for page in pages])

GM_NOTES = {
    "notes": [
        ("Trollskull Alley NPC ideas", "https://thealexandrian.net/wordpress/43319/roleplaying-games/a-night-in-trollskull-manor-part-5-patrons"),
        ("Trollskull Alley Visitors", "https://www.dndbeyond.com/posts/316-visitors-to-trollskull-alley"),
        ("Gang activities", "/dragon_heist/Gang Activities"),
        ("Putting Lif to rest", "https://www.reddit.com/r/WaterdeepDragonHeist/comments/9hpi1c/putting_lif_the_poltergeist_to_rest_a_checklist/")
    ],
    "images": [
        ("The Dock Ward", "https://www.worldanvil.com/media/cache/cover/uploads/images/effb94edf3fe17980edfd7e3fcde124f.jpg"),
        ("Old Xoblob Shop", "https://i.redd.it/rrogyk1thlu21.jpg"),
        ("Old Xoblob", "https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/8/87/Svirfneblin.jpg/revision/latest/top-crop/width/360/height/450?cb=20181220044213"),
        ("The Skewered Dragon", "https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/0/01/41d312aaac79078c70abf4462859da93.jpg/revision/latest?cb=20181212190835"),
        ("Zhentarim Hideout", "https://db4sgowjqfwig.cloudfront.net/campaigns/212984/assets/939176/skewered.jpg?1548469910"),
        ("Zhentarim Logo", "https://db4sgowjqfwig.cloudfront.net/campaigns/135685/assets/573194/zhentarim.png?1459111892"),
        ("Kenku", "https://vignette.wikia.nocookie.net/forgottenrealms/images/0/04/Kenku-5e.png/revision/latest?cb=20171010191131"),
        ("Gazer", "https://vignette.wikia.nocookie.net/forgottenrealms/images/5/58/Gazer-5e.jpg/revision/latest?cb=20171011162621"),
        ("Sewer 1", "https://3.bp.blogspot.com/-vKbLxrhJOwE/VRLhGhg0BjI/AAAAAAAAA_k/nk1uO9KhEY4/s1600/520_1024x1024.jpg"),
        ("Sewer 2", "https://vignette.wikia.nocookie.net/witcher/images/4/4a/Loading_Sewers_day.png/revision/latest?cb=20170511225814"),
        ("Sewer 3", "https://www.worldanvil.com/media/cache/cover/uploads/images/478b9ac0162129dde50e83cb666ac3ce.jpg"),
        ("Sewer 4", "https://i.pinimg.com/originals/81/29/97/812997b3f365f3f89eb5ab33bce3486b.jpg"),
        ("Sewer 5", "https://i.redd.it/xzlwzsdg8ck31.jpg"),
        ("Gray ooze", "https://i.pinimg.com/474x/b4/e3/89/b4e3895b089e8d0b70f1dbb9a4bb3d75.jpg"),
        ("Intellect Devourer", "https://vignette.wikia.nocookie.net/forgottenrealms/images/f/f0/Intellect_devourer-3e.jpg/revision/latest?cb=20190507141455"),
        ("Trollskull Manor 1", "https://www.seekpng.com/png/detail/41-413278_four-stories-tall-and-boasting-balconies-a-turret.png"),
        ("Trollskull Manor 2", "https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/d/de/Rkwbhhl78l021.jpg/revision/latest?cb=20181219225432"),
        ("Trollskull Manor 3", "https://i.imgur.com/8PCaZrv.png"),
        ("Flying kitchen utensils", "https://media.istockphoto.com/photos/flying-kitchen-utensils-towards-stunned-chef-picture-id149070075")
    ],
    "friendly_npcs_1": [
        ("Volothamp Geddarm", "https://live.staticflickr.com/7843/46342397195_761a48e73f_b.jpg"),
        ("Floon Bladmaar", "https://cdna.artstation.com/p/assets/images/images/005/831/352/large/anna-helme-.jpg?1494074377"),
        ("Renaer Neverember", "https://vignette.wikia.nocookie.net/risenlore/images/4/4f/74fb5130fecd30a69e25f88cc88e755c.jpg/revision/latest?cb=20190423234639")
    ],
    "trollskull_alley_npcs": [
        ("Lif Erwaren, poltergeist, ex-owner of Trollskull Manor", "https://db4sgowjqfwig.cloudfront.net/images/5138100/ae3c08bfa96dadb022e64a66ccb4e7c4.jpg"),
        ("Talisolvanar \"Tally\" Fellbranch, carpenter, owner of The Bent Nail", "https://db4sgowjqfwig.cloudfront.net/images/4942578/tally.jpg"),
        ("Embric, weaponsmith, co-owner of Steam and Steel", "https://vignette.wikia.nocookie.net/animus-cycle/images/4/46/Embric.jpg"),
        ("Avi, armorsmith, co-owner of Steam and Steel", "https://db4sgowjqfwig.cloudfront.net/images/5048085/Avi.jpg"),
        ("Fala Lefaliir, herbalist, owner of Corellon's Crown", "https://i.pinimg.com/originals/45/1d/4e/451d4eb92ae4fa7becc2e2c142b72fb4.jpg"),
        ("Vincent Trench, detective, disguised Rak'shasa, owner of the Tiger's Eye", "https://db4sgowjqfwig.cloudfront.net/images/5190829/detective.jpg"),
        ("Rishaal the Page-Turner, mage, owner of the Book Wyrm's Treasure", "https://vignette.wikia.nocookie.net/animus-cycle/images/3/3a/Rishaal.jpg/revision/latest/top-crop/width/360/height/450?cb=20190425031152")
    ],
    "guild_npcs": [
        ("Broxley Fairkettle, representative for the Fellowship of Innkeepers", "https://db4sgowjqfwig.cloudfront.net/images/5048113/Broxley.jpg"),
        ("Hammon Kraddoc, representative for the Vintners', Distillers', and Brewers' Guild", "https://db4sgowjqfwig.cloudfront.net/images/5048118/Hammond.jpg"),
        ("Justyn Rassk, representative for the Guild of Butchers", "https://i.pinimg.com/474x/f6/38/02/f63802aa830ea96a9adab1d00929d14e.jpg"),
        ("Ulkoria Stronemarrow, representative for the Watchful Order of Magists and Protectors", "https://www.rpnation.com/gallery/16cd198adc13eb77682d47f560f9c127.3480/full?d=1444402724")
    ],
    "force_grey_npcs": [
        ("Vajra Safahr, blackstaff of Waterdeep", "https://vignette.wikia.nocookie.net/forgottenrealms/images/f/f9/Vajra-5e.png/revision/latest/top-crop/width/360/height/450?cb=20180925013042")
    ],
    "harpers_npcs": [
        ("Mirt, Harper contact", "https://vignette.wikia.nocookie.net/forgottenrealms/images/4/44/Mirt-5e.jpg/revision/latest?cb=20181208035731")
    ],
    "lords_alliance_npcs": [
        ("Jalester Silvermane, field agent", "https://vignette.wikia.nocookie.net/forgottenrealms/images/6/6e/Jalester.jpg/revision/latest/top-crop/width/360/height/450?cb=20190301155331")
    ],
    "order_of_the_gauntlet_npcs": [
        ("Savra Belabranta, knight", "https://www.worldanvil.com/uploads/images/a8734ae15f9246236f07065a555a5435.jpg")
    ],
    "zhentarim_npcs": [
        ("Davil Starsong, retired adventurer", "https://vignette.wikia.nocookie.net/forgottenrealms/images/8/80/DavilStarsong.png/revision/latest?cb=20190118105332")
    ],
    "enemy_npcs": [
        ("Zemk, duergar", "https://vignette.wikia.nocookie.net/forgottenrealms/images/6/68/Duergar-5e.jpg/revision/latest?cb=20190315010252"),
        ("Krentz, the bandit who got beat up by Yagra", "https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/d/d1/D05961d80krentzea386c80777682a0fbad4e5.jpg/revision/latest?cb=20180916045442"),
        ("Grum'shar, half-orc apprentice wizard", "https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/0/0b/9251a162d90ca4d7d60199a7ef93a4d6.png/revision/latest/top-crop/width/360/height/450?cb=20181214005233"),
        ("Nihiloor, mind-flayer", "https://s3.amazonaws.com/aws-website-sansdrop-pjtrh/img/DnD/Nihiloor.png"),
        ("Emmek Frewn, owner of Frewn's Brews", "http://www.artofmtg.com/wp-content/uploads/2019/09/Edgewall-Innkeeper-Throne-of-Eldraine-MtG-Art.jpg"),
        ("Shard Shunners", "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4d66e72f-13bd-4733-a17c-45a971c3301f/da6zhrc-05bddf52-e7fc-4238-ac09-e6d4407054ab.png/v1/fill/w_772,h_1036,q_70,strp/weredogs_adopts_closed__by_honeydipply_da6zhrc-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTM3NCIsInBhdGgiOiJcL2ZcLzRkNjZlNzJmLTEzYmQtNDczMy1hMTdjLTQ1YTk3MWMzMzAxZlwvZGE2emhyYy0wNWJkZGY1Mi1lN2ZjLTQyMzgtYWMwOS1lNmQ0NDA3MDU0YWIucG5nIiwid2lkdGgiOiI8PTEwMjQifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.5dWjY64bZx9WGy1WAphrAw-JyclISQoxEXXMGqVjge4")
    ]
}


def load_wsgi_endpoints(app: Bottle):
    @app.get()
    @view("dragon_heist/gmnotes.tpl")
    def home():
        return GM_NOTES

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "dragon_heist")
