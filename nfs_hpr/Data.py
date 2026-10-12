from __future__ import annotations

from typing import Dict, List

GAME_NAME = "Need for Speed Hot Pursuit Remastered"

# ======================================================================================
# EVENTS (78 Racer / 63 Cop), grouped by series
# ======================================================================================

# Fixed event order: location and item IDs depend on it. Never reorder; append new events.
RACER_EVENTS: List[str] = [
    "Roadsters Reborn",
    "First Offence",
    "Vanishing Point",
    "Breach Of The Peace",
    "Future Perfect",
    "Unlimited Driving Pleasure",
    "Sports Car Named Desire",
    "Title Fight",
    "Muscle Reflex",
    "Beauty And The Beasts",
    "Sidewinder",
    "Encore Performance",
    "Extreme Truth",
    "Escape Lane",
    "Awe Inspired",
    "The Ultimate Road Car",
    "The Prestige",
    "Complete Control",
    "Experience More",
    "Shock And Awe",
    "M Power",
    "Rocket Science",
    "Avalanche",
    "Racing Stripes",
    "V12 For Victory",
    "Stampede",
    "Fast Lane",
    "Ultimately Open",
    "No Substitute",
    "Power Trip",
    "Previous Conviction",
    "Cannonball",
    "Coast To Coast",
    "Timed Machine",
    "Sand Timer",
    "Trail Of Destruction",
    "Road To Ruin",
    "Barnstormer",
    "Heart To Heart",
    "Sun, Sand And Supercars",
    "Sunset Racers",
    "Resisting Arrest",
    "Blacklisted",
    "Unreasonable Force",
    "Jet Set",
    "Against All Odds",
    "The Art of Driving",
    "Passione Italia",
    "Ageless",
    "Bull Run",
    "Tough Torque",
    "Wing And A Prayer",
    "Double Jeopardy",
    "Born In The USA",
    "Twin Turbo",
    "Comeback Tour",
    "One Of Five",
    "Foot To The Floor",
    "Power Struggle",
    "Spoilt For Choice",
    "Slide Show",
    "Glorious Fourth",
    "Hotting Up",
    "Rogue Element",
    "Breaking Point",
    "Spirit Of Performance",
    "Faster Than Light",
    "Wild Ride",
    "Fast Track",
    "One Step Ahead",
    "Pushing The Envelope",
    "Calm Before The Storm",
    "King Of The Road",
    "Highway Battle",
    "Hunted",
    "Blast From The Past",
    "Redline Racing",
    "Seacrest Tour",
]

COP_EVENTS: List[str] = [
    "Chase 101",
    "Escape to the Beach",
    "Block Buster",
    "Reventon Reveal",
    "Fighting Dirty",
    "Do Look After It",
    "Past Master",
    "Dark Horse",
    "Lightning Reflex",
    "Denial Of Service",
    "More Haste, Less Speed",
    "Protect And Swerve",
    "Eye In The Sky",
    "Precision Pursuit",
    "French Connection",
    "Spike Out",
    "Point of Impact",
    "Summit Assault",
    "Turn The Tables",
    "Porsche Patrol",
    "Locking On",
    "Arrest Warrant",
    "Turn It Up",
    "Snake Pit",
    "Swedish Swoop",
    "Under Pressure",
    "Hang Tough",
    "Run To The Hills",
    "Coming In Hot",
    "Limited Emission",
    "Rule Of Law",
    "Crimewave",
    "Arms Race",
    "Untouchable",
    "Fight Night",
    "Infernal Rampage",
    "Marked Man",
    "Out For The Count",
    "Tough Justice",
    "Weapon Of Choice",
    "Sunset Scalpel",
    "Desert Strike",
    "Charged Attack",
    "Priority Call",
    "Heavy Hitters",
    "Guided Missile",
    "Takedown Notice",
    "Elements Of Speed",
    "Dust Storm",
    "Zero Tolerance",
    "Fight Or Flight",
    "Contact Sport",
    "Hard To Handle",
    "Lockdown",
    "Damage Limitation",
    "Double Cross",
    "Cut To The Chase",
    "Natural Selection",
    "Duty Calls",
    "Any Means Necessary",
    "Hard Target",
    "Show Of Force",
    "End Of The Line",
]

