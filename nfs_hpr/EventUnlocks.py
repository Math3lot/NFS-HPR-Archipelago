"""
In-game event unlock tree, read from the game data (GAMEPLAY bundle): an event opens
once the events listed for it have been completed. Generated: do not edit by hand.
The first event of each side has no prerequisite.
"""
from typing import Dict, List

RACER_EVENT_PREREQUISITES: Dict[str, List[str]] = {
    'Against All Odds': ['Jet Set'],
    'Ageless': ['Jet Set'],
    'Avalanche': ['M Power'],
    'Awe Inspired': ['Breach Of The Peace'],
    'Barnstormer': ['Coast To Coast'],
    'Beauty And The Beasts': ['Muscle Reflex'],
    'Blacklisted': ['Coast To Coast'],
    'Blast From The Past': ['Calm Before The Storm'],
    'Born In The USA': ['Double Jeopardy'],
    'Breach Of The Peace': ['Title Fight', 'Vanishing Point'],
    'Breaking Point': ['Hotting Up'],
    'Bull Run': ['Passione Italia', 'The Art of Driving'],
    'Calm Before The Storm': ['Wild Ride'],
    'Cannonball': ['No Substitute'],
    'Coast To Coast': ['Power Trip', 'Timed Machine'],
    'Comeback Tour': ['Double Jeopardy'],
    'Complete Control': ['Sidewinder', 'The Ultimate Road Car'],
    'Double Jeopardy': ['Bull Run', 'Tough Torque'],
    'Encore Performance': ['Sidewinder', 'The Ultimate Road Car'],
    'Escape Lane': ['Complete Control', 'Encore Performance'],
    'Experience More': ['Escape Lane', 'Extreme Truth'],
    'Extreme Truth': ['Complete Control', 'Encore Performance'],
    'Fast Lane': ['Stampede'],
    'Fast Track': ['Wild Ride'],
    'Faster Than Light': ['Breaking Point'],
    'First Offence': ['Roadsters Reborn'],
    'Foot To The Floor': ['Double Jeopardy'],
    'Future Perfect': ['Breach Of The Peace'],
    'Glorious Fourth': ['Power Struggle'],
    'Heart To Heart': ['Trail Of Destruction'],
    'Highway Battle': ['Blast From The Past', 'King Of The Road'],
    'Hotting Up': ['Glorious Fourth', 'Slide Show'],
    'Hunted': ['Highway Battle'],
    'Jet Set': ['Unreasonable Force'],
    'King Of The Road': ['Calm Before The Storm'],
    'M Power': ['Shock And Awe'],
    'Muscle Reflex': ['Sports Car Named Desire'],
    'No Substitute': ['Stampede'],
    'One Of Five': ['Born In The USA'],
    'One Step Ahead': ['Breaking Point'],
    'Passione Italia': ['Against All Odds', 'Ageless'],
    'Power Struggle': ['One Of Five', 'Spoilt For Choice', 'Twin Turbo'],
    'Power Trip': ['No Substitute'],
    'Previous Conviction': ['Stampede'],
    'Pushing The Envelope': ['Wild Ride'],
    'Racing Stripes': ['Avalanche'],
    'Redline Racing': ['Calm Before The Storm'],
    'Resisting Arrest': ['Heart To Heart'],
    'Road To Ruin': ['Trail Of Destruction'],
    'Rocket Science': ['Shock And Awe'],
    'Rogue Element': ['Power Struggle'],
    'Sand Timer': ['Coast To Coast'],
    'Seacrest Tour': ['Hunted'],
    'Shock And Awe': ['Experience More', 'The Prestige'],
    'Sidewinder': ['Beauty And The Beasts'],
    'Slide Show': ['Power Struggle'],
    'Spirit Of Performance': ['Breaking Point'],
    'Spoilt For Choice': ['Born In The USA'],
    'Sports Car Named Desire': ['Future Perfect', 'Unlimited Driving Pleasure'],
    'Stampede': ['Racing Stripes', 'Ultimately Open', 'V12 For Victory'],
    'Sun, Sand And Supercars': ['Heart To Heart'],
    'Sunset Racers': ['Sun, Sand And Supercars'],
    'The Art of Driving': ['Against All Odds', 'Ageless'],
    'The Prestige': ['Escape Lane', 'Extreme Truth'],
    'The Ultimate Road Car': ['Beauty And The Beasts'],
    'Timed Machine': ['No Substitute'],
    'Title Fight': ['First Offence'],
    'Tough Torque': ['Passione Italia', 'The Art of Driving'],
    'Trail Of Destruction': ['Blacklisted', 'Sand Timer'],
    'Twin Turbo': ['Born In The USA'],
    'Ultimately Open': ['Avalanche'],
    'Unlimited Driving Pleasure': ['Breach Of The Peace'],
    'Unreasonable Force': ['Sun, Sand And Supercars'],
    'V12 For Victory': ['Avalanche'],
    'Vanishing Point': ['First Offence'],
    'Wild Ride': ['Faster Than Light', 'Spirit Of Performance'],
    'Wing And A Prayer': ['Jet Set'],
}

