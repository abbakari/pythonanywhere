document.addEventListener('DOMContentLoaded', function() {
    // Check if we should play voice notification
    if (document.body.classList.contains('admin-dashboard')) {
        checkForNotifications();
    }
});

function checkForNotifications() {
    fetch('/check_notification/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.play_notification && data.pending_count > 0) {
            speakNotification(data.pending_count);
        }
    })
    .catch(error => console.error('Error:', error));
}

function speakNotification(count) {
    // Check if browser supports speech synthesis
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance();
        utterance.text = `Attention administrator. You have ${count} ${count === 1 ? 'ticket' : 'tickets'} waiting for review.`;
        utterance.volume = 1;
        utterance.rate = 0.9;
        utterance.pitch = 1;
        
        // Try to get a female voice if available
        const voices = window.speechSynthesis.getVoices();
        const femaleVoice = voices.find(voice => voice.name.includes('Female'));
        if (femaleVoice) {
            utterance.voice = femaleVoice;
        }
        
        speechSynthesis.speak(utterance);
    } else {
        console.log('Text-to-speech not supported in this browser');
    }
}