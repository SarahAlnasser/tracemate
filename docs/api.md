# TraceMate API contract

The device and website talk to the backend with JSON over HTTP.
Agree on a shape here BEFORE coding it. Base URL: `http://<laptop-ip>/tracemate/backend/api`

## GET /health.php
Checks the backend and database are up.
```json
{ "ok": true, "letter_templates": 3 }
```

## POST /auth.php  (website)
Request: `{ "email": "specialist@efada.sa", "password": "..." }`
Response: `{ "user_id": 1, "name": "Specialist", "role": "specialist" }`

## GET /sessions.php?device_key=KEY  (device)
The next scheduled session for the student using this device.
```json
{ "session_id": 7, "student_name": "Student A",
  "letters": [ { "template_id": 1, "name": "alif", "letter": "ا" },
               { "template_id": 2, "name": "baa",  "letter": "ب" } ] }
```

## POST /sessions.php  (website, specialist)
Request: `{ "student_id": 3, "scheduled_date": "2026-10-20", "template_ids": [1, 2, 3] }`
Response: `{ "session_id": 8 }`

## POST /attempts.php  (device)
Sent after every tracing attempt. Also used by the offline queue.
```json
{ "device_key": "KEY", "session_id": 7, "template_id": 1, "attempt_no": 2,
  "score": 87.5, "passed": true, "points": [[[0.50, 0.16], [0.50, 0.17]]],
  "created_at": "2026-10-20T16:05:00" }
```
Response: `{ "saved": true, "attempt_id": 41 }`

## GET /attempts.php?student_id=3  (website charts)
```json
[ { "date": "2026-10-20", "letter": "ا", "score": 87.5, "passed": true } ]
```

## GET /alerts.php?student_id=3  (website, parent)
```json
[ { "alert_id": 2, "reason": "Average accuracy dropped 18% below baseline", "created_at": "2026-11-02", "is_read": false } ]
```
