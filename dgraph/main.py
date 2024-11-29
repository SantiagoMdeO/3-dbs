#!/usr/bin/env python3
import os
import pydgraph
import modeldgraph

# Set the Dgraph URI from environment variable, or use default
DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def print_menu():
    mm_options = {
        2: "populate data",
        3: "Follow Tracking Before Registration",
        4: "New Follower Tracking",
        5: "Unfollow Tracking",
        6: "Follower Growth Analytics",
        7: "Content Reach Analysis",
        8: "Profile Interaction Mapping",
        9: "User Block Tracking",
        10: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)

def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)

def close_client_stub(client_stub):
    client_stub.close()

def main():
    # Init Client Stub and Dgraph Client
    client_stub = create_client_stub()
    client = create_client(client_stub)

    # Create schema ////////////////////////////////////
    try:
        print("\n\n")
        modeldgraph.set_schema(client)
        print("Successfully applied schema\n\n")
    except ValueError:
        print("Invalid schema. Please enter a number.\n")
   

    

    while True:
        print_menu()
        try:
            option = int(input('\nEnter your choice: '))
        except ValueError:
            print("Invalid input. Please enter a number.\n")
            continue

        if option == 2:
            modeldgraph.create_data(client)
            print("Data inserted successfully.\n")

        elif option == 3:
            modeldgraph.query_follow_tracking_before(client)

        elif option == 4:
            modeldgraph.query_new_follower_tracking(client)
        
        elif option == 5:
            modeldgraph.query_unfollow_tracking(client)

        elif option == 6:
            # model.query_follower_growth_analytics(client)
            print("No ah\n")

        elif option == 7:
            modeldgraph.query_content_reach_analysis(client)

        elif option == 8:
            modeldgraph.query_profile_interaction_mapping(client)

        elif option == 9:
            modeldgraph.query_user_block_tracking(client)

        elif option == 10:
            close_client_stub(client_stub)
            print("Exiting...")
            break
        else:
            print("Invalid option, try again.\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {}'.format(e))

