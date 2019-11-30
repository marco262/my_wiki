beneficial_mutations = [
    (1, 5, "Strengthened bones", "You gain +5 to your Might Pool."),
    (6, 10, "Improved circulation", "You gain +5 to your Might Pool."),
    (11, 15, "Improved musculature", "You gain +5 to your Might Pool."),
    (16, 20, "Improved nervous system", "You gain +5 to your Speed Pool."),
    (21, 25, "Improved neural processes", "You gain +5 to your Intellect Pool."),
    (26, 30, "Thick hide", "You gain +1 to Armor."),
    (31, 33, "Increased lung capacity", "You can hold your breath for five minutes."),
    (34, 36, "Adhesion pads", "Your hands and feet have naturally adhesive pads and thus are assets in tasks "
                              "involving climbing, keeping your footing, or retaining your grip."),
    (37, 39, "Slippery skin", "You secrete a slippery oil, giving you an asset in any task involving slipping from "
                              "another’s grip, slipping from bonds, squeezing through a small opening, and so on."),
    (40, 45, "Telekinetic shield", "You reflexively use telekinesis to ward away attacks, giving you an asset in "
                                   "Speed defense tasks."),
    (46, 50, "Suggestive voice", "Your voice is so perfectly modulated that it is an asset in all interaction tasks."),
    (51, 53, "Processor dreams", 'When you sleep, you process information so that after you wake, you have an asset '
                                 'in any Intellect actions held over from the previous day. For example, if you have '
                                 'to determine whether an unknown plant is poisonous, you could "sleep on it" and '
                                 'make the determination the next day with an asset on the action.'),
    (54, 60, "Poison immunity", "You are immune to all poisons."),
    (61, 65, "Disease immunity", "You are immune to all diseases."),
    (66, 70, "Fire resistance", "You have +3 to Armor against damage from fire."),
    (71, 75, "Cold resistance", "You have +4 to Armor against damage from cold."),
    (76, 80, "Psychic resistance", "You have +3 to Armor against Intellect damage."),
    (81, 85, "Acid resistance", "You have +5 to Armor against damage from acid."),
    (86, 88, "Puncture resistance", "You have +2 to Armor against damage from puncturing attacks."),
    (89, 91, "Slicing resistance", "You have +2 to Armor against damage from slicing attacks."),
    (92, 94, "Bludgeoning resistance", "You have +2 to Armor against damage from crushing attacks."),
    (95, 96, "No scent", "You cannot be tracked or located by scent, and you never have offensive odors."),
    (97, 99, "Scent", "You can sense creatures, objects, and terrain by scent as well as a normal human can by sight. "
                      "You can detect scents with that degree of accuracy only in short range, but you can sense "
                      "strong odors from much farther away (far better than a normal human can). Like a hound, you "
                      "can track creatures by their scent."),
    (100, None, "Sense Material", "You can sense the presence of any single substance within short range, although "
                                  "you don't learn details or the precise location. You and the GM should work "
                                  "together to determine the substance: water, iron, synth, granite, wood, flesh, "
                                  "salt, and so on. You do not need to concentrate to sense the material.")
]

harmful_mutations = [
    (1, 10, "Deformed leg", "All movement tasks are increased in difficulty by one step."),
    (11, 20, "Deformed face/appearance", "All pleasant interaction tasks are increased in difficulty by one step."),
    (21, 30, "Deformed arm/hand", "All tasks involving the arm or hand are increased in difficulty by one step."),
    (31, 40, "Malformed brain", "The difficulty of all memory- or cognitive-related tasks is increased by one step."),
    (41, 45, "Mentally vulnerable", "The difficulty of all Intellect defense tasks is increased by one step."),
    (46, 50, "Slow and lumbering", "The difficulty of all Speed defense tasks is increased by one step."),
    (51, 60, "Sickly", "The difficulty of all Might defense tasks is increased by one step."),
    (61, 63, "Horrible growth", "A large goiter, immobile tendril, or useless extra eye hangs from your face, "
                                "increasing the difficulty of all pleasant interactions (with most creatures, "
                                "particularly humans) by one step."),
    (64, 66, "Useless limb", "One of your limbs is unusable or missing."),
    (67, 71, "Useless eye", "One of your eyes is unusable or missing. The difficulty of tasks specifically involving "
                            "eyesight (spotting, searching, and so on) is increased by one step."),
    (72, 76, "Useless ear", "One of your ears is unusable or missing. The difficulty of tasks specifically involving "
                            "hearing is increased by one step."),
    (77, 84, "Weakness in Might", "Any time you spend points from your Might Pool, the cost is increased by 1 point."),
    (85, 92, "Weakness in Speed", "Any time you spend points from your Speed Pool, the cost is increased by 1 point."),
    (93, 100, "Weakness in Intellect", "Any time you spend points from your Intellect Pool, the cost is increased by "
                                       "1 point.")
]

