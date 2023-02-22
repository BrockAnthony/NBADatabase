
from create_list import *
from edit_list import *
import datetime

def get_list_info(cnx, user_id, lst_name, entry_id, type_ans):
    
    # display desired info for list entry (type dependent)
    
    proc = ""

    if type_ans == "1":
        proc = "view_player_list"
    elif type_ans == "2":
        proc = "view_team_list"
    elif type_ans == "3":
        proc = "view_game_list"

    cur = cnx.cursor()
    cur.callproc(proc, (entry_id,))
    result = cur.fetchone()
    cur.close()
    cnx.commit()
    
    print("\n")
    print("Stats:")
    print(result)
    
def view_boxscore(cnx, entry_id):
    
    # view box score stats for a chosen game
    
    cur = cnx.cursor()
    cur.callproc("view_boxscore", (entry_id,))
    results = cur.fetchall()
    cur.close()
    cnx.commit()
    
    print("Boxscore: ")
    for result in results:
        print(result)
        print()

        
def lists(cnx, user_id, lst_name, type_ans):
   
    id_str = ""
    
    if type_ans == "1":
        id_str = "player_id"
    elif type_ans == "2":
        id_str = "team_name"
    elif type_ans == "3":
        id_str = "game_id"
    
    
    entry_ans = None
    box_ans = None
    while entry_ans != "n":
        entries = get_entries(cnx, user_id, lst_name, type_ans)
        
        # make sure list types aren't empty
        if len(entries) == 0:
            break
        else:
        
            print("\nEntries for", lst_name + ":")
            for entry in entries:
                print(entry)
                
            prompt = "\nWould you like to view data from an entry on your list?\n"
            prompt += "[y/n]"
            print(prompt)
            
            entry_ans = input("-> ")
            if entry_ans == "y":
                print("\nPlease enter the", id_str, "of the entry you would like to view.")
                entry_id = input("-> ")
                
                # int for player and game lists for id matching
                if type_ans == "1" or type_ans == "3":
                    try:
                        entry_id = int(entry_id)
                    except ValueError:
                        print("\nImproper Input. (must be a number)")
                        continue
                elif type_ans == "2":
                    entry_id = entry_id.lower()
                       
                error = True
                
                # view entry infor
                for entry in entries:
                    if entry_id in entry.values():
                        get_list_info(cnx, user_id, lst_name, entry_id, type_ans)
                        error = False
                if error == True:
                    print("\nERROR: you do not have any entry with that", id_str, 
                              "in your list.")
                    
                # box score option
                if type_ans == "3" and error == False:                     
                    while box_ans != "n":
                        prompt = "Would you like to view the box score for this game?\n"
                        prompt += "[y/n]"
                        print(prompt)
                            
                        box_ans = input("-> ")
                        if box_ans == "y":
                            view_boxscore(cnx, entry_id)
                            break
                        else:
                            print("\nImproper Input. Please try again.")
                        
            elif entry_ans != "n":
                print("\nImproper Input. Please try again.")


def view_lists(cnx, user_id):
    type_ans, lst_names = type_prompt(cnx, user_id)
    lst_name = pick_list(lst_names)
    lists(cnx, user_id, lst_name, type_ans)


    
    