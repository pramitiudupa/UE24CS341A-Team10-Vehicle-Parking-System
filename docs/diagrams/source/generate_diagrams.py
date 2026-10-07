"""Regenerates the UML diagrams in docs/diagrams/ (requires: pip install matplotlib)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") + os.sep
plt.rcParams["font.family"] = "DejaVu Sans"


def component(ax, x, y, w, h, name, stereo="«component»", fc="#FFFFFF", fs=8.5):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#222", lw=1.2))
    # UML component icon (top-right)
    ix, iy = x + w - 0.42, y + h - 0.38
    ax.add_patch(Rectangle((ix, iy), 0.28, 0.24, fc="white", ec="#222", lw=0.8))
    ax.add_patch(Rectangle((ix - 0.06, iy + 0.04), 0.12, 0.05, fc="white", ec="#222", lw=0.8))
    ax.add_patch(Rectangle((ix - 0.06, iy + 0.14), 0.12, 0.05, fc="white", ec="#222", lw=0.8))
    nl = name.count(chr(10))
    ax.text(x + w / 2, y + h / 2 + 0.13 + nl * 0.2, stereo, ha="center", va="center", fontsize=fs - 1.5, style="italic")
    ax.text(x + w / 2, y + h / 2 - 0.13 - nl * 0.08, name, ha="center", va="center", fontsize=fs, weight="bold")
    return (x, y, w, h)


def package(ax, x, y, w, h, title, fc):
    ax.add_patch(Rectangle((x, y + h), min(3.4, w * 0.45), 0.32, fc=fc, ec="#555", lw=1))
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#555", lw=1))
    ax.text(x + 0.12, y + h + 0.16, title, va="center", fontsize=8.5, weight="bold")


def arrow(ax, p, q, label=None, dashed=True, lo=(0, 0), fs=7):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="->", lw=1.0, color="#222",
                                linestyle=(0, (4, 3)) if dashed else "-", shrinkA=0, shrinkB=0))
    if label:
        mx, my = (p[0] + q[0]) / 2 + lo[0], (p[1] + q[1]) / 2 + lo[1]
        ax.text(mx, my, label, fontsize=fs, ha="center", va="center",
                bbox=dict(fc="white", ec="none", pad=0.6))


def lollipop(ax, x, y, label, side="up"):
    # provided interface: small circle on a stick
    dy = 0.35 if side == "up" else -0.35
    ax.plot([x, x], [y, y + dy], color="#222", lw=1)
    ax.add_patch(plt.Circle((x, y + dy + (0.09 if side == "up" else -0.09)), 0.09, fc="white", ec="#222", lw=1))
    ax.text(x + 0.15, y + dy + (0.09 if side == "up" else -0.09), label, fontsize=6.5, va="center")



# ---------------------------------------------------------------- sequence diagram engine
def sequence(fname, title, parts, msgs, width=14, actor_idx=(0,), frames=()):
    n = len(parts)
    rows = len(msgs)
    H = rows * 0.62 + 2.9 + 0.95 * len(frames) + 0.3 * sum(len(f[5::2]) for f in frames) + 0.3 * sum(1 for m in msgs if m[0] == m[1])
    fig, ax = plt.subplots(figsize=(width, H * 0.62))
    ax.set_xlim(0, width); ax.set_ylim(0, H); ax.axis("off")
    ax.text(width / 2, H - 0.25, title, ha="center", fontsize=12, weight="bold")
    xs = [1.3 + i * (width - 2.6) / (n - 1) for i in range(n)]
    top = H - 1.0
    bottom = 0.3
    for i, (p, x) in enumerate(zip(parts, xs)):
        if i in actor_idx:
            # stick figure
            cy = top + 0.05
            ax.add_patch(plt.Circle((x, cy + 0.42), 0.13, fc="white", ec="#222", lw=1))
            ax.plot([x, x], [cy + 0.29, cy + 0.02], color="#222", lw=1)
            ax.plot([x - 0.18, x + 0.18], [cy + 0.2, cy + 0.2], color="#222", lw=1)
            ax.plot([x, x - 0.15], [cy + 0.02, cy - 0.2], color="#222", lw=1)
            ax.plot([x, x + 0.15], [cy + 0.02, cy - 0.2], color="#222", lw=1)
            ax.text(x, cy - 0.3, p, ha="center", va="top", fontsize=8, weight="bold")
            ystart = cy - 0.3 - 0.3 * (p.count(chr(10)) + 1)
        else:
            bw = 1.75
            ax.add_patch(Rectangle((x - bw / 2, top - 0.35), bw, 0.75, fc="#EAF2FB", ec="#222", lw=1))
            ax.text(x, top + 0.02, p, ha="center", va="center", fontsize=7.6, weight="bold")
            ystart = top - 0.35
        ax.plot([x, x], [ystart, bottom], color="#777", lw=0.9, ls=(0, (4, 3)))
    y = top - 0.95 - 0.3 * max(parts[i].count(chr(10)) for i in actor_idx)
    frame_rows = {f[0]: f for f in frames}
    open_frames = []
    for idx, m in enumerate(msgs):
        if idx in frame_rows:
            f = frame_rows[idx]
            y -= 0.35
            open_frames.append((f, y + 0.67))
        for f in frames:
            # f[5:] holds (divider_index, label) pairs for alt/else operands
            for di, dl in zip(f[5::2], f[6::2]):
                if di == idx:
                    ax.plot([xs[f[3]] - 0.95, xs[f[4]] + 0.95], [y + 0.3, y + 0.3], color="#B05", lw=1, ls=(0, (5, 3)))
                    ax.text(xs[f[3]] - 0.85, y + 0.12, dl, fontsize=7, color="#B05", style="italic", va="center")
                    y -= 0.3
        a, b, text, kind = m
        if kind == "sep":
            ax.plot([xs[0] - 0.9, xs[-1] + 0.9], [y, y], color="#888", lw=0.9, ls=(0, (2, 2)))
            ax.text(width / 2, y, text, fontsize=8, ha="center", va="center", weight="bold",
                    bbox=dict(fc="#F3F3F3", ec="#888", pad=2.5))
            y -= 0.62
            continue
        if a == b:
            x = xs[a]
            ax.plot([x, x + 0.45, x + 0.45, x], [y + 0.12, y + 0.12, y - 0.18, y - 0.18], color="#222", lw=1)
            ax.annotate("", xy=(x, y - 0.18), xytext=(x + 0.2, y - 0.18), arrowprops=dict(arrowstyle="-|>", color="#222", lw=1))
            ax.text(x + 0.55, y - 0.03, text, fontsize=7.2, va="center")
            y -= 0.3
        else:
            xa, xb = xs[a], xs[b]
            ret = kind == "ret"
            ax.annotate("", xy=(xb, y), xytext=(xa, y),
                        arrowprops=dict(arrowstyle="->" if ret else "-|>", color="#222", lw=1,
                                        linestyle=(0, (4, 3)) if ret else "-", shrinkA=0, shrinkB=0))
            ax.text((xa + xb) / 2, y + 0.14, text, fontsize=7.2, ha="center", va="bottom")
        y -= 0.62
        # close frames ending at this index
        for of in list(open_frames):
            f, ytop = of
            if f[1] == idx:
                x0 = xs[f[3]] - 0.95; x1 = xs[f[4]] + 0.95
                ax.add_patch(Rectangle((x0, y + 0.3), x1 - x0, ytop - (y + 0.3), fc="none", ec="#B05", lw=1))
                ax.add_patch(Rectangle((x0, ytop - 0.3), 0.75, 0.3, fc="#FBE3EE", ec="#B05", lw=1))
                ax.text(x0 + 0.37, ytop - 0.15, f[2].split(" ")[0], fontsize=7, ha="center", va="center", weight="bold")
                ax.text(x0 + 0.85, ytop - 0.15, " ".join(f[2].split(" ")[1:]), fontsize=7, va="center", style="italic", color="#B05")
                open_frames.remove(of)
                y -= 0.3
    fig.savefig(OUT + fname, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)



# ---------------------------------------------------------------- component diagram
def component_diagram():
    fig, ax = plt.subplots(figsize=(13, 10.5))
    ax.set_xlim(0, 26); ax.set_ylim(0, 21); ax.axis("off")
    ax.text(13, 20.6, "Vehicle Parking System – UML Component Diagram", ha="center", fontsize=13, weight="bold")

    # Presentation layer
    package(ax, 0.5, 16.2, 25, 3.6, "Presentation Layer  –  React.js SPA (Browser)", "#EAF2FB")
    ui = [("Login & Session UI", 1.0), ("Parking Attendant UI", 7.1), ("Administrator UI", 13.2), ("API Client\n(Axios + Auth Context)", 19.3)]
    uib = {}
    for n, x in ui:
        uib[n] = component(ax, x, 16.7, 5.6, 1.5, n, fc="#FFFFFF")
    for n in ui[:3]:
        bx = uib[n[0]]
        ax.plot([bx[0] + bx[2] / 2, bx[0] + bx[2] / 2], [18.2, 18.6], color="#222", lw=1, ls=(0, (4, 3)))
    ax.plot([3.8, 22.1], [18.6, 18.6], color="#222", lw=1, ls=(0, (4, 3)))
    arrow(ax, (22.1, 18.6), (22.1, 18.2), dashed=True)
    ax.text(13, 18.75, "«use»", ha="center", fontsize=7, style="italic")
    ax.text(13, 19.35, "Role-based navigation: only the functions permitted to the logged-in role are shown (SRS 3.1)",
            ha="center", fontsize=7.5, style="italic")

    # Application layer
    package(ax, 0.5, 4.2, 25, 10.9, "Application Layer  –  Node.js + Express.js REST API Server", "#EEF8EE")
    component(ax, 1.0, 12.6, 11.6, 1.4, "Application / API Layer (Router, Controllers, Error Handler)", fc="#FFFDE8", fs=8.2)
    component(ax, 13.4, 12.6, 11.6, 1.4, "Security Middleware (AuthN, Session, RBAC, Validation)", fc="#FFF0E0", fs=8.2)
    arrow(ax, (12.6, 13.3), (13.4, 13.3), dashed=False)
    lollipop(ax, 6.8, 14.0, "REST /api/v1 (HTTPS, JSON)")

    svcs = [("Auth\nService", 1.0, 9.6), ("User Management\nService", 5.9, 9.6), ("Vehicle\nService", 10.8, 9.6),
            ("Parking Slot\nService", 15.7, 9.6), ("Parking Transaction\nService", 20.6, 9.6),
            ("Report\nService", 15.7, 6.9), ("Fee\nService", 20.6, 6.9)]
    for n, x, y in svcs:
        component(ax, x, y, 4.4, 1.9, n, fc="white", fs=8)
    for n, x, y in svcs[:5]:
        arrow(ax, (x + 2.2, 12.6), (x + 2.2, y + 1.9))
    ax.text(13, 12.25, "controllers delegate to services through defined service interfaces", fontsize=7,
            ha="center", style="italic", bbox=dict(fc="#EEF8EE", ec="none", pad=0.5))
    # service-to-service dependencies
    arrow(ax, (22.8, 9.6), (22.8, 8.8))
    ax.text(23.0, 9.2, "calculate fee", fontsize=6.3, style="italic", ha="left")
    arrow(ax, (20.6, 10.9), (20.1, 10.9))
    ax.text(20.35, 11.75, "allocate /\nrelease slot", fontsize=6.3, style="italic", ha="center")

    component(ax, 1.0, 4.6, 24.0, 1.4, "Database Layer – Mongoose ODM models & repositories (users, sessions, vehicles, slots, parkingRecords, feeRates, counters)", fc="#FFFDE8", fs=8.0)
    for n, x, y in svcs[5:]:
        arrow(ax, (x + 2.2, y), (x + 2.2, 6.0))
    for x in (1.0, 5.9, 10.8):
        arrow(ax, (x + 2.2, 9.6), (x + 2.2, 6.0))

    # Data layer
    package(ax, 0.5, 0.3, 25, 3.0, "Data Layer", "#FBEFE6")
    component(ax, 9.25, 0.75, 7.5, 1.6, "MongoDB (Replica Set)", stereo="«database»", fc="white")
    arrow(ax, (13.0, 4.6), (13.0, 2.35), "MongoDB driver (TLS, write concern majority)", dashed=True, lo=(3.0, 0.4))

    arrow(ax, (22.1, 16.7), (22.1, 14.0), "HTTPS + JSON", dashed=False, lo=(1.3, 0.6))
    fig.savefig(OUT + "component.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- sequence diagrams
def seq_entry():
    P = ["Parking\nAttendant", "React SPA", "Security\nMiddleware", "Parking Transaction\nService", "Parking Slot\nService", "MongoDB"]
    M = [
        (0, 1, "1: search vehicle by reg. no., click Record Entry (optional: choose slot)", "call"),
        (1, 2, "2: POST /api/v1/parking/entry {vehicleId, slotId?}  + Bearer token", "call"),
        (2, 2, "3: check session (not idle > 15 min), role ∈ {ATTENDANT, ADMIN}, validate body", "self"),
        (2, 3, "4: recordEntry(vehicleId, slotId?, attendantId)", "call"),
        (3, 5, "5: find Active parking record for vehicle", "call"),
        (5, 3, "6: none (else 409 VEHICLE_ALREADY_PARKED)", "ret"),
        (3, 5, "7: startTransaction()", "call"),
        (3, 4, "8: allocate(vehicleType, slotId?)", "call"),
        (4, 5, "9: findOneAndUpdate(Available + type → Occupied, lowest slotId)", "call"),
        (5, 4, "10: slot A-01", "ret"),
        (4, 3, "11: slot A-01", "ret"),
        (3, 5, "12: insert parkingRecord {ticketNo, vehicleId, slotId, entryTime, status:Active}; commit", "call"),
        (3, 1, "13: 201 Created {ticketNo, slotId, entryTime}", "ret"),
        (1, 0, "14: show ticket number and slot", "ret"),
        (5, 4, "10a: no matching Available slot (null)", "ret"),
        (3, 1, "13a: 409 {NO_SLOT_AVAILABLE} → abortTransaction()", "ret"),
        (1, 0, "14a: 'No parking slot available for this vehicle type'", "ret"),
        (5, 3, "12b: write conflict / unique-index violation (concurrent entry)", "ret"),
        (3, 1, "13b: 409 {SLOT_CONFLICT_RETRY} → abortTransaction()", "ret"),
        (1, 0, "14b: 'Slot was just taken – please retry'", "ret"),
    ]
    sequence("seq_entry.png", "Sequence Diagram 1 – Record Vehicle Entry & Allocate Slot (FR-11 – FR-14, NFR-04)", P, M,
             width=15, frames=[(9, 19, "alt [matching slot found and committed]", 0, 5, 14,
                                "[else: no Available slot of this type]", 17, "[else: concurrent entry took the slot]")])


def seq_exit():
    P = ["Parking\nAttendant", "React SPA", "Security\nMiddleware", "Parking Transaction\nService", "Fee\nService", "Parking Slot\nService", "MongoDB"]
    M = [
        (0, 0, "STEP 1 – RECORD EXIT AND SHOW FEE SUMMARY", "sep"),
        (0, 1, "1: search vehicle, click Record Exit", "call"),
        (1, 2, "2: POST /api/v1/parking/exit {vehicleId}", "call"),
        (2, 3, "3: recordExit(vehicleId)   [role ∈ {ATTENDANT, ADMIN}]", "call"),
        (3, 6, "4: find Active record (else 404 NO_ACTIVE_RECORD); set exitTime = server time", "call"),
        (3, 4, "5: calculateFee(vehicleType, entryTime, exitTime)", "call"),
        (4, 6, "6: read current hourly rate for the vehicle type", "call"),
        (4, 4, "7: billable = d ≤ 15 ? 0 : ceil((d − 15)/60);  fee = billable × hourlyRate", "self"),
        (4, 3, "8: {durationMin, billableHours, fee}", "ret"),
        (3, 1, "9: 200 {ticketNo, entryTime, exitTime, duration, fee}", "ret"),
        (1, 0, "10: show summary (FR-17)", "ret"),
        (0, 0, "STEP 2 – CONFIRM EXIT", "sep"),
        (0, 1, "11: click Confirm Exit", "call"),
        (1, 2, "12: POST /api/v1/parking/{ticketNo}/confirm-exit", "call"),
        (2, 3, "13: confirmExit(ticketNo)", "call"),
        (3, 6, "14: startTransaction(); record → Completed with fee", "call"),
        (3, 5, "15: release(slotId)", "call"),
        (5, 6, "16: slot status → Available; commit (write concern majority)", "call"),
        (3, 1, "17: 200 {ticketNo, fee, status: Completed}", "ret"),
        (1, 0, "18: exit complete – collect fee at counter", "ret"),
    ]
    sequence("seq_exit.png", "Sequence Diagram 2 – Record Vehicle Exit, Calculate Fee & Release Slot (FR-15 – FR-18)", P, M,
             width=15)


def seq_login():
    P = ["User\n(Attendant / Admin)", "React SPA", "Security\nMiddleware", "Auth\nService", "MongoDB"]
    M = [
        (0, 0, "LOGIN", "sep"),
        (0, 1, "1: enter username + password", "call"),
        (1, 2, "2: POST /api/v1/auth/login {username, password}", "call"),
        (2, 2, "3: validate type / length / format (SEC-05)", "self"),
        (2, 3, "4: login(username, password)", "call"),
        (3, 4, "5: find active user by username", "call"),
        (4, 3, "6: user {passwordHash, role}  (or none)", "ret"),
        (3, 3, "7: bcrypt.compare(password, passwordHash)", "self"),
        (3, 4, "8: insert session {jti, userId, lastActivityAt}", "call"),
        (3, 1, "9: 200 {token (JWT with jti), user {username, role}}", "ret"),
        (1, 0, "10: open role home page", "ret"),
        (3, 1, "9a: 401 'Invalid username or password'", "ret"),
        (1, 0, "10a: show the same generic message (FR-02)", "ret"),
        (0, 0, "EVERY LATER REQUEST", "sep"),
        (1, 2, "11: any request + Bearer token", "call"),
        (2, 4, "12: find session by jti", "call"),
        (2, 2, "13: revoked or idle > 15 min → 401 (FR-03, SEC-06); else lastActivityAt = now", "self"),
        (0, 0, "LOGOUT", "sep"),
        (1, 2, "14: POST /api/v1/auth/logout", "call"),
        (2, 4, "15: session.revoked = true", "call"),
        (2, 1, "16: 200 – token no longer accepted", "ret"),
    ]
    sequence("seq_login.png", "Sequence Diagram 3 – Login, Session Timeout & Logout (FR-01 – FR-03, SEC-03, SEC-06)", P, M,
             width=14, frames=[(8, 12, "alt [user found and password matches]", 0, 4, 11, "[else]")])


def seq_search():
    P = ["Parking\nAttendant", "React SPA", "Security\nMiddleware", "Vehicle\nService", "Parking Transaction\nService", "MongoDB"]
    M = [
        (0, 1, "1: enter registration number", "call"),
        (1, 2, "2: GET /api/v1/vehicles/search?regNo=KA01AB1234", "call"),
        (2, 2, "3: authenticate; role ∈ {ATTENDANT, ADMIN}", "self"),
        (2, 3, "4: search(regNo)", "call"),
        (3, 5, "5: find vehicle by regNo (upper case)", "call"),
        (5, 3, "6: vehicle {_id, regNo, vehicleType}  (or none → 404)", "ret"),
        (3, 4, "7: getCurrentStatus(vehicleId)", "call"),
        (4, 5, "8: find Active parking record", "call"),
        (4, 3, "9: Parked {slotId, entryTime, elapsed} | Not Parked", "ret"),
        (3, 4, "10: getHistory(vehicleId)  (Completed records, newest first)", "call"),
        (4, 3, "11: [{entryTime, exitTime, slotId, fee}]", "ret"),
        (3, 1, "12: 200 {vehicle, status, history}   or   404 VEHICLE_NOT_FOUND", "ret"),
        (1, 0, "13: show status and history (FR-21, FR-22)", "ret"),
    ]
    sequence("seq_search.png", "Sequence Diagram 4 – Search & Track a Vehicle (FR-20 – FR-22, NFR-01)", P, M, width=14)


def deployment():
    fig, ax = plt.subplots(figsize=(13, 6.0))
    ax.set_xlim(0, 26); ax.set_ylim(0, 12); ax.axis("off")
    ax.text(13, 11.6, "Vehicle Parking System – Deployment View", ha="center", fontsize=13, weight="bold")

    def node(x, y, w, h, title, items, fc):
        d = 0.35
        ax.add_patch(plt.Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)], fc="#ddd", ec="#222"))
        ax.add_patch(plt.Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)], fc="#ccc", ec="#222"))
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#222", lw=1.2))
        ax.text(x + w / 2, y + h - 0.65, title, ha="center", va="center", fontsize=8.3, weight="bold")
        for i, it in enumerate(items):
            ax.add_patch(Rectangle((x + 0.3, y + h - 2.0 - i * 0.85), w - 0.6, 0.65, fc="white", ec="#555"))
            ax.text(x + w / 2, y + h - 1.67 - i * 0.85, it, ha="center", va="center", fontsize=7.5)

    node(0.6, 3.2, 6.0, 4.9, "«device» Client Device\n(Web browser, ≥ 360 px wide)", ["React SPA bundle", "Attendant / Admin UI", "Token kept in memory only"], "#EAF2FB")
    node(9.0, 1.2, 7.0, 7.9, "«execution env» Application Server\n(Ubuntu 22.04 LTS, Node.js LTS)", ["Nginx: TLS 1.2+, HTTP → HTTPS", "Static React build (dist/)", "Express REST API (PM2)", "Security middleware", "Winston logs (no passwords)", ".env: DB URI, JWT secret"], "#EEF8EE")
    node(18.8, 2.0, 6.4, 6.0, "«database server»\nMongoDB (3-member Replica Set)", ["Primary", "2 × Secondary", "Journaled, majority writes", "Daily backup (mongodump)"], "#FBEFE6")
    arrow(ax, (6.95, 5.6), (9.0, 5.6), "HTTPS (443)\nJSON / REST", dashed=False, lo=(0, 0.8))
    arrow(ax, (16.35, 5.0), (18.8, 5.0), "MongoDB wire\nprotocol, TLS + auth", dashed=False, lo=(0, 0.8))
    fig.savefig(OUT + "deployment.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    component_diagram()
    seq_entry()
    seq_exit()
    seq_login()
    seq_search()
    deployment()
    print("done")