powerful_mutations = [
    (1, 5, "Darksight", "You can see in complete darkness as if it were light. Enabler."),
    (6, 10, "No breath", "You do not need to breathe. Enabler."),
    (11, 15, "No water", "You do not need to drink water to survive. Enabler."),
    (16, 20, "Chameleon skin", "Your skin changes colors as you wish. This is an asset in tasks involving hiding. "
                               "Enabler."),
    (21, 24, "Savage bite", "Your mouth widens surprisingly, and hidden, pointed teeth emerge when you wish it. "
                            "You can make a bite attack that inflicts 3 points of damage. Enabler."),
    (25, 26, "Gluey globs", "You can produce gluey globs at your fingertips. This is an asset in tasks involving "
                            "climbing or keeping your grip. You can also fling these globs in immediate range, "
                            "and if they hit, they increase the difficulty of the target's physical tasks by one "
                            "step for one round. Enabler to use in a task; action to use as an attack."),
    (27, 30, "Face dancing", "You can alter your features enough that you possess an asset in all tasks involving "
                             "disguise. Enabler."),
    (31, 35, "Sense numenera", "You can sense the presence of a functioning numenera device or esotery within "
                               "short range. You do not learn details or the precise location. Action."),
    (36, 40, "Stinger in finger", "You can make an attack with your hand that inflicts 1 point of damage. If you "
                                  "make a second successful attack roll, your stinger also injects a poison that "
                                  "inflicts 4 points of Speed damage. Action."),
    (41, 44, "Stinger in elbow", "You can make an attack with your elbow that inflicts 2 points of damage. If you "
                                 "make a second successful attack roll, your stinger also injects a poison that "
                                 "inflicts 4 points of Speed damage. Action."),
    (45, 47, "Spit needles", "You can make an attack with immediate range. You spit a needle that inflicts 1 point "
                             "of damage. If you make a second successful attack roll, the needle also injects a "
                             "poison that inflicts 4 points of Speed damage. Action."),
    (48, 50, "Spit acid", "You can make an attack with immediate range. You spit a glob of acid that inflicts 2 "
                          "points of damage. Action."),
    (51, 53, "Spit webs", "You can make up to 10 feet (3 m) of a strong, ropelike material each day at the rate "
                          "of about 1 foot (0.3 m) per minute. The webbing is level 3. You can also spit globs of "
                          "webbing in immediate range, and if they hit, they increase the difficulty of the target's "
                          "physical tasks by one step for one round. Action."),
    (54, 59, "Filtered lungs", "You have an asset to Might defense actions against vapors or noxious gases. You "
                               "can survive in a hostile breathing environment (such as underwater or in a vacuum) "
                               "for up to ten minutes. Enabler."),
    (60, 62, "Disruptive field (electronics) (2 Intellect points)",
        "When you wish it, you disrupt devices within immediate range (no roll needed). All devices operate as if "
        "they were 3 levels lower while in range of your field. Devices reduced to level 0 or below do not function. "
        "Action."),
    (63, 65, "Disruptive field (flesh) (2 Intellect points)",
        "When you wish it, you disrupt flesh within immediate range. All creatures within range of your field take "
        "1 point of damage. If you apply a level of Effort to increase the damage rather than affect the difficulty, "
        "each target takes 2 additional points of damage. If your attack fails, targets in the area still take 1 "
        "point of damage. Action."),
    (66, 68, "Disruptive field (thoughts) (1 Intellect point)",
        "When you wish it, you disrupt thoughts within immediate range. The difficulty of Intellect actions for "
        "all creatures within range is increased by one step. Action."),
    (69, 70, "Magnetic flesh", "You attract or repel metal when you desire. Not only do small metal objects cling "
                               "to you, but this mutation is an asset in tasks involving climbing on metal or "
                               "keeping your grip on a metal item. This mutation is an asset to Speed defense "
                               "tasks when being attacked by a metal foe or a foe with a metal weapon. Enabler."),
    (71, 73, "Gravity negation (2 Intellect points)",
        "You float slowly into the air. If you concentrate, you can control your movement at half your normal "
        "speed; otherwise, you drift with the wind or with any momentum you have gained. This effect lasts for "
        "up to ten minutes. If you also have the Hover esotery or trick of the trade, you can hover for twenty "
        "minutes and move your normal speed. Action to initiate."),
    (74, 80, "Telepathy (2 Intellect points)",
        "You can speak telepathically with others who are within short range. Communication is two-way, but the "
        "other party must be willing and able to communicate. You don't have to see the target, but you must know "
        "that it's within range. You can have more than one active contact at once, but you must establish contact "
        "with each target individually. Each contact lasts up to ten minutes. If you apply a level of Effort to "
        "increase the duration rather than affect the difficulty, the contact lasts for 28 hours. Action to "
        "establish contact."),
    (81, 85, "Pyrokinesis (1 Intellect point)",
        "You can cause a flammable object you can see within immediate range to spontaneously catch fire. If used "
        "as an attack, this power inflicts 2 points of damage. Action."),
    (86, 90, "Telekinesis (2 Intellect points)",
        "You can exert force on objects within short range. Once activated, your power has an effective Might "
        "Pool of 10, a Might Edge of 1, and an Effort of 2 (approximately equal to the strength of a fit, capable, "
        "adult human), and you can use it to move objects, push against objects, and so on. For example, you could "
        "lift and pull a light object anywhere within range to yourself or move a heavy object (like a piece of "
        "furniture) about 10 feet (3 m). This power lacks the fine control to wield a weapon or move objects with "
        "much speed, so in most situations, it's not a means of attack. You can't use this ability on your own "
        "body. The power lasts for one hour or until its Might Pool is depleted, whichever comes first. Action."),
    (91, 92, "Phaseshifting (2 Intellect points)",
        "You can pass slowly through solid barriers at a rate of 1 inch (2.5 cm) per round (minimum of one round "
        "to pass through the barrier). You can't act (other than moving) or perceive anything until you pass "
        "entirely through the barrier. You can't pass through energy barriers. Action."),
    (93, 94, "Power device (1+ Intellect points)",
        "You can charge an artifact or other device (except a cypher) so that it can be used once. The cost is "
        "1 Intellect point plus 1 point per level of the device. Action."),
    (95, 96, "Drain power", "You can drain the power from an artifact or device, allowing you to regain 1 "
                            "Intellect point per level of the device. You regain points at the rate of 1 point "
                            "per round and must give your full concentration to the process each round. The GM "
                            "determines whether the device is fully drained (likely true of most handheld or "
                            "smaller devices) or retains some power (likely true of large machines). Action to "
                            "initiate; action each round to drain."),
    (97, 99, "Regeneration", "In addition to regaining points through normal recovery rolls, you regain 1 point "
                             "of your Might Pool or Speed Pool per hour, regardless of whether you rest, until "
                             "both Pools are at their maximum. Enabler."),
    (100, None, "Feed off pain", "Any time a creature within immediate range suffers at least 3 points of damage "
                                 "(after Armor subtraction) in one attack, you can restore 1 point to one of your "
                                 "Pools, up to its maximum. You can feed off any creature in this way, whether "
                                 "friend or foe. You never regain more than 1 point per round. Enabler.")
]

