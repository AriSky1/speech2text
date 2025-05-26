function startRecording() {
    const lang = document.getElementById("language").value;
    fetch('/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: lang })
    }).then(res => res.json()).then(data => {
        document.getElementById("status").textContent = "Listening...";
        console.log(data);
    });
}

function stopRecording() {
    fetch('/stop', {
        method: 'POST'
    }).then(() => {
        setTimeout(() => {
            fetch('/result')
                .then(res => res.json())
                .then(data => {
                    const output = document.getElementById("output");
                    const status = document.getElementById("status");

                    if (data.text) {
                        output.textContent = data.text;
                    }

                    status.textContent = "Idle";
                });
        }, 1500); // Give time for recording thread to finish
    });
}

function resetTranscription() {
    fetch('/reset', { method: 'POST' })
        .then(() => {
            document.getElementById("output").textContent = "(reset)";
            document.getElementById("status").textContent = "Idle";
        });
}
