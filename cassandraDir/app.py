#!/usr/bin/env python3
import logging
import os
import uuid
from cassandra.cluster import Cluster
import model
import subprocess


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('investments.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'cassandrafinal')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

# Function to display the main menu options
def print_menu():
    print('\n')
    mm_options = {
        0: "Populate data",
        1: "User Activity",
        2: "Engagement Rate",
        3: "Interaction Duration",
        4: "Trending Content",
        5: "User Sessions",
        6: "Inactive User Data",
        7: "Engagement by Time",
        8: "Print Users",
        9: "Print Posts",
        10: "Exit",
        11: "MongoDB: Posts Collection",
        12: "MongoDB: Post Likes Collection",
        13: "MongoDB: Post Comments Collection",
        14: "MongoDB: Highlight Interactions Collection",
        15: "MongoDB: Profile Visits Collection",
        16: "MongoDB: Mentions Collection",
        17: "MongoDB: Shares Collection",
        18: "MongoDB: Activities Collection",
        19: "MongoDB: Notifications Collection"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def attempt_to_execute_command(command):

    # The command you want to run
    command = command.split()

    # Start the process with Popen (non-blocking)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Continuously read the output without blocking
    while True:
        # Read a line of output
        line = process.stdout.readline()
        
        # If there's output, process it
        if line:
            print(line.decode(), end='')  # Print the line from the command's output
        # Check if the process has finished
        elif process.poll() is not None:
            break  # Exit the loop when the process finishes

    # Optionally, handle any error output (stderr)
    stderr_output = process.stderr.read()
    if stderr_output:
        print(stderr_output.decode())

def print_menu_for_mongo(collection):
    print('\n')
    menu_options = {
        0: "Get All",
        1: "Get Single ID",
        2: "Get with Filters",
        3: "Update",
        4: "Delete",
        5: "Exit"
    }
    
    # Display menu options
    for key in menu_options.keys():
        print(key, '--', menu_options[key])
    
    # Ask for user's choice
    choice = int(input("Please choose an option: "))
    
    # Prepare command string
    command = "python ../mongoDB/client.py "
    
    if choice == 0:
        # Get all
        command += f"{collection} list"
        print(f"Generated command: {command}")
    
    elif choice == 1:
        # Get single by ID
        object_id = input("Please enter the ID of the object: ")
        command += f"{collection} get -i {object_id}"
        print(f"Generated command: {command}")
    
    elif choice == 2:
        # Get with filters
        filter_input = input("Please enter the filter parameters in the format field+value (e.g., 'visibility_status+public user_id+12345'): ")
        command += f"{collection} get -p {filter_input}"
        print(f"Generated command: {command}")
    
    elif choice == 3:
        # Update
        object_id = input("Please enter the ID of the object to update: ")
        update_input = input("Please enter the field and value to update in the format field+value (e.g., 'content+New content'): ")
        command += f"{collection} update -i {object_id} -p {update_input}"
        print(f"Generated command: {command}")
    
    elif choice == 4:
        # Delete
        object_id = input("Please enter the ID of the object to delete: ")
        command += f"{collection} delete -i {object_id}"
        print(f"Generated command: {command}")
    
    elif choice == 5:
        # Exit
        print("Exiting menu.")
        # Exit the program or return to main menu
        return 1
    
    print("attempting to run command:" + command)
    attempt_to_execute_command(command)

    return 0
    


# Main function that controls the application flow
def main():
    # Connect to Cassandra cluster
    log.info("Connecting to Cluster \n")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

      # Create keyspace and set it
    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    # Create database schema (tables)
    model.create_schema(session)

    #this is for mongodb
    choices = ["posts", "likes", "comments", "highlights", "profile_visits", "mentions", "shares", "activity", "notifications"]

    while(True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 0:
            model.bulk_insert(session)
            model.print_all_users(session)
            model.print_all_posts(session)
        elif option == 1:
            user_id = uuid.UUID(input("Enter user ID (UUID format): "))
            model.get_user_activity(session, user_id)
        elif option == 2:
            user_id = uuid.UUID(input("Enter user ID (UUID format): "))
            model.get_engagement_rate(session, user_id)
        elif option == 3:
            user_id = uuid.UUID(input("Enter user ID (UUID format): "))
            other_user_id = uuid.UUID(input("Enter other user ID (UUID format): "))
            model.get_interaction_duration(session, user_id, other_user_id)
        elif option == 4:
            post_id = uuid.UUID(input("Enter post ID (UUID format): "))
            model.get_trending_content(session, post_id)
        elif option == 5:
            user_id = uuid.UUID(input("Enter user ID (UUID format): "))
            model.get_user_sessions(session, user_id)
        elif option == 6:
            user_id = uuid.UUID(input("Enter user ID (UUID format): "))
            model.get_inactive_users(session, user_id)
        elif option == 7:
            user_id = uuid.UUID(input("Enter user ID (UUID format): "))
            model.get_engagement_by_time(session, user_id)
        elif option == 8:
            model.print_all_users(session)
        elif option == 9:
            model.print_all_posts(session)
        elif option == 10:
            print("Exiting...")
            session.shutdown()
            cluster.shutdown()
            exit(0)
        elif option >10 and option <20:
            while(True):
                if print_menu_for_mongo(choices[int(option)-11]):
                    break


        else:
            print("Invalid option. Please choose a number between 0 and 19.")

# Main entry point of the application
if __name__ == '__main__':
    main()