# Series of each event, from the NFS wiki career pages (Hot Pursuit Remastered).
RACER_EVENTS_BY_SERIES: Dict[str, List[str]] = {
    "Sports": [
        "Roadsters Reborn",
        "First Offence",
        "Vanishing Point",
        "Breach Of The Peace",
        "Future Perfect",
        "Unlimited Driving Pleasure",
        "Sports Car Named Desire",
        "Title Fight",
        "Awe Inspired",
        "Previous Conviction",
    ],
    "Performance": [
        "Muscle Reflex",
        "Beauty And The Beasts",
        "Sidewinder",
        "Encore Performance",
        "Extreme Truth",
        "Escape Lane",
        "The Ultimate Road Car",
        "The Prestige",
        "Complete Control",
        "Experience More",
        "Shock And Awe",
        "M Power",
        "Rocket Science",
    ],
    "Super": [
        "Avalanche",
        "Racing Stripes",
        "V12 For Victory",
        "Stampede",
        "Fast Lane",
        "Ultimately Open",
        "No Substitute",
        "Power Trip",
        "Cannonball",
        "Coast To Coast",
        "Timed Machine",
        "Sand Timer",
        "Trail Of Destruction",
        "Road To Ruin",
        "Barnstormer",
        "Heart To Heart",
        "Sun, Sand And Supercars",
        "Sunset Racers",
        "Resisting Arrest",
        "Blacklisted",
        "Unreasonable Force",
    ],
    "Exotic": [
        "Jet Set",
        "Against All Odds",
        "The Art of Driving",
        "Passione Italia",
        "Ageless",
        "Bull Run",
        "Tough Torque",
        "Wing And A Prayer",
        "Double Jeopardy",
        "Born In The USA",
        "Twin Turbo",
        "Comeback Tour",
        "One Of Five",
        "Foot To The Floor",
        "Power Struggle",
        "Spoilt For Choice",
        "Slide Show",
        "Glorious Fourth",
        "Hotting Up",
        "Rogue Element",
    ],
    "Hyper": [
        "Breaking Point",
        "Spirit Of Performance",
        "Faster Than Light",
        "Wild Ride",
        "Fast Track",
        "One Step Ahead",
        "Pushing The Envelope",
        "Calm Before The Storm",
        "King Of The Road",
        "Highway Battle",
        "Hunted",
        "Blast From The Past",
        "Redline Racing",
        "Seacrest Tour",
    ],
}

COP_EVENTS_BY_SERIES: Dict[str, List[str]] = {
    "Traffic Police": [
        "Chase 101",
        "Escape to the Beach",
        "Block Buster",
        "Reventon Reveal",
        "Fighting Dirty",
        "Do Look After It",
        "Past Master",
        "Dark Horse",
        "Lightning Reflex",
        "Arrest Warrant",
    ],
    "Highway Patrol": [
        "Denial Of Service",
        "More Haste, Less Speed",
        "Protect And Swerve",
        "Eye In The Sky",
        "Precision Pursuit",
        "French Connection",
        "Spike Out",
        "Point of Impact",
        "Summit Assault",
        "Turn The Tables",
    ],
    "Rapid Deployment": [
        "Porsche Patrol",
        "Locking On",
        "Turn It Up",
        "Snake Pit",
        "Swedish Swoop",
        "Under Pressure",
        "Hang Tough",
        "Run To The Hills",
        "Coming In Hot",
        "Limited Emission",
        "Rule Of Law",
        "Crimewave",
        "Marked Man",
        "Out For The Count",
        "Guided Missile",
    ],
    "Speed Enforcement": [
        "Arms Race",
        "Untouchable",
        "Fight Night",
        "Infernal Rampage",
        "Tough Justice",
        "Weapon Of Choice",
        "Sunset Scalpel",
        "Desert Strike",
        "Charged Attack",
        "Priority Call",
        "Heavy Hitters",
        "Takedown Notice",
        "Elements Of Speed",
        "Dust Storm",
        "Zero Tolerance",
        "Show Of Force",
    ],
    "Special Response": [
        "Fight Or Flight",
        "Contact Sport",
        "Hard To Handle",
        "Lockdown",
        "Damage Limitation",
        "Double Cross",
        "Cut To The Chase",
        "Natural Selection",
        "Duty Calls",
        "Any Means Necessary",
        "Hard Target",
        "End Of The Line",
    ],
}

RACER_EVENT_SERIES: Dict[str, str] = {e: s for s, es in RACER_EVENTS_BY_SERIES.items() for e in es}
COP_EVENT_SERIES: Dict[str, str] = {e: s for s, es in COP_EVENTS_BY_SERIES.items() for e in es}

