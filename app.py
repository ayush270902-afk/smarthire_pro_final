from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

# ---------- DATABASE ----------
def db():
    conn = sqlite3.connect("database.db", timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- AUTH ----------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        u = request.form['username']
        p = request.form['password']

        con = db()

        cur = con.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        ).fetchone()

        con.close()

        if cur:
            session['user'] = u
            session['role'] = cur['role']
            return redirect('/')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ---------- DASHBOARD ----------
@app.route('/')
def index():

    if 'user' not in session:
        return redirect('/login')

    con = db()

    jobs = con.execute(
        "SELECT count(*) as c FROM jobs"
    ).fetchone()['c']

    cand = con.execute(
        "SELECT count(*) as c FROM candidates"
    ).fetchone()['c']

    offers = con.execute(
        "SELECT count(*) as c FROM offers"
    ).fetchone()['c']

    con.close()

    return render_template(
        'dashboard.html',
        jobs=jobs,
        cand=cand,
        offers=offers,
        role=session['role']
    )


# ---------- JOB ----------
@app.route('/jobs', methods=['GET', 'POST'])
def jobs():

    con = db()

    if request.method == 'POST':

        con.execute(
            "INSERT INTO jobs(title,dept) VALUES(?,?)",
            (request.form['title'], request.form['dept'])
        )

        con.commit()

    data = con.execute("SELECT * FROM jobs").fetchall()

    con.close()

    return render_template('jobs.html', data=data)


# ---------- CANDIDATE ----------
@app.route('/candidates', methods=['GET', 'POST'])
def candidates():

    con = db()

    if request.method == 'POST':

        con.execute(
            "INSERT INTO candidates(name,skill,status) VALUES(?,?,?)",
            (
                request.form['name'],
                request.form['skill'],
                "Applied"
            )
        )

        con.commit()

    data = con.execute("SELECT * FROM candidates").fetchall()

    con.close()

    return render_template('candidates.html', data=data)


# ---------- PIPELINE ----------
@app.route('/pipeline')
def pipeline():

    con = db()

    data = con.execute(
        "SELECT * FROM candidates"
    ).fetchall()

    con.close()

    return render_template('pipeline.html', data=data)


@app.route('/update_status/<int:id>/<status>')
def update_status(id, status):

    con = db()

    con.execute(
        "UPDATE candidates SET status=? WHERE id=?",
        (status, id)
    )

    con.commit()

    con.close()

    return redirect('/pipeline')


# ---------- INTERVIEW ----------
@app.route('/schedule', methods=['GET', 'POST'])
def schedule():

    con = db()

    if request.method == 'POST':

        con.execute(
            "INSERT INTO interviews(name,date) VALUES(?,?)",
            (
                request.form['name'],
                request.form['date']
            )
        )

        con.commit()

    data = con.execute(
        "SELECT * FROM interviews"
    ).fetchall()

    con.close()

    return render_template('schedule.html', data=data)


# ---------- OFFER ----------
@app.route('/offers', methods=['GET', 'POST'])
def offers():

    con = db()

    if request.method == 'POST':

        con.execute(
            "INSERT INTO offers(name,role,status) VALUES(?,?,?)",
            (
                request.form['name'],
                request.form['role'],
                "Sent"
            )
        )

        con.commit()

    data = con.execute(
        "SELECT * FROM offers"
    ).fetchall()

    con.close()

    return render_template('offers.html', data=data)


# ---------- ANALYTICS ----------
@app.route('/analytics')
def analytics():

    con = db()

    total = con.execute(
        "SELECT count(*) as c FROM candidates"
    ).fetchone()['c']

    selected = con.execute(
        "SELECT count(*) as c FROM candidates WHERE status='Selected'"
    ).fetchone()['c']

    rejected = con.execute(
        "SELECT count(*) as c FROM candidates WHERE status='Rejected'"
    ).fetchone()['c']

    con.close()

    return render_template(
        'analytics.html',
        total=total,
        selected=selected,
        rejected=rejected
    )


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)