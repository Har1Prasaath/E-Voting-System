import sqlite3

class VoteDatabase:
    def __init__(self, db_name="votes.db"):
        self.db_name = db_name
        self.create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.get_connection()
        try:
            with conn:
                conn.execute('''CREATE TABLE IF NOT EXISTS votes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id TEXT NOT NULL,
                                    candidate TEXT NOT NULL)''')
                conn.execute('''CREATE TABLE IF NOT EXISTS candidates (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    candidate_name TEXT NOT NULL)''')
                conn.execute('''CREATE TABLE IF NOT EXISTS voters (
                                    id TEXT PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    has_voted BOOLEAN DEFAULT 0)''')
        finally:
            conn.close()

    def add_voter(self, voter_id, voter_name):
        conn = self.get_connection()
        try:
            with conn:
                conn.execute("INSERT INTO voters (id, name) VALUES (?, ?)", (voter_id, voter_name))
        finally:
            conn.close()

    def get_voters(self):
        conn = self.get_connection()
        try:
            with conn:
                cursor = conn.execute("SELECT id, name, has_voted FROM voters")
                return cursor.fetchall()
        finally:
            conn.close()

    def voter_exists(self, voter_id):
        conn = self.get_connection()
        try:
            with conn:
                cursor = conn.execute("SELECT 1 FROM voters WHERE id = ?", (voter_id,))
                return cursor.fetchone() is not None
        finally:
            conn.close()

    def has_voted(self, voter_id):
        conn = self.get_connection()
        try:
            with conn:
                cursor = conn.execute("SELECT has_voted FROM voters WHERE id = ?", (voter_id,))
                result = cursor.fetchone()
                return result[0] if result else False
        finally:
            conn.close()

    def mark_as_voted(self, voter_id):
        conn = self.get_connection()
        try:
            with sqlite3.connect(self.db_name, timeout=10) as conn:
                conn.execute("UPDATE voters SET has_voted = 1 WHERE id = ?", (voter_id,))
        finally:
            conn.commit()
            conn.close()

    def add_vote(self, user_id, candidate):
        if not self.voter_exists(user_id):
            raise ValueError("Voter not in the list")
        if self.has_voted(user_id):
            raise ValueError("Voter has already voted")
        conn = self.get_connection()
        try:
            with sqlite3.connect(self.db_name, timeout=10) as conn:
                conn.execute("INSERT INTO votes (user_id, candidate) VALUES (?, ?)", (user_id, candidate))
                conn.commit()
                self.mark_as_voted(user_id)
        finally:
            conn.close()
    
    def remove_voter(self, voter_id):
        conn = self.get_connection()
        try:
            with conn:
                # First, check if the voter exists
                cursor = conn.execute("SELECT 1 FROM voters WHERE id = ?", (voter_id,))
                if cursor.fetchone() is None:
                    raise ValueError("Voter not found")
                
                # Remove the voter
                conn.execute("DELETE FROM voters WHERE id = ?", (voter_id,))
                
                # Also remove any votes cast by this voter
                conn.execute("DELETE FROM votes WHERE user_id = ?", (voter_id,))
        finally:
            conn.close()

    def get_vote_details(self):
        conn = self.get_connection()
        try:
            with conn:
                cursor = conn.execute("""
                    SELECT v.user_id, vr.name, v.candidate 
                    FROM votes v
                    JOIN voters vr ON v.user_id = vr.id
                """)
                return cursor.fetchall()
        finally:
            conn.close()

    def get_vote_count(self):
        conn = self.get_connection()
        try:
            with conn:
                cursor = conn.execute("SELECT candidate, COUNT(*) FROM votes GROUP BY candidate")
                return cursor.fetchall()
        finally:
            conn.close()

    def get_candidates(self):
        conn = self.get_connection()
        try:
            with conn:
                cursor = conn.execute("SELECT candidate_name FROM candidates")
                return [row[0] for row in cursor]
        finally:
            conn.close()

    def add_candidate(self, candidate_name):
        conn = self.get_connection()
        try:
            with conn:
                conn.execute("INSERT INTO candidates (candidate_name) VALUES (?)", (candidate_name,))
        finally:
            conn.close()

    def delete_candidate(self, candidate_name):
        conn = self.get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM candidates WHERE candidate_name = ?", (candidate_name,))
        finally:
            conn.close()

    def update_candidate(self, old_name, new_name):
        conn = self.get_connection()
        try:
            with conn:
                conn.execute("UPDATE candidates SET candidate_name = ? WHERE candidate_name = ?", (new_name, old_name))
        finally:
            conn.close()

    def clear_votes(self):
        conn = self.get_connection()
        try:
            with conn:
                conn.execute("DELETE FROM votes")
                conn.execute("UPDATE voters SET has_voted = 0")
        finally:
            conn.close()
    
    def get_results(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Assuming your votes are stored in a table called 'votes'
        # Modify the query based on your database structure
        cursor.execute("SELECT candidate, COUNT(*) FROM votes GROUP BY candidate")
        results = cursor.fetchall()

        conn.close()

        # Format the results into a more readable structure if necessary
        formatted_results = {row[0]: row[1] for row in results}
        return formatted_results