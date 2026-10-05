# Sprint Plan — Vehicle Parking System (Team 10)

The backlog follows the components and requirement IDs in the [SAD](SAD/Team10_Vehicle_Parking_System_SAD.pdf). Each feature should have one owner, as the project guidelines require ("product ownership"). Fill in the **Owner** column at sprint planning.

## Sprint 1 — Foundation & authentication (07-10-2026 → 17-10-2026)

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S1-1 | Set up `client/` (React + Vite) and `server/` (Express) projects, ESLint and the folder layout from SAD §4.1 | – | | To do |
| S1-2 | MongoDB replica set (local / Docker) and Mongoose connection | VPS-NF-03 | | To do |
| S1-3 | Register / login / refresh / logout APIs with bcrypt and JWT | VPS-F-01, VPS-SEC-01 | | To do |
| S1-4 | RBAC middleware (DRIVER / ATTENDANT / ADMIN), Joi validation, rate limiter, central error handler | VPS-F-02, VPS-SEC-02, VPS-SEC-04 | | To do |
| S1-5 | Login / register pages and role-based routing in the SPA | VPS-F-01, VPS-NF-05 | | To do |

## Sprint 2 — Slots & bookings

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S2-1 | Admin CRUD for lots, levels, slots and tariffs | VPS-F-10 | | To do |
| S2-2 | Slot availability API and live slot map (Socket.IO `slot:update`) | VPS-F-03, VPS-NF-02 | | To do |
| S2-3 | Create / cancel booking with a transaction-based overlap check | VPS-F-04, VPS-F-05, VPS-NF-04 | | To do |
| S2-4 | Booking-expiry scheduler and e-mail notifications | VPS-F-12 | | To do |

## Sprint 3 — Entry / exit, billing, tracking & reports

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S3-1 | Vehicle check-in / check-out (attendant console) | VPS-F-06, VPS-F-07 | | To do |
| S3-2 | Fee calculation, payments (cash + gateway test mode) and receipts | VPS-F-07, VPS-F-08 | | To do |
| S3-3 | Vehicle locator and parking history | VPS-F-09 | | To do |
| S3-4 | Occupancy and revenue reports with CSV export | VPS-F-11 | | To do |
| S3-5 | Audit log | VPS-SEC-05 | | To do |

## Sprint 4 — Testing & hardening

| ID | Backlog item | Requirement(s) | Owner | Status |
|---|---|---|---|---|
| S4-1 | Run the test cases from the Test Plan; log defects | All | | To do |
| S4-2 | Performance test (JMeter, 100 concurrent users) | VPS-NF-01 | | To do |
| S4-3 | Security validation (Test Plan §5.1) | VPS-SEC-01 … 05 | | To do |