COP_EVENT_PREREQUISITES: Dict[str, List[str]] = {
    'Any Means Necessary': ['Double Cross'],
    'Arms Race': ['Limited Emission'],
    'Arrest Warrant': ['Turn The Tables'],
    'Block Buster': ['Escape to the Beach'],
    'Charged Attack': ['Tough Justice'],
    'Coming In Hot': ['Guided Missile', 'Hang Tough'],
    'Contact Sport': ['Fight Or Flight'],
    'Crimewave': ['Limited Emission'],
    'Cut To The Chase': ['Hard To Handle'],
    'Damage Limitation': ['Hard To Handle'],
    'Dark Horse': ['Fighting Dirty'],
    'Denial Of Service': ['Dark Horse'],
    'Desert Strike': ['Dust Storm', 'Sunset Scalpel'],
    'Do Look After It': ['Block Buster'],
    'Double Cross': ['Damage Limitation', 'Hard Target'],
    'Dust Storm': ['Charged Attack', 'Weapon Of Choice'],
    'Duty Calls': ['Double Cross'],
    'Elements Of Speed': ['Desert Strike'],
    'End Of The Line': ['Any Means Necessary', 'Duty Calls'],
    'Escape to the Beach': ['Chase 101'],
    'Eye In The Sky': ['Protect And Swerve', 'Summit Assault'],
    'Fight Night': ['Arms Race'],
    'Fight Or Flight': ['Takedown Notice'],
    'Fighting Dirty': ['Do Look After It', 'Lightning Reflex', 'Reventon Reveal'],
    'French Connection': ['Eye In The Sky'],
    'Guided Missile': ['Under Pressure'],
    'Hang Tough': ['Under Pressure'],
    'Hard Target': ['Hard To Handle'],
    'Hard To Handle': ['Contact Sport', 'Natural Selection'],
    'Heavy Hitters': ['Desert Strike'],
    'Infernal Rampage': ['Arms Race'],
    'Lightning Reflex': ['Block Buster'],
    'Limited Emission': ['Coming In Hot', 'Run To The Hills'],
    'Lockdown': ['Fight Or Flight'],
    'Locking On': ['Porsche Patrol'],
    'Marked Man': ['Under Pressure'],
    'More Haste, Less Speed': ['Denial Of Service'],
    'Natural Selection': ['Fight Or Flight'],
    'Out For The Count': ['Snake Pit'],
    'Past Master': ['Escape to the Beach'],
    'Point of Impact': ['Eye In The Sky'],
    'Porsche Patrol': ['Turn The Tables'],
    'Precision Pursuit': ['Eye In The Sky'],
    'Priority Call': ['Desert Strike'],
    'Protect And Swerve': ['More Haste, Less Speed', 'Spike Out'],
    'Reventon Reveal': ['Block Buster'],
    'Rule Of Law': ['Limited Emission'],
    'Run To The Hills': ['Guided Missile', 'Hang Tough'],
    'Show Of Force': ['Tough Justice'],
    'Snake Pit': ['Locking On', 'Swedish Swoop'],
    'Spike Out': ['Denial Of Service'],
    'Summit Assault': ['More Haste, Less Speed', 'Spike Out'],
    'Sunset Scalpel': ['Charged Attack', 'Weapon Of Choice'],
    'Swedish Swoop': ['Porsche Patrol'],
    'Takedown Notice': ['Heavy Hitters', 'Priority Call'],
    'Tough Justice': ['Fight Night', 'Untouchable'],
    'Turn It Up': ['Porsche Patrol'],
    'Turn The Tables': ['French Connection', 'Point of Impact', 'Precision Pursuit'],
    'Under Pressure': ['Snake Pit'],
    'Untouchable': ['Arms Race'],
    'Weapon Of Choice': ['Tough Justice'],
    'Zero Tolerance': ['Takedown Notice'],
}