assert set(RACER_EVENT_SERIES) == set(RACER_EVENTS) and len(RACER_EVENT_SERIES) == len(RACER_EVENTS)
assert set(COP_EVENT_SERIES) == set(COP_EVENTS) and len(COP_EVENT_SERIES) == len(COP_EVENTS)

# Preview and Gauntlet events lend the player a car: no owned vehicle is needed.
RACER_LOANED_VEHICLE_EVENTS = {
    # Preview
    "Awe Inspired", "Unlimited Driving Pleasure", "Vanishing Point", "Extreme Truth",
    "Rocket Science", "The Ultimate Road Car", "Sand Timer", "Ultimately Open", "Ageless",
    # Gauntlet
    "M Power", "Barnstormer", "Cannonball", "Trail Of Destruction", "One Of Five",
    "Tough Torque", "Blast From The Past", "Pushing The Envelope",
}

COP_LOANED_VEHICLE_EVENTS = {
    # Preview
    "Do Look After It", "Reventon Reveal", "French Connection", "Protect And Swerve", "Swedish Swoop",
}

assert RACER_LOANED_VEHICLE_EVENTS <= set(RACER_EVENTS)
assert COP_LOANED_VEHICLE_EVENTS <= set(COP_EVENTS)

RACER_FINAL_EVENT = "Seacrest Tour"
COP_FINAL_EVENT = "End Of The Line"

RACER_MEDAL_TIERS = ["Bronze", "Silver", "Gold"]
COP_MEDAL_TIERS = ["Pass", "Merit", "Distinction"]

# ======================================================================================
# VEHICLES
# ======================================================================================

RACER_VEHICLES_BY_CLASS: Dict[str, List[str]] = {
    "Sports": [
        "Porsche 911 Turbo", "Porsche Boxster Spyder", "Mazda RX-8", "Dodge Charger SRT8",
        "Mitsubishi Lancer Evolution X", "BMW Z4 sDrive35is", "Nissan 370Z Roadster",
        "Subaru Impreza WRX STI", "Nissan 370Z",
    ],
    "Performance": [
        "Chevrolet Camaro SS", "Audi TT RS", "Maserati GranCabrio", "Jaguar XKR", "BMW M3 E92",
        "Dodge Challenger SRT8", "Porsche 911 Targa 4S", "Maserati GranTurismo S",
        "Alfa Romeo 8C Spider", "Alfa Romeo 8C Competizione", "Ford Shelby GT500",
        "Maserati Quattroporte Sport GT S", "Porsche Cayman S",
    ],
    "Super": [
        "Porsche 959", "Lamborghini Countach 5000 Quattrovalvole", "Porsche 911 Speedster",
        "Porsche 911 Turbo S Cabriolet", "Chevrolet Corvette Grand Sport",
        "Audi R8 Spyder 5.2 FSI quattro", "Aston Martin DBS Volante",
        "Lamborghini Gallardo LP 560-4", "Ford Shelby GT500 Super Snake", "Porsche 911 GT3 RS",
        "Lamborghini Gallardo Spyder LP 560-4", "Mercedes-Benz SLS AMG", "Nissan GT-R SpecV",
        "BMW M6 Convertible", "Aston Martin V12 Vantage",
        "Lamborghini Gallardo Superleggera LP 570-4", "Mercedes-Benz SL65 AMG Black Series",
        "Porsche 918 Spyder Concept Study", "Aston Martin DBS", "Audi R8 Coupe 5.2 FSI quattro",
        "Chevrolet Corvette Z06", "Dodge Viper SRT10",
        "Lamborghini Gallardo Valentino Balboni LP 550-2", "Dodge Viper SRT10 Final Edition",
        "Porsche Panamera Turbo",
    ],
    "Exotic": [
        "Bentley Continental Supersports Coupe", "Ford GT", "McLaren MP4-12C",
        "Porsche Carrera GT", "Lamborghini Murcielago LP 640", "Lamborghini Sesto Elemento",
        "Chevrolet Corvette ZR1", "Pagani Zonda Cinque", "Pagani Zonda Cinque NFS Edition",
        "Aston Martin One-77", "Lamborghini Murcielago LP 670-4 SuperVeloce",
        "Dodge Viper SRT10 ACR", "Pagani Zonda Cinque Roadster",
        "Pagani Zonda Cinque NFS Edition Roadster", "Lamborghini Reventon Roadster",
        "Lamborghini Murcielago LP 650-4 Roadster", "Lamborghini Diablo SV",
        "Porsche 911 GT2 RS", "Bentley Continental Supersports Convertible",
        "Lamborghini Reventon",
    ],
    "Hyper": [
        "Koenigsegg CCX", "Koenigsegg Agera", "McLaren F1", "Koenigsegg CCXR Edition",
        "Bugatti Veyron 16.4 Grand Sport", "Bugatti Veyron 16.4",
        "Bugatti Veyron 16.4 Super Sport", "Gumpert Apollo S",
    ],
}

