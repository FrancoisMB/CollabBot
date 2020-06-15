# -*- coding: utf-8 -*-
"""
@author: Francois

Bot collaborateurs parlementaires http://twitter.com/Collab_Bot

J'ai pas dit que c'était du beau code.
"""
from urllib.request import urlopen
from pathlib import Path
from datetime import datetime
import pandas, os, numpy as np, time, tweepy

# set le dossier de travail à l'endroit où se trouve 
path_wd = r"C:\Users\Francois\Documents\Code_Python\scrapper_collaborateurs_parlement"
os.chdir(path_wd)

# connexion twitter
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

send_to_twitter = 1
update_wbm_enabled = 1

#%%
if not os.path.exists('date_dernier_run.txt'):Path('date_dernier_run.txt').touch()
f = open("date_dernier_run.txt", "r")
date_dernier_run = f.read()
f.close()

print("date_dernier_run =",date_dernier_run)

def update_wayback_machine(url):
    if update_wbm_enabled:
        #["depute"]["url_an"]
        try:
            update_waybackmachine = urlopen("https://web.archive.org/save/"+url)
            if update_waybackmachine.getcode() == 200:
                print("Update wayback machine OK")
            else:
                print("L'update wayback machine n'a pas pu se faire pour l'url", url)
                print("error code =", update_waybackmachine.getcode())
            time.sleep(3)
            return update_waybackmachine     
        except Exception as err:
            print("Erreur update waybackmachine pour l'url", url)
            print(err)


def find_group_and_twitter(row): #on passe un df.loc[i]
    if row["fonction"] in ["député", "députée"]:
        for i in range(len(dict_d["deputes"])):
            if row["parlementaire"] == dict_d["deputes"][i]["depute"]["nom"]:
                result = {"groupe":dict_d["deputes"][i]["depute"]["groupe_sigle"], "twitter":dict_d["deputes"][i]["depute"]["twitter"]}
                try:
                    update_wayback_machine(dict_d["deputes"][i]["depute"]["url_an"])
                except:
                    pass
                return result
                break
    elif row["fonction"] in ["sénateur", "sénatrice"]:
        for i in range(len(dict_s["senateurs"])):
            if row["parlementaire"] == dict_s["senateurs"][i]["senateur"]["nom"]:
                result = {"groupe":dict_s["senateurs"][i]["senateur"]["groupe_sigle"], "twitter":dict_s["senateurs"][i]["senateur"]["twitter"]}
                try:
                    update_wayback_machine("http://www.senat.fr/trombinoaga/trombinoSE_" + dict_s["senateurs"][i]["senateur"]["id_institution"][-6:].upper() +".html")
                except:
                    pass
                return result
                break
    
# find_group_and_twitter(df_final.loc[1])["twitter"]
# find_group_and_twitter(df_final.loc[1])["groupe"]


def find_changes_collabs(df):
    dict_tweets = {}
    for i in range(len(df)):
        
        try:
            group_and_twitter = find_group_and_twitter(df_final.loc[i])
            groupe = group_and_twitter["groupe"]
            if group_and_twitter["twitter"] == "":
                twitter_account = ""
            else:
                twitter_account = " twitter.com/"+group_and_twitter["twitter"] # espace et @ au début pour que, dans le tweet, le @ soit pas collé au nom du parlementaire
            phrase2 = ""
            del group_and_twitter
        except:
            groupe, twitter_account = "", ""
            

        if df.loc[i]["add_or_del"] == "del":
            if df.loc[i]["sexe_collaborateur"] == "H":
                el2 = ", collaborateur de"
            else:
                el2 = ", collaboratrice de"
            phrase1 = "%s%s %s %s%s (%s %s), a cessé ses fonctions." % (df.loc[i]["collaborateur"], el2, df.loc[i]["titre"], df.loc[i]["parlementaire"], twitter_account, df.loc[i]["fonction"], groupe)
        elif df.loc[i]["add_or_del"] == "add":
            if df.loc[i]["sexe_collaborateur"] == "H":
                el1 = "a un nouveau collaborateur,"
            else:
                el1 = "a une nouvelle collaboratrice,"
                
            phrase1 = "%s %s%s (%s %s) %s %s." % (df.loc[i]["titre"], df.loc[i]["parlementaire"], twitter_account, df.loc[i]["fonction"], groupe, el1, df.loc[i]["collaborateur"])
            try:
                retour_requete_twitter_probable = api.search_users(df.loc[i]["prénom_collaborateur"]+" "+df.loc[i]["nom_collaborateur"])
                phrase2 = "Peut-être est-ce twitter.com/%s ?" % (retour_requete_twitter_probable[0].screen_name)
            except Exception as err:
                print("Pas réussi à trouver un twitter de collaborateur")
                print("Print de retour_requete_twitter_probable :", retour_requete_twitter_probable)
                print("Print de l'erreur : ")
                print(err)
        dict_tweets[df.loc[i]["collaborateur"]] = {}
        dict_tweets[df.loc[i]["collaborateur"]]["phrase1"] = phrase1
        if not phrase2 == "": dict_tweets[df.loc[i]["collaborateur"]]["phrase2"] = phrase2
        dict_tweets[df.loc[i]["collaborateur"]]["add_or_del"] = df.loc[i]["add_or_del"]

    return dict_tweets