distinctive_mutations = [
    (1, 4, "Extra mouth", "You have an extra mouth on your hand, face, or stomach. This mouth is filled with "
                          "razor-sharp teeth and, if used to attack, inflicts 3 points of damage. You can also "
                          "speak with two voices at once. Enabler."),
    (5, 8, "Snakelike arm", "One of your arms ends in a fanged mouth. You can use it to attack, inflicting 3 "
                            "points of damage. If you make a second successful attack with the arm, you also "
                            "inject a poison that inflicts 4 points of Speed damage. You can't use the snakelike "
                            "arm for anything other than biting. Enabler."),
    (9, 12, "Tendrils on forehead", "Four to six tendrils, each 12 to 24 inches (30 to 61 cm) long, come out of "
                                    "your forehead. They can grasp and carry anything that your hand could, "
                                    "although a large object would block your field of vision. Also roll on the "
                                    "beneficial mutations list (page 124). Enabler."),
    (13, 16, "Tendrils instead of fingers",
        "Your fingers are tendrils 12 inches (30 cm) long. They are an asset to any task involving climbing, "
        "grasping, or keeping your grip. Further, you can effectively pick up and hold two objects in each hand "
        "rather than one. You can't wield more than one weapon per hand. Also roll on the beneficial mutations "
        "table. Enabler."),
    (17, 20, "Tendrils instead of arms",
        "Your arms are tendrils 6 feet (1.8 m) long (or only one arm is a tendril, if you prefer). Although you "
        "lose the fine manipulative ability of fingers and a thumb, you can still grasp objects, have a much longer "
        "reach, and have an asset for all tasks involving grappling or wrestling. Also roll on the beneficial "
        "mutations table. Enabler."),
    (21, 23, "Tendrils instead of eyes",
        "You are blind, but each eye socket has a retractable tendril that is 10 feet (3 m) long. These tendrils "
        "can feel around rapidly to give you a physical sense of everything within immediate range. Further, they "
        "can be used to manipulate very light objects, activate controls, and so forth. Also roll on the beneficial "
        "mutations table. Enabler."),
    (24, 26, "Tendrils instead of legs/feet",
        "Your legs or feet are tendrils that are 6 feet (1.8 m) long (or only one leg or foot is a tendril, if "
        "you prefer). You can still walk and move normally, and you have an asset for all tasks involving grappling "
        "or wrestling. The tendrils are prehensile enough to grasp large objects. Also roll on the beneficial "
        "mutations table. Enabler."),
    (27, 32, "Scaly body", "You gain +2 to Armor. Enabler."),
    (33, 36, "Covered in spiny needles/spikes",
        "Any creature striking you with its body automatically suffers 1 point of damage. Enabler."),
    (37, 39, "Quills", "You have quills that you can launch from your body to attack a foe within short range. "
                       "This attack inflicts 4 points of damage, and you never run out of ammo. You can also use "
                       "this attack in melee. Action."),
    (40, 44, "Carapace", "You gain +2 to Armor. Enabler."),
    (45, 49, "Chlorophyll", "You gain nutrients from the sun and don't need to eat or breathe if you have daily "
                            "exposure to sunlight. Your skin, not surprisingly, is green. Enabler."),
    (50, 54, "Extra joint in arms",
        "Your arms are long and jointed so that you have two elbows in each. You have a long reach and can strike "
        "foes from unexpected angles. This mutation is an asset when making melee attacks. However, you can modify "
        "your attacks only by using Speed, not Might. Enabler."),
    (55, 59, "Extra joint in legs",
        "Your legs are long and jointed so that you have two knees in each. You have a long stride, and this "
        "mutation is an asset for all running, climbing, jumping, and balancing tasks. Also roll on the beneficial "
        "mutations table. Enabler."),
    (60, 62, "Spider legs from torso",
        "In addition to your normal limbs, six or eight spiderlike legs, each 6 feet (1.8 m) long, extend from "
        "your sides. They are an asset in any task involving running, keeping your feet, standing your ground, and "
        "climbing. Also roll on the beneficial mutations table. Enabler."),
    (63, 67, "Extra arms", "You have one or two extra arms. They can hold objects, wield weapons, hold a shield, "
                           "and so on. This mutation does not increase the number of actions you can take in a round "
                           "or the number of attacks you can attempt. Enabler."),
    (68, 70, "Extra legs", "You have two extra legs. They are an asset in any task involving running, keeping your "
                           "feet, and standing your ground. Also roll on the beneficial mutations table. Enabler."),
    (71, 73, "Spider legs", "Instead of normal legs, you have a wide torso with six or eight spiderlike legs. They "
                            "are an asset in any task involving running, keeping your feet, standing your ground, "
                            "and climbing. Also roll on the beneficial mutations table. Enabler."),
    (74, 78, "Snake tail", "You have a prehensile tail that is 6 feet (1.8 m) long. It is an asset for all tasks "
                           "involving grappling or wrestling. The tail can grasp large objects. Also roll on the "
                           "beneficial mutations table. Enabler."),
    (79, 80, "Snake tail instead of legs",
        "Instead of legs, you have a snaky tail that is 8 feet (2.4 m) long. You move at the same speed and have "
        "an asset for all tasks involving grappling or wrestling. The tail is prehensile enough to grasp large "
        "objects. Also roll on the beneficial mutations table. Enabler."),
    (81, 85, "Stinging tendril", "You have a prehensile tendril (or tail) that grows from some part of your body and "
                                 "ends in a poisonous stinger. You can make an attack with your stinger that inflicts "
                                 "2 points of damage. If you make a second successful attack roll, the stinger "
                                 "also injects a poison that inflicts 4 points of Speed damage. The tendril (or tail) "
                                 "can't be used for anything else. Action."),
    (86, 90, "Eyes on stalks", "Your eyes are on stalks and can move in any direction, independently of each other. "
                               "You can peek around corners without exposing yourself to danger. This is an asset in "
                               "initiative and all perceiving tasks. Also roll on the beneficial mutations table. "
                               "Enabler."),
    (91, 92, "Extra eyes on hands/fingers",
        "You can peek around corners without exposing yourself to danger. This is an asset in initiative and all "
        "perceiving tasks. Also roll on the beneficial mutations table. Enabler."),
    (93, 97, "Aquatic", "Your body is streamlined and finned, your fingers and toes webbed. This is an asset "
                        "(two steps) in swimming, and you can see perfectly underwater (as if above water). Although "
                        "you have lungs, you also have gills, so you can also breathe underwater. Enabler."),
    (98, 100, "Wings", "You have feathered or fleshy wings on your back that allow you to glide, carried by the "
                       "wind. They are not powerful enough to carry you aloft like a bird's wings. Enabler.")
]

