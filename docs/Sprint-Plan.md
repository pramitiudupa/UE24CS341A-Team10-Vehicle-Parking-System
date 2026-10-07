# Sprint Plan — Vehicle Parking System (Team 10)

The backlog follows the components in [SAD v1.1](SAD/Team10_Vehicle_Parking_System_SAD.pdf) and the requirement IDs in [SRS v1.1](SRS/Vehicle_Parking_System_SRS_v1.1.pdf). Each feature should have one owner, as the project guidelines require ("product ownership"). Fill in the **Owner** column at sprint planning.

## Sprint 1 — Foundation, authentication & users

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S1-1 | Set up `client/` (React + Vite) and `server/` (Express) with the folder layout from SAD §4.1; read secrets from `.env` | SEC-07 | | To do |
| S1-2 | MongoDB replica set (local / Docker), Mongoose models and indexes (SAD §3.6) | NFR-04, NFR-05 | | To do |
| S1-3 | Login and logout; bcrypt hashing; server-side sessions with a 15-minute idle timeout | FR-01 – FR-03, SEC-03, SEC-06 | | To do |
| S1-4 | Security middleware: role matrix (SAD §4.3), Joi validation, error handler | FR-05, SEC-01, SEC-02, SEC-05 | | To do |
| S1-5 | Admin user management (create, update, deactivate accounts; assign roles) | FR-04 | | To do |

## Sprint 2 — Vehicles & slots

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S2-1 | Vehicle registration with validation | FR-06, FR-07 | | To do |
| S2-2 | Slot management (add a slot; set it Unavailable or Available) | FR-08, FR-09 | | To do |
| S2-3 | Slot availability screen with counts per slot type | FR-10 | | To do |

## Sprint 3 — Entry, exit, fees, tracking & report

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S3-1 | Vehicle entry with atomic slot allocation and ticket numbers | FR-11 – FR-14, NFR-04, BR-01 – BR-03 | | To do |
| S3-2 | Vehicle exit, fee calculation (fixed 15-minute grace period), summary, confirm or cancel | FR-15 – FR-18, BR-04 | | To do |
| S3-3 | Hourly rate configuration | FR-19 | | To do |
| S3-4 | Vehicle search, current status and parking history | FR-20 – FR-22 | | To do |
| S3-5 | Parking Occupancy Report | FR-23, BR-05 | | To do |

## Sprint 4 — Testing & hardening (Test Plan v1.1)

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S4-1 | Run the 37 test cases in STP Appendix B; log defects in GitHub Issues | All | | To do |
| S4-2 | Performance tests (JMeter: 50 users for search; 20 users for entry and exit) | NFR-01 – NFR-03 | | To do |
| S4-3 | Concurrency and reliability tests | NFR-04, NFR-05 | | To do |
| S4-4 | Security validation (STP §5.1: ZAP, testssl.sh, gitleaks, npm audit) | SEC-01 – SEC-07 | | To do |
| S4-5 | Usability and browser/screen-size compatibility checks | NFR-06, NFR-07 | | To do |
