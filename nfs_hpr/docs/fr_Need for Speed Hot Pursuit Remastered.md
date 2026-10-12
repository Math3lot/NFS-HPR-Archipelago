# Need for Speed Hot Pursuit Remastered

## Que fait la randomisation dans ce jeu ?

Chaque épreuve pilote et police doit être débloquée par un objet avant de pouvoir être jouée.
Les séries (de Sports à Hyper, de Traffic Police à Special Response), les voitures et les
améliorations d'armes progressives sont aussi des objets. Les médailles (Bronze/Argent/Or et
Pass/Merit/Distinction), les niveaux pilote et police de 1 à 20, et chaque série et voiture
débloquée en jeu sont des checks.

Les épreuves, les voitures et séries, les armes et les checks de niveau peuvent chacun rester
comme dans le jeu normal avec les options `randomize_events`, `randomize_vehicles`,
`randomize_weapons` et `randomize_levels`.

## Quel est l'objectif ?

Selon vos options : obtenir toutes les meilleures médailles, terminer Seacrest Tour et End Of
The Line, ou atteindre le niveau 20 dans les deux camps.

## Quels autres objets existe-t-il ?

Des Bounty Bundles et des Nitro Refills comme remplissage, plus des pièges : Flat Tire, EMP
Impact, Speed Limiter, Roadblock Deployed, System Jammed et Reversed Steering.
`trap_percentage` règle la part de remplissage remplacée par des pièges ; chaque piège et chaque
type de remplissage a son propre poids (0 le désactive).

## Combien de bounty la logique attend-elle ?

`bounty_multiplier` (Bounty Expectation) : 100 correspond au rythme de bounty du jeu normal,
suffisant pour tout débloquer. Une valeur plus haute attend plus de bounty par épreuve : les
niveaux et les voitures à bounty entrent dans la logique après moins d'épreuves.
