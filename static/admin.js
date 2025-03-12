document.getElementById('candidateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const candidateName = document.getElementById('candidateName').value;
    const action = document.getElementById('action').value;
    const newName = document.getElementById('newName').value;

    fetch('/manage_candidates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `action=${action}&candidate_name=${candidateName}&new_name=${newName}`
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    });
});

document.getElementById('addVoterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const voterId = document.getElementById('voterId').value;
    const voterName = document.getElementById('voterName').value;

    fetch('/manage_voters', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `action=add&voter_id=${encodeURIComponent(voterId)}&voter_name=${encodeURIComponent(voterName)}`
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    });
});

document.getElementById('removeVoterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const voterId = document.getElementById('removeVoterId').value;

    if (confirm(`Are you sure you want to remove voter with ID ${voterId}?`)) {
        fetch('/manage_voters', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `action=remove&voter_id=${encodeURIComponent(voterId)}`
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        });
    }
});

document.getElementById('publishResults').addEventListener('click', function() {
    fetch('/publish_results')
    .then(response => response.json())
    .then(data => {
        const resultsList = document.getElementById('resultsList');
        resultsList.innerHTML = '';
        for (const [candidate, votes] of Object.entries(data)) {
            const li = document.createElement('li');
            li.textContent = `${candidate}: ${votes} votes`;
            resultsList.appendChild(li);
        }
    });
});

document.getElementById('clear_votes_button').addEventListener('click', function() {
    if (confirm('Are you sure you want to clear all votes?')) {
        fetch('/clear_votes', {
            method: 'GET',  // Ensure POST method is used
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

