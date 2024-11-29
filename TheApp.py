#!/usr/bin/env python3
import logging
import os
import uuid
from cassandra.cluster import Cluster
from cassandraDir import model
import subprocess

#dgraph
import pydgraph
from dgraph import modeldgraph


#setting up everything for connections
# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('./cassandraDir/investments.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

#Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'cassandrafinal')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')
#drgaph
DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)

def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)

def close_client_stub(client_stub):
    client_stub.close()

def createUnicorn():
    #check if this is running or not

    # Define the directory to navigate to and the command to run
    directory = "./mongoDB/"
    command = "python -m uvicorn main:app --reload"

    # Construct the full PowerShell command
    powershell_command = f"pwd; cd {directory}; {command}"

    # Open a new PowerShell window and execute the command
    subprocess.Popen(
        ["powershell", "-Command", powershell_command],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )





#prety neesssss---------------------------------------
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

        11: "MongoDB: Posts Collection",
        12: "MongoDB: Post Likes Collection",
        13: "MongoDB: Post Comments Collection",
        14: "MongoDB: Highlight Interactions Collection",
        15: "MongoDB: Profile Visits Collection",
        16: "MongoDB: Mentions Collection",
        17: "MongoDB: Shares Collection",
        18: "MongoDB: Notifications Collection",

        20: "populate data",
        21: "Follow Tracking Before Registration",
        22: "New Follower Tracking",
        23: "Unfollow Tracking",
        24: "Follower Growth Analytics",
        25: "Content Reach Analysis",
        26: "Profile Interaction Mapping",
        27: "User Block Tracking",
        28: "Exit"
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
    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)
    model.create_schema(session) #schemaaaaaaaaaa

    # Init Client Stub and Dgraph Client
    client_stub = create_client_stub()
    client = create_client(client_stub)
    try:
        print("\n\n")
        modeldgraph.set_schema(client)
        print("Successfully applied schema\n\n")
    except ValueError:
        print("Invalid schema. Please enter a number.\n")

    #mongo db client
    createUnicorn()




    #options menu necesities
    #this is for mongodb
    choices = ["posts", "likes", "comments", "highlights", "profile_visits", "mentions", "shares", "notifications"]

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
        elif option >10 and option <19:
            while(True):
                if print_menu_for_mongo(choices[int(option)-11]):
                    break
        elif option == 20:
            model.create_data(client)
            print("Data inserted successfully.\n")

        elif option == 21:
            model.query_follow_tracking_before(client)

        elif option == 22:
            model.query_new_follower_tracking(client)
        
        elif option == 23:
            model.query_unfollow_tracking(client)

        elif option == 24:
            # model.query_follower_growth_analytics(client)
            print("No ah\n")

        elif option == 25:
            model.query_content_reach_analysis(client)

        elif option == 26:
            model.query_profile_interaction_mapping(client)

        elif option == 27:
            model.query_user_block_tracking(client)

        elif option == 28:
            close_client_stub(client_stub)
            session.shutdown()
            cluster.shutdown()
            exit(0)
            break

        else:
            print("Invalid option. Please choose a number between 0 and 19.")

# Main entry point of the application
if __name__ == '__main__':
    main()