COP_VEHICLES_BY_UNIT: Dict[str, List[str]] = {
    "Traffic Police": [
        "Ford Crown Victoria Police Interceptor", "Ford Police Interceptor Concept",
        "Porsche 911 Turbo", "Mazda RX-8", "Dodge Charger SRT8", "Mitsubishi Lancer Evolution X",
        "Subaru Impreza WRX STI", "Nissan 370Z",
    ],
    "Highway Patrol": [
        "Chevrolet Camaro SS", "Audi TT RS", "Jaguar XKR", "BMW M3 E92", "Dodge Challenger SRT8",
        "Porsche 911 Targa 4S", "Maserati GranTurismo S", "Alfa Romeo 8C Competizione",
        "Ford Shelby GT500", "Maserati Quattroporte Sport GT S", "Porsche Cayman S",
    ],
    "Rapid Deployment": [
        "Porsche 959", "Lamborghini Countach 5000 Quattrovalvole", "Porsche 911 Speedster",
        "Lamborghini Gallardo LP 560-4", "Ford Shelby GT500 Super Snake", "Porsche 911 GT3 RS",
        "Mercedes-Benz SLS AMG", "Nissan GT-R SpecV", "Aston Martin V12 Vantage",
        "Lamborghini Gallardo Superleggera LP 570-4", "Mercedes-Benz SL65 AMG Black Series",
        "Aston Martin DBS", "Audi R8 Coupe 5.2 FSI quattro", "Chevrolet Corvette Z06",
        "Dodge Viper SRT10", "Lamborghini Gallardo Valentino Balboni LP 550-2",
        "Porsche Panamera Turbo",
    ],
    "Speed Enforcement": [
        "Bentley Continental Supersports Coupe", "Ford GT", "McLaren MP4-12C",
        "Porsche Carrera GT", "Lamborghini Murcielago LP 640", "Lamborghini Sesto Elemento",
        "Chevrolet Corvette ZR1", "Pagani Zonda Cinque", "Aston Martin One-77",
        "Lamborghini Murcielago LP 670-4 SuperVeloce", "Dodge Viper SRT10 ACR",
        "Lamborghini Diablo SV", "Porsche 911 GT2 RS", "Lamborghini Reventon",
    ],
    "Special Response": [
        "Koenigsegg CCX", "Koenigsegg Agera", "McLaren F1", "Koenigsegg CCXR Edition",
        "Bugatti Veyron 16.4", "Bugatti Veyron 16.4 Super Sport", "Gumpert Apollo S",
    ],
}

RACER_VEHICLES = [v for vs in RACER_VEHICLES_BY_CLASS.values() for v in vs]
COP_VEHICLES = [v for vs in COP_VEHICLES_BY_UNIT.values() for v in vs]

# Cars allowed in each event, from the game data (EventCars.py). For Preview and Gauntlet
# events (and a few others) this is the car the game lends for the event.
from .EventCars import EVENT_CARS


def _event_cars(side: str, event: str) -> List[str]:
    return list(dict.fromkeys(EVENT_CARS[(side, event)]))


RACER_EVENT_VEHICLES: Dict[str, List[str]] = {e: _event_cars("Racer", e) for e in RACER_EVENTS}
COP_EVENT_VEHICLES: Dict[str, List[str]] = {e: _event_cars("Cop", e) for e in COP_EVENTS}


