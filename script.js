document.getElementById("message").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {
    const messageInput = document.getElementById("message");
    const responseContainer = document.getElementById("response");
    const message = messageInput.value.trim();

    if (!message) return;

    // Display user message
    const userMessage = document.createElement("div");
    userMessage.textContent = `You: ${message}`;
    userMessage.classList.add("user-message");
    responseContainer.appendChild(userMessage);

    messageInput.value = ""; // Clear input field

    try {
        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        if (!res.ok) throw new Error(`Server error: ${res.statusText}`);

        const data = await res.json(); // Proper JSON response
        const botMessage = document.createElement("div");
        botMessage.classList.add("bot-message");
        botMessage.textContent = `Bot: ${data.response}`;
        responseContainer.appendChild(botMessage);
    } catch (error) {
        responseContainer.innerText = "Error: " + error.message;
    }
}
