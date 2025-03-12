// static/result.js
const socket = new WebSocket('ws://' + location.host + '/ws');

socket.onmessage = function(event) {
    const results = event.data;
    document.getElementById('resultsContainer').textContent = results;
};

socket.onclose = function(event) {
    console.log('WebSocket connection closed:', event);
};

socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};