
"""
Functions that Create Favorites List
"""

def check_exists(cnx, user_id, lst_name, stmt):
     
    """
    see if list name for that type already exists for the user
    """
    cur = cnx.cursor()
    query = "SELECT" + stmt
    cur.execute(query, (user_id, lst_name))
    results = cur.fetchall()
    cur.close()
        
    if len(results) != 0:
        return True
    else:
        return False
    

def create_type_prompt():
    prompt = "\nWould you like to create a player, team, or game list?\n"
    prompt += "1. Create Player List\n"
    prompt += "2. Create Team List\n"
    prompt += "3. Create Game List"

    print(prompt)
    answer = input('-> ')
   
    return answer
 
def name_input_prompt():
    print("\nCreating New Favorites List.\n")
    print("Please input the name for your new list")
    lst_name = input("Name: ")
    
    return lst_name


def get_entries(cnx, user_id, lst_name, type_ans):
    
    """
    get all entries on a specific list
    """
    
    proc = ""
    
    if type_ans == "1":
        proc = "get_player_entries"
    elif type_ans == "2":
        proc = "get_team_entries"
    elif type_ans == "3":
        proc = "get_game_entries"
        
    cur = cnx.cursor()
    cur.callproc(proc, (user_id, lst_name))
    results = cur.fetchall()
    cur.close()
    cnx.commit()

    
    return results

def player_insert(cnx, user_id, lst_name):
    print("\nWhat player would you like to add?")
    player_input = input("Player Name (first and last): ").lower()
    team_input = input("Plays for (i.e. Celtics, Nets, etc.): ").lower()
    
    try:
        cur = cnx.cursor()
        cur.callproc("insert_player_list", (user_id, lst_name, player_input, team_input))
        cur.close()
        cnx.commit()
        print("\nNew Player Successfully Added\n")
    except cnx.Error as err:
        print()
        print(format(err))
    

def team_insert(cnx, user_id,lst_name):
   
    print("\nWhat team would you like to add?")
    team_input = input("Team Name (i.e. Celtics, Nets, etc.): ").lower()
    try:
        cur = cnx.cursor()
        cur.callproc("insert_team_list", (user_id, lst_name, team_input))
        cur.close()
        cnx.commit()
        print("\nNew Team Successfully Added\n")
    except cnx.Error as err:
        print()
        print(format(err))
    
def game_insert(cnx, user_id, lst_name):
    print("\nWhat game would you like to add?")
    home_input = input("Home Team (i.e. Celtics, Nets, etc.): ").lower()
    away_input = input("Away Team (i.e. Celtics, Nets, etc.): ").lower()
    date_input = input("Date of Game (YYYY-MM-DD): ")

    try:
        cur = cnx.cursor()
        cur.callproc("insert_game_list", (user_id, lst_name, home_input, 
                                          away_input, date_input))
        cur.close()
        cnx.commit()
        print("\nNew Game Successfully Added\\n")
    except cnx.Error as err:
        print()
        if err.args[0] == 1292:
            print("ERROR: Improper Date Format")
            return 0
        else:
            print(format(err))
            return 0
        

def add_to_list(cnx, user_id, lst_name, type_ans):
    
    # while they continue to want toa dd
    i = None
    while i != "n":
        
        entries = get_entries(cnx, user_id, lst_name, type_ans)
        print("\nCurrent Entries: ")
        for entry in entries:
            print(entry)        
        prompt = "\nWould you like to add to your list?\n"
        prompt += "[y/n]\n"
        print(prompt)
        
        i = input("-> ")
        if i == "y":
            if type_ans == "1":
                player_insert(cnx, user_id, lst_name)
            elif type_ans == "2":
                team_insert(cnx, user_id, lst_name)
            elif type_ans == "3":
                game_insert(cnx, user_id, lst_name)
                

def create_list(cnx, user_id):
    type_ans = create_type_prompt()
    
    exists_error = "You already have a list with that name.", \
          "Please try again.\n"
          

    while type_ans != None:
        
        # create player list
        if type_ans == "1":
            lst_name = name_input_prompt()
            check_stmt = " player_list_name FROM player_list WHERE user_id =" + \
                " %s AND player_list_name = %s"
            exists = check_exists(cnx, user_id, lst_name, check_stmt)
            if exists == True:
                print(exists_error)
            else:
                player_insert(cnx, user_id, lst_name)
                add_to_list(cnx, user_id, lst_name, type_ans)
                break
            
        # create team list
        elif type_ans == "2":
            lst_name = name_input_prompt()
            check_stmt = " team_list_name FROM team_list WHERE user_id = %s" + \
                " AND team_list_name = %s"
            exists = check_exists(cnx, user_id, lst_name, check_stmt)
            if exists == True:
                print(exists_error)
            else:
                team_insert(cnx, user_id, lst_name)
                add_to_list(cnx, user_id, lst_name, type_ans)
                break
     
        # create game list
        elif type_ans == "3":
            lst_name = name_input_prompt()
            check_stmt = " game_list_name FROM game_list WHERE user_id = %s" + \
                " AND game_list_name = %s"
            exists = check_exists(cnx, user_id, lst_name, check_stmt)
            if exists == True:
                print(exists_error)
            else:
                game_insert(cnx, user_id, lst_name)
                add_to_list(cnx, user_id, lst_name, type_ans)
                break
        else:
            print("Incorrect Input. Please try again.")
            type_ans = create_type_prompt()

    
