
from create_list import *

 
def get_lists(cnx, user_id, proc):
    
    # get the names of all lists of the chosen type
    
    cur = cnx.cursor()
    cur.callproc(proc, (user_id,))
    results = cur.fetchall()
    cur.close()
    cnx.commit()
    
    
    lst_name = []
    for i in results:
        for val in i.values():
            lst_name.append(val)    
    return lst_name
    
def delete_list(cnx, user_id, lst_name, proc):
    
    cur = cnx.cursor()
    cur.callproc(proc, (user_id, lst_name))
    cur.close()
    cnx.commit()


    
def delete_entries(cnx, user_id, lst_name, type_ans):
    
    entry_proc = ""
    delete_proc = ""
    id_str = ""
    
    if type_ans == "1":
        entry_proc = "get_player_entries"
        delete_proc = "delete_from_player_list"
        id_str = "player_id"
    elif type_ans == "2":
        entry_proc = "get_team_entries"
        delete_proc = "delete_from_team_list"
        id_str = "team_name"
    elif type_ans == "3":
        entry_proc = "get_game_entries"
        delete_proc = "delete_from_game_list"
        id_str = "game_id"
    
    
    
    i = None
    while i != "n":
        entries = get_entries(cnx, user_id, lst_name, type_ans)
                
        # check to see if any entries left on list
        if len(entries) == 0:
            print("Last Entry Deleted. List Deleted.")
            break
        
        # list of entry names
        entry_names = []
        for dct in entries:
            entry = dct[id_str]
            entry_names.append(entry)
                
        
        print("\nCurrent Entries: ")
        for entry in entries:
            print(entry)
            
        prompt = "\nWould you like to delete entries from your list?\n"
        prompt += "[y/n]"
        print(prompt)
        
        i = input("-> ")
        
        if i == "y":
            print("\nPlease enter the", id_str, "of the entry you would like to delete.")
            del_id = input("-> ")
            print()
            
            # change input to int so ids can match (only for player and game)
            if type_ans == "1" or type_ans == "3":
                try:
                    del_id = int(del_id)
                except ValueError:
                    print("Improper Input. (must be a number)")
                    continue
                
            elif type_ans == "2":
                del_id = del_id.lower()
                
            # delete entry if it exists in the list
            if del_id in entry_names:
                cur = cnx.cursor()
                cur.callproc(delete_proc, (user_id, lst_name, del_id))
                results = cur.fetchall()
                cur.close()
                cnx.commit()
                print("Entry deleted from list.")            
                
            else:
                print("ERROR: you do not have any entry with that", id_str, 
                      "in your list")
                
            
def update_list_names(cnx, user_id, lst_name, type_ans, lst_names):
    
    update_proc = ""
    
    if type_ans == "1":
        update_proc = "update_player_list"
    elif type_ans == "2":
        update_proc = "update_team_list"
    elif type_ans == "3":
        update_proc = "update_game_list"
    
    
    new_name = ""
    
    # change name of list 
    while new_name != None:
        print("What would you like to change the name to?")
        new_name = input("New Name: ")
        
        # cannot already have type list with that name
        if new_name not in lst_names:
            cur = cnx.cursor()
            cur.callproc(update_proc, (user_id, lst_name, new_name))
            cur.close()
            cnx.commit()
            break
        else:
            print("\nThat name is already used. Please try again.\n")
            
    
    
def type_prompt(cnx, user_id):
    type_ans = 0
    while type_ans != None:
        prompt = "\nWhich list would you like to chose?\n"
        prompt += "1. Player Lists\n"
        prompt += "2. Team Lists\n"
        prompt += "3. Game Lists"
        print(prompt)
        
        type_ans = input("-> ")
        print()
    
        if type_ans == "1":
            lst_names = get_lists(cnx, user_id, "get_player_lists")
            break
        elif type_ans == "2":
            lst_names = get_lists(cnx, user_id, "get_team_lists")
            break
        elif type_ans == "3":
            lst_names = get_lists(cnx, user_id, "get_game_lists")
            break
        else:
            print("Incorrect Input. Please try again.")
    
    return type_ans, lst_names
    
def pick_list(lst_names):
    
    lst_name = ""
    
    # if they pick a list type with 0 lists
    if len(lst_names) == 0:
        print("\nYou have no current lists of this type.")   
        return None
    else:
        while lst_name != None:
            print("Which list would you like to chose?" )
            print("list names: ", lst_names)
            lst_name = input("List Name: ").lower()
            
            if lst_name not in lst_names:
                print("That list does not exist. Please try again.\n")
            else:
                break
            
    return lst_name

def edit_list(cnx, user_id):
    
    type_ans, lst_names = type_prompt(cnx, user_id)
    lst_name = pick_list(lst_names)
    
    if lst_name == None:
        return 0
    
    action_ans = ""
    while action_ans != None:
        if action_ans == None:
            break
        
        prompt = "\nWhat would you like to do with " + str(lst_name) + "?\n"
        prompt += "1. Add to List\n"
        prompt += "2. Delete Entry on List\n"
        prompt += "3. Delete List\n"
        prompt += "4. Change Name of List"
        print(prompt)
        
        action_ans = input("-> ")
        print()
        
        
        # actions based on menu answer
        if action_ans == "1":
            add_to_list(cnx, user_id, lst_name, type_ans)
            break
        elif action_ans == "2":
            delete_entries(cnx, user_id, lst_name, type_ans)
            break
        elif action_ans == "3":
            if type_ans == "1":
                delete_list(cnx, user_id, lst_name, "delete_player_list")    
            elif type_ans == "2":
                delete_list(cnx, user_id, lst_name, "delete_team_list")
            elif type_ans == "3":
                delete_list(cnx, user_id, lst_name, "delete_game_list")
            break
        elif action_ans == "4":
            update_list_names(cnx, user_id, lst_name, type_ans, lst_names)
            break
        else:
            print("Improper Input. Please try again.")
            
