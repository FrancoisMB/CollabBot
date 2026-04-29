# CollabBot

Un bot twitter codé entre midi et deux qui poste les arrivées et départs de collaborateurs parlementaires sur [https://bsky.app/profile/collab-bot.bsky.social](https://bsky.app/profile/collab-bot.bsky.social).

v2 : possible grace à Regards Citoyens : https://github.com/regardscitoyens/Collaborateurs-Parlement

v3 : adaptation à l'arrache suite à l'absence de reprise de Regards citoyens, à partir des fichiers open data de l'AN sur data.assemblee-nationale.fr, et de cette page du Sénat https://www.senat.fr/trombinoaga/trombinoSR_1.html

v4 : la page du Sénat ci-dessus n'intègrait pas tous les collaborateurs. Le suivi des collaborateurs du Sénat se fait donc désormais via les pages https://www.senat.fr/pubagas/liste_senateurs_collaborateurs.pdf et https://www.senat.fr/pubagas/liste_collaborateurs_senateurs2.pdf. Lire les warnings ci-dessous
v4.1 : passage de twitter (poster via l'API est devenu payant) à bluesky

⚠️ : Ce bot est "relativement" fiable, mais il peut produire des erreurs. C'est un outil que je fournis gratuitement, pas un service que je garantis. Ne faites confiance à ses infos qu'à vos risques et périls.

⚠️ : Le code utilise une reconnaissance optique des tableaux des PDF du Sénat, ce qui peut produire des erreurs. Pour les éviter, il faudrait que le Sénat publie ces tableaux dans à peu près n'importe quel autre format que pdf (csv idéalement). N'hésitez pas à leur envoyer un mail pour le leur demander.

FAQ :
- Et les collaborateurs du Parlement européen ?
-> Il faudrait un document ou une page qui les regroupe tous en un seul endroit, ce qui n'existe à ma connaissance pas (n'hésitez pas à envoyer des mails aux webmasters du PE pour qu'ils créent ça). A défaut, il faudrait parcourir chaque jour les pages des 81 eurodéputés français (ou des 720 eurodéputés pour tous les faire), ce qui est faisable, mais lourd. Je le ferait peut être un jour, mais ce n'est pas prévu dans un futur proche.
- Je suis un des collaborateurs concerné et je ne souhaite pas figurer sur ce bot. 
-> Ce bot ne fait que reposter des données déjà publiques (et par ailleurs d'intérêt public, à mon avis) - données qui sont par ailleurs sauvegardées régulièrement sur wayback machine. Autrement dit, je suis le mauvais interlocuteur, et je ne compte pas gérer tous les cas individuels : il ne fallait pas travailler pour quelqu'un pour qui vous n'assumez plus d'avoir travaillé...!
- Le bot a fait une erreur !
-> Soit l'erreur vient des fichiers publiés par l'AN et le Sénat (qui, par exemple, délistent les collaborateurs lorsqu'ils prennent des congés sans solde, notamment pour faire campagne, mais les "réembauchent" pour un jour lors de l'établissement des fiches de paie). Dans ce cas, le bot la reproduira forcément, et je ne corrigerai pas l'erreur, désolé, je n'ai pas vocation à enquêter sur la fiabilité des données publiques...
  Soit l'erreur est produite par le code, le plus probable étant à cause de l'imparfaite reconnaissance optique des fichiers du Sénat (cf le second warning quelques lignes plus haut). Je ne consens à corriger que les erreurs les plus substantielles (si le bot dit que vous avez travaillé pour un élu d'un autre camp politique que le votre, par exemple), auquel cas vous pouvez m'envoyer un message privé sur bluesky (malauss.bsky.social).
- Je suis journaliste et je voudrais savoir...
-> Envoyez moi un message privé.