# In-game unlock condition of each vehicle (from the NFS wiki career pages):
# an int is the bounty required, a str is the event that must be completed.
RACER_VEHICLE_UNLOCKS: Dict[str, object] = {
    # Sports
    "Porsche Boxster Spyder": 0, "Subaru Impreza WRX STI": 120_000, "Mazda RX-8": 5_000,
    "Dodge Charger SRT8": 10_000, "Mitsubishi Lancer Evolution X": 15_000, "BMW Z4 sDrive35is": 30_000,
    "Nissan 370Z Roadster": 60_000, "Nissan 370Z": 1_032_500, "Porsche 911 Turbo": "Previous Conviction",
    # Performance
    "Chevrolet Camaro SS": 20_000, "Audi TT RS": 40_000, "Maserati GranCabrio": 50_000, "Jaguar XKR": 90_000,
    "BMW M3 E92": 157_500, "Dodge Challenger SRT8": 195_000, "Porsche 911 Targa 4S": 255_000,
    "Maserati GranTurismo S": 317_500, "Alfa Romeo 8C Spider": 382_500, "Alfa Romeo 8C Competizione": 1_065_000,
    "Ford Shelby GT500": 1_178_000, "Maserati Quattroporte Sport GT S": 1_226_000, "Porsche Cayman S": 1_360_250,
    # Super
    "Porsche 911 Turbo S Cabriolet": 75_000, "Chevrolet Corvette Grand Sport": 105_000,
    "Audi R8 Spyder 5.2 FSI quattro": 138_750, "Aston Martin DBS Volante": 176_250,
    "Lamborghini Gallardo LP 560-4": 235_000, "Ford Shelby GT500 Super Snake": 296_250, "Porsche 911 GT3 RS": 360_000,
    "Lamborghini Gallardo Spyder LP 560-4": 427_500, "Mercedes-Benz SLS AMG": 497_500, "Nissan GT-R SpecV": 545_000,
    "BMW M6 Convertible": 595_000, "Aston Martin V12 Vantage": 645_000,
    "Lamborghini Gallardo Superleggera LP 570-4": 700_000, "Mercedes-Benz SL65 AMG Black Series": 785_000,
    "Porsche 918 Spyder Concept Study": 845_000, "Aston Martin DBS": 1_202_000,
    "Audi R8 Coupe 5.2 FSI quattro": 1_270_750, "Chevrolet Corvette Z06": 1_405_000, "Dodge Viper SRT10": 1_477_500,
    "Lamborghini Gallardo Valentino Balboni LP 550-2": 1_550_000, "Dodge Viper SRT10 Final Edition": 1_625_000,
    "Porsche Panamera Turbo": 1_700_000, "Lamborghini Countach 5000 Quattrovalvole": "Cannonball",
    "Porsche 911 Speedster": "Barnstormer", "Porsche 959": "Fast Lane",
    # Exotic
    "Bentley Continental Supersports Coupe": 215_000, "Ford GT": 275_000, "McLaren MP4-12C": 338_750,
    "Porsche Carrera GT": 405_000, "Lamborghini Murcielago LP 640": 473_750, "Lamborghini Sesto Elemento": 521_250,
    "Chevrolet Corvette ZR1": 570_000, "Pagani Zonda Cinque": 672_500, "Pagani Zonda Cinque NFS Edition": 672_500,
    "Aston Martin One-77": 727_500, "Lamborghini Murcielago LP 670-4 SuperVeloce": 815_000,
    "Dodge Viper SRT10 ACR": 875_000, "Pagani Zonda Cinque Roadster": 906_250,
    "Pagani Zonda Cinque NFS Edition Roadster": 906_250, "Lamborghini Reventon Roadster": 968_750,
    "Lamborghini Murcielago LP 650-4 Roadster": 1_097_500, "Lamborghini Diablo SV": 1_130_000,
    "Porsche 911 GT2 RS": 1_315_500, "Bentley Continental Supersports Convertible": 1_441_250,
    "Lamborghini Reventon": 1_513_750,
    # Hyper
    "Koenigsegg CCX": 450_000, "McLaren F1": 620_000, "Koenigsegg Agera": 755_000,
    "Koenigsegg CCXR Edition": 937_500, "Bugatti Veyron 16.4 Grand Sport": 1_000_000,
    "Bugatti Veyron 16.4": 1_154_000, "Bugatti Veyron 16.4 Super Sport": 1_850_000, "Gumpert Apollo S": 2_000_000,
}

COP_VEHICLE_UNLOCKS: Dict[str, object] = {
    # Traffic Police
    "Ford Crown Victoria Police Interceptor": 0, "Subaru Impreza WRX STI": 5_000, "Mazda RX-8": 10_000,
    "Ford Police Interceptor Concept": 15_000, "Nissan 370Z": 30_000, "Dodge Charger SRT8": 75_000,
    "Mitsubishi Lancer Evolution X": 138_750, "Porsche 911 Turbo": "Past Master",
    # Highway Patrol
    "Porsche Cayman S": 20_000, "Audi TT RS": 40_000, "Porsche 911 Targa 4S": 50_000,
    "Maserati GranTurismo S": 60_000, "Ford Shelby GT500": 105_000, "Dodge Challenger SRT8": 176_250,
    "Chevrolet Camaro SS": 215_000, "Alfa Romeo 8C Competizione": 275_000,
    "Maserati Quattroporte Sport GT S": 338_750, "BMW M3 E92": 405_000, "Jaguar XKR": 570_000,
    # Rapid Deployment
    "Aston Martin DBS": 90_000, "Lamborghini Gallardo LP 560-4": 120_000, "Porsche Panamera Turbo": 157_500,
    "Chevrolet Corvette Z06": 195_000, "Dodge Viper SRT10": 255_000, "Mercedes-Benz SLS AMG": 317_500,
    "Ford Shelby GT500 Super Snake": 382_500, "Lamborghini Gallardo Valentino Balboni LP 550-2": 450_000,
    "Nissan GT-R SpecV": 545_000, "Aston Martin V12 Vantage": 645_000, "Porsche 911 GT3 RS": 700_000,
    "Mercedes-Benz SL65 AMG Black Series": 785_000, "Audi R8 Coupe 5.2 FSI quattro": 845_000,
    "Lamborghini Gallardo Superleggera LP 570-4": 1_265_000,
    "Lamborghini Countach 5000 Quattrovalvole": "Out For The Count", "Porsche 911 Speedster": "Marked Man",
    "Porsche 959": "Turn It Up",
    # Speed Enforcement
    "Ford GT": 235_000, "Bentley Continental Supersports Coupe": 296_250, "Lamborghini Murcielago LP 640": 360_000,
    "Dodge Viper SRT10 ACR": 427_500, "Chevrolet Corvette ZR1": 521_250, "Porsche Carrera GT": 595_000,
    "Lamborghini Sesto Elemento": 672_500, "Lamborghini Reventon": 727_500, "McLaren MP4-12C": 815_000,
    "Aston Martin One-77": 875_000, "Pagani Zonda Cinque": 906_250,
    "Lamborghini Murcielago LP 670-4 SuperVeloce": 968_750, "Lamborghini Diablo SV": 1_130_000,
    "Porsche 911 GT2 RS": 1_405_000,
    # Special Response
    "Koenigsegg CCX": 473_750, "Koenigsegg Agera": 620_000, "McLaren F1": 755_000,
    "Bugatti Veyron 16.4": 937_500, "Koenigsegg CCXR Edition": 1_000_000,
    "Bugatti Veyron 16.4 Super Sport": 1_700_000, "Gumpert Apollo S": 2_000_000,
}

# Bounty awarded for each medal, by series tier (same values for Racer and Cop).
# Index 0 = Sports / Traffic Police ... index 4 = Hyper / Special Response.
MEDAL_BOUNTY_BY_TIER = [
    {"bronze": 2_000, "silver": 4_000, "gold": 6_000},
    {"bronze": 2_500, "silver": 5_000, "gold": 8_000},
    {"bronze": 3_000, "silver": 6_000, "gold": 10_000},
    {"bronze": 4_000, "silver": 8_000, "gold": 12_500},
    {"bronze": 5_000, "silver": 10_000, "gold": 15_000},
]

# Event whose completion unlocks each series in-game (the first series is open from the start).
RACER_SERIES_UNLOCK_EVENT: Dict[str, object] = {
    "Sports": None,
    "Performance": "Sports Car Named Desire",
    "Super": "M Power",
    "Exotic": "Unreasonable Force",
    "Hyper": "Hotting Up",
}
COP_SERIES_UNLOCK_EVENT: Dict[str, object] = {
    "Traffic Police": None,
    "Highway Patrol": "Dark Horse",
    "Rapid Deployment": "Turn The Tables",
    "Speed Enforcement": "Limited Emission",
    "Special Response": "Takedown Notice",
}

RACER_EVENT_GOLD_BOUNTY: Dict[str, int] = {
    e: MEDAL_BOUNTY_BY_TIER[list(RACER_EVENTS_BY_SERIES).index(s)]["gold"] for e, s in RACER_EVENT_SERIES.items()
}
COP_EVENT_GOLD_BOUNTY: Dict[str, int] = {
    e: MEDAL_BOUNTY_BY_TIER[list(COP_EVENTS_BY_SERIES).index(s)]["gold"] for e, s in COP_EVENT_SERIES.items()
}

assert set(RACER_VEHICLE_UNLOCKS) == set(RACER_VEHICLES), set(RACER_VEHICLES) ^ set(RACER_VEHICLE_UNLOCKS)
assert set(COP_VEHICLE_UNLOCKS) == set(COP_VEHICLES), set(COP_VEHICLES) ^ set(COP_VEHICLE_UNLOCKS)


