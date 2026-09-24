<!-- MEDICARE HOSPITAL PLATFORM · medical emerald #10b981 on #0d1117 · widgets verified 2026-09-12 -->

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,100:10b981&height=195&section=header&text=MEDICARE%20HOSPITAL&fontSize=54&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=appointments%20%C2%B7%20meet%20consultations%20%C2%B7%20pdf%20system%20%C2%B7%20barcode%20id%20%E2%80%94%20django%205.2&descSize=15&descAlignY=60" alt="MediCare Hospital" />

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=18&duration=2600&pause=900&color=34D399&center=true&vCenter=true&width=780&height=110&lines=roles%3A+superadmin+%C2%B7+doctor+%C2%B7+staff+%C2%B7+patient;appointments+%2B+google+meet+consultations;pdf+templates+%2B+code128+barcode+id+cards;medi+news+%E2%80%94+ckeditor-powered+medical+blog" alt="typing" />

<p>
  <img src="https://img.shields.io/badge/django-5.2-0d1117?style=for-the-badge&logo=django&logoColor=44b78b" alt="django" />
  <img src="https://img.shields.io/badge/python-3.11%2B-0d1117?style=for-the-badge&logo=python&logoColor=3776ab" alt="python" />
  <img src="https://img.shields.io/badge/bootstrap-5.3-0d1117?style=for-the-badge&logo=bootstrap&logoColor=7952b3" alt="bootstrap" />
  <img src="https://img.shields.io/badge/barcode-code128-10b981?style=for-the-badge&logoColor=white" alt="barcode" />
  <img src="https://img.shields.io/badge/video-google%20meet-0d1117?style=for-the-badge&logo=googlemeet&logoColor=00897b" alt="meet" />
  <img src="https://img.shields.io/badge/license-MIT-0d1117?style=for-the-badge&logoColor=34d399" alt="license" />
</p>

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:10b981,100:0d1117&height=3" alt="" />

## ▍$ cat chart.txt

A full medical platform: role-based access across four user types, appointment
lifecycle management, Google Meet video consultations, a CKEditor-powered medical
news system, a **template-driven PDF generator**, and **digital ID cards with
scannable Code128 barcodes** wired into an access-control scanner for restricted areas.

> demo/learning build — no real patient data; not a certified medical system

```yaml
roles     : superadmin · doctor · staff · patient
meet flow : book → accept → paste meet link → join (active 15 min before)
id cards  : auto medi-id (DOC-A1B2C3D4 · STF-E5F6G7H8) + barcode + photo
pdf       : placeholder-based templates (prescription, report, invoice…)
scanner   : quagga.js live camera scan → access grant/deny + audit log
```

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:10b981,100:0d1117&height=3" alt="" />

## ▍$ ls modules/

| $\color{#34d399}{\text{ROLE}}$ | AUTHORITY |
|---|---|
| `superadmin` | full control — create doctors/staff, content, pdf templates, id cards, audit logs, reports |
| `doctor` | manage appointments · accept/reject · add meet links · write medi-news · generate pdfs · own id card |
| `staff` | assigned appointments view · limited dashboard · own id card |
| `patient` | signup · book / track appointments · join video consults · documents · profile + history |

**platform modules** — `accounts` · `core` · `doctors` · `news` · `appointments` · `services` · `pdf_system` · `media_manager` · `admin_tools`

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:10b981,100:0d1117&height=3" alt="" />

## ▍$ man barcode-access

**the id system** — each medic gets a generated vertical ID card: hospital logo,
photo, name, designation, department, blood group, Medi ID, and a **Code128 barcode**.

**the scanner** (`/doctors/scanner/`) — camera-based, quagga.js driven:

```
select location (reception · ot · lab · icu · pharmacy · locker…)
  → scan medi-id (camera or manual entry)
    → POST /doctors/verify-barcode/
      → ✓ grant: name · type · designation · department + audit log
      → ✗ deny : reason recorded, attempt logged
```

Every grant and denial is written to the audit trail — who, where, when.

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:10b981,100:0d1117&height=3" alt="" />

## ▍$ cat pdf.placeholders

Template bodies accept dynamic placeholders — build prescriptions, medical
reports, discharge summaries, invoices, referrals, consent forms:

| TOKEN | RESOLVES TO | TOKEN | RESOLVES TO |
|---|---|---|---|
| `{{patient_name}}` | full name | `{{doctor_name}}` | attending doctor |
| `{{patient_age}}` | age | `{{doctor_designation}}` | title |
| `{{patient_gender}}` | gender | `{{date}}` / `{{time}}` | stamped |
| `{{patient_blood_group}}` | group | `{{diagnosis}}` / `{{prescription}}` | free text |

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:10b981,100:0d1117&height=3" alt="" />

## ▍$ ./setup

```bash
git clone https://github.com/mhjahed/emedical.git && cd emedical
python -m venv venv && source venv/bin/activate    # windows: venv\Scripts\activate
pip install -r requirements.txt

echo "SECRET_KEY=change-me" > .env && echo "DEBUG=True" >> .env
python manage.py makemigrations && python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| SURFACE | URL |
|---|---|
| website | `http://127.0.0.1:8000/` |
| django admin | `/admin/` |
| superadmin dashboard | `/admin-tools/` |
| barcode scanner | `/doctors/scanner/` · manual `/doctors/manual-barcode/` |

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:10b981,100:0d1117&height=3" alt="" />

## ▍$ tree .

```
medical_platform/
├── medical_project/   settings · urls · wsgi
├── accounts/          auth + role model
├── core/              home · contact · static pages
├── doctors/           profiles · id cards · barcode scanner
├── news/              medi news blog (ckeditor)
├── appointments/      booking · slots · meet links
├── services/          hospital services
├── pdf_system/        templates + rendering
├── media_manager/     uploads + folders
├── admin_tools/       superadmin dashboard · audit
├── templates/ · static/ · media/
└── manage.py
```

## ▍$ cat api.http

| METHOD | ROUTE | PURPOSE |
|---|---|---|
| GET | `/appointments/get-slots/<doctor_id>/` | available slots |
| POST | `/appointments/accept/<id>/` · `/reject/<id>/` · `/complete/<id>/` | lifecycle |
| POST | `/doctors/verify-barcode/` | scanner verification |
| POST | `/media-manager/upload/` · `/create-folder/` | media ops |

<details>
<summary><b>▸ troubleshooting quick table</b></summary>

| SYMPTOM | FIX |
|---|---|
| static 404 | `python manage.py collectstatic` |
| db errors | `makemigrations && migrate` |
| module not found | `pip install -r requirements.txt` |
| permission denied | check role + login + url guards |
| template missing | verify path/name · `python manage.py check` |
</details>

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:10b981,100:0d1117&height=3" alt="" />

## ▍$ diff roadmap.now roadmap.next

```diff
- sqlite · single-node · manual meet links
+ postgres · celery reminders · rooms scheduling
+ e-prescription signing · lab-result attachments
+ role matrix per department · hl7/fhir bridge (long-term)
```

<br/>

<div align="center">

`why google meet? zero api complexity · zero server load · every device works · zero cost`
`built end-to-end by` **[MH JAHED](https://github.com/mhjahed)** · `mhjahed@proton.me`
`contact me <b>I'm available now!</b>`


</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:10b981,100:0d1117&height=110&section=footer" alt="" />
