async function enroll() {
  const file = document.getElementById('enrollFile').files[0];
  const userId = document.getElementById('enrollUser').value;
  const form = new FormData();
  form.append('user_id', userId);
  form.append('audio_file', file);

  const res = await fetch('/enroll-voice', { method: 'POST', body: form });
  const data = await res.json();
  document.getElementById('enrollResult').textContent = JSON.stringify(data, null, 2);
}

async function verify() {
  const file = document.getElementById('verifyFile').files[0];
  const userId = document.getElementById('verifyUser').value;
  const form = new FormData();
  form.append('user_id', userId);
  form.append('audio_file', file);

  const res = await fetch('/verify-voice', { method: 'POST', body: form });
  const data = await res.json();
  document.getElementById('verifyResult').textContent = JSON.stringify(data, null, 2);
}