# Where each event's unlock nodes sit in that GAMEPLAY resource, with the event ids each node
# needs. The client finds the resource in game memory from one node and edits the needs of
# events Archipelago has not given yet, so the game keeps them off the map.
# Node layout: u32 event id, u32 0, u64 pointer, u32 count, u32 8, then `count` entries of
# 16 bytes whose first u64 points 4 bytes after a reference [u32 needed event id, u32 ...].
TREE_RESOURCE_SIZE = 84608
EVENT_NODES = {
    321154: [(27008, [572398])],  # Racer - King Of The Road
    321166: [(11824, [572384]), (31376, [695477])],  # Racer - The Art of Driving
    321180: [(22016, [572382])],  # Racer - Glorious Fourth
    321302: [(17024, [572386])],  # Racer - Born In The USA
    321304: [(23264, [572454]), (46096, [572362])],  # Racer - The Prestige
    321305: [(48800, [572225])],  # Racer - Muscle Reflex
    321308: [(16400, [572384]), (30960, [695477])],  # Racer - Passione Italia
    321309: [(7456, [572380])],  # Racer - Jet Set
    321311: [(35328, [1070000])],  # Racer - Seacrest Tour
    321313: [(35120, [572354])],  # Racer - Future Perfect
    321314: [(10576, [572456]), (12032, [695485])],  # Racer - Coast To Coast
    321315: [(12448, [695456])],  # Racer - Heart To Heart
    321316: [(4128, [572376])],  # Racer - No Substitute
    389604: [(48384, [572316])],  # Cop - Locking On
    389611: [(18480, [674922]), (45888, [572338])],  # Cop - Limited Emission
    389614: [(48592, [572342])],  # Cop - Fight Night
    529337: [(20768, [572302])],  # Cop - Block Buster
    529339: [(3504, [572474]), (50880, [572324])],  # Cop - Eye In The Sky
    529341: [(36368, [572466]), (36784, [674897]), (37200, [572470])],  # Cop - Fighting Dirty
    529343: [(21808, [529351])],  # Cop - Spike Out
    529349: [(5376, [572476]), (21184, [674920]), (49840, [572318])],  # Cop - Turn The Tables
    529351: [(50464, [572306])],  # Cop - Denial Of Service
    529353: [(46512, [572330])],  # Cop - Under Pressure
    529355: [(6416, [572314]), (20144, [674992])],  # Cop - Takedown Notice
    529357: [(18064, [529353])],  # Cop - Hang Tough
    529361: [(14528, [674991]), (19520, [389614])],  # Cop - Tough Justice
    529363: [(6000, [572348]), (12864, [674998])],  # Cop - Double Cross
    529365: [(17232, [674993]), (20352, [572336])],  # Cop - Desert Strike
    529367: [(19104, [529361])],  # Cop - Weapon Of Choice
    529369: [(5584, [572334])],  # Cop - Natural Selection
    529371: [(5792, [529369]), (12656, [674997])],  # Cop - Hard To Handle
    572222: [(7872, [572457]), (22432, [572455])],  # Racer - Encore Performance
    572223: [(15776, [572396])],  # Racer - Spirit Of Performance
    572224: [(16608, [321302])],  # Racer - Spoilt For Choice
    572225: [(22848, [572452]), (34912, [321313])],  # Racer - Sports Car Named Desire
    572226: [(29504, [321315])],  # Racer - Sun, Sand And Supercars
    572302: [(49008, [529335])],  # Cop - Escape to the Beach
    572306: [(19936, [529341])],  # Cop - Dark Horse
    572314: [(20560, [529365])],  # Cop - Heavy Hitters
    572316: [(50256, [529349])],  # Cop - Porsche Patrol
    572318: [(20976, [529339])],  # Cop - Point of Impact
    572324: [(21392, [674919]), (50672, [529343])],  # Cop - Summit Assault
    572330: [(38240, [389604]), (38448, [572477])],  # Cop - Snake Pit
    572334: [(14736, [529355])],  # Cop - Fight Or Flight
    572336: [(14112, [529367]), (18688, [572344])],  # Cop - Dust Storm
    572338: [(18272, [674921]), (46928, [529357])],  # Cop - Run To The Hills
    572342: [(17856, [389611])],  # Cop - Arms Race
    572344: [(14320, [529361])],  # Cop - Charged Attack
    572348: [(13696, [529371])],  # Cop - Hard Target
    572350: [(28256, [1070002]), (28464, [1070005])],  # Cop - End Of The Line
    572352: [(9536, [321312])],  # Racer - First Offence
    572354: [(25968, [572453]), (35952, [572460])],  # Racer - Breach Of The Peace
    572360: [(35744, [321305])],  # Racer - Beauty And The Beasts
    572362: [(10784, [695488]), (16192, [572222])],  # Racer - Escape Lane
    572370: [(46304, [572462]), (47552, [321304])],  # Racer - Shock And Awe
    572372: [(6832, [695455])],  # Racer - Avalanche
    572376: [(23888, [572463]), (34080, [572461]), (47136, [695486])],  # Racer - Stampede
    572378: [(10368, [321314])],  # Racer - Blacklisted
    572380: [(11616, [572226])],  # Racer - Unreasonable Force
    572382: [(9120, [572224]), (9744, [695458]), (34288, [695491])],  # Racer - Power Struggle
    572384: [(7248, [321309])],  # Racer - Against All Odds
    572386: [(8080, [674798]), (48176, [695457])],  # Racer - Double Jeopardy
    572392: [(9952, [674799]), (34496, [321180])],  # Racer - Hotting Up
    572396: [(15568, [572392])],  # Racer - Breaking Point
    572398: [(15984, [695476])],  # Racer - Calm Before The Storm
    572400: [(16816, [695459]), (32208, [321154])],  # Racer - Highway Battle
    572452: [(35536, [572354])],  # Racer - Unlimited Driving Pleasure
    572453: [(3920, [572352])],  # Racer - Vanishing Point
    572454: [(10992, [695488]), (11200, [572222])],  # Racer - Extreme Truth
    572455: [(22640, [572360])],  # Racer - The Ultimate Road Car
    572456: [(3296, [321316])],  # Racer - Timed Machine
    572457: [(47760, [572360])],  # Racer - Sidewinder
    572459: [(11408, [321314])],  # Racer - Sand Timer
    572460: [(9328, [572352])],  # Racer - Title Fight
    572461: [(33872, [572372])],  # Racer - V12 For Victory
    572462: [(24096, [572454]), (47968, [572362])],  # Racer - Experience More
    572463: [(23472, [572372])],  # Racer - Ultimately Open
    572466: [(40112, [529337])],  # Cop - Reventon Reveal
    572470: [(19728, [529337])],  # Cop - Do Look After It
    572474: [(4960, [674919]), (6624, [529343])],  # Cop - Protect And Swerve
    572476: [(5168, [529339])],  # Cop - French Connection
    572477: [(4336, [572316])],  # Cop - Swedish Swoop
    674798: [(8496, [321308]), (8912, [321166])],  # Racer - Bull Run
    674799: [(8288, [572382])],  # Racer - Slide Show
    674897: [(36992, [529337])],  # Cop - Lightning Reflex
    674919: [(21600, [529351])],  # Cop - More Haste, Less Speed
    674920: [(50048, [529339])],  # Cop - Precision Pursuit
    674921: [(46720, [529353])],  # Cop - Guided Missile
    674922: [(17440, [674921]), (17648, [529357])],  # Cop - Coming In Hot
    674991: [(19312, [572342])],  # Cop - Untouchable
    674992: [(6208, [529365])],  # Cop - Priority Call
    674993: [(13904, [529367]), (18896, [572344])],  # Cop - Sunset Scalpel
    674997: [(13072, [572334])],  # Cop - Contact Sport
    674998: [(13488, [529371])],  # Cop - Damage Limitation
    695455: [(47344, [572370])],  # Racer - M Power
    695456: [(12240, [572378]), (30128, [572459])],  # Racer - Trail Of Destruction
    695457: [(8704, [321166]), (13280, [321308])],  # Racer - Tough Torque
    695458: [(10160, [321302])],  # Racer - One Of Five
    695459: [(27216, [572398])],  # Racer - Blast From The Past
    695476: [(14944, [695482]), (15152, [572223])],  # Racer - Wild Ride
    695477: [(7664, [321309])],  # Racer - Ageless
    695482: [(15360, [572396])],  # Racer - Faster Than Light
    695485: [(3712, [321316])],  # Racer - Power Trip
    695486: [(7040, [572372])],  # Racer - Racing Stripes
    695488: [(4752, [572457]), (22224, [572455])],  # Racer - Complete Control
    695491: [(34704, [321302])],  # Racer - Twin Turbo
    1070000: [(28672, [572400])],  # Racer - Hunted
    1070001: [(24512, [529361])],  # Cop - Show Of Force
    1070002: [(25760, [529363])],  # Cop - Any Means Necessary
    1070003: [(30544, [321309])],  # Racer - Wing And A Prayer
    1070004: [(28048, [695476])],  # Racer - Pushing The Envelope
    1070005: [(26176, [529363])],  # Cop - Duty Calls
    1070006: [(29088, [572398])],  # Racer - Redline Racing
    1070007: [(26384, [572334])],  # Cop - Lockdown
    1070008: [(27424, [572396])],  # Racer - One Step Ahead
    1070009: [(26592, [529371])],  # Cop - Cut To The Chase
    1070079: [(31168, [572226])],  # Racer - Sunset Racers
    1070080: [(23680, [572376])],  # Racer - Fast Lane
    1070081: [(27632, [572386])],  # Racer - Foot To The Floor
    1070082: [(30752, [572386])],  # Racer - Comeback Tour
    1070083: [(26800, [572376])],  # Racer - Previous Conviction
    1070084: [(38032, [572316])],  # Cop - Turn It Up
    1070085: [(24928, [572342])],  # Cop - Infernal Rampage
    1070086: [(27840, [572382])],  # Racer - Rogue Element
    1070087: [(29296, [695456])],  # Racer - Road To Ruin
    1070088: [(25344, [389611])],  # Cop - Crimewave
    1070089: [(25136, [389611])],  # Cop - Rule Of Law
    1070090: [(30336, [321315])],  # Racer - Resisting Arrest
    1070091: [(37408, [529349])],  # Cop - Arrest Warrant
    1070093: [(37824, [529353])],  # Cop - Marked Man
    1070094: [(37616, [572330])],  # Cop - Out For The Count
    1070095: [(24720, [529365])],  # Cop - Elements Of Speed
    1070096: [(36576, [572302])],  # Cop - Past Master
    1070097: [(29712, [321314])],  # Racer - Barnstormer
    1070098: [(29920, [321316])],  # Racer - Cannonball
    1070107: [(25552, [529355])],  # Cop - Zero Tolerance
    1093012: [(28880, [695476])],  # Racer - Fast Track
    1093015: [(23056, [572354])],  # Racer - Awe Inspired
    1093016: [(24304, [572370])],  # Racer - Rocket Science
}

