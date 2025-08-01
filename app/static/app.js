// Utility to reset a file input
function resetFileInput(input) {
  input.value = "";
}

document.getElementById("enrollForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("Enroll form submitted");
  const fileInput = document.getElementById("enrollFile");
  const userInput = document.getElementById("enrollUser");
  const resultBox = document.getElementById("enrollResult");

  if (!fileInput.files.length) {
    resultBox.textContent = "❌ No file selected";
    return;
  }

  const form = new FormData();
  form.append("user_id", userInput.value);
  form.append("audio_file", fileInput.files[0]);

  try {
    const res = await fetch("/enroll-voice", { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || JSON.stringify(data));
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    console.error("Enroll error:", err);
    resultBox.textContent = `❌ ${err.message}`;
  }

  // Clear inputs so you can submit again
  resetFileInput(fileInput);
  userInput.value = "";
});

document.getElementById("verifyForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("Verify form submitted");
  const fileInput = document.getElementById("verifyFile");
  const userInput = document.getElementById("verifyUser");
  const resultBox = document.getElementById("verifyResult");

  if (!fileInput.files.length) {
    resultBox.textContent = "❌ No file selected";
    return;
  }

  const form = new FormData();
  form.append("user_id", userInput.value);
  form.append("audio_file", fileInput.files[0]);

  try {
    const res = await fetch("/verify-voice", { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || JSON.stringify(data));
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    console.error("Verify error:", err);
    resultBox.textContent = `❌ ${err.message}`;
  }

  // Clear inputs for reuse
  resetFileInput(fileInput);
  userInput.value = "";
});
