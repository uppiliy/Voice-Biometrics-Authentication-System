# Voice Biometrics API

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API
- GET `/` → UI
- POST `/enroll-voice`
- POST `/verify-voice`

## CI/CD
On push, runs lint, tests, build and Docker push.