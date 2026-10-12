# Guide d'installation de Need for Speed Hot Pursuit Remastered

## Logiciels requis

- Need for Speed Hot Pursuit Remastered (PC, Steam ou EA app)
- Archipelago 0.6.4 ou plus récent

## Installation

1. Mettez `nfs_hpr.apworld` dans le dossier `custom_worlds` de votre installation Archipelago
   (en général `C:\ProgramData\Archipelago\custom_worlds`).
2. Créez votre YAML avec l'**Options Creator** de l'Archipelago Launcher.
3. Remplissez votre nom de joueur et vos options, puis générez comme d'habitude.

## Avant de jouer : les sauvegardes

Le jeu n'a qu'une seule carrière, donc le client garde une sauvegarde par seed, dans le dossier
`nfs_hpr_saves` d'Archipelago.

**Désactivez d'abord la sauvegarde dans le cloud** pour le jeu : dans l'EA app (propriétés du
jeu), version Steam comprise (le Steam Cloud n'intervient pas).
Sinon votre ancienne carrière est retéléchargée par-dessus la sauvegarde échangée.

Jeu fermé, dans le client :
- `/use_save new` met de côté votre sauvegarde actuelle (la première fois sous le nom
  `original`) et vide le dossier de sauvegarde du jeu : le jeu démarre une nouvelle carrière,
  qui appartient à cette seed.
- `/use_save current` joue cette seed sur la sauvegarde déjà présente dans le jeu (sa
  progression compte comme des checks).
- `/use_save NOM` remet une sauvegarde stockée (par exemple `/use_save original`).
- `/saves` liste les sauvegardes stockées et indique celle qui est dans le jeu.

Tant que la sauvegarde du jeu n'appartient pas à la seed à laquelle vous êtes connecté, le
client n'envoie aucun check : la progression d'une autre carrière n'est jamais envoyée par
erreur. Quand vous vous connectez à une seed dont la sauvegarde est stockée et que le jeu est
fermé, le client la remet tout seul (après avoir mis de côté celle qui était là). Rien n'est
supprimé sans copie.

## Jouer

1. Dans l'Archipelago Launcher, ouvrez **Need for Speed Hot Pursuit Remastered Client** et
   connectez-vous avec votre nom de joueur, **avant** de charger votre carrière.
2. Lancez le jeu et chargez votre carrière.
3. Jouez : à chaque sauvegarde du jeu (après chaque épreuve), le client lit la sauvegarde et
   envoie vos nouvelles médailles, niveaux, voitures et séries comme checks.

Le client trouve la sauvegarde tout seul dans
`Documents\Criterion Games\Need for Speed(TM) Hot Pursuit Remastered\Save`.
S'il n'y arrive pas, utilisez `/save <chemin complet du fichier .NFS11Save>`.
`/checks` liste les checks trouvés dans la sauvegarde.

Le client lit et écrit dans la mémoire du jeu : lancez-le en administrateur s'il indique qu'il
ne peut pas ouvrir le processus du jeu.

## Épreuves et voitures

Le jeu suit Archipelago : les épreuves et voitures que vous n'avez pas reçues sont retirées du
jeu (absentes de la carte et du garage). Celles que vous recevez sont débloquées par le client,
quelles que soient les conditions du jeu (bounty, épreuves précédentes). Les objets reçus en
cours de partie apparaissent une fois votre prochaine épreuve terminée (ou lancée puis quittée),
car le jeu met ses déblocages à jour à ce moment-là. La logique en tient compte.

Épreuves verrouillées : si vous lancez une épreuve qu'Archipelago n'a pas débloquée (objet de
l'épreuve, ou, avec les voitures randomisées, objet de sa série ou de la voiture choisie non
reçu), après quelques secondes (le temps que le départ scripté se termine) le client ralentit
votre voiture au pas et vous dit ce qui manque ; déconnecter le client la libère. Quittez
l'épreuve depuis le menu pause, ou relancez-la avec une autre voiture. Chaque épreuve demande
une de ses propres voitures (la liste du jeu), épreuves Preview et Gauntlet comprises : il vous
faut la voiture qu'elles prêtent.

Random Start (option) : chaque camp commence avec une voiture au hasard, une épreuve au hasard
qu'elle peut conduire et la série de cette épreuve, plus d'autres épreuves de cette série avec
Starting Events.

Tracker : l'onglet **Tracker** du client montre, pour chaque série pilote et police, si la
série est débloquée et quelles voitures et épreuves vous avez reçues (vert : débloqué, gris :
verrouillé). `/tracker` (ou `/tracker racer`, `/tracker cop`) affiche la même chose dans le
journal.

## Objets

Les Bounty Bundles reçus sont ajoutés à la bounty du jeu pendant qu'il tourne (au camp qui est
en retard). Le client les rajoute à chaque lancement du jeu, car la sauvegarde ne garde que la
bounty gagnée en épreuve.

Les Nitro Refills reçus attendent que vous rouliez dans une épreuve (la jauge bouge), puis
remplissent la jauge de nitro.

Les pièges vous frappent après un avertissement de 5 secondes pendant que vous roulez dans une
épreuve (`/trap_delay` change ce délai) :
- **Roadblock Deployed** arrête net votre voiture.
- **Speed Limiter** limite votre vitesse à 72 km/h pendant 10 secondes.
- **System Jammed** vide votre nitro pendant 10 secondes.
- **EMP Impact** abîme votre voiture (+25 %), lui retire l'essentiel de sa vitesse et la secoue.
- **Flat Tire** abîme votre voiture (+15 %), la fait partir en tête-à-queue ou déraper et vous
  ralentit pendant 8 secondes (une voiture au maximum de dégâts est détruite au prochain choc).
- **Reversed Steering** inverse votre direction pendant 10 secondes.

Les pièges à durée se mettent en pause avec le jeu.

Armes progressives (quand les armes sont randomisées), appliquées au début de chaque épreuve,
pour votre camp seulement : une arme non reçue a 0 charge ; le premier objet donne les charges
normales de l'épreuve, chaque objet suivant +1 charge. Les niveaux d'armes du jeu continuent de
monter avec les tirs réussis. Quand vous n'avez aucune charge dans une épreuve, l'arme qu'une
épreuve d'introduction tient prête vous est retirée aussi.
