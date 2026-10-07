# Sprint Plan — Vehicle Parking System (Team 10)

The backlog follows the components in [SAD v1.1](SAD/Team10_Vehicle_Parking_System_SAD.pdf) and the requirement IDs in SRS v1.1. Each feature should have one owner, as the project guidelines require ("product ownership"). Fill in the **Owner** column at sprint planning.

## Sprint 1 — Foundation, authentication & users

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S1-1 | Set up `client/` (React + Vite) and `server/` (Express) with the folder layout from SAD §4.1; read secrets from `.env` | NFR-10, SEC-10 | | To do |
| S1-2 | MongoDB replica set (local / Docker), Mongoose models and indexes (SAD §3.6) | NFR-05, NFR-06 | | To do |
| S1-3 | Login, logout and Vehicle Owner self-registration; bcrypt hashing; server-side sessions with a 15-min idle timeout; lock-out after 5 failed logins | FR-01 – FR-04, SEC-03, SEC-07, SEC-08 | | To do |
| S1-4 | Security middleware: role matrix (SAD §4.3), ownership checks, Joi validation, error handler, audit log | FR-06, SEC-01, SEC-02, SEC-05, SEC-06, SEC-09 | | To do |
| S1-5 | Admin user management (create, update, deactivate accounts; assign roles) | FR-05 | | To do |

## Sprint 2 — Vehicles & slots

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S2-1 | Vehicle registration, validation, update and deactivation | FR-07 – FR-10 | | To do |
| S2-2 | Slot management (add a slot, change its type, mark it Unavailable) | FR-11 – FR-13 | | To do |
| S2-3 | Slot availability screen and counts per type | FR-14, FR-15, NFR-02 | | To do |

## Sprint 3 — Entry, exit, fees, tracking & reports

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S3-1 | Vehicle entry with atomic slot allocation and ticket numbers | FR-16 – FR-19, NFR-05, BR-01 – BR-03 | | To do |
| S3-2 | Vehicle exit, fee calculation, summary screen, confirm or cancel | FR-20 – FR-24, BR-04, BR-06 | | To do |
| S3-3 | Fee rule configuration (hourly rates, grace period) | FR-25 – FR-27 | | To do |
| S3-4 | Vehicle search, current status, history, and list of parked vehicles | FR-28 – FR-31 | | To do |
| S3-5 | Parking Occupancy Report and Vehicle Tracking Report | FR-32, FR-33 | | To do |

## Sprint 4 — Testing & hardening (Test Plan v1.1)

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S4-1 | Run the STP test cases; log defects in GitHub Issues | All | | To do |
| S4-2 | Performance tests (JMeter, 50 concurrent users) | NFR-01 – NFR-04 | | To do |
| S4-3 | Security validation (STP §5.1: ZAP, testssl.sh, gitleaks, npm audit) | SEC-01 – SEC-10 | | To do |
| S4-4 | Usability and browser/screen-size compatibility checks | NFR-08, NFR-09, NFR-12 | | To do |
