import socket
from database import VoteDatabase
import json

class Admin:
    def __init__(self, udp_host='127.0.0.1', udp_port=6000):
        self.db = VoteDatabase()
        self.udp_host = udp_host
        self.udp_port = udp_port

    def manage_voters(self):
        print("1. Add Voter")
        print("2. List Voters")
        choice = input("Enter your choice: ")

        if choice == "1":
            voter_id = input("Enter voter ID: ")
            voter_name = input("Enter voter name: ")
            self.db.add_voter(voter_id, voter_name)
            print("Voter added successfully")
        elif choice == "2":
            voters = self.db.get_voters()
            for voter in voters:
                print(f"ID: {voter[0]}, Name: {voter[1]}, Has Voted: {'Yes' if voter[2] else 'No'}")

    def view_vote_details(self):
        vote_details = self.db.get_vote_details()
        for detail in vote_details:
            print(f"Voter ID: {detail[0]}, Encrypted Name: {detail[1]}, Voted For: {detail[2]}")

    def manage_candidates(self):
        print("1. Add Candidate")
        print("2. Delete Candidate")
        print("3. Update Candidate")
        choice = input("Enter your choice: ")

        if choice == "1":
            candidate_name = input("Enter candidate name to add: ")
            self.db.add_candidate(candidate_name)
        elif choice == "2":
            candidate_name = input("Enter candidate name to delete: ")
            self.db.delete_candidate(candidate_name)
        elif choice == "3":
            old_name = input("Enter current candidate name: ")
            new_name = input("Enter new candidate name: ")
            self.db.update_candidate(old_name, new_name)

    def publish_results(self):
        results = self.db.get_vote_count()
        results_json = json.dumps([{"candidate": candidate, "votes": count} for candidate, count in results])
        print("Publishing results:\n", results_json)
        
        # Broadcast results to all clients via UDP
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.sendto(results_json.encode(), (self.udp_host, self.udp_port))
        udp_socket.close()

    def clear_votes(self):
        self.db.clear_votes()
        print("Cleared all votes from the database.")
if __name__ == "__main__":
    admin = Admin()
    while True:
        print("1. Manage Candidates")
        print("2. Manage Voters")
        print("3. Publish Results")
        print("4. Clear Votes")
        print("5. View Vote Details")
        choice = input("Enter your choice: ")
        if choice == "1":
            admin.manage_candidates()
        elif choice == "2":
            admin.manage_voters()
        elif choice == "3":
            admin.publish_results()
        elif choice == "4":
            admin.clear_votes()
        elif choice == "5":
            admin.view_vote_details()
