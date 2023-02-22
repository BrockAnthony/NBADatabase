
"""
4/15/22
CS 3200 Project
"""

import pymysql
from getpass import getpass
import sys

from create_list import *
from edit_list import *
from view_lists import *


def prompt_login():

    username = input('\nEnter mysql username: ')
    password = getpass('Enter mysql password: ')
    return username, password

def connect_to_mysql(username, password):
    """
    Parameters
    ----------
    username : string
    password : string

    Returns
    -------
    cnx : connection

    Function:
        connect to database from mysql
    """
    
    cnx = pymysql.connect(host='localhost', user=username, password=password, 
                          db='nba_db', charset='utf8mb4', 
                          cursorclass=pymysql.cursors.DictCursor)
    
    return cnx

    
def login_prompt():
    
    print("\nWelcome to NBA Stats Database!")

    prompt = "What would you like to do?\n"
    prompt += "1. Login / Create an Account.\n"
    prompt += "2. Quit Program"

    print(prompt)
    answer = input('-> ')
    print()
    
    return answer

def check_user(username, cnx):
    
    """
    see if this username already exists
    """
    
    cur = cnx.cursor()
    user_select = "select user_name from users"
    cur.execute(user_select)
    users = cur.fetchall()
    cur.close()
    
    exists = False
    for d in users:
        
        if username in d.values():
            exists = True
            
    return exists
    
def get_user_id(user, cnx):
    
    """
    create new account / login to existing one
    - return user_id
    """
    
    
    exists = check_user(user, cnx)

    # create new user
    if exists == False:
        query = "INSERT INTO users(user_name) VALUES(%s)"
        
        cur = cnx.cursor()
        cur.execute(query, (user))
        cur.close()
        cnx.commit()
        print("\nNew Account Successfully Created")
        
    # login
    else:
        print("Logging in to Existing Account")
    
    # get user id
    cur = cnx.cursor()
    user_id_select = "select get_user_id(%s)"
    cur.execute(user_id_select, (user,))
    result = cur.fetchone()
    cur.close()

    return list(result.items())[0][1]

        
def menu_prompt(cnx):
    
    prompt = '\nWhat would you like to do?\n\n'
    prompt += '1. Create New Favorites List\n'
    prompt += '2. Update Favorites List\n'
    prompt += '3. View Favorites List\n'    
    prompt += '4. Logout\n'
    prompt += 'Please enter the number of the menu option you wish to complete: '

    print(prompt)
    answer = input('-> ')
    return answer

def main():
    
    # connect to db
    try:
        sql_user, sql_pass = prompt_login()
        print("")
        cnx = connect_to_mysql(sql_user, sql_pass)
    except:
        print('Invalid credentials.')
        return 0
    
    
    login_ans = login_prompt()
    
    # login to database username
    while login_ans != None:
        if login_ans == "1":
            print("Please enter your pre-existing username or your new one.")
            print("(not case sensitive)")
            user_input = input("Username: ").lower()
            print()
            
            user_id = get_user_id(user_input, cnx)
            break
        elif login_ans == "2":
            sys.exit()
            break
        else:
            print("Improper Input. Please try again.")
            login_ans = login_prompt()
           
    # main menu
    menu_ans = ""
    while menu_ans != None:
        menu_ans = menu_prompt(cnx)
        if menu_ans == "1":
            create_list(cnx, user_id)
        elif menu_ans == "2":
            lsts = edit_list(cnx, user_id)
        elif menu_ans == "3":
            lsts = view_lists(cnx, user_id)
        elif menu_ans == "4":
            sys.exit()
            
            

if __name__ == "__main__":
    main()