if not date_dernier_run == datetime.today().strftime('%Y-%m-%d'):

    # les json qui permettent de trouver les groupes des parlementaires et leurs twitters
    import json
    url_d = "http://www.nosdeputes.fr/deputes/json"
    url_s = "http://www.nossenateurs.fr/senateurs/json"
    json_raw_d = urlopen(url_d).read()
    json_raw_s = urlopen(url_s).read()
    dict_d = json.loads(json_raw_d)
    dict_s = json.loads(json_raw_s)
    del json_raw_d, json_raw_s

    # créé des fichiers vides s'ils n'existent pas
    if not os.path.exists('deputes_j_minus_three.csv'):Path('deputes_j_minus_three.csv').touch()
    if not os.path.exists('senateurs_j_minus_three.csv'):Path('senateurs_j_minus_three.csv').touch()
    if not os.path.exists('deputes_j_minus_two.csv'):Path('deputes_j_minus_two.csv').touch()
    if not os.path.exists('senateurs_j_minus_two.csv'):Path('senateurs_j_minus_two.csv').touch()
    if not os.path.exists('deputes_yesterday.csv'):Path('deputes_yesterday.csv').touch()
    if not os.path.exists('senateurs_yesterday.csv'):Path('senateurs_yesterday.csv').touch()
        
    # décale d'un jour tous les fichiers
    os.replace("deputes_j_minus_two.csv", "deputes_j_minus_three.csv")
    os.replace("deputes_yesterday.csv", "deputes_j_minus_two.csv")
    os.replace("deputes_today.csv", "deputes_yesterday.csv")
    
    os.replace("senateurs_j_minus_two.csv", "senateurs_j_minus_three.csv")
    os.replace("senateurs_yesterday.csv", "senateurs_j_minus_two.csv")
    os.replace("senateurs_today.csv", "senateurs_yesterday.csv")
    if os.path.exists('rollback_effectue.txt'):os.remove("rollback_effectue.txt")

    # fetch les deux csv du jour et les load en dt
    df_d = pandas.read_csv("https://raw.githubusercontent.com/regardscitoyens/Collaborateurs-Parlement/master/data/liste_deputes_collaborateurs.csv")
    df_s = pandas.read_csv("https://raw.githubusercontent.com/regardscitoyens/Collaborateurs-Parlement/master/data/liste_collaborateurs_senateurs2.csv")
    
    # les enregistre en _today
    df_d.to_csv('deputes_today.csv', encoding="utf-8", index = False)
    df_s.to_csv('senateurs_today.csv', encoding="utf-8", index = False)
    
    f = open("date_dernier_run.txt","w")
    f.write(datetime.today().strftime('%Y-%m-%d'))
    f.close()
    print("dl et save des files ok")
    #%%
    # on les reload en mémoire pour faire la diff
    df_d = pandas.read_csv('deputes_today.csv', encoding="utf-8")
    df_s = pandas.read_csv('senateurs_today.csv', encoding="utf-8")
    
    # on load ceux d'hier en mémoire pour faire la diff
    df_y_d = pandas.read_csv('deputes_yesterday.csv', encoding="utf-8")
    df_y_s = pandas.read_csv('senateurs_yesterday.csv', encoding="utf-8")
    
    # rows uniques
    
    df_diff_d = pandas.concat([df_d, df_y_d]).drop_duplicates(keep = False)
    df_diff_s = pandas.concat([df_s, df_y_s]).drop_duplicates(keep = False)
    
    # check si c'est ajout ou retrait
    temp = pandas.concat([df_d, df_diff_d])
    df_added_d = temp[temp.duplicated(keep="first")].reset_index()
    temp = pandas.concat([df_y_d, df_diff_d])
    df_deleted_d = temp[temp.duplicated(keep="first")].reset_index()
    
    temp = pandas.concat([df_s, df_diff_s])
    df_added_s = temp[temp.duplicated(keep="first")].reset_index()
    temp = pandas.concat([df_y_s, df_diff_s])
    df_deleted_s = temp[temp.duplicated(keep="first")].reset_index()
    
    # on ajoute les colonnes qu'il faut pour la fonction
    df_added_d['fonction'] = np.where(df_added_d['sexe_parlementaire']=='H', 'député', 'députée')
    df_deleted_d['fonction'] = np.where(df_deleted_d['sexe_parlementaire']=='H', 'député', 'députée')
    df_added_s['fonction'] = np.where(df_added_s['sexe_parlementaire']=='H', 'sénateur', 'sénatrice')
    df_deleted_s['fonction'] = np.where(df_deleted_s['sexe_parlementaire']=='H', 'sénateur', 'sénatrice')
    
    # et pour le titre
    df_added_d['titre'] = np.where(df_added_d['sexe_parlementaire']=='H', 'M.', 'Mme')
    df_deleted_d['titre'] = np.where(df_deleted_d['sexe_parlementaire']=='H', 'M.', 'Mme')
    df_added_s['titre'] = np.where(df_added_s['sexe_parlementaire']=='H', 'M.', 'Mme')
    df_deleted_s['titre'] = np.where(df_deleted_s['sexe_parlementaire']=='H', 'M.', 'Mme')
    
    # on précise si c'est un arrivant ou un partant
    df_added_d['add_or_del'] = 'add'
    df_deleted_d['add_or_del'] = 'del'
    df_added_s['add_or_del'] = 'add'
    df_deleted_s['add_or_del'] = 'del'
    
    df_final = pandas.concat([df_added_d, df_deleted_d, df_added_s, df_deleted_s]).reset_index()
    # trie les départs avant les arrivées
    df_final = df_final.sort_values(by='add_or_del', ascending=False)
    #df_deleted_d.empty
    
    dict_phrases_a_tweeter = find_changes_collabs(df_final)
    
    if send_to_twitter == True:
        for collab in dict_phrases_a_tweeter.values():
            print(collab["phrase1"])
            # ici ou dans find_changes_collabs(), ajouter IF SOC, ça l'écrit dans un fichier par exemple
            if len(collab["phrase1"]) >= 260 or len(collab["phrase1"]) >= 260 :
                raise ValueError("TWEET TROP LONG : Plus de 260 signes dans le tweet, il y a un risque qu'avec les metadata (le @compte au début) le tweet dépasse les 280. Faire un rollback, et il est temps de gérer ce cornercase dans le code.")
                break
            try:
                tweeted = api.update_status(collab["phrase1"])
            except Exception as err:
                print("Erreur lors du tweet de", collab["phrase1"])
                print(err)
                continue
            time.sleep(5)
            if collab.get("phrase2"):
                print(collab["phrase2"])
                try:
                    api.update_status(collab["phrase2"], in_reply_to_status_id = tweeted.id_str, auto_populate_reply_metadata = True)               
                except Exception as err:
                    print("Erreur lors du tweet de", collab["phrase2"])
                    print(err)
            time.sleep(10)
    else: # afficher dans le stdout sans poster sur twitter
        for collab in dict_phrases_a_tweeter.values():
            print(collab["phrase1"])
            if collab.get("phrase2"):print(collab["phrase2"])


else:
    print("Script already ran today")


def rollback():
    os.replace("deputes_yesterday.csv", "deputes_today.csv")
    os.replace("deputes_j_minus_two.csv", "deputes_yesterday.csv")
    os.replace("deputes_j_minus_three.csv", "deputes_j_minus_two.csv")

    os.replace("senateurs_yesterday.csv", "senateurs_today.csv")
    os.replace("senateurs_j_minus_two.csv", "senateurs_yesterday.csv")
    os.replace("senateurs_j_minus_three.csv", "senateurs_j_minus_two.csv")
    os.replace("date_dernier_run.txt","rollback_effectue.txt")
 
