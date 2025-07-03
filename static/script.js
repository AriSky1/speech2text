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

let recording = false;

document.addEventListener("keydown", function (event) {
    if (event.code === "Space") {
        event.preventDefault();  // Prevent scrolling when pressing space
        if (!recording) {
            startRecording();
            recording = true;
        } else {
            stopRecording();
            recording = false;
        }
    }
});
function downloadCSV() {
    const outputEl = document.getElementById('output');
    const text = outputEl.innerText.trim();

    if (!text) {
        alert("No transcript available to download!");
        return;
    }

    // Convert transcript text into CSV format (one line per transcript line)
    // If your transcript contains multiple paragraphs separated by new lines, split on those.
    // Here, we create CSV with two columns: Timestamp, Text
    // Since your transcript already includes timestamps, you can parse it if needed.
    // For simplicity, just save whole text in one CSV cell.

    // Escape double quotes for CSV
    const csvContent = `"Transcript"\n"${text.replace(/"/g, '""')}"`;

    // Create a blob and trigger download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'transcript.csv';
    document.body.appendChild(a);
    a.click();

    // Clean up
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
}