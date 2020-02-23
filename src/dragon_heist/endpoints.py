from bottle import Bottle, template, view


def init():
    pass


def popup_link(link, text):
    return """<a href="{link}" 
              target="popup" 
              onclick="window.open('{link}','popup','width=600,height=600', menubar=yes); return false;">
                {text}
            </a>\n""".format(link=link, text=text)


def popup_list(pages):
    return "\n".join(["<li>{}</li>".format(popup_link(page[0], page[1])) for page in pages])


def load_wsgi_endpoints(app: Bottle):
    @app.get()
    @view("dragon_heist/gmnotes.tpl")
    def home():
        images = popup_list([
            ("https://www.worldanvil.com/media/cache/cover/uploads/images/effb94edf3fe17980edfd7e3fcde124f.jpg", "The Dock Ward"),
            ("https://i.redd.it/rrogyk1thlu21.jpg", "Old Xoblob Shop"),
            ("https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/8/87/Svirfneblin.jpg/revision/latest/top-crop/width/360/height/450?cb=20181220044213", "Old Xoblob"),
            ("https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/0/01/41d312aaac79078c70abf4462859da93.jpg/revision/latest?cb=20181212190835", "The Skewered Dragon"),
            ("https://db4sgowjqfwig.cloudfront.net/campaigns/212984/assets/939176/skewered.jpg?1548469910", "Zhentarim Hideout"),
            ("https://db4sgowjqfwig.cloudfront.net/campaigns/135685/assets/573194/zhentarim.png?1459111892", "Zhentarim Logo"),
            ("https://vignette.wikia.nocookie.net/forgottenrealms/images/0/04/Kenku-5e.png/revision/latest?cb=20171010191131", "Kenku"),
            ("https://vignette.wikia.nocookie.net/forgottenrealms/images/5/58/Gazer-5e.jpg/revision/latest?cb=20171011162621", "Gazer"),
            ("https://3.bp.blogspot.com/-vKbLxrhJOwE/VRLhGhg0BjI/AAAAAAAAA_k/nk1uO9KhEY4/s1600/520_1024x1024.jpg", "Sewer 1"),
            ("https://vignette.wikia.nocookie.net/witcher/images/4/4a/Loading_Sewers_day.png/revision/latest?cb=20170511225814", "Sewer 2"),
            ("https://www.worldanvil.com/media/cache/cover/uploads/images/478b9ac0162129dde50e83cb666ac3ce.jpg", "Sewer 3"),
            ("https://i.pinimg.com/originals/81/29/97/812997b3f365f3f89eb5ab33bce3486b.jpg", "Sewer 4"),
            ("https://i.redd.it/xzlwzsdg8ck31.jpg", "Sewer 5"),
            ("https://i.pinimg.com/474x/b4/e3/89/b4e3895b089e8d0b70f1dbb9a4bb3d75.jpg", "Gray ooze"),
            ("https://vignette.wikia.nocookie.net/forgottenrealms/images/f/f0/Intellect_devourer-3e.jpg/revision/latest?cb=20190507141455", "Intellect Devourer"),
            ("https://www.seekpng.com/png/detail/41-413278_four-stories-tall-and-boasting-balconies-a-turret.png", "Trollskull Manor")
        ])
        friendly_npcs = popup_list([
            ("https://live.staticflickr.com/7843/46342397195_761a48e73f_b.jpg", "Volothamp Geddarm"),
            ("https://cdna.artstation.com/p/assets/images/images/005/831/352/large/anna-helme-.jpg?1494074377", "Floon Bladmaar"),
            ("https://vignette.wikia.nocookie.net/risenlore/images/4/4f/74fb5130fecd30a69e25f88cc88e755c.jpg/revision/latest?cb=20190423234639", "Renaer Neverember")
        ])
        enemy_npcs = popup_list([
            ("https://vignette.wikia.nocookie.net/forgottenrealms/images/6/68/Duergar-5e.jpg/revision/latest?cb=20190315010252", "Zemk, duergar"),
            ("https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/d/d1/D05961d80krentzea386c80777682a0fbad4e5.jpg/revision/latest?cb=20180916045442", "Krentz, the bandit who got beat up by Yagra"),
            ("https://vignette.wikia.nocookie.net/kingsway-role-playing-group/images/0/0b/9251a162d90ca4d7d60199a7ef93a4d6.png/revision/latest/top-crop/width/360/height/450?cb=20181214005233", "Grum'shar, half-orc apprentice wizard"),
            ("https://s3.amazonaws.com/aws-website-sansdrop-pjtrh/img/DnD/Nihiloor.png", "Nihiloor, mind-flayer")
        ])
        return {
            "title": "Dragon Heist Home",
            "images": images,
            "friendly_npcs": friendly_npcs,
            "enemy_npcs": enemy_npcs
        }
