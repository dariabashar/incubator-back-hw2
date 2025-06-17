async function sendPrompt() {
    const prompt = document.getElementById("prompt").value;
    const responseDiv = document.getElementById("response");
  
    responseDiv.innerText = "Editing...";
  
    try {
      const res = await fetch("http://localhost:8000/assistant/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
  
      const data = await res.json();
      responseDiv.innerText = data.response || "No answer";
    } catch (err) {
      responseDiv.innerText = "Error.";
      console.error(err);
    }
  }
  