cosmetic_mutations = [
    (1, 2, "Purple skin"),
    (3, 4, "Green skin"),
    (5, 6, "Red skin"),
    (7, 8, "Yellow skin"),
    (9, 10, "White skin"),
    (11, 12, "Black skin"),
    (13, 14, "Blue skin"),
    (15, None, "Purple hair"),
    (16, None, "Green hair"),
    (17, None, "Red hair"),
    (18, None, "Yellow hair"),
    (19, None, "White hair"),
    (20, None, "Blue hair"),
    (21, None, "Striped hair"),
    (22, None, "Horns"),
    (23, None, "Antlers"),
    (24, None, "Extremely hirsute"),
    (25, None, "Entirely hairless"),
    (26, None, "Scaly skin"),
    (27, None, "Leathery skin"),
    (28, None, "Transparent skin"),
    (29, None, "Skin turns transparent in sunlight"),
    (30, None, "Skin changes color in sunlight"),
    (31, None, "Very tall"),
    (32, None, "Very large"),
    (33, None, "Very short"),
    (34, None, "Very thin"),
    (35, None, "Very long neck"),
    (36, None, "Hunched back"),
    (37, None, "Long, thin tail"),
    (38, None, "Short, broad tail"),
    (39, None, "Long arms"),
    (40, None, "Short arms"),
    (41, None, "Long legs"),
    (42, None, "Short legs"),
    (43, None, "Bony ridge on face"),
    (44, None, "Bony ridge on back"),
    (45, None, "Bony ridge on arms"),
    (46, None, "Purple eye(s)"),
    (47, None, "Red eye(s)"),
    (48, None, "Yellow eye(s)"),
    (49, None, "White eye(s)"),
    (50, None, "Black eye(s)"),
    (51, None, "Large eyes"),
    (52, None, "Bulbous eyes"),
    (53, None, "Two pupils in one eye"),
    (54, None, "Large ears"),
    (55, 56, "Pointed ears"),
    (57, 58, "Webbed fingers"),
    (59, 60, "Webbed toes"),
    (61, 62, "Four fingers on each hand"),
    (63, 64, "Six fingers on each hand"),
    (65, None, "Long fingers"),
    (66, None, "Purple nails"),
    (67, None, "Green nails"),
    (68, None, "Yellow nails"),
    (69, None, "White nails"),
    (70, None, "Black nails"),
    (71, None, "Blue nails"),
    (72, None, "Odd lumps on flesh"),
    (73, None, "Useless antennae (like an insect)"),
    (74, None, "Extra useless limb"),
    (75, None, "Extra useless eye"),
    (76, None, "Fleshy frills or useless flagella (small)"),
    (77, None, "Useless tendrils (large)"),
    (78, None, "Mandibles"),
    (79, 80, "Pointed teeth"),
    (81, None, "Tusks"),
    (82, None, "Black teeth"),
    (83, None, "Red teeth"),
    (84, None, "Purple teeth"),
    (85, None, "Green teeth"),
    (86, None, "Purple lips"),
    (87, None, "Green lips"),
    (88, None, "Yellow lips"),
    (89, None, "White lips"),
    (90, None, "Black lips"),
    (91, None, "Blue lips"),
    (92, None, "Purple spittle"),
    (93, None, "Red spittle"),
    (94, None, "Yellow spittle"),
    (95, None, "White spittle"),
    (96, None, "Black spittle"),
    (97, 98, "Distinctive odor"),
    (99, None, "Feathers"),
    (00, None, "Head crest")
]