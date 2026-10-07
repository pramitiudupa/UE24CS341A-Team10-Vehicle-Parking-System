# Vehicle Parking System — Team 10

**Software Engineering (UE24CS341A) Mini-Project · Semester 5 · Section F · PES University, Bengaluru**

A web-based system for managing parking slots and tracking vehicles. Vehicle owners register their vehicles, see which slots are free, and find where their vehicle is parked. Parking attendants record vehicle entry and exit: the system allocates a matching slot, calculates the fee from the configured hourly rates, and releases the slot. Administrators manage slots, users and fee rules, and generate occupancy and vehicle tracking reports.

| | |
|---|---|
| **Team #** | 10 (Section F) |
| **Problem statement** | Vehicle Parking System – a system for managing parking slots and vehicle tracking |
| **Tech stack** | MERN – MongoDB, Express.js, React.js, Node.js |

## Team

| Name | SRN |
|---|---|
| Pandi Snehitha | PES1UG24CS315 |
| Pramiti Ragavendra Udupa | PES1UG24CS331 |
| Ramitha R | PES1UG24CS368 |

## Part-1 Deliverables (due 07-10-2026)

| # | Deliverable | Location | Status |
|---|---|---|---|
| 1 | Software Requirements Specification (IEEE format) | [`docs/SRS/`](docs/SRS/) | v1.1 completed by team – to be uploaded |
| 2 | Software Test Plan (IEEE format, with test cases) | [`docs/TestPlan/`](docs/TestPlan/) | v1.1 completed by team – to be uploaded |
| 3 | Software Architecture & Design Specification (SAD) | [`docs/SAD/`](docs/SAD/) | ✅ v1.1 uploaded (aligned with SRS v1.1) |
| 4 | Implementation start + sprint activity | [`docs/Sprint-Plan.md`](docs/Sprint-Plan.md) | Sprint 1 planned |

## SAD at a glance

SAD v1.1 is aligned with SRS v1.1 (FR-01…FR-33, NFR-01…NFR-12, SEC-01…SEC-10, BR-01…BR-06) and with the Test Plan v1.1 test-case IDs.

- **Architecture:** Layered three-tier (React SPA → Express REST API → MongoDB replica set), with the routes, security middleware, services and repositories kept in separate layers.
- **Components** (the names used in the SRS RTM): Security Middleware, Auth Service, User Management Service, Vehicle Service, Parking Slot Service, Parking Transaction Service, Fee Service, Report Service, Audit Logging Component, Database Layer.
- **Key design points:** slot allocation and exit run inside transactions, backed by unique indexes, so a slot can never hold two vehicles. The fee is billable hours × hourly rate, with a grace period. Each JWT is tied to a server-side session, which lets logout cancel the token and ends the session after 15 minutes idle. bcrypt hashing, account lock-out after 5 failed logins, server-side role checks (Vehicle Owner / Parking Attendant / Administrator), an audit log, TLS, and a STRIDE threat model.

| Component diagram | Deployment view |
|---|---|
| ![Component diagram](docs/diagrams/component.png) | ![Deployment](docs/diagrams/deployment.png) |

Sequence diagrams: [Vehicle entry & slot allocation](docs/diagrams/seq_entry.png) · [Vehicle exit & fee](docs/diagrams/seq_exit.png) · [Login](docs/diagrams/seq_login.png) · [Search & track vehicle](docs/diagrams/seq_search.png)

## Repository structure

```
.
├── README.md
├── docs/
│   ├── SRS/                  # Software Requirements Specification
│   ├── SAD/                  # Software Architecture & Design Specification (PDF + DOCX)
│   ├── TestPlan/             # Software Test Plan + test cases
│   ├── Sprint-Plan.md        # Sprint backlog for implementation
│   ├── diagrams/             # UML component, deployment and sequence diagrams (PNG)
│   │   └── source/           # Python scripts that regenerate the diagrams and the SAD .docx
│   └── course-material/      # Templates and instructions given by the course
├── client/                   # React front end   (added in Sprint 1)
└── server/                   # Express back end  (added in Sprint 1)
```

## Regenerating the diagrams / SAD

```bash
pip install matplotlib python-docx
python docs/diagrams/source/generate_diagrams.py
python docs/diagrams/source/build_sad_docx.py
```
