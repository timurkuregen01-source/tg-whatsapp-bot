import os
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

from services.database import (
    init_db,
    get_representatives,
    get_representative,
    add_representative,
    update_representative,
    delete_representative,
    toggle_status,
    reorder_representatives,
)
from services.telegram_bot import handle_update

# .env'i panel.py'nin yanından kesin yolla yükle (PythonAnywhere WSGI için önemli).
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

app = Flask(__name__)
app.secret_key = os.getenv("PANEL_SECRET_KEY", "amiral-dev-secret")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "")

# Veritabanını import anında hazırla — gunicorn/production'da __main__ çalışmaz.
init_db()


# --------------------------------------------------------------------- auth ---
def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapper


@app.context_processor
def inject_user():
    return {"current_user": session.get("username")}


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        valid = (
            username == ADMIN_USERNAME
            and ADMIN_PASSWORD_HASH
            and check_password_hash(ADMIN_PASSWORD_HASH, password)
        )
        if valid:
            session["logged_in"] = True
            session["username"] = username
            nxt = request.args.get("next") or url_for("dashboard")
            if not nxt.startswith("/"):
                nxt = url_for("dashboard")
            return redirect(nxt)

        flash("Kullanıcı adı veya parola hatalı.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış yapıldı.", "success")
    return redirect(url_for("login"))


# -------------------------------------------------------------------- helpers -
def _stats(reps):
    total = len(reps)
    online = len([r for r in reps if r["status"] == 1])
    return {
        "total": total,
        "online": online,
        "offline": total - online,
    }


# ---------------------------------------------------------------------- pages -
@app.route("/")
@login_required
def dashboard():
    reps = get_representatives()
    stats = _stats(reps)
    recent = list(reversed(reps))[:5]
    return render_template(
        "dashboard.html",
        active="dashboard",
        stats=stats,
        recent=recent,
    )


@app.route("/representatives")
@login_required
def representatives():
    reps = get_representatives()
    stats = _stats(reps)
    return render_template(
        "representatives.html",
        active="representatives",
        representatives=reps,
        stats=stats,
    )


@app.post("/representatives/add")
@login_required
def representatives_add():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    status = request.form.get("status", "1")

    if not name or not phone:
        flash("İsim ve telefon zorunludur.", "error")
        return redirect(url_for("representatives"))

    add_representative(name, phone, status)
    flash(f"{name} eklendi.", "success")
    return redirect(url_for("representatives"))


@app.post("/representatives/<int:rep_id>/edit")
@login_required
def representatives_edit(rep_id):
    if get_representative(rep_id) is None:
        flash("Temsilci bulunamadı.", "error")
        return redirect(url_for("representatives"))

    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    status = request.form.get("status", "1")

    if not name or not phone:
        flash("İsim ve telefon zorunludur.", "error")
        return redirect(url_for("representatives"))

    update_representative(rep_id, name, phone, status)
    flash(f"{name} güncellendi.", "success")
    return redirect(url_for("representatives"))


@app.post("/representatives/<int:rep_id>/delete")
@login_required
def representatives_delete(rep_id):
    rep = get_representative(rep_id)
    if rep is None:
        flash("Temsilci bulunamadı.", "error")
        return redirect(url_for("representatives"))

    delete_representative(rep_id)
    flash(f"{rep['name']} silindi.", "success")
    return redirect(url_for("representatives"))


@app.post("/representatives/<int:rep_id>/toggle")
@login_required
def representatives_toggle(rep_id):
    new_status = toggle_status(rep_id)
    if new_status is None:
        return jsonify(ok=False, error="not_found"), 404
    return jsonify(ok=True, status=new_status)


@app.post("/representatives/reorder")
@login_required
def representatives_reorder():
    data = request.get_json(silent=True) or {}
    order = data.get("order", [])
    try:
        ids = [int(x) for x in order]
    except (TypeError, ValueError):
        return jsonify(ok=False, error="bad_order"), 400
    reorder_representatives(ids)
    return jsonify(ok=True)


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", active="settings")


# --------------------------------------------------------------- telegram ----
# Telegram webhook'u — HERKESE AÇIK olmalı (Telegram çağırır), path'teki token
# ile korunur. Bot ile panel aynı process/DB'yi paylaşır.
@app.post("/webhook/<token>")
def telegram_webhook(token):
    if token != os.getenv("BOT_TOKEN", ""):
        return "forbidden", 403
    update = request.get_json(silent=True)
    if update:
        try:
            handle_update(update, base_url=request.host_url)
        except Exception:
            # Telegram'ı gereksiz retry döngüsüne sokmamak için her zaman 200 dön.
            pass
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