# ======================================================================================
# WEAPONS (4 weapons x 4 levels per side, progressive items)
# ======================================================================================

RACER_WEAPONS = ["Spike Strip", "EMP", "Turbo", "Jammer"]
COP_WEAPONS = ["Spike Strip", "EMP", "Helicopter", "Roadblock"]
WEAPON_MAX_LEVEL = 4

RACER_WEAPON_ITEMS = [f"Progressive Racer {w}" for w in RACER_WEAPONS]
COP_WEAPON_ITEMS = [f"Progressive Cop {w}" for w in COP_WEAPONS]
ALL_WEAPON_ITEMS = RACER_WEAPON_ITEMS + COP_WEAPON_ITEMS

# ======================================================================================
# LEVELS
# ======================================================================================

MAX_LEVEL = 20

# Bounty needed to reach each rank (index 0 = rank 1 ... index 19 = rank 20).
# Same ladder for Racer and Cop.
LEVEL_BOUNTY = [
    0, 20_000, 60_000, 120_000, 195_000, 275_000, 360_000, 450_000, 545_000, 645_000,
    755_000, 875_000, 1_000_000, 1_130_000, 1_226_000, 1_405_000, 1_550_000, 1_700_000,
    1_850_000, 2_000_000,
]
assert len(LEVEL_BOUNTY) == MAX_LEVEL

# ======================================================================================
# ITEM NAMES
# ======================================================================================

RACER_EVENT_UNLOCK_ITEMS = [f"Unlock Racer Event - {e}" for e in RACER_EVENTS]
COP_EVENT_UNLOCK_ITEMS = [f"Unlock Cop Event - {e}" for e in COP_EVENTS]
ALL_EVENT_UNLOCK_ITEMS = RACER_EVENT_UNLOCK_ITEMS + COP_EVENT_UNLOCK_ITEMS

RACER_VEHICLE_UNLOCK_ITEMS = [f"Unlock Racer Vehicle - {v}" for v in RACER_VEHICLES]
COP_VEHICLE_UNLOCK_ITEMS = [f"Unlock Cop Vehicle - {v}" for v in COP_VEHICLES]
ALL_VEHICLE_UNLOCK_ITEMS = RACER_VEHICLE_UNLOCK_ITEMS + COP_VEHICLE_UNLOCK_ITEMS

RACER_SERIES_UNLOCK_ITEMS = [f"Unlock Racer Series - {c}" for c in RACER_VEHICLES_BY_CLASS]
COP_SERIES_UNLOCK_ITEMS = [f"Unlock Cop Series - {u}" for u in COP_VEHICLES_BY_UNIT]
ALL_SERIES_UNLOCK_ITEMS = RACER_SERIES_UNLOCK_ITEMS + COP_SERIES_UNLOCK_ITEMS

# Starting series (matching the starting vehicles)
STARTING_SERIES_UNLOCKS = [
    "Unlock Racer Series - Sports",
    "Unlock Cop Series - Traffic Police",
]

STARTING_EVENT_UNLOCKS = [
    f"Unlock Racer Event - {RACER_EVENTS[0]}",
    f"Unlock Cop Event - {COP_EVENTS[0]}",
]
# One starting vehicle per side is picked at random from these, so that the
# starting event of each side is always playable.
# They are the cars a new career owns from the start (unlock bounty 0): the Porsche Boxster
# Spyder and the Ford Crown Victoria, which can drive the first event of each side.
STARTING_RACER_VEHICLE_CHOICES = [v for v, c in RACER_VEHICLE_UNLOCKS.items() if c == 0]
STARTING_COP_VEHICLE_CHOICES = [v for v, c in COP_VEHICLE_UNLOCKS.items() if c == 0]
assert set(STARTING_RACER_VEHICLE_CHOICES) <= set(RACER_EVENT_VEHICLES.get(RACER_EVENTS[0]) or RACER_VEHICLES)

TRAP_ITEMS = [
    "Trap - Flat Tire",
    "Trap - EMP Impact",
    "Trap - Speed Limiter 10s",
    "Trap - Roadblock Deployed",
    "Trap - System Jammed",
    "Trap - Reversed Steering",
]

# Trap effects (for the client): duration in seconds, 0 = instant
TRAP_DURATIONS = {
    "Trap - Flat Tire": 8,
    "Trap - EMP Impact": 0,
    "Trap - Speed Limiter 10s": 10,
    "Trap - Roadblock Deployed": 0,
    "Trap - System Jammed": 10,
    "Trap - Reversed Steering": 10,
}

