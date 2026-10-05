"""Regenerates the UML diagrams in docs/diagrams/ (requires: pip install matplotlib)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

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


# ---------------------------------------------------------------- component diagram
def component_diagram():
    fig, ax = plt.subplots(figsize=(13, 10.5))
    ax.set_xlim(0, 26); ax.set_ylim(0, 21); ax.axis("off")
    ax.text(13, 20.6, "Vehicle Parking System – UML Component Diagram", ha="center", fontsize=13, weight="bold")

    # Presentation tier
    package(ax, 0.5, 16.2, 25, 3.6, "Presentation Tier  –  React SPA (Browser)", "#EAF2FB")
    ui = [("Driver Portal UI", 1.0), ("Attendant Console UI", 7.1), ("Admin Dashboard UI", 13.2), ("API Client & Socket Client", 19.3)]
    uib = {}
    for n, x in ui:
        uib[n] = component(ax, x, 16.7, 5.6, 1.5, n, fc="#FFFFFF")
    for n in ui[:3]:
        bx = uib[n[0]]
        ax.plot([bx[0] + bx[2] / 2, bx[0] + bx[2] / 2], [18.2, 18.6], color="#222", lw=1, ls=(0, (4, 3)))
    ax.plot([3.8, 22.1], [18.6, 18.6], color="#222", lw=1, ls=(0, (4, 3)))
    arrow(ax, (22.1, 18.6), (22.1, 18.2), dashed=True)
    ax.text(13, 18.75, "«use»", ha="center", fontsize=7, style="italic")
    ax.text(13, 19.35, "Shared modules: Auth Context (access token in memory) · Role-based Route Guards · Live Slot Map (Socket.IO)", ha="center", fontsize=7.5, style="italic")

    # Application tier
    package(ax, 0.5, 4.2, 25, 10.9, "Application Tier  –  Node.js + Express.js REST API Server", "#EEF8EE")
    gw = component(ax, 1.0, 12.6, 24.0, 1.4, "API Layer: Router + Middleware (Helmet, CORS, Rate Limiter, JWT Auth, RBAC, Input Validation, Error Handler)", fc="#FFFDE8", fs=8.2)
    lollipop(ax, 12.0, 14.0, "REST /api/v1  (HTTPS)")
    lollipop(ax, 21.5, 14.0, "WebSocket (Socket.IO)")

    svcs = [("Auth & User\nService", 1.0, 9.6), ("Slot Management\nService", 5.9, 9.6), ("Booking\nService", 10.8, 9.6),
            ("Parking Session\n(Entry/Exit) Service", 15.7, 9.6), ("Billing & Payment\nService", 20.6, 9.6),
            ("Vehicle Tracking\nService", 1.0, 6.9), ("Reporting &\nAnalytics Service", 5.9, 6.9), ("Notification\nService", 10.8, 6.9),
            ("Audit Logging\nService", 15.7, 6.9), ("Scheduler (Booking\nExpiry Job)", 20.6, 6.9)]
    sb = {}
    for n, x, y in svcs:
        sb[n.split("\n")[0]] = component(ax, x, y, 4.4, 1.9, n, fc="white", fs=8)
    # API layer -> services
    for n, x, y in svcs[:5]:
        arrow(ax, (x + 2.2, 12.6), (x + 2.2, y + 1.9))
    ax.text(13, 12.25, "delegates to service layer (controllers call services)", fontsize=7, ha="center", style="italic",
            bbox=dict(fc="#EEF8EE", ec="none", pad=0.5))

    dal = component(ax, 1.0, 4.6, 24.0, 1.4, "Data Access Layer – Mongoose ODM Models & Repositories (User, ParkingLot, Slot, Tariff, Booking, ParkingSession, Payment, AuditLog)", fc="#FFFDE8", fs=8.2)
    for n, x, y in svcs[5:]:
        arrow(ax, (x + 2.2, y), (x + 2.2, 6.0))

    # Data tier + external
    package(ax, 0.5, 0.3, 11.5, 3.0, "Data Tier", "#FBEFE6")
    db = component(ax, 2.5, 0.75, 7.5, 1.6, "MongoDB (Replica Set)", stereo="«database»", fc="white")
    arrow(ax, (6.25, 4.6), (6.25, 2.35), "Mongoose driver (TLS)", dashed=True, lo=(1.6, 0.4))

    package(ax, 13.0, 0.3, 12.5, 3.0, "External Systems", "#F2ECF8")
    pg = component(ax, 19.5, 0.75, 5.6, 1.6, "Payment Gateway", stereo="«external» (Razorpay test mode)", fc="white", fs=8)
    em = component(ax, 13.5, 0.75, 5.6, 1.6, "Email (SMTP) Server", stereo="«external»", fc="white", fs=8)
    arrow(ax, (22.8, 9.6), (22.3, 2.35), "HTTPS order / verify", lo=(0.3, -2.9))
    arrow(ax, (13.6, 6.9), (16.3, 2.35), "SMTP (Nodemailer)", lo=(0.6, -1.6))

    # client -> API
    arrow(ax, (22.1, 16.7), (22.1, 14.55), "HTTPS JSON + WSS", dashed=False, lo=(1.6, 0.4))
    fig.savefig(OUT + "component.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- sequence diagram engine
def sequence(fname, title, parts, msgs, width=14, actor_idx=(0,), frames=()):
    n = len(parts)
    rows = len(msgs)
    H = rows * 0.62 + 2.6 + 0.95 * len(frames) + 0.3 * sum(1 for m in msgs if m[0] == m[1])
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
    y = top - 0.95
    for fr in frames:
        pass
    frame_rows = {f[0]: f for f in frames}
    open_frames = []
    for idx, m in enumerate(msgs):
        if idx in frame_rows:
            f = frame_rows[idx]
            y -= 0.35
            open_frames.append((f, y + 0.67))
        for f in frames:
            if len(f) > 5 and f[5] == idx:
                ax.plot([xs[f[3]] - 0.95, xs[f[4]] + 0.95], [y + 0.3, y + 0.3], color="#B05", lw=1, ls=(0, (5, 3)))
                ax.text(xs[f[3]] - 0.85, y + 0.12, f[6], fontsize=7, color="#B05", style="italic", va="center")
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


def seq_booking():
    P = ["Driver", "React SPA", "API Layer\n(Auth+RBAC+Validate)", "Booking\nService", "Slot Mgmt\nService", "MongoDB", "Notification\nService"]
    M = [
        (0, 1, "1: select lot, vehicle type, time window", "call"),
        (1, 2, "2: GET /api/v1/slots/availability?lotId&type&from&to", "call"),
        (2, 4, "3: getAvailableSlots(lotId, type, from, to)", "call"),
        (4, 5, "4: find slots with no overlapping active booking", "call"),
        (5, 4, "5: slot list", "ret"),
        (4, 1, "6: 200 OK {slots[]}", "ret"),
        (0, 1, "7: choose slot & confirm", "call"),
        (1, 2, "8: POST /api/v1/bookings {slotId, vehicleNo, from, to}  + Bearer JWT", "call"),
        (2, 2, "9: verify JWT, role = DRIVER, validate body", "self"),
        (2, 3, "10: createBooking(userId, dto)", "call"),
        (3, 5, "11: startTransaction(); check overlap on slotId", "call"),
        (5, 3, "12: no conflict", "ret"),
        (3, 5, "13: insert Booking{status:CONFIRMED, code}; commit", "call"),
        (5, 3, "14: bookingId", "ret"),
        (3, 6, "15: notify(bookingConfirmed) – email + socket 'slot:update'", "call"),
        (3, 1, "16: 201 Created {bookingId, code, slot, amountEstimate}", "ret"),
        (1, 0, "17: show confirmation + booking code", "ret"),
        (5, 3, "12a: overlap found → abortTransaction()", "ret"),
        (3, 1, "16a: 409 Conflict {SLOT_ALREADY_BOOKED}", "ret"),
        (1, 0, "17a: 'Slot just got booked – pick another'", "ret"),
    ]
    sequence("seq_booking.png", "Sequence Diagram 1 – Reserve a Parking Slot (VPS-F-03, VPS-F-04)", P, M,
             width=15, frames=[(10, 19, "alt [no overlapping booking]", 0, 6, 17, "[else: overlap found]")])


def seq_entry_exit():
    P = ["Parking\nAttendant", "Attendant\nConsole (SPA)", "API Layer\n(Auth+RBAC)", "Parking Session\nService", "Billing &\nPayment Svc", "MongoDB", "Payment\nGateway"]
    M = [
        (0, 0, "VEHICLE ENTRY (CHECK-IN)", "sep"),
        (0, 1, "1: enter vehicle no. (+ booking code if any)", "call"),
        (1, 2, "2: POST /api/v1/sessions/entry {vehicleNo, type, bookingCode?}", "call"),
        (2, 3, "3: checkIn(dto)  [role = ATTENDANT]", "call"),
        (3, 5, "4: validate booking / atomically pick free slot (findOneAndUpdate)", "call"),
        (5, 3, "5: slot → OCCUPIED", "ret"),
        (3, 5, "6: insert ParkingSession{entryTime, slotId, status:ACTIVE}", "call"),
        (3, 1, "7: 201 {sessionId, slotCode, entryTime}  + socket 'slot:update'", "ret"),
        (0, 0, "VEHICLE EXIT (CHECK-OUT, FEE & PAYMENT)", "sep"),
        (0, 1, "8: vehicle leaving – scan/enter vehicle no.", "call"),
        (1, 2, "9: POST /api/v1/sessions/{id}/exit", "call"),
        (2, 3, "10: checkOut(sessionId)", "call"),
        (3, 4, "11: calculateFee(session, tariff)", "call"),
        (4, 4, "12: hours = ceil((exit − entry − grace)/60); fee = base + rate × hours", "self"),
        (4, 3, "13: fee breakdown", "ret"),
        (3, 1, "14: 200 {fee, duration, paymentId}", "ret"),
        (1, 2, "15: POST /api/v1/payments/{id}/pay {mode: CASH | UPI | CARD}", "call"),
        (2, 4, "16: processPayment()", "call"),
        (4, 6, "17: create order & verify payment signature", "call"),
        (6, 4, "18: payment success", "ret"),
        (4, 5, "19: Payment PAID, Session CLOSED, Slot AVAILABLE (transaction)", "call"),
        (4, 1, "20: 200 {receiptNo, amount}  + socket 'slot:update'", "ret"),
        (1, 0, "21: print / show receipt, open gate", "ret"),
    ]
    sequence("seq_entry_exit.png", "Sequence Diagram 2 – Vehicle Entry, Exit, Fee Calculation & Payment (VPS-F-06/07/08)", P, M,
             width=15, frames=[(18, 19, "opt [mode = UPI or CARD]", 4, 6)])


def seq_login():
    P = ["User", "React SPA", "API Layer\n(Rate limiter+Validate)", "Auth & User\nService", "MongoDB", "Audit Log\nService"]
    M = [
        (0, 1, "1: enter email + password", "call"),
        (1, 2, "2: POST /api/v1/auth/login {email, password}", "call"),
        (2, 2, "3: rate-limit check (max 5 attempts / 15 min / IP+email)", "self"),
        (2, 3, "4: login(email, password)", "call"),
        (3, 4, "5: findUserByEmail(email)", "call"),
        (4, 3, "6: user {passwordHash, role, failedAttempts}", "ret"),
        (3, 3, "7: bcrypt.compare(password, passwordHash)", "self"),
        (3, 3, "8: sign access JWT (15 min) + refresh token (7 days)", "self"),
        (3, 5, "9: log LOGIN_SUCCESS", "call"),
        (3, 1, "10: 200 {accessToken, user{id, name, role}} + HttpOnly refresh cookie", "ret"),
        (1, 0, "11: redirect to role dashboard", "ret"),
        (3, 4, "8a: increment failedAttempts; lock account after 5", "call"),
        (3, 5, "9a: log LOGIN_FAILURE", "call"),
        (3, 1, "10a: 401 {INVALID_CREDENTIALS}  (generic message)", "ret"),
        (1, 0, "11a: show 'Invalid email or password'", "ret"),
    ]
    sequence("seq_login.png", "Sequence Diagram 3 – User Login & Token Issue (VPS-F-01, VPS-SEC-01)", P, M,
             width=14, frames=[(7, 14, "alt [password matches]", 0, 5, 11, "[else: password mismatch / user not found]")])


def deployment():
    fig, ax = plt.subplots(figsize=(13, 6.4))
    ax.set_xlim(0, 26); ax.set_ylim(0, 12.6); ax.axis("off")
    ax.text(13, 12.2, "Vehicle Parking System – Deployment View", ha="center", fontsize=13, weight="bold")

    def node(x, y, w, h, title, items, fc):
        d = 0.35
        ax.add_patch(plt.Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)], fc="#ddd", ec="#222"))
        ax.add_patch(plt.Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)], fc="#ccc", ec="#222"))
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#222", lw=1.2))
        ax.text(x + w / 2, y + h - 0.65, title, ha="center", va="center", fontsize=8.3, weight="bold")
        for i, it in enumerate(items):
            ax.add_patch(Rectangle((x + 0.3, y + h - 2.0 - i * 0.85), w - 0.6, 0.65, fc="white", ec="#555"))
            ax.text(x + w / 2, y + h - 1.67 - i * 0.85, it, ha="center", va="center", fontsize=7.5)

    node(0.4, 3.6, 5.6, 4.9, "«device» Client Device\n(Web Browser)", ["React SPA bundle", "Socket.IO client", "Driver / Attendant / Admin"], "#EAF2FB")
    node(7.6, 1.6, 6.6, 7.9, "«execution env» App Server\n(Ubuntu 22.04 LTS, Node.js 20 LTS)", ["Nginx reverse proxy (TLS 1.2+)", "Static React build (dist/)", "Express API (PM2 cluster mode)", "Socket.IO server", "node-cron scheduler", "Winston log files"], "#EEF8EE")
    node(16.4, 0.4, 4.8, 4.6, "«database server»\nMongoDB 7 (Replica Set)", ["Primary", "2 × Secondary", "Daily backup (mongodump)"], "#FBEFE6")
    node(16.4, 7.4, 4.8, 3.0, "«external system»\nPayment Gateway", ["Razorpay test-mode API"], "#F2ECF8")
    node(22.1, 7.4, 3.6, 3.0, "«external system»\nSMTP Mail Server", ["Email delivery"], "#F2ECF8")
    arrow(ax, (6.35, 6.0), (7.6, 6.0), "HTTPS / WSS\n:443", dashed=False, lo=(0, 0.8))
    arrow(ax, (14.55, 2.7), (16.4, 2.7), "TCP 27017\n(TLS + auth)", dashed=False, lo=(0, 0.8))
    arrow(ax, (14.55, 8.6), (16.4, 8.6), "HTTPS REST", dashed=False, lo=(0, 0.45))
    ax.plot([14.55, 15.3, 15.3, 23.9, 23.9], [6.6, 6.6, 6.4, 6.4, 6.6], color="#222", lw=1)
    arrow(ax, (23.9, 6.6), (23.9, 7.4), dashed=False)
    ax.text(19.6, 6.15, "SMTP + STARTTLS :587", fontsize=7, ha="center", va="center")
    fig.savefig(OUT + "deployment.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


component_diagram()
seq_booking()
seq_entry_exit()
seq_login()
deployment()
print("done")