# Vehicle unlock nodes in the same resource: u32 vehicle id, u32 bounty needed, u64 pointer,
# u32 number of events needed, u32 8, then event references laid out as for events.
# vehicle id -> (offset, bounty needed, [event ids needed]).
VEHICLE_NODES = {
    1111785: (4544, 0, [1070093]),  # Cop - Porsche 911 Speedster
    1111604: (38656, 0, [1070094]),  # Cop - Lamborghini Countach 5000 Quattrovalvole
    1111395: (38864, 0, [1070083]),  # Racer - Porsche 911 Turbo
    1111341: (39696, 0, [1070080]),  # Racer - Porsche 959
    1111618: (39904, 0, [1070084]),  # Cop - Porsche 959
    1111632: (40320, 0, [1070096]),  # Cop - Porsche 911 Turbo
    1111494: (40528, 0, [1070097]),  # Racer - Porsche 911 Speedster
    1111099: (40736, 0, [1070098]),  # Racer - Lamborghini Countach 5000 Quattrovalvole
    380243: (43648, 0, []),  # Cop - Ford Crown Victoria Police Interceptor
    118196: (44352, 0, []),  # Racer - Porsche Boxster Spyder
    383620: (51088, 5000, []),  # Cop - Subaru Impreza WRX STI
    172670: (51232, 5000, []),  # Racer - Mazda RX-8
    383613: (51376, 10000, []),  # Cop - Mazda RX-8
    380286: (51520, 10000, []),  # Racer - Dodge Charger SRT8
    118530: (51664, 15000, []),  # Racer - Mitsubishi Lancer Evolution X
    380372: (51808, 15000, []),  # Cop - Ford Police Interceptor Concept
    292069: (51952, 20000, []),  # Racer - Chevrolet Camaro SS
    383403: (52384, 20000, []),  # Cop - Porsche Cayman S
    172966: (52528, 30000, []),  # Racer - BMW Z4 sDrive35is
    383627: (52672, 30000, []),  # Cop - Nissan 370Z
    529397: (52816, 40000, []),  # Cop - Audi TT RS
    380028: (52960, 40000, []),  # Racer - Audi TT RS
    380544: (53104, 50000, []),  # Racer - Maserati GranCabrio
    383396: (53248, 50000, []),  # Cop - Porsche 911 Targa 4S
    380931: (53392, 60000, []),  # Racer - Nissan 370Z Roadster
    529516: (53536, 60000, []),  # Cop - Maserati GranTurismo S
    380845: (53968, 75000, []),  # Racer - Porsche 911 Turbo S Cabriolet
    383641: (54112, 75000, []),  # Cop - Dodge Charger SRT8
    383198: (54256, 90000, []),  # Racer - Jaguar XKR
    529411: (54400, 90000, []),  # Cop - Aston Martin DBS
    380114: (54544, 105000, []),  # Racer - Chevrolet Corvette Grand Sport
    345203: (54688, 105000, []),  # Cop - Ford Shelby GT500
    383347: (54832, 120000, []),  # Cop - Lamborghini Gallardo LP 560-4
    172714: (55264, 120000, []),  # Racer - Subaru Impreza WRX STI
    383382: (55408, 138750, []),  # Cop - Mitsubishi Lancer Evolution X
    118984: (55552, 138750, []),  # Racer - Audi R8 Spyder 5.2 FSI quattro
    383410: (55696, 157500, []),  # Cop - Porsche Panamera Turbo
    292004: (55840, 157500, []),  # Racer - BMW M3 E92
    383026: (55984, 176250, []),  # Racer - Aston Martin DBS Volante
    383333: (56128, 176250, []),  # Cop - Dodge Challenger SRT8
    292146: (56272, 195000, []),  # Racer - Dodge Challenger SRT8
    383749: (56560, 195000, []),  # Cop - Chevrolet Corvette Z06
    383112: (56848, 215000, []),  # Racer - Bentley Continental Supersports Coupe
    383326: (56992, 215000, []),  # Cop - Chevrolet Camaro SS
    383340: (57136, 235000, []),  # Cop - Ford GT
    172321: (57280, 235000, []),  # Racer - Lamborghini Gallardo LP 560-4
    529453: (57424, 255000, []),  # Cop - Dodge Viper SRT10
    321070: (57568, 255000, []),  # Racer - Porsche 911 Targa 4S
    293191: (58000, 275000, []),  # Racer - Ford GT
    383297: (58144, 275000, []),  # Cop - Alfa Romeo 8C Competizione
    380329: (58288, 296250, []),  # Racer - Ford Shelby GT500 Super Snake
    529376: (58432, 296250, []),  # Cop - Bentley Continental Supersports Coupe
    380587: (58576, 317500, []),  # Racer - Maserati GranTurismo S
    529537: (58720, 317500, []),  # Cop - Mercedes-Benz SLS AMG
    529523: (58864, 338750, []),  # Cop - Maserati Quattroporte Sport GT S
    172586: (59008, 338750, []),  # Racer - McLaren MP4-12C
    121050: (59152, 360000, []),  # Cop - Lamborghini Murcielago LP 640
    380802: (59584, 360000, []),  # Racer - Porsche 911 GT3 RS
    118940: (59728, 382500, []),  # Racer - Alfa Romeo 8C Spider
    383742: (59872, 382500, []),  # Cop - Ford Shelby GT500 Super Snake
    383311: (60016, 405000, []),  # Cop - BMW M3 E92
    329096: (60160, 405000, []),  # Racer - Porsche Carrera GT
    383249: (60304, 427500, []),  # Racer - Lamborghini Gallardo Spyder LP 560-4
    529460: (60448, 427500, []),  # Cop - Dodge Viper SRT10 ACR
    118492: (60736, 450000, []),  # Racer - Koenigsegg CCX
    383853: (61024, 450000, []),  # Cop - Lamborghini Gallardo Valentino Balboni LP 550-2
    383242: (61168, 473750, []),  # Cop - Koenigsegg CCX
    97331: (61312, 473750, []),  # Racer - Lamborghini Murcielago LP 640
    380888: (61456, 497500, []),  # Racer - Mercedes-Benz SLS AMG
    383756: (61600, 521250, []),  # Cop - Chevrolet Corvette ZR1
    1111150: (61744, 521250, []),  # Racer - Lamborghini Sesto Elemento
    383389: (61888, 545000, []),  # Cop - Nissan GT-R SpecV
    118570: (62176, 545000, []),  # Racer - Nissan GT-R SpecV
    383735: (62464, 570000, []),  # Cop - Jaguar XKR
    380200: (62608, 570000, []),  # Racer - Chevrolet Corvette ZR1
    172756: (62752, 595000, []),  # Racer - BMW M6 Convertible
    383686: (62896, 595000, []),  # Cop - Porsche Carrera GT
    529481: (63040, 620000, []),  # Cop - Koenigsegg Agera
    172460: (63184, 620000, []),  # Racer - McLaren F1
    383069: (63472, 645000, []),  # Racer - Aston Martin V12 Vantage
    383658: (63616, 645000, []),  # Cop - Aston Martin V12 Vantage
    1111597: (63904, 672500, []),  # Cop - Lamborghini Sesto Elemento
    380630: (64048, 672500, []),  # Racer - Pagani Zonda Cinque
    745251: (64192, 672500, []),  # Racer - Pagani Zonda Cinque NFS Edition
    383693: (64336, 700000, []),  # Cop - Porsche 911 GT3 RS
    383480: (64480, 700000, []),  # Racer - Lamborghini Gallardo Superleggera LP 570-4
    383527: (64624, 727500, []),  # Racer - Aston Martin One-77
    383354: (64768, 727500, []),  # Cop - Lamborghini Reventon
    383361: (64912, 755000, []),  # Cop - McLaren F1
    383808: (65344, 755000, []),  # Racer - Koenigsegg Agera
    383714: (65488, 785000, []),  # Cop - Mercedes-Benz SL65 AMG Black Series
    329012: (65632, 785000, []),  # Racer - Mercedes-Benz SL65 AMG Black Series
    172363: (65776, 815000, []),  # Racer - Lamborghini Murcielago LP 670-4 SuperVeloce
    383425: (65920, 815000, []),  # Cop - McLaren MP4-12C
    383432: (66064, 845000, []),  # Racer - Porsche 918 Spyder Concept Study
    118889: (66208, 845000, []),  # Cop - Audi R8 Coupe 5.2 FSI quattro
    529425: (66640, 875000, []),  # Cop - Aston Martin One-77
    172882: (66784, 875000, []),  # Racer - Dodge Viper SRT10 ACR
    380673: (66928, 906250, []),  # Racer - Pagani Zonda Cinque Roadster
    745296: (67072, 906250, []),  # Racer - Pagani Zonda Cinque NFS Edition Roadster
    383707: (67216, 906250, []),  # Cop - Pagani Zonda Cinque
    172279: (67360, 937500, []),  # Racer - Koenigsegg CCXR Edition
    118240: (67504, 937500, []),  # Cop - Bugatti Veyron 16.4
    383728: (67648, 968750, []),  # Cop - Lamborghini Murcielago LP 670-4 SuperVeloce
    380501: (67792, 968750, []),  # Racer - Lamborghini Reventon Roadster
    380071: (68224, 1000000, []),  # Racer - Bugatti Veyron 16.4 Grand Sport
    529488: (68368, 1000000, []),  # Cop - Koenigsegg CCXR Edition
    172237: (68512, 1032500, []),  # Racer - Nissan 370Z
    293124: (68656, 1065000, []),  # Racer - Alfa Romeo 8C Competizione
    1065371: (68800, 1097500, []),  # Racer - Lamborghini Murcielago LP 650-4 Roadster
    1111611: (68944, 1130000, []),  # Cop - Lamborghini Diablo SV
    1111287: (69376, 1130000, []),  # Racer - Lamborghini Diablo SV
    118158: (69520, 1154000, []),  # Racer - Bugatti Veyron 16.4
    118454: (69664, 1178000, []),  # Racer - Ford Shelby GT500
    380982: (69808, 1202000, []),  # Racer - Aston Martin DBS
    172798: (69952, 1226000, []),  # Racer - Maserati Quattroporte Sport GT S
    529502: (70384, 1265000, []),  # Cop - Lamborghini Gallardo Superleggera LP 570-4
    210008: (70528, 1270750, []),  # Racer - Audi R8 Coupe 5.2 FSI quattro
    1065090: (70672, 1315500, []),  # Racer - Porsche 911 GT2 RS
    118608: (70816, 1360250, []),  # Racer - Porsche Cayman S
    1065135: (71104, 1405000, []),  # Cop - Porsche 911 GT2 RS
    380157: (71248, 1405000, []),  # Racer - Chevrolet Corvette Z06
    1065045: (71536, 1441250, []),  # Racer - Bentley Continental Supersports Convertible
    172840: (71680, 1477500, []),  # Racer - Dodge Viper SRT10
    293008: (71824, 1513750, []),  # Racer - Lamborghini Reventon
    380415: (72256, 1550000, []),  # Racer - Lamborghini Gallardo Valentino Balboni LP 550-2
    1065326: (72400, 1625000, []),  # Racer - Dodge Viper SRT10 Final Edition
    329054: (72544, 1700000, []),  # Racer - Porsche Panamera Turbo
    1065194: (72832, 1700000, []),  # Cop - Bugatti Veyron 16.4 Super Sport
    1065149: (73264, 1850000, []),  # Racer - Bugatti Veyron 16.4 Super Sport
    1065267: (73840, 2000000, []),  # Racer - Gumpert Apollo S
    1065312: (74272, 2000000, []),  # Cop - Gumpert Apollo S
}

# First event of each side: no node, open from the start. Unlocked events and cars are
# made to need it instead of their own prerequisites.
ROOT_EVENTS = {"Racer": 321312, "Cop": 529335}  # Roadsters Reborn, Chase 101

# The first events have no node: the game always shows them (lending them another event's node
# was tried and the game ignores it). The client takes them out of the map lists instead.
ROOT_DONORS = {}
