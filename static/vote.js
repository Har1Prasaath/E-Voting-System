document.getElementById('voteForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const userId = document.getElementById('userId').value;
    const userName = document.getElementById('userName').value;
    const candidate = document.getElementById('candidate').value;

    fetch('/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_id=${userId}&user_name=${userName}&candidate=${candidate}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = data.message;
    });
});