BOUNTY_BUNDLE_VALUES = {
    "Bounty Bundle - 1,000": 1000,
    "Bounty Bundle - 2,500": 2500,
    "Bounty Bundle - 5,000": 5000,
    "Bounty Bundle - 10,000": 10000,
    "Bounty Bundle - 15,000": 15000,
    "Bounty Bundle - 20,000": 20000,
}
BOUNTY_BUNDLE_WEIGHTS = {
    "Bounty Bundle - 1,000": 40,
    "Bounty Bundle - 2,500": 30,
    "Bounty Bundle - 5,000": 18,
    "Bounty Bundle - 10,000": 8,
    "Bounty Bundle - 15,000": 3,
    "Bounty Bundle - 20,000": 1,
}

NITRO_REFILL_VALUES = {
    "Nitro Refill - Small": 25,
    "Nitro Refill - Medium": 50,
    "Nitro Refill - Large": 75,
    "Nitro Refill - Full": 100,
}
NITRO_REFILL_WEIGHTS = {
    "Nitro Refill - Small": 45,
    "Nitro Refill - Medium": 30,
    "Nitro Refill - Large": 18,
    "Nitro Refill - Full": 7,
}

FILLER_TYPE_WEIGHTS = {"bounty": 75, "nitro": 25}

BOUNTY_BUNDLE_ITEMS = list(BOUNTY_BUNDLE_VALUES)
NITRO_REFILL_ITEMS = list(NITRO_REFILL_VALUES)
FILLER_ITEMS = BOUNTY_BUNDLE_ITEMS + NITRO_REFILL_ITEMS

VICTORY_ITEM = "Victory"

# ======================================================================================
# LOCATION NAMES
# ======================================================================================

def racer_medal_location(event: str, tier: str) -> str:
    return f"Racer Medal - {event} - {tier}"


def cop_medal_location(event: str, tier: str) -> str:
    return f"Cop Medal - {event} - {tier}"


RACER_MEDAL_LOCATIONS = [racer_medal_location(e, t) for e in RACER_EVENTS for t in RACER_MEDAL_TIERS]
COP_MEDAL_LOCATIONS = [cop_medal_location(e, t) for e in COP_EVENTS for t in COP_MEDAL_TIERS]

RACER_LEVEL_LOCATIONS = [f"Racer Level {lvl} Reached" for lvl in range(1, MAX_LEVEL + 1)]
COP_LEVEL_LOCATIONS = [f"Cop Level {lvl} Reached" for lvl in range(1, MAX_LEVEL + 1)]

RACER_VEHICLE_LOCATIONS = [f"Racer Vehicle - {v} Unlocked" for v in RACER_VEHICLES]
COP_VEHICLE_LOCATIONS = [f"Cop Vehicle - {v} Unlocked" for v in COP_VEHICLES]

RACER_SERIES_LOCATIONS = [f"Racer Series - {c} Unlocked" for c in RACER_VEHICLES_BY_CLASS]
COP_SERIES_LOCATIONS = [f"Cop Series - {u} Unlocked" for u in COP_VEHICLES_BY_UNIT]

# New locations are always appended at the end to keep existing IDs stable.
ALL_LOCATIONS = (
    RACER_MEDAL_LOCATIONS + COP_MEDAL_LOCATIONS
    + RACER_LEVEL_LOCATIONS + COP_LEVEL_LOCATIONS
    + RACER_VEHICLE_LOCATIONS + COP_VEHICLE_LOCATIONS
    + RACER_SERIES_LOCATIONS + COP_SERIES_LOCATIONS
)

# Done by every new career before playing anything (rank 1, the first series and cars):
# not checks, the matching items are starting items instead.
FREE_AT_START_LOCATIONS = (
    {"Racer Level 1 Reached", "Cop Level 1 Reached"}
    | {f"Racer Series - {s} Unlocked" for s, e in RACER_SERIES_UNLOCK_EVENT.items() if e is None}
    | {f"Cop Series - {s} Unlocked" for s, e in COP_SERIES_UNLOCK_EVENT.items() if e is None}
    | {f"Racer Vehicle - {v} Unlocked" for v, c in RACER_VEHICLE_UNLOCKS.items() if c == 0}
    | {f"Cop Vehicle - {v} Unlocked" for v, c in COP_VEHICLE_UNLOCKS.items() if c == 0}
)
assert FREE_AT_START_LOCATIONS <= set(ALL_LOCATIONS)

GOAL_LOCATION = "Goal Completed"  # event location (no ID) holding the Victory item
