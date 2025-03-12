from flask import Flask, render_template, request, jsonify, session, redirect,flash
from database import VoteDatabase
import secrets
import socket
import threading

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
db = VoteDatabase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    candidates = db.get_candidates()
    voters = db.get_voters()
    results = db.get_vote_count()
    vote_details = db.get_vote_details()
    return render_template('admin.html', candidates=candidates, voters=voters, results=results, vote_details=vote_details)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_name = request.form['user_name']
        candidate = request.form['candidate']
        try:
            db.add_vote(user_id, candidate)
            return jsonify({'message': 'Vote recorded successfully'})
        except ValueError as e:
            return jsonify({'message': str(e)}), 400
    candidates = db.get_candidates()
    return render_template('vote.html', candidates=candidates)

@app.route('/manage_candidates', methods=['POST'])
def manage_candidates():
    action = request.form['action']
    candidate_name = request.form['candidate_name']
    if action == 'add':
        db.add_candidate(candidate_name)
    elif action == 'delete':
        db.delete_candidate(candidate_name)
    elif action == 'update':
        new_name = request.form['new_name']
        db.update_candidate(candidate_name, new_name)
    return jsonify({'message': f'Candidate {action}d successfully'})

@app.route('/manage_voters', methods=['POST'])
def manage_voters():
    action = request.form['action']
    voter_id = request.form['voter_id']
    
    if action == 'add':
        voter_name = request.form['voter_name']
        db.add_voter(voter_id, voter_name)
        return jsonify({'message': 'Voter added successfully'})
    elif action == 'remove':
        try:
            db.remove_voter(voter_id)
            return jsonify({'message': 'Voter removed successfully'})
        except ValueError as e:
            return jsonify({'message': str(e)}), 400
    
    return jsonify({'message': 'Invalid action'}), 400

@app.route('/publish_results', methods=['POST'])
def publish_results():
    # Gather the results using the new method
    try:
        results = db.get_results()  # Fetch election results from your database
        results_str = str(results)  # Convert the results to a string for broadcasting
        
        # Set up UDP broadcast
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        udp_port = 6000  # Specify the UDP port to send the results
        broadcast_address = ('192.168.56.101', udp_port)

        # Broadcast the results
        udp_socket.sendto(results_str.encode(), broadcast_address)
        udp_socket.close()
        flash("Results published successfully!")
    except Exception as e:
        flash(f"An error occurred: {e}")
    
    # return jsonify({'results': results})
    return redirect('/admin') # Redirect back to the admin page after publishing

@app.route('/clear_votes')
def clear_votes():
    db.clear_votes()
    return redirect('/admin')
    return jsonify({'message': 'All votes cleared'})

received_results = None  # Global variable to store the received results

# Function to listen for UDP results on the client side

# Route to display the results page
@app.route('/results')
def show_results():
    global received_results
    if received_results is None:
        return "<h1>No results have been published yet.</h1>"
    elif received_results == "":
        return "<h1>No results available.</h1>"
    else:
        # Assuming received_results is a string in the format "Candidate1: 10\nCandidate2: 5\n..."
        return f"<h1>Election Results:</h1><pre>{received_results}</pre>"
    
@app.route('/get_results', methods=['POST'])
def update_results():
    global received_results
    received_results = request.json['results']
    return 'Results updated successfully!'

if __name__ == '__main__':
    app.run(debug=True)