// Utility to reset a file input
function resetFileInput(input) {
  input.value = "";
}

async function handleResponse(res, resultBox) {
  // Read the raw text first
  const text = await res.text();

  // Try to parse JSON; if it fails, show the raw response and bail out
  let payload;
  try {
    payload = JSON.parse(text);
  } catch (e) {
    resultBox.textContent = `❌ Non-JSON response (status ${res.status}):\n${text}`;
    return null;
  }

  // If server responded with an error code, display its JSON error payload
  if (!res.ok) {
    const errMsg = payload.error || JSON.stringify(payload);
    resultBox.textContent = `❌ ${errMsg}`;
    return null;
  }

  // Success!
  resultBox.textContent = JSON.stringify(payload, null, 2);
  return payload;
}

document.getElementById("enrollForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput  = document.getElementById("enrollFile");
  const userInput  = document.getElementById("enrollUser");
  const resultBox  = document.getElementById("enrollResult");

  if (!fileInput.files.length) {
    resultBox.textContent = "❌ No file selected";
    return;
  }

  const form = new FormData();
  form.append("user_id",    userInput.value);
  form.append("audio_file", fileInput.files[0]);

  const res = await fetch("/enroll-voice", { method: "POST", body: form });
  await handleResponse(res, resultBox);

  document.getElementById("enrollForm").reset();
});

document.getElementById("verifyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput  = document.getElementById("verifyFile");
  const userInput  = document.getElementById("verifyUser");
  const resultBox  = document.getElementById("verifyResult");

  if (!fileInput.files.length) {
    resultBox.textContent = "❌ No file selected";
    return;
  }

  const form = new FormData();
  form.append("user_id",    userInput.value);
  form.append("audio_file", fileInput.files[0]);

  const res = await fetch("/verify-voice", { method: "POST", body: form });
  await handleResponse(res, resultBox);

  document.getElementById("verifyForm").reset();
});
