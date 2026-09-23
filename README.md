# TraceMate

Handwriting tracing device + monitoring website for students with Down syndrome.
IT492 Graduation Project, Group 14, CCIS, IMAMU. 

## Folders

| Folder | What lives here |
| --- | --- |
| `device/` | Python + Pygame app that runs on the Raspberry Pi |
| `templates/` | Letter templates (JSON), shared by the device and the backend |
| `backend/` | PHP REST API + MySQL schema |
| `web/` | Monitoring website (HTML, CSS, JS, Chart.js) |
| `docs/` | API contract, ERD, screenshots, meeting notes |

## Run it

### Device (laptop or Pi)
```
cd device
pip install -r requirements.txt
python main.py alif          # trace ا with the mouse; R = reset, Esc = quit
```

### Make a letter template
```
cd device
python tools/template_maker.py --letter ب --name baa --font NotoNaskhArabic-Regular.ttf --out ../templates
python tools/template_maker.py --view ../templates/baa.json
```

### Backend + website (XAMPP)
1. Copy (or clone) this repo into `xampp/htdocs/tracemate`.
2. Start Apache and MySQL in XAMPP.
3. In phpMyAdmin, import `backend/schema.sql`.
4. Copy `backend/config.example.php` to `backend/config.php` and set your DB password.
5. Test: open http://localhost/tracemate/backend/api/health.php (should show `"ok": true`).
6. Website: http://localhost/tracemate/web/

## Team rules
- `main` always works. Never push broken code to it.
- One branch per task: `slice1/accuracy-engine`, `slice3/login`, ...
- Open a pull request; one teammate reviews before merging.
- Any change to a JSON shape between device and backend: update `docs/api.md` first.
- Never commit `backend/config.php` (it has passwords).
