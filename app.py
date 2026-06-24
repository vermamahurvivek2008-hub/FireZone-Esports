#===========================================
#firezone - esport
#===========================================
import random
import string
import requests
import os
from flask import Flask
from flask import flash, render_template_string, request, redirect, url_for, session
import sqlite3
import hashlib
from datetime import datetime, timedelta
from functools  import wraps
from flask import send_from_directory

def admin_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if "admin" not in session:
            return redirect("/admin")
        return f(*args,**kwargs)
    return wrap
#send otp
def send_otp(phone,otp):
    url = "https://control.msg91.com/api/v5/otp"
    payload = {
        "mobile" : "91" + phone,
        "otp" : otp
    }
    print(payload)
    headers = {
        "authkey" : "521131Tu34rRIuWj6a1a7314P1"
    }
    response = requests.post(url, data=payload, headers=headers)
    print("msg91 STATUS :", response.status_code)
    print("msg91 response :", response.text)
    requests.post(url, data=payload, headers=headers)
    def db_connect():
        return sqlite3.connect("database.db")
def db_connect():
    return sqlite3.connect("database.db")
def fetch_one(query,params=()):
    conn = db_connect()
    c = conn.cursor()
    c.execute(query,params)
    data = c.fetchone()
    conn.close()
    return data

# =========================================
# APP START
# =========================================

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.secret_key = "firezone_secret"
@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json", mimetype="application/manifest+json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js", mimetype="application/javascript")

def generate_referral_code(username):
    random_part = ''.join(random.choices(string.digits, k=4))
    return username[:4].upper() + random_part


def update_referral_system():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute("ALTER TABLE users ADD COLUMN referral_code TEXT")
    except:
        pass

    try:
        c.execute("ALTER TABLE users ADD COLUMN referred_by TEXT")
    except:
        pass

    c.execute("""
    CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referrer_username TEXT,
        referred_username TEXT,
        referral_code TEXT,
        status TEXT DEFAULT 'PENDING',
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


update_referral_system()

ADMIN_USER = "admin"
ADMIN_PASS = "vivek123"
TEAM_USER = "team ff"
TEAM_PASS = "team2026"

START_HOUR = 8
END_HOUR = 23
GAP_MINUTES = 30

# =========================================

# STYLE

# =========================================

STYLE = """
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#ff3b00">

<script>
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/service-worker.js")
    .then(function() {
        console.log("Service Worker Registered");
    });
}
</script>

<style>


body{

    margin:0;

    padding:0;

    font-family: 'Arial Black', Arial, sans-serif;

    background: url('/static/images/bg.png') no-repeat center center fixed;

    background-size: cover;

    color:white;

    text-align:center;

}


/* DARK OVERLAY */

.overlay{

    min-height:100vh;

    background: rgba(0,0,0,0.75);

    padding:20px;

}


/* TITLE */

h1{

    font-size:34px;

    color:#00f7ff;

    text-shadow: 0px 0px 20px #00f7ff;

    margin-bottom:20px;

}


/* GLASS BOX */

.box{

    width:340px;

    margin:auto;

    margin-top:60px;

    background: rgba(0,0,0,0.7);

    padding:25px;

    border-radius:18px;

    box-shadow: 0px 0px 25px #00f7ff;

}


/* INFO CARD */

.info{

    background: rgba(255,255,255,0.08);

    margin:10px auto;

    padding:15px;

    border-radius:12px;

    width:320px;

    border:1px solid rgba(0,255,255,0.3);

}


/* MODE CARD */

.mode-card{

    width:320px;

    margin:20px auto;

    border-radius:18px;

    overflow:hidden;

    background: rgba(0,0,0,0.6);

    box-shadow: 0px 0px 18px #00f7ff;

    transition:0.3s;

}


.mode-card:hover{

    transform: scale(1.05);

    box-shadow: 0px 0px 30px #00f7ff;

}


.mode-card img{

    width:100%;

    height:180px;

    object-fit:cover;

}


/* MODE TITLE */

.mode-title{

    padding:12px;

    font-size:20px;

    font-weight:bold;

    color:#ffea00;

    text-shadow: 0px 0px 10px black;

}


.mode-title a{

    color:#ffea00;

    text-decoration:none;

}


/* INPUT */

input{

    width:90%;

    padding:12px;

    margin:8px 0;

    border:none;

    border-radius:10px;

    outline:none;

    font-size:15px;

}


/* BUTTON */

button{

    width:100%;

    padding:12px;

    background: linear-gradient(90deg,#00f7ff,#0066ff);

    border:none;

    border-radius:10px;

    color:white;

    font-weight:bold;

    cursor:pointer;

    transition:0.3s;

}


button:hover{

    background: linear-gradient(90deg,#0066ff,#00f7ff);

    transform: scale(1.03);

}


/* NAV BUTTON */

.mode-btn{

    display:block;

    width:260px;

    margin:15px auto;

    padding:14px;

    background: rgba(0,255,255,0.15);

    border:1px solid #00f7ff;

    border-radius:12px;

    color:white;

    text-decoration:none;

    font-weight:bold;

    transition:0.3s;

}


.mode-btn:hover{

    background: rgba(0,255,255,0.35);

    transform: scale(1.05);

}


/* LIST */

ul{

    list-style:none;

    padding:0;

}


li{

    background: rgba(255,255,255,0.08);

    margin:10px auto;

    width:320px;

    padding:15px;

    border-radius:12px;

    border:1px solid rgba(0,255,255,0.3);

}


/* GLOW ANIMATION */

@keyframes glow{

    0% { box-shadow: 0 0 10px #00f7ff; }

    50% { box-shadow: 0 0 25px #00f7ff; }

    100% { box-shadow: 0 0 10px #00f7ff; }

}


.box, .mode-card{

    animation: glow 2s infinite;

}




</style>
"""
RULES = """

<div class="mode-card">

<h2>📜 TOURNAMENT RULES</h2>

<br>

⚠️ Screen Recording Required

<br><br>

1️⃣ SNIPER & VECTOR Not Allowed

<br><br>

2️⃣ Team up with other players Not Allowed

<br><br>

3️⃣ Only mobile players allowed

<br><br>

4️⃣ Minimum level required : 40

<br><br>

5️⃣ Unregistered invites = kicked immediately

<br><br>

6️⃣ Room ID & Password shared 5 minutes before match

<br><br>

7️⃣ Screen recording mandatory for every player

<br><br>

8️⃣ POV not provided within 3 hours → action taken

<br><br>

9️⃣ Missed room join = No refund

<br><br>

🔟 Match suspension = 100% refund

<br><br>

1️⃣1️⃣ Hack / Panel / unfair use = Permanent Ban

<br><br>

1️⃣2️⃣ Result declared within 1 hour

<br><br>

1️⃣3️⃣ Multiple account not allowed

<br><br>

1️⃣4️⃣ No abusing / toxic behavior

<br><br>

1️⃣5️⃣ Admin decision final

</div>

"""

#   leaderboard

@app.route("/leaderboard")
def leaderboard():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        SELECT username, SUM(kills) as total_kills, SUM(reward) as total_reward
        FROM results
        GROUP BY username
        ORDER BY total_kills DESC
        LIMIT 10
    """)

    data = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🏆 LEADERBOARD</h1>

        <ul>
        {% for r in data %}
            <li>
                👤 {{r[0]}} <br><br>
                🔫 Kills: {{r[1]}} <br><br>
                💰 Earned: ₹{{r[2]}}
            </li>
        {% endfor %}
        </ul>

        <a class="mode-btn" href="/">BACK</a>

    </div>
    """, data=data)
#auto time calculate
def auto_format_slot(slot):

    slot = str(slot).strip().upper()

    if "AM" in slot or "PM" in slot:
        return slot

    now = datetime.now()

    try:
        input_time = datetime.strptime(slot, "%H:%M")
    except:
        return slot

    today_time = input_time.replace(
        year=now.year,
        month=now.month,
        day=now.day
    )

    # Agar time abhi se pehle nikal chuka hai,
    # to PM assume karo
    if today_time < now:
        return today_time.strftime("%I:%M PM")

    return today_time.strftime("%I:%M AM")
#normalize slot
def normalize_slot(slot):
    slot = str(slot).strip().upper()
    try:
        t = datetime.strptime(slot,"%I:%M:%P")
        return t.strftime("%I:%M:%P")    
    except:
        pass
    try:
        t = datetime.strptime(slot,"%I:%M:%P")
        return t.strptime("%I,%M,%P")
    except:
        pass
    return slot
# =========================================
# DATABASE
# =========================================

def init_db():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE tournament ADD COLUMN match_id INTEGER")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN banned INTEGER DEFAULT 0")
    except:
        pass

    c.execute("""
     CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    phone TEXT UNIQUE,
              game_name TEXT,
    referral_by TEXT
     )
      """)

    try:
        c.execute("ALTER TABLE users ADD COLUMN banned INTEGER DEFAULT 0")
    except:
        pass
    try:
        c.execute("ALTER TABLE users ADD COLUMN game_name TEXT")
    except:
        pass
    c.execute("""CREATE TABLE IF NOT EXISTS admin_rooms(id INTEGER PRIMARY KEY AUTOINCREMENT,
              mode TEXT,
              slot TEXT,
              room_id TEXT,
              password TEXT,
              UNIQUE(mode,slot)
              )"""
              )
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS wallet(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        balance INTEGER DEFAULT 0
    )
    """)

    c.execute("""
CREATE TABLE IF NOT EXISTS tournament(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    mode TEXT,
    slot TEXT,
    status TEXT DEFAULT 'UPCOMING'
)
""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS matches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mode TEXT,
        slot TEXT,
        room_id TEXT,
        password TEXT,
        status TEXT,
              entry_fee INTEGER,
              winning_prize INTEGER,
              created_by TEXT 
    )
    """)
    try:
        c.execute("ALTER TABLE matches ADD COLUMN created_by TEXT")
    except:
        pass
    c.execute("""
              CREATE TABLE IF NOT EXISTS custom_join(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT,
              room_id INTEGER )
              """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        mode TEXT,
        slot TEXT,
        kills INTEGER,
        reward INTEGER
    )
    """)
    
    c.execute(""" CREATE TABLE IF NOT EXISTS result_requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    mode TEXT,
    slot TEXT,
    kills INTEGER,
    reward INTEGER,
    screenshot TEXT,
    status TEXT DEFAULT 'PENDIND')
    """)

    try:
        c.execute("ALTER TABLE result_requests ADD COLUMN entry_fee INTEGER DEFAULT 0")
    except:
        pass

    try:
        c.execute("ALTER TABLE result_requests ADD COLUMN total_winners INTEGER DEFAULT 1")
    except:
        pass

    c.execute("""
CREATE TABLE IF NOT EXISTS withdrawal_requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    amount INTEGER,
    method TEXT,
    details TEXT,
    status TEXT DEFAULT 'PENDING'
)
""")

    try:
      c.execute("ALTER TABLE withdrawal_requests ADD COLUMN method TEXT")
    except:
      pass

    try:
      c.execute("ALTER TABLE withdrawal_requests ADD COLUMN details TEXT")
    except:
      pass
    try:
        c.execute("ALTER TABLE withdrawal_requests ADD COLUMN date TEXT")
    except:
        pass

    try:
        c.execute("ALTER TABLE withdrawal_requests ADD COLUMN time TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE withdrawal_requests ADD COLUMN qr_code TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE withdrawal_requests ADD COLUMN redeem_code TEXT")
    except:
        pass

    try:
        c.execute("ALTER TABLE withdrawal_requests ADD COLUMN transaction_code TEXT")
    except:
        pass

    try:
        c.execute("ALTER TABLE withdrawal_requests ADD COLUMN processed_date TEXT")
    except:
        pass

    try:
        c.execute("ALTER TABLE withdrawal_requests ADD COLUMN processed_time TEXT")
    except:
        pass


    c.execute("""
    CREATE TABLE IF NOT EXISTS daily_reward(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        current_day INTEGER DEFAULT 1,
        last_claim TEXT,
        recharge_active INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporter TEXT,
        reported_player TEXT,
        reason TEXT,
        status TEXT
    )
    """)

    c.execute("""
              CREATE TABLE IF NOT EXISTS notifications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# =========================================
# FUNCTIONS
# =========================================

def get_balance(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        "SELECT balance FROM wallet WHERE username=?",(username,)
    )
    data = c.fetchone()
    conn.close()
    if data:
        return data[0]
    return 0

def generate_slots():

    slots = []

    current = datetime.now().replace(
        hour=START_HOUR,
        minute=0,
        second=0,
        microsecond=0
    )

    end = current.replace(hour=END_HOUR)

    while current <= end:

        if current > datetime.now():
            slots.append(current.strftime("%I:%M %p"))

        current += timedelta(minutes=GAP_MINUTES)

    return slots
#delete old match
def delete_old_matches():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    now = datetime.now()

    c.execute("""
    SELECT id, slot
    FROM matches
    WHERE status!='COMPLETED'
    """)

    matches = c.fetchall()

    for m in matches:

        match_id = m[0]
        slot = str(m[1]).strip()

        try:
            if "AM" in slot.upper() or "PM" in slot.upper():
                slot_time = datetime.strptime(slot, "%I:%M %p")
            else:
                slot_time = datetime.strptime(slot, "%H:%M")

            slot_time = slot_time.replace(
                year=now.year,
                month=now.month,
                day=now.day
            )

            diff = (now - slot_time).total_seconds() / 60

            if diff >= 120:
                c.execute("""
                UPDATE matches
                SET status='COMPLETED'
                WHERE id=?
                """, (match_id,))

        except:
            pass

    conn.commit()
    conn.close()

#claim rewards
def can_claim_reward(username):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT last_claim
    FROM daily_reward
    WHERE username=?
    """,(username,))

    data = c.fetchone()

    conn.close()

    if not data:
        return True

    last_claim = datetime.strptime(
        data[0],
        "%Y-%m-%d"
    ).date()

    today = datetime.now().date()

    return today > last_claim


#count function
def get_count(mode, slot):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT COUNT(*)
    FROM tournament
    WHERE mode=? AND slot=?
    """, (mode, slot))

    count = c.fetchone()[0]

    conn.close()

    return count

def get_entry_fee(mode):

    if mode == "solo br":
        return 8

    elif mode == "duo br":
        return 8

    elif mode == "1v1 cs challenge":
        return 25

    elif mode == "2v2 cs challenge":
        return 25

    elif mode == "4v4 cs challenge":
        return 25

    elif mode == "lone wolf":
        return 25

    elif mode == "sniper only br":
        return 8

    elif mode == "booyah only br":
        return 8
    return 8

# =========================================
# HOME
# =========================================

@app.route("/")
def home():
    delete_old_matches()
    if "user" not in session:
        return redirect("/login")

    balance = get_balance(session["user"])

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>🔥 FIREZONE ESPORTS</h1>
        <div class="mode-card">
           <img src="/static/images/admin mode.png">
                                  <div class="mode-title">
                                  <a href="/admin_mode">
                                    ADMIN TOURNAMENT MODE
                                  </a>
                            </div>
                        </div>
        <div class="mode-card">
            <img src="/static/images/user mode.jpg">
                                  <div class="mode-title">
                                  <a href="/user_mode">
                                   USER CREATE ROOM MODE
                                  </a>
                                </div>
                            </div>
        <h3>balance:{{balance}}</h3>
        <a class="mode-btn" href="/recharge">RECHARGE</a>

        <a class="mode-btn" href="/withdrawal">WITHDRAWAL</a>

        <a class="mode-btn" href="/results">RESULTS</a>

        <a class="mode-btn" href="/profile">PROFILE</a>
                                  <a class="mode-btn" href="/support">SUPPORT</a>
                                  <a class="mode-btn" href="/report">REPORT PLAYER</a>
                                  <a class="mode-btn" href="/my_matches">MY MATCHES</a>
         <a class="mode-btn" href="/daily_reward">DAILY_REWARD</a>
        <a class="mode-btn" href="/leaderboard">LEADERBOARD</a>

                                  <a class="mode-btn" href="/notifications">NOTIFICATIONS</a>
                                  <br><br>

                                  <a href="/privacy" class="btn">Privacy Policy</a>

                                  <a href="/terms" class="btn">Terms & Conditions</a>

                                  <a href="/contact" class="btn">Contact</a>
                                  <a class="mode-btn" href="/logout">LOGOUT</a>

    </div>

    """,
    user=session["user"],
    balance=session.get("balance",0)
    )

#admin route
@app.route("/admin_mode")
def admin_mode():
    if "user" not in session:
        return redirect("/login")


    return render_template_string(STYLE + RULES + """

    <div class="overlay">

        <h1>🔥 ADMIN TOURNAMENT MODE 🔥</h1>


        <!-- SOLO BR -->

        <div class="mode-card">
        <img src="/static/images/solo br.png">
                                  <div class="mode-title">
                                  <a href="/mode/solo br">
                                       SOLO BR
                                  </a>
                        </div>
                    </div>


        <!-- DUO BR -->

        <div class="mode-card">

        <img src="/static/images/duo br.png">
                                  <div class="mode-title">
                                  <a href="/mode/duo br">

                DUO BR
                                  </a>
                        </div>
            </div>


        <!-- 1V1 -->

        <div class="mode-card">

            <img src="/static/images/1v1 cs challenge.png">
                                  <div class="mode-title">
                                  <a href="/mode/1v1 cs challenge">

            1v1 CS CHALLENGE
                                  </a>
                        </div>
            </div>


        <!-- 2V2 -->

        <div class="mode-card">

            <img src="/static/images/2v2 cs challenge.png">
                                  <div class="mode-title">
                                  <a href="/mode/2v2 cs challenge">

            2v2 CS CHALLENGE
                                  </a>
                        </div>
            </div>


        <!-- 4V4 -->

        <div class="mode-card">

            <img src="/static/images/4v4 cs challenge.png">
                                  <div class="mode-title">
                                  <a href="/mode/4v4 cs challenge">

            4v4 CS CHALLENGE
                                  </a>
                        </div>
            </div>


        <!-- LONE WOLF -->

        <div class="mode-card">

            <img src="/static/images/lone wolf.png">
                                  <div class="mode-title">
                                  <a href="/mode/lone wolf">

            LONE WOLF
                                  </a>
                        </div>
            </div>


        <!-- SNIPER -->

        <div class="mode-card">

            <img src="/static/images/sniper only br.png">
                                  <div class="mode-title">
                                  <a href="/mode/sniper only br">

                SNIPER ONLY BR
                                  </a>
                            </div>
            </div>


        <!-- BOOYAH -->

        <div class="mode-card">

            <img src="/static/images/booyah only br.png">
                                  <div class="mode-title">
                                  <a href="/mode/booyah only br">

                BOOYAH ONLY BR
                                  </a>
                            </div>
            </div>
                                  <a class="mode-btn"
                                  href="/create_free_match">
                                  CREATE FREE MATCH
                                  </a>


        <a class="mode-btn" href="/">⬅ BACK</a>

    </div>

    """
    )
#admin result route
@app.route("/admin/results")
@admin_required
def admin_results():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT id, mode, slot, entry_fee, winning_prize, status
    FROM matches
    ORDER BY id DESC
    """)

    data = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🏆 ADMIN MATCH RESULTS</h1>

        {% for m in data %}
        <div class="mode-card">

            🎮 {{m[1].upper()}} <br><br>
            ⏰ Slot : {{m[2]}} <br><br>
            💸 Entry Fee : ₹{{m[3]}} <br><br>

            {% if "cs" in m[1] or m[1] == "lone wolf" %}
                🏆 Winning Prize : ₹{{m[4]}}
            {% else %}
                🔫 Per Kill Reward : ₹{{m[4]}}
            {% endif %}

            <br><br>
            📢 Status : {{m[5]}} <br><br>

            <a class="mode-btn" href="/admin/match_results/{{m[0]}}">
                ENTER ALL PLAYER KILLS
            </a>

        </div>
        {% endfor %}

        <a class="mode-btn" href="/admin/dashboard">BACK</a>

    </div>
    """, data=data)

@app.route("/admin/match_results/<int:match_id>", methods=["GET", "POST"])
@admin_required
def admin_match_results(match_id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT mode, slot, entry_fee, winning_prize
    FROM matches
    WHERE id=?
    """, (match_id,))

    match = c.fetchone()

    if not match:
        conn.close()
        return "❌ Match not found"

    mode = match[0]
    slot = match[1]
    entry_fee = match[2]
    winning_prize = match[3]

    if request.method == "POST":

        usernames = request.form.getlist("username")
        kills_list = request.form.getlist("kills")

        for i in range(len(usernames)):

            username = usernames[i]
            kills = int(kills_list[i])

            if "cs" in mode or mode == "lone wolf":
                reward = winning_prize
            else:
                reward = kills * winning_prize

            c.execute("""
            INSERT INTO results(username, mode, slot, kills, reward)
            VALUES(?,?,?,?,?)
            """, (username, mode, slot, kills, reward))

        conn.commit()
        conn.close()

        return redirect("/admin/results")

    c.execute("""
    SELECT tournament.username, users.game_name
    FROM tournament
    LEFT JOIN users
    ON tournament.username = users.username
    WHERE tournament.match_id=?
    ORDER BY tournament.id ASC
    """, (match_id,))

    players = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">

            <h1>🏆 ENTER RESULTS</h1>

            🎮 {{mode.upper()}} <br><br>
            ⏰ {{slot}} <br><br>
            💸 Entry Fee : ₹{{entry_fee}} <br><br>

            {% if "cs" in mode or mode == "lone wolf" %}
                🏆 Winning Prize : ₹{{winning_prize}}
            {% else %}
                🔫 Per Kill Reward : ₹{{winning_prize}}
            {% endif %}

            <br><br>

            <form method="POST">

                {% for p in players %}
                <div class="info">
                    👤 {{p[0]}} <br>
                    🎮 {{p[1]}} <br><br>

                    <input type="hidden" name="username" value="{{p[0]}}">
                    <input name="kills" type="number" placeholder="Kills" required>
                </div>
                {% endfor %}

                {% if players|length > 0 %}
                <button>SUBMIT ALL RESULTS</button>
                {% endif %}

            </form>

            <br>
            <a class="mode-btn" href="/admin/results">BACK</a>

        </div>
    </div>
    """, players=players, mode=mode, slot=slot,
       entry_fee=entry_fee, winning_prize=winning_prize)

#auto reward route
@app.route("/admin/add_kills/<int:id>", methods=["POST"])
@admin_required
def add_kills(id):

    kills = int(request.form["kills"])

    reward = kills * 2

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT username, mode, slot
    FROM tournament
    WHERE id=?
    """,(id,))

    data = c.fetchone()

    if not data:
        conn.close()
        return "❌ PLAYER NOT FOUND"

    username = data[0]
    mode = data[1]
    slot = data[2]

    c.execute("""
    INSERT INTO results(
    username,
    mode,
    slot,
    kills,
    reward
    )
    VALUES(?,?,?,?,?)
    """,(username,mode,slot,kills,reward))

    c.execute("""
    UPDATE wallet
    SET balance = balance + ?
    WHERE username=?
    """,(reward,username))

    c.execute("""
    INSERT INTO notifications(message)
    VALUES(?)
    """,(f"🏆 {username}, result added | Kills: {kills} | Reward: ₹{reward}",))

    conn.commit()
    conn.close()

    return redirect("/admin/results")

#user route
@app.route("/user_mode")
def user_mode():

    return render_template_string(STYLE + RULES + """

    <div class="overlay">

        <h1>🎮 USER TOURNAMENT MODE</h1>

        <br><br>

        <div class="mode-card">


            <h2>🌍 PUBLIC TOURNAMENTS</h2>

            <br>

            <a class="mode-btn"
            href="/public_tournaments">

            ENTER

            </a>

        </div>

        <br><br>

        <div class="mode-card">

            <h2>🎁 FREE MATCHES</h2>

            <br>

            <a class="mode-btn"
            href="/free_matches">

            ENTER

            </a>

        </div>

    </div>

    """)
#admin free match
@app.route("/create_free_match", methods=["GET","POST"])
@admin_required
def create_free_match():

    if request.method == "POST":

        mode = "solo br"
        slot = auto_format_slot(request.form["slot"])

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO matches(
            mode,
            slot,
            status,
            entry_fee,
            winning_prize,
            room_id,
            password
        )
        VALUES(?,?,?,?,?,?,?)
        """, (
            (
    mode,
slot,
"UPCOMING",
0,
0,
"",
""
)
        ))

        conn.commit()
        conn.close()

        return "✅ FREE MATCH CREATED"

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">

            <h1>🎁 CREATE FREE MATCH</h1>

            <h3>🏆 1st = ₹10</h3>
            <h3>🥈 2nd = ₹8</h3>
            <h3>🥉 3rd = ₹5</h3>

            <form method="POST">

                <input name="slot"
                placeholder="Slot"
                required>

                

                <button>CREATE FREE MATCH</button>

            </form>

        </div>
    </div>
    """)
@app.route("/admin/update_room/<int:match_id>", methods=["GET","POST"])
@admin_required
def admin_update_room(match_id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":

        room_id = request.form["room_id"]
        password = request.form["password"]

        c.execute("""
        UPDATE matches
        SET room_id=?, password=?
        WHERE id=?
        """, (room_id, password, match_id))

        conn.commit()
        conn.close()

        return redirect("/admin_dashboard")

    c.execute("""
    SELECT mode, slot, room_id, password
    FROM matches
    WHERE id=?
    """, (match_id,))

    match = c.fetchone()
    conn.close()

    if not match:
        return "❌ Match not found"

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">

            <h1>🔑 UPDATE ROOM</h1>

            🎮 {{match[0].upper()}} <br><br>
            ⏰ {{match[1]}} <br><br>

            <form method="POST">

                <input name="room_id"
                placeholder="Room ID"
                value="{{match[2]}}"
                required>

                <input name="password"
                placeholder="Password"
                value="{{match[3]}}"
                required>

                <button>UPDATE ROOM</button>

            </form>

        </div>
    </div>
    """, match=match)
#public tournament page
@app.route("/public_tournaments")
def public_tournaments():

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>🌍 PUBLIC TOURNAMENTS</h1>

        <br><br>

        <a class="mode-btn"
        href="/join_custom_rooms">

        JOIN TOURNAMENTS

        </a>

        <br><br>

        <a class="mode-btn"
        href="/create_room">

        CREATE TOURNAMENT

        </a>

    </div>

    """)
#free match page
@app.route("/free_matches")
def free_matches():

    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("""
SELECT matches.id,
       matches.mode,
       matches.slot,
       matches.winning_prize,
       COUNT(tournament.id)
FROM matches
LEFT JOIN tournament
ON matches.id = tournament.match_id
WHERE matches.entry_fee=0
GROUP BY matches.id
ORDER BY matches.id DESC
""")

    data = c.fetchall()

    conn.close()


    if not data:

        return render_template_string(STYLE + RULES + """

        <div class="overlay">

            <div class="box">

                <h1>❌ NO TOURNAMENT HELD</h1>

                <br><br>

                <h2>COME BACK LATER</h2>

            </div>

        </div>

        """)


    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>🎁 FREE MATCHES</h1>

        <br>

        {% for m in data %}

        <div class="mode-card">

            <h2>{{m[1].upper()}}</h2>

            <br>

            ⏰ Slot : {{m[2]}}

            <br><br>

            🏆 1st Prize : ₹10
<br><br>

🥈 2nd Prize : ₹8
<br><br>

🥉 3rd Prize : ₹5
<br><br>

👥 Players : {{m[4]}} / 48
<br><br>

{% if m[4] < 48 %}

<a class="mode-btn"
href="/user_custom_room/{{m[0]}}">

JOIN MATCH

</a>

{% else %}

<h3>❌ MATCH FULL</h3>

{% endif %}

        </div>

        <br>

        {% endfor %}

    </div>

    """, data=data)
#join_custom_rooms
@app.route("/join_custom_rooms")
def join_custom_rooms():
    delete_old_matches()
    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("""

    SELECT id,mode,slot,entry_fee,winning_prize,status,created_by
    FROM matches
    ORDER BY id DESC

    """)

    data = c.fetchall()

    conn.close()

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>🔥 TOURNAMENTS</h1>

        {% for m in data %}

        <div class="mode-card">

            <h2>{{m[1].upper()}}</h2>

            <br>

            💸 Entry Fee : ₹{{m[3]}}

            <br><br>

            🏆 Prize : ₹{{m[4]}}

            <br><br>

            ⏰ Slot : {{m[2]}}

                                  status : {{m[5]}}
                                  <br><br>
                                  <a class="mode-btn" href="/join_match/{{m[0]}}">
                                  JOIN TOURNAMENT
                                  </a>
                                  {% if session.get("user") == m[6] %}
                                  <a class="mode-btn" href="/creator/add_room/{{m[0]}}">
                                  ADD ROOM ID / PASSWORD
                                  </a>
                                  <a class="mode-btn" href="/submit_result/{{m[0]}}">
                                  SUBMIT RESULT
                                  </a>
                                  {% endif %}
                                  {% endfor %}
                                  <a class="mode-btn" href="/user_mode">
                                  BACK
                                  </a>


    </div>

    """, data=data)
#custom room
@app.route("/custom_room/<int:id>")
def custom_room(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("""

    SELECT mode,slot,status,entry_fee,winning_prize

    FROM matches

    WHERE id=?

    """,(id,))

    data = c.fetchone()
    c.execute("""
SELECT tournament.username, users.game_name
FROM tournament
LEFT JOIN users
ON tournament.username = users.username
WHERE tournament.match_id=?
ORDER BY tournament.id ASC
""", (id,))

    players = c.fetchall()
    username = session["user"]
    c.execute("""SELECT id FROM tournament WHERE username=? AND match_id=?""",(username,id))
    joined = c.fetchone()

    conn.close()

    if not data:
        return "MATCH NOT FOUND"
    mode = data[0]
    slot = data[1]
    status = data[2]
    entry_fee = data[3]
    winning_prize = data[4]

    return render_template_string(STYLE + RULES + """

    <div class="overlay">

        <div class="box">

            <h1>🎮 ROOM DETAILS</h1>

            <br><br>

            <h2>{{mode.upper()}}</h2>

            <br><br>
                                  <br><br>
                                  status : {{status}}
                                  <br><br>
                                  entry_fee : {{entry_fee}}
                                  <br><br>
            ⏰ Slot : {{slot}}

            <br><br>

            🏆 Prize : ₹{{winning_prize}}
                                  <br><br>

                                  <h3>👥 JOINED PLAYERS</h3>

                                  {% if players|length == 0 %}
                                  No Players Joined Yet
                                  {% endif %}

                                  {% for p in players %}
                                  <div class="info">
                                  👤 {{p[0]}} - {{p[1]}}
                                  </div>
                                  {% endfor %}
             <br><br>
                                  {% if joined %}
                                  <h3> JOINED </h3>
                                  <a class="mode-btn" href="/my_matches">
                                  SEE DETAILS IN MY MATCHES </a>
                                  {% else %}
                                  <a class="mode-btn" href="/join_match/{{id}}">
                                  JOIN TOURNAMENT
                                  </a>
                                  {% endif %}
                                  <a class="mode-btn" href="/join_custom_rooms">
                                  BACK
                                  </a>
        </div>

    </div>

    """,mode=mode,slot=slot,status=status, entry_fee=entry_fee,winning_prize=winning_prize,
      data=data,id=id,joined=joined,players=players)
#join match id
@app.route("/join_match/<int:match_id>")
def join_match(match_id):

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT mode, slot, entry_fee
    FROM matches
    WHERE id=?
    """, (match_id,))

    match = c.fetchone()

    if not match:
        conn.close()
        return "❌ Match not found"

    mode = match[0]
    slot = match[1]
    entry_fee = match[2]

    c.execute("""
    SELECT id
    FROM tournament
    WHERE username=? AND match_id=?
    """, (username, match_id))

    already_joined = c.fetchone()

    if already_joined:
        conn.close()
        return redirect(f"/custom_room/{match_id}")

    c.execute("""
    SELECT COUNT(*)
    FROM tournament
    WHERE match_id=?
    """, (match_id,))

    total_players = c.fetchone()[0]

    if total_players >= 48:
        conn.close()
        return "❌ MATCH FULL"

    c.execute("""
    SELECT balance
    FROM wallet
    WHERE username=?
    """, (username,))

    bal = c.fetchone()

    if not bal or bal[0] < entry_fee:
        conn.close()
        return "❌ LOW BALANCE"

    c.execute("""
    UPDATE wallet
    SET balance = balance - ?
    WHERE username=?
    """, (entry_fee, username))

    c.execute("""
INSERT INTO tournament(username, mode, slot, status, match_id)
VALUES(?,?,?,?,?)
""", (username, mode, slot, "UPCOMING", match_id))

# referral completed
    c.execute("""
UPDATE referrals
SET status='COMPLETED'
WHERE referred_username=? AND status='PENDING'
""", (session["user"],))

    conn.commit()
    conn.close()

    return redirect(f"/custom_room/{match_id}")

#create room
@app.route("/create_room")
def create_room_select():

    if "user" not in session:
        return redirect("/login")

    return render_template_string(STYLE + RULES + """
    <div class="overlay">

        <div class="box">

            <h1>🎮 CREATE ROOM</h1>

            <form method="POST" action="/submit_room">

                <select name="mode" required>
                    <option value="">Select Mode</option>
                    <option value="solo br">Solo BR</option>
                    <option value="duo br">Duo BR</option>
                    <option value="1v1 cs challange">1V1 CS CHALLENGE</option>
                    <option value="2v2 cs challange">2V2 CS CHALLENGE</option>
                    <option value="4v4 cs challange">4V4 CS CHALLENGE</option>
                    <option value="lone wolf">LONE WOLF</option>
                    <option value="sniper only br">SNIPER ONLY BR</option>
                    <option value="booyah only br">BOOYAH ONLY BR</option>
                </select>

                <input name="slot" placeholder="Slot (08:00 PM)" required>

                <input name="entry_fee" type="number" placeholder="Entry Fee" required>

                <button>CREATE ROOM</button>

            </form>

        </div>

    </div>
    """)


#user create room
@app.route("/create_room/<mode>")
def create_user_room(mode):

    return render_template_string(STYLE + RULES + """

    <div class="overlay">

        <div class="box">

            <h1>🎮 CREATE ROOM</h1>


            <form method="POST" action="/submit_room">

                <input type="hidden"
                       name="mode"
                       value="{{mode}}">

                <input name="slot"
                       placeholder="Slot (08:00 PM)"
                       required>

                <input name="entry_fee"
                       type="number"
                       placeholder="Entry Fee"
                       required>

                <button>CREATE ROOM</button>

            </form>

        </div>

    </div>

    """, mode=mode)
#submit room
@app.route("/submit_room", methods=["POST"])
def submit_room():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    mode = request.form["mode"]
    slot = auto_format_slot(request.form["slot"])
    entry_fee = int(request.form["entry_fee"])

    # AUTO PRIZE SYSTEM

    if "cs" in mode or mode == "lone wolf":

        winning_prize = int(entry_fee * 0.80)

    else:

        if entry_fee < 15:
            winning_prize = entry_fee - 1
        else:
            winning_prize = entry_fee - 2

    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("""

    INSERT INTO matches(

        mode,
        slot,
        status,
        entry_fee,
        winning_prize,
              created_by

    )

    VALUES(?,?,?,?,?,?)

    """, (

        mode,
        slot,
        "UPCOMING",
        entry_fee,
        winning_prize,
        username

    ))
    
    conn.commit()
    match_id = c.lastrowid
    conn.close()

    return render_template_string(STYLE + RULES + """

    <div class="overlay">

        <div class="box">

            <h1>✅ TOURNAMENT CREATED</h1>

            <br>

            <h2>{{mode.upper()}}</h2>

            <br>

            💸 Entry Fee : ₹{{entry_fee}}

            <br><br>

            {% if "cs" in mode or mode == "lone wolf" %}

                🏆 Winning Prize : ₹{{winning_prize}}

            {% else %}

                🔫 Per Kill Reward : ₹{{winning_prize}}

            {% endif %}

            <br><br>

            ⏰ Slot : {{slot}}

            <br><br>

            <a class="mode-btn"
               href="/join_custom_rooms">

               VIEW TOURNAMENT

            </a>

            <br><br>
                                  <a class="mode-btn" href="/creator/add_room/{{match_id}}">
                                  ADD ROOM ID /PASSWORD
                                  </a>
                                  <br><br>

            <a class="mode-btn"
               href="/user_mode">

               BACK

            </a>

        </div>

    </div>

    """,

    mode=mode,
    entry_fee=entry_fee,
    winning_prize=winning_prize,
    slot=slot,
    match_id=match_id
    )

#delete tournament
@app.route("/delete_tournaments/<int:id>")
def delete_tournament(id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM tournaments WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/admin")
#public tournament list

@app.route("/join_room")
def join_room():

    conn = sqlite3.connect("database.db")

    c = conn.cursor()
    c.execute("""

    SELECT id,mode,slot,status,
    entry_fee,winning_prize,created_by

    FROM matches

    ORDER BY id DESC

    """)

    matches = c.fetchall()

    conn.close()


    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>🎮 USER TOURNAMENTS</h1>

        {% for m in matches %}

        <div class="mode-card">

            <h2>{{m[1].upper()}}</h2>

            <br>

            ⏰ Slot : {{m[2]}}

            <br><br>

            💸 Entry Fee : ₹{{m[4]}}

            <br><br>

            {% if "cs" in m[1] or m[1] == "lone wolf" %}

                🏆 Winning Prize : ₹{{m[5]}}

            {% else %}

                🔫 Per Kill Reward : ₹{{m[5]}}

            {% endif %}

            <br><br>

            📢 Status : {{m[3]}}

            <br><br>

            <a class="mode-btn"
            href="/custom_room/{{m[0]}}">

            JOIN TOURNAMENT

            </a>
                                  {% if session_user == m[6] %}
                                  <a class="mode-btn" href="/creator/add_room/{{m[0]}}">
                                  ADD ROOM ID /PASSWORD
                                  </a>
                                  {% endif %}

        </div>

        <br>

        {% endfor %}

    </div>

    """, matches=matches,
    session_user=session.get("user"))

#room detail page
@app.route("/user_custom_room/<int:id>")
def user_custom_room(id):

    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("""

    SELECT mode,slot,status,
    room_id,password,
    entry_fee,winning_prize

    FROM matches

    WHERE id=?

    """,(id,))

    data = c.fetchone()

    conn.close()


    mode = data[0]

    slot = data[1]

    status = data[2]

    room_id = data[3]

    password = data[4]

    entry_fee = data[5]

    winning_prize = data[6]


    return render_template_string(STYLE + """

    <div class="overlay">

        <div class="box">

            <h1>{{mode.upper()}}</h1>

            <br>

            ⏰ Slot : {{slot}}

            <br><br>

            💸 Entry Fee : ₹{{entry_fee}}

            <br><br>

            {% if entry_fee == 0 %}

            🏆 1st Prize : ₹10
            <br><br>

            🥈 2nd Prize : ₹8
            <br><br>

            🥉 3rd Prize : ₹5

            {% elif "cs" in mode or mode == "lone wolf" %}

           🏆 Winning Prize : ₹{{winning_prize}}

           {% else %}

         🔫 Per Kill Reward : ₹{{winning_prize}}

           {% endif %}

            📢 Status : {{status}}

            <br><br>

            {% if room_id %}

                🎮 Room ID : {{room_id}}

                <br><br>

                🔐 Password : {{password}}

            {% else %}

                ⏳ Room Details Not Added Yet

            {% endif %}

        </div>

    </div>

    """,

    mode=mode,

    slot=slot,

    status=status,

    room_id=room_id,

    password=password,

    entry_fee=entry_fee,

    winning_prize=winning_prize
    )

#add room detail
@app.route("/add_room_details/<int:id>", methods=["GET","POST"])
@admin_required
def add_room_details(id):

    if request.method == "POST":

        room_id = request.form["room_id"]

        password = request.form["password"]

        conn = sqlite3.connect("database.db")

        c = conn.cursor()

        c.execute("""

        UPDATE matches

        SET room_id=?,
            password=?,
            status='LIVE'

        WHERE id=?

        """,(room_id,password,id))

        conn.commit()

        conn.close()

        return "✅ ROOM DETAILS ADDED"


    return render_template_string(STYLE + """

    <div class="overlay">

        <div class="box">

            <h1>🎮 ADD ROOM DETAILS</h1>

            <form method="POST">

                <input name="room_id"
                placeholder="Room ID"
                required>

                <input name="password"
                placeholder="Password"
                required>

                <button>SUBMIT</button>

            </form>

        </div>

    </div>

    """)

#creator roiute
@app.route("/creator/add_room/<int:id>", methods=["GET","POST"])
def creator_add_room(id):

    if "admin" not in session and "team" not in session and "user" not in session:
        return redirect("/login")

    username = session.get("user")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT created_by FROM matches WHERE id=?", (id,))
    data = c.fetchone()
    if "team" not in session and "admin" not in session:   
     if  not data or data[0] != username:
        conn.close()
        return "❌ You are not allowed to add room details"

    if request.method == "POST":

        room_id = request.form["room_id"]
        password = request.form["password"]

        c.execute("""
        UPDATE matches
        SET room_id=?, password=?
        WHERE id=? AND created_by=?
        """, (room_id, password, id, username))

        conn.commit()
        conn.close()

        return redirect("/join_room")

    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">
            <h1>🎮 ADD ROOM ID / PASSWORD</h1>

            <form method="POST">
                <input name="room_id" placeholder="Room ID" required>
                <input name="password" placeholder="Room Password" required>
                <button>SAVE ROOM</button>
            </form>

            <br>
            <a class="mode-btn" href="/join_room">BACK</a>
        </div>
    </div>
    """)


# =========================================
# SIGNUP
# =========================================

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()
        phone = request.form["phone"]
        game_name = request.form["game_name"]
        referral_input = request.form.get("referral_code", "").strip().upper()
        my_referral_code = generate_referral_code(username)
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT phone FROM users WHERE phone=?", (phone,))
        data = c.fetchone()
        if data:
            return "❌ Phone number already registered"
        referral = referral_input


        # 🔥 check user already exists
        c.execute("SELECT username FROM users WHERE username=?", (username,))
        data = c.fetchone()

        if data:
            return "❌ Username already exists"



        otp = random.randint(100000, 999999)


        session["signup_data"] = {
        "username": username,
        "password": password,
        "phone": phone,
        "game_name": game_name,
        "referral": referral,
        "otp": otp
        }
        c.execute("""
INSERT INTO users (username, phone, password, balance, referral_code, referred_by)
VALUES (?, ?, ?, ?, ?, ?)
""", (username, phone, password, 0, my_referral_code, referral_input))

        #wallet create
        c.execute("""
    INSERT OR IGNORE INTO wallet(username,balance)
    VALUES(?,0)
""", (username,))

        if referral_input:
          c.execute("SELECT username FROM users WHERE referral_code=?", (referral_input,))
          referrer = c.fetchone()

          if referrer:
            c.execute("""
        INSERT INTO referrals (referrer_username, referred_username, referral_code, status, date)
        VALUES (?, ?, ?, ?, ?)
        """, (referrer[0], username, referral_input, "PENDING", datetime.now().strftime("%d-%m-%Y %H:%M")))

        conn.commit()
        conn.close()

        return redirect("/login")
    return render_template_string(STYLE + """

    <div class="overlay">

        <div class="box">

            <h1>🔥 SIGNUP</h1>

            <form method="POST">

                <input name="username" placeholder="Username" required>

                <input name="password" type="password" placeholder="Password" required>

                <input name="phone" placeholder="Phone Number" required>
                                  <input name="game_name" placeholder="free fire game name" required>
                                  <input type="text" name="referral_code" placeholder="Referral Code (Optional)">

                <button>SIGNUP</button>

            </form>

            <br>

            <a href="/login">LOGIN</a>

        </div>

    </div>

    """
                                  )
#otp verification
@app.route("/verify_otp", methods=["GET","POST"])
def verify_otp():

    if "signup_data" not in session:
        return redirect("/signup")

    data = session["signup_data"]

    if request.method == "POST":

        otp = request.form["otp"]

        if otp != str(data["otp"]):
            return "❌ WRONG OTP"

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO users(username,password,phone,game_name,referral_by)
        VALUES(?,?,?,?,?)
        """,(data["username"],data["password"],data["phone"],data["game_name"],data["referral"]))

        c.execute("""
        INSERT OR IGNORE INTO wallet(username,balance)
        VALUES(?,0)
        """,(data["username"],))

        conn.commit()
        conn.close()

        session.pop("signup_data", None)
        session["user"] = data["username"]
        return redirect("/")

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">

            <h1>🔐 VERIFY OTP</h1>

            <form method="POST">
                <input name="otp" placeholder="Enter OTP" required>
                <button>VERIFY</button>
            </form>

        </div>
    </div>
    """)

# =========================================
# LOGIN
# =========================================
@app.route("/login", methods=["GET","POST"])
def login():



    if request.method == "POST":

        username = request.form["username"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
            SELECT * FROM users
            WHERE username=? AND password=? AND IFNULL(banned,0)=0
        """, (username,password))

        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "❌ Wrong username or password"


        return "Wrong Username or Password"

    return render_template_string(STYLE + """

    <div class="overlay">

        <div class="box">

            <h1>🔥 LOGIN</h1>

            <form method="POST">

                <input name="username" placeholder="Username" required>

                <input name="password" type="password" placeholder="Password" required>

                <button>LOGIN</button>

            </form>

            <br>

            <a href="/signup">CREATE ACCOUNT</a>

        </div>

    </div>

    """)

#admin login
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["pass"]
        if user == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin/dashboard")
        else:
            return "❌ Wrong Admin Credentials"

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">
            <h1>🔐 ADMIN LOGIN</h1>

            <form method="POST">
                <input name="user" placeholder="Admin Username" required>
                <input name="pass" type="password" placeholder="Password" required>
                <button>LOGIN</button>
            </form>

        </div>
    </div>
    """)
#taem route
#team login
@app.route("/team_login", methods=["GET","POST"])
def team_login():

    if request.method == "POST":

        user = request.form["user"]
        password = request.form["pass"]

        if user == TEAM_USER and password == TEAM_PASS:
            session["team"] = True
            return redirect("/team")

        return "❌ Wrong Team Login"

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">

            <h1>👥 TEAM LOGIN</h1>

            <form method="POST">

                <input name="user"
                placeholder="Username"
                required>

                <input name="pass"
                type="password"
                placeholder="Password"
                required>

                <button>LOGIN</button>

            </form>

        </div>
    </div>
    """)
#team panel
@app.route("/team")
def team_panel():

    if "team" not in session:
        return redirect("/team_login")

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>👥 TEAM PANEL</h1>

        <a class="mode-btn" href="/team/result_requests">
            🏆 PENDING RESULTS
        </a>

        <br><br>

        <a class="mode-btn" href="/team/matches">
            🎮 ADD ROOM ID / PASSWORD
        </a>

        <br><br>

        <a class="mode-btn" href="/team/reports">
            🚫 PLAYER REPORTS
        </a>

        <br><br>

        <a class="mode-btn" href="/team/tasks">
            📋 MY TASKS
        </a>

        <br><br>

        <a class="mode-btn" href="/team_logout">
            🚪 LOGOUT
        </a>

    </div>
    """)
# team approve result
@app.route("/team/result_requests")
def team_result_requests():

    if "team" not in session:
        return redirect("/team_login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT id, username, mode, slot, kills, reward, screenshot, status
    FROM result_requests
    WHERE status='PENDING'
    ORDER BY id DESC
    """)

    data = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>🏆 TEAM PENDING RESULTS</h1>

        {% for r in data %}
        <div class="mode-card">

            👤 {{r[1]}} <br><br>
            🎮 {{r[2]}} <br><br>
            ⏰ {{r[3]}} <br><br>
            🔫 Kills : {{r[4]}} <br><br>
            💰 Reward : ₹{{r[5]}} <br><br>

            <img src="/{{r[6]}}" width="250">
            <br><br>

            <a class="mode-btn" href="/team/approve_result/{{r[0]}}">
                APPROVE
            </a>

            <a class="mode-btn" href="/team/update_result/{{r[0]}}">
                UPDATE RESULT
            </a>

        </div>
        <br>
        {% endfor %}

        <a class="mode-btn" href="/team">BACK</a>
    </div>
    """, data=data)


@app.route("/team/update_result/<int:id>", methods=["GET", "POST"])
def team_update_result(id):

    if "team" not in session:
        return redirect("/team_login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":

        kills = int(request.form["kills"])
        total_winners = int(request.form.get("total_winners", 1))

        if total_winners <= 0:
            total_winners = 1

        c.execute("""
        SELECT mode, entry_fee
        FROM result_requests
        WHERE id=?
        """, (id,))

        data = c.fetchone()

        if not data:
            conn.close()
            return "❌ Result not found"

        mode = data[0].lower()
        entry_fee = float(data[1])

        if "cs" in mode or "lone wolf" in mode:
            reward = (entry_fee * 80 / 100) / total_winners
        else:
            reward = kills * (entry_fee * 87.5 / 100)
        reward = round(reward, 2)

        c.execute("""
        UPDATE result_requests
        SET kills=?, reward=?, total_winners=?
        WHERE id=?
        """, (kills, reward,total_winners,id))

        conn.commit()
        conn.close()

        return redirect("/team/result_requests")

    c.execute("""
    SELECT result_requests.username,
           users.game_name,
           result_requests.mode,
           result_requests.slot,
           result_requests.kills,
           result_requests.reward,
           result_requests.entry_fee
    FROM result_requests
    LEFT JOIN users
    ON result_requests.username = users.username
    WHERE result_requests.id=?
    """, (id,))

    r = c.fetchone()
    conn.close()

    if not r:
        return "❌ Result not found"

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">

            <h1>✏️ UPDATE RESULT</h1>

            👤 User : {{r[0]}} <br><br>
            🎮 Game Name : {{r[1]}} <br><br>
            🎮 Mode : {{r[2]}} <br><br>
            ⏰ Slot : {{r[3]}} <br><br>
            💵 Entry Fee : ₹{{r[6]}} <br><br>
            💰 Current Reward : ₹{{r[5]}} <br><br>

            <form method="POST">
                🔫 Kills:
                <input name="kills" type="number" value="{{r[4]}}" required>
                <br><br>

                🏆 Total Winners:
                <input name="total_winners" type="number" value="1" required>
                <br><br>

                <button class="mode-btn">UPDATE RESULT</button>
            </form>

            <br>
            <a class="mode-btn" href="/team/result_requests">BACK</a>

        </div>
    </div>
    """, r=r)

#team result
@app.route("/team/matches")
def team_matches():

    if "team" not in session:
        return redirect("/team_login")

    modes = [
        "solo br",
        "duo br",
        "1v1 cs challenge",
        "2v2 cs challenge",
        "4v4 cs challenge",
        "lone wolf",
        "sniper only br",
        "booyah only br"
    ]

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🎮 SELECT MODE</h1>

        {% for mode in modes %}
        <div class="mode-card">
            <h2>{{mode.upper()}}</h2>

            <a class="mode-btn" href="/team/matches/{{mode}}">
                OPEN MATCHES
            </a>
        </div>
        <br>
        {% endfor %}

        <a class="mode-btn" href="/team">BACK</a>

    </div>
    """, modes=modes)

#team matches mode
@app.route("/team/matches/<mode>")
def team_mode_matches(mode):

    if "team" not in session:
        return redirect("/team_login")

    slots = generate_slots()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>{{mode.upper()}} MATCHES</h1>

        {% for slot in slots %}
        <div class="mode-card">

            🎮 {{mode.upper()}} <br><br>
            ⏰ {{slot}} <br><br>

            <a class="mode-btn" href="/team/admin_add_room_by_slot/{{mode}}/{{slot}}">
                ADD / UPDATE ROOM
            </a>

        </div>
        <br>
        {% endfor %}

        <a class="mode-btn" href="/team/matches">BACK</a>

    </div>
    """, mode=mode, slots=slots)

@app.route("/team/admin_add_room_by_slot/<mode>/<path:slot>", methods=["GET","POST"])
def team_admin_add_room_by_slot(mode, slot):

    if "team" not in session:
        return redirect("/team_login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":
        room_id = request.form["room_id"]
        password = request.form["password"]

        c.execute("""
        INSERT OR REPLACE INTO admin_rooms(mode, slot, room_id, password)
        VALUES(?,?,?,?)
        """, (mode, slot, room_id, password))

        conn.commit()
        conn.close()

        return redirect("/team/matches")

    c.execute("""
    SELECT room_id, password
    FROM admin_rooms
    WHERE mode=? AND slot=?
    """, (mode, slot))

    data = c.fetchone()
    conn.close()

    room_id = data[0] if data else ""
    password = data[1] if data else ""

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">
            <h1>🎮 UPDATE ADMIN ROOM</h1>

            <h2>{{mode.upper()}}</h2>
            ⏰ Slot : {{slot}}
            <br><br>

            <form method="POST">
                <input name="room_id" placeholder="Room ID" value="{{room_id}}" required>
                <input name="password" placeholder="Password" value="{{password}}" required>
                <button>UPDATE ROOM</button>
            </form>
        </div>
    </div>
    """, mode=mode, slot=slot, room_id=room_id, password=password)


#team add room id admin
@app.route("/team/admin_add_room/<int:id>", methods=["GET","POST"])
def team_admin_add_room(id):

    if "team" not in session:
        return redirect("/team_login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if request.method == "POST":

        room_id = request.form["room_id"]
        password = request.form["password"]

        c.execute("""
        UPDATE admin_rooms
        SET room_id=?, password=?
        WHERE id=?
        """, (room_id, password, id))

        conn.commit()
        conn.close()

        return redirect("/team/matches")

    c.execute("""
    SELECT mode, slot, room_id, password
    FROM admin_rooms
    WHERE id=?
    """, (id,))

    data = c.fetchone()
    conn.close()

    if not data:
        return "❌ Admin match not found"

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">

            <h1>🎮 UPDATE ADMIN ROOM</h1>

            <h2>{{data[0].upper()}}</h2>

            ⏰ Slot : {{data[1]}}
            <br><br>

            <form method="POST">

                <input name="room_id"
                       placeholder="Room ID"
                       value="{{data[2] or ''}}"
                       required>

                <input name="password"
                       placeholder="Password"
                       value="{{data[3] or ''}}"
                       required>

                <button>UPDATE ROOM</button>

            </form>

        </div>
    </div>
    """, data=data)

#team report
@app.route("/team/reports")
def team_reports():

    if "team" not in session:
        return redirect("/team_login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT id, reporter, reported_player, reason, status
    FROM reports
    ORDER BY id DESC
    """)

    reports = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>🚫 TEAM PLAYER REPORTS</h1>

        {% for r in reports %}
        <div class="mode-card">

            👤 Reporter : {{r[1]}} <br><br>
            🚫 Reported : {{r[2]}} <br><br>
            📝 Reason : {{r[3]}} <br><br>
            📢 Status : {{r[4]}} <br><br>

        </div>
        <br>
        {% endfor %}

        <a class="mode-btn" href="/team">BACK</a>
    </div>
    """, reports=reports)

#team task
@app.route("/team/tasks")
def team_tasks():

    if "team" not in session:
        return redirect("/team_login")

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>📋 MY TASKS</h1>

        <div class="info">

            🏆 Verify pending result screenshots

            <br><br>

            🎮 Add room ID and password before match

            <br><br>

            🚫 Review player reports

            <br><br>

            ⚠️ Do not approve withdrawals

            <br><br>

            ⚠️ Do not edit wallet balances

        </div>

    </div>
    """)
#team logout
@app.route("/team_logout")
def team_logout():

    session.pop("team", None)

    return redirect("/team_login")


# admin result declare
@app.route("/admin/add_result", methods=["GET","POST"])
@admin_required
def add_result():
    if "admin" not in session:
        return redirect("/admin")

    if request.method == "POST":
        username = request.form["username"]
        mode = request.form["mode"]
        slot = request.form["slot"]
        kills = int(request.form["kills"])

        if "cs" in mode or "lone wolf" in mode:
            reward = 40
        else:
            reward = kills * 7

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # insert result
        c.execute("""
            INSERT INTO results(username,mode,slot,kills,reward)
            VALUES(?,?,?,?,?)
        """,(username,mode,slot,kills,reward))

        # update wallet
        c.execute("""
            UPDATE wallet
            SET balance = balance + ?
            WHERE username=?
        """,(reward,username))

        conn.commit()
        conn.close()

        return "✅ RESULT ADDED + REWARD GIVEN"

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">
            <h2>🏆 ADD RESULT</h2>

            <form method="POST">

                <input name="username" placeholder="Username" required>
                <input name="mode" placeholder="Mode" required>
                <input name="slot" placeholder="Slot" required>
                <input name="kills" type="number" placeholder="Kills" required>

                <button>ADD RESULT</button>

            </form>

        </div>
    </div>
    """)


# admin dashboard
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin")

    return render_template_string(STYLE + """
    <div class="overlay">


        <a class="mode-btn" href="/admin/create_room_page">CREATE ROOM</a>
                                  <a class="admin-btn" href="/admin/analytics">
                   📊 Admin Analytics
                                </a>
                                  <a class="mode-btn" href="/admin/matches"> ADD ROOM ID / PASSWORD</a>
                                  <a class="mode-btn" href="/admin_rooms">ADMIN ROOMS</a>
                                  <a class="mode-btn" href="/create_free_match">
🎁 CREATE FREE MATCH
</a>
                                  <a class="mode-btn" href="/admin/free_matches">
📋 FREE MATCH LIST
</a>
                                  <a class="mode-btn" href="/team_login">TEAM PANEL</a>
        <a class="mode-btn" href="/admin/withdrawals">WITHDRAW REQUESTS</a>
                                  <a class="mode-btn" href="/admin/notification">SEND NOTIFICATIONS</a>
                                  <a class="mode-btn" href="/admin/result_requests"> PENDING REQUESTS </a>
                                  <a class="mode-btn" href="/admin/reports">VIEW REPORTS</a>
                                  <a class="mode-btn" href="/admin/banned_users">
                                  BANNED USERS </a>
                                  <a class="mode-btn" href="/admin/results">AUTO RESULTS</a>
        <a class="mode-btn" href="/logout">LOGOUT</a>

    </div>
    """)
#admin rooms
@app.route("/admin_rooms", methods=["GET","POST"])
@admin_required
def admin_rooms():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS admin_rooms(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              mode TEXT,
              slot TEXT,
              room_id TEXT,
              password TEXT,
              unique(mode,slot)
              )
              """)
    if request.method == "POST":
        mode = request.form["mode"]
        slot = normalize_slot(request.form["slot"])
        room_id = request.form["room_id"]
        password = request.form["password"]

        c.execute("""
        INSERT OR REPLACE INTO admin_rooms(mode, slot, room_id, password)
        VALUES(?,?,?,?)
        """,(mode, slot, room_id,password))

        conn.commit()

    c.execute("SELECT * FROM admin_rooms")
    rooms = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
    <h1>ADMIN ROOM ID / PASSWORD</h1>

    <form method="POST">
        <select name="mode">
            <option value="solo br">SOLO BR</option>
            <option value="duo br">DUO BR</option>
            <option value="1v1 cs challenge">1V1 CS</option>
            <option value="2v2 cs challenge">2V2 CS</option>
            <option value="4v4 cs challenge">4V4 CS</option>
        </select>
        <input name="slot" placeholder="slot time e.g 08:00 PM" required>
        <input name="room_id" placeholder="Room ID" required>
        <input name="password" placeholder="Room Password" required>

        <button class="mode-btn">SAVE ROOM</button>
    </form>

    {% for r in rooms %}
        <div class="mode-card">
        {{r[1]}}<br>
                                  slot: {{r[2]}}<br>
        Room ID: {{r[3]}}<br>
        Password: {{r[4]}}
        </div>
    {% endfor %}
    </div>
    """, rooms=rooms)

@app.route("/admin/free_matches")
@admin_required
def admin_free_matches():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
SELECT matches.id,
       matches.mode,
       matches.slot,
       matches.winning_prize,
       COUNT(tournament.id)
FROM matches
LEFT JOIN tournament
ON matches.id = tournament.match_id
WHERE matches.entry_fee=0
GROUP BY matches.id
ORDER BY matches.id DESC
""")

    data = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🎁 FREE MATCH LIST</h1>

        {% for m in data %}

        <div class="mode-card">

            🎮 {{m[1].upper()}}<br><br>

            ⏰ {{m[2]}}<br><br>

            📢 {{m[3]}}<br><br>

            <a class="mode-btn"
            href="/add_room_details/{{m[0]}}">
            ADD ROOM ID / PASSWORD
            </a>

        </div>

        {% endfor %}

        <a class="mode-btn" href="/admin/dashboard">
        BACK
        </a>

    </div>
    """, data=data)

# =========================================
# ADMIN MATCHES
# =========================================

@app.route("/admin/matches")
@admin_required
def admin_matches():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT id, mode, slot, status, room_id,password
    FROM matches
    ORDER BY id DESC
    """)

    data = c.fetchall()

    conn.close()

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>🎮 ADMIN MATCHES</h1>

        <br>

        {% for m in data %}

        <div class="mode-card">

            <h2>🎮 {{m[1].upper()}}</h2>

            <br>

            ⏰ SLOT : {{m[2]}}

            <br><br>

            📢 STATUS : {{m[3]}}

            <br><br>

            🆔 ROOM ID : {{m[4]}}

            <br><br>

            🔐 PASSWORD : {{m[5]}}

            <br><br>

            <a class="mode-btn"
            href="/add_room_details/{{m[0]}}">

            ADD / UPDATE ROOM

            </a>

        </div>

        <br>

        {% endfor %}

        <a class="mode-btn"
        href="/admin/dashboard">

        ⬅ BACK

        </a>

    </div>

    """,data=data)

#admin withdrawals
@app.route("/admin/withdrawals")
@admin_required
def admin_withdrawals():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
     SELECT id, username, amount, method, details, status, qr_code
FROM withdrawal_requests
ORDER BY id DESC
    """)

    data = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>💸 WITHDRAW REQUESTS</h1>

        {% for w in data %}

        <div class="info">

            👤 Username : {{w[1]}}
            <br><br>

            💰 Amount : ₹{{w[2]}}
            <br><br>

            🏦 Method : {{w[3]}}
            <br><br>

            📱 Details : {{w[4]}}
            <br><br>

            📢 Status : {{w[5]}}
            <br><br>
                                  {% if w[6] %}
    📷 QR Code : <br><br>
    <img src="/{{w[6]}}" width="220">
    <br><br>
{% else %}
    📷 QR Code : Not uploaded
    <br><br>
{% endif %}

            {% if w[5] == "PENDING" %}

            <form action="/admin/approve_withdraw/{{w[0]}}" method="POST">

    {% if w[3] == "PLAYSTORE_REDEEM" %}
        <input name="redeem_code"
        placeholder="Enter Play Store Redeem Code"
        required>
    {% endif %}

    <button type="submit">✅ APPROVE</button>
</form>

            <br>

            <form action="/admin/reject_withdraw/{{w[0]}}" method="GET">
                <button type="submit">❌ REJECT</button>
            </form>

            {% endif %}

        </div>

        {% endfor %}

        <a class="mode-btn" href="/admin/dashboard">BACK</a>

    </div>
    """, data=data)

#admin approve withdrawals
@app.route("/admin/approve_withdraw/<int:id>", methods=["POST"])
@admin_required
def approve_withdraw(id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT username, amount, method, details, status
    FROM withdrawal_requests
    WHERE id=?
    """, (id,))

    data = c.fetchone()

    if not data:
        conn.close()
        return "❌ REQUEST NOT FOUND"

    username = data[0]
    amount = data[1]
    method = data[2]
    details = data[3]
    status = data[4]
    redeem_code = ""

    if method == "PLAYSTORE_REDEEM":
        redeem_code = request.form.get("redeem_code", "").strip()

        if redeem_code == "":
            conn.close()
            return "❌ Redeem code required before approve"

    if status != "PENDING":
       conn.close()
       return "❌ Request already processed"

    c.execute("""
UPDATE wallet
SET balance = balance - ?
WHERE username=? AND balance >= ?
""", (amount, username, amount))

    if c.rowcount == 0:
      conn.close()
      return "❌ Low balance or wallet not found"

    now = datetime.now()
    processed_date = now.strftime("%d/%m/%Y")
    processed_time = now.strftime("%I:%M %p")

    c.execute("""
    UPDATE withdrawal_requests
    SET status='APPROVED',
        processed_date=?,
        processed_time=?,
        redeem_code=?
    WHERE id=?
    """, (processed_date, processed_time, redeem_code, id))
    c.execute("""
    INSERT INTO notifications(message)
    VALUES(?)
    """, (f"✅ {username}, your withdrawal of ₹{amount} via {method} is APPROVED",))

    conn.commit()
    conn.close()

    return redirect("/admin/withdrawals")


#admin reject withdrawal
@app.route("/admin/reject_withdraw/<int:id>")
@admin_required
def reject_withdraw(id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT username, amount, method, details, status
    FROM withdrawal_requests
    WHERE id=?
    """, (id,))

    data = c.fetchone()

    if not data:
        conn.close()
        return "❌ REQUEST NOT FOUND"

    username = data[0]
    amount = data[1]
    method = data[2]
    details = data[3]
    status = data[4]

    if status != "PENDING":
        conn.close()
        return "❌ Request already processed"

    now = datetime.now()
    processed_date = now.strftime("%d/%m/%Y")
    processed_time = now.strftime("%I:%M %p")

    c.execute("""
UPDATE withdrawal_requests
SET status='REJECTED', processed_date=?, processed_time=?
WHERE id=?
""", (processed_date, processed_time, id))

    c.execute("""
    INSERT INTO notifications(message)
    VALUES(?)
    """, (f"❌ {username}, your withdrawal of ₹{amount} via {method} is REJECTED",))

    conn.commit()
    conn.close()

    return redirect("/admin/withdrawals")

# =========================================
# ADMIN ANALYTICS
# =========================================

@app.route("/admin/analytics")
@admin_required
def admin_analytics():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM matches")
    total_matches = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM tournament")
    total_joins = c.fetchone()[0]

    c.execute("SELECT SUM(balance) FROM wallet")
    total_wallet_balance = c.fetchone()[0] or 0

    c.execute("SELECT COUNT(*) FROM withdrawal_requests")
    total_withdrawals = c.fetchone()[0]

    c.execute("SELECT SUM(reward) FROM results")
    total_rewards = c.fetchone()[0] or 0

    c.execute("SELECT COUNT(*) FROM reports WHERE status='PENDING'")
    pending_reports = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM notifications")
    total_notifications = c.fetchone()[0]

    conn.close()

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>📊 ADMIN ANALYTICS</h1>

        <div class="info">👥 Total Users : {{total_users}}</div>

        <div class="info">🎮 Total Matches : {{total_matches}}</div>

        <div class="info">✅ Total Joins : {{total_joins}}</div>

        <div class="info">💰 Total Wallet Balance : ₹{{total_wallet_balance}}</div>

        <div class="info">💸 Withdrawal Requests : {{total_withdrawals}}</div>

        <div class="info">🏆 Total Rewards Given : ₹{{total_rewards}}</div>

        <div class="info">🚫 Pending Reports : {{pending_reports}}</div>

        <div class="info">📢 Notifications Sent : {{total_notifications}}</div>

        <br>

        <a class="mode-btn" href="/admin/dashboard">
        BACK
        </a>

    </div>

    """,
    total_users=total_users,
    total_matches=total_matches,
    total_joins=total_joins,
    total_wallet_balance=total_wallet_balance,
    total_withdrawals=total_withdrawals,
    total_rewards=total_rewards,
    pending_reports=pending_reports,
    total_notifications=total_notifications
    )

# =========================================
# ADMIN REPORTS
# =========================================

@app.route("/admin/reports")
@admin_required
def admin_reports():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT reporter, reported_player, reason, status
    FROM reports
    ORDER BY id DESC
    """)

    data = c.fetchall()

    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🚫 PLAYER REPORTS</h1>

        {% for r in data %}

        <div class="info">
            👤 Reporter : {{r[0]}}
            <br><br>
            🎮 Reported Player : {{r[1]}}
            <br><br>
            📄 Reason : {{r[2]}}
            <br><br>
            📢 Status : {{r[3]}}
        <br><br>
                                 <form action="/admin/ban/{{r[1]}}" method="GET">

                             <button type="submit">
                               BAN PLAYER
                              </button>

                                     </form>

                                  </div>

        {% endfor %}

        <a class="mode-btn" href="/admin/dashboard">
        BACK
        </a>

    </div>
    """, data=data)
#ban user
@app.route("/admin/ban/<username>")
@admin_required
def ban_user(username):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    UPDATE users
    SET banned=1
    WHERE username=?
    """,(username,))

    update = c.rowcount

    conn.commit()
    conn.close()
    if update == 0:
        return f" USER NOT FOUND : {username}"
    return f"USER BANNED :{username}"

    return redirect("/admin/reports")
#banned user
@app.route("/admin/banned_users")
@admin_required
def banned_users():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT username, phone
    FROM users
    WHERE banned=1
    """)

    data = c.fetchall()

    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🚫 BANNED USERS</h1>

        {% for u in data %}

        <div class="info">

            👤 Username : {{u[0]}}

            <br><br>

            📱 Phone : {{u[1]}}

            <br><br>

            <form action="/admin/unban/{{u[0]}}" method="GET">

                <button type="submit">
                    UNBAN USER
                </button>

            </form>

        </div>

        {% endfor %}

        <a class="mode-btn" href="/admin/dashboard">
        BACK
        </a>

    </div>
    """, data=data)

#unbann user
@app.route("/admin/unban/<username>")
@admin_required
def unban_user(username):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "UPDATE users SET banned=0 WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin/banned_users")

#notifications
@app.route("/admin/notification", methods=["GET","POST"])
@admin_required
def admin_notification():

    if request.method == "POST":

        message = request.form["message"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO notifications(message)
        VALUES(?)
        """,(message,))

        conn.commit()
        conn.close()

        return "✅ NOTIFICATION SENT"

    return render_template_string(STYLE + """
    <div class="overlay">

        <div class="box">

            <h1>📢 SEND NOTIFICATION</h1>

            <form method="POST">

                <input name="message"
                placeholder="Notification Message"
                required>

                <button>SEND</button>

            </form>

        </div>

    </div>
    """)
#admin check user result
@app.route("/admin/result_requests")
@admin_required
def admin_result_requests():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT id, username, mode, slot,
    kills, reward, screenshot, status
    FROM result_requests
    WHERE status='PENDING'
    ORDER BY id DESC
    """)

    data = c.fetchall()

    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🏆 PENDING RESULTS</h1>

        {% for r in data %}

        <div class="info">

            👤 User : {{r[1]}}
            <br><br>

            🎮 Mode : {{r[2]}}
            <br><br>

            ⏰ Slot : {{r[3]}}
            <br><br>

            🔫 Kills : {{r[4]}}
            <br><br>

            💰 Reward : ₹{{r[5]}}
            <br><br>

            <img src="/{{r[6]}}" width="250">

            <br><br>

            <a class="mode-btn"
            href="/team/approve_result/{{r[0]}}"
            APPROVE
            </a>

        </div>

        {% endfor %}

    </div>
    """, data=data)

@app.route("/team/approve_result/<int:id>")
def team_approve_result(id):

    if "team" not in session:
        return redirect("/team_login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT username, mode, slot, kills, reward
    FROM result_requests
    WHERE id=?
    """, (id,))

    r = c.fetchone()

    if not r:
        conn.close()
        return "❌ Result not found"

    c.execute("""
    INSERT INTO results(username, mode, slot, kills, reward)
    VALUES(?,?,?,?,?)
    """, (r[0], r[1], r[2], r[3], r[4]))

    c.execute("""
    UPDATE wallet
    SET balance = balance + ?
    WHERE username=?
    """, (r[4], r[0]))

    c.execute("""
    UPDATE result_requests
    SET status='APPROVED'
    WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/team/result_requests")

#admin approve user result
@app.route("/admin/approve_result/<int:id>")
@admin_required
def approve_result(id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT username, mode, slot, kills, reward
    FROM result_requests
    WHERE id=?
    """,(id,))

    r = c.fetchone()

    if not r:
        conn.close()
        return "❌ Result not found"

    c.execute("""
    INSERT INTO results(username,mode,slot,kills,reward)
    VALUES(?,?,?,?,?)
    """,(r[0],r[1],r[2],r[3],r[4]))

    c.execute("""
    UPDATE wallet
    SET balance = balance + ?
    WHERE username=?
    """,(r[4],r[0]))

    c.execute("""
    UPDATE result_requests
    SET status='APPROVED'
    WHERE id=?
    """,(id,))

    conn.commit()
    conn.close()

    return redirect("/admin/result_requests")



# create room page
@app.route("/admin/create_room_page")
@admin_required
def create_room_page():
    if "admin" not in session:
        return redirect("/admin")

    return render_template_string(STYLE + """
    <div class="overlay">

        <div class="box">
            <h2>🎮 CREATE ROOM</h2>

            <form method="POST" action="/admin/create_room">

                <select name="mode" required>
                                  <option value="solo br">SOLO BR</option>
                                  <option value="duo br">DUO BR</option>
                                  <option value="1v1 cs challenge">1V1 CS CHALLENGE</option>
                                  <option value="4v4 cs challenge">4v4 CS CHALLENGE</option>
                                  <option value="2v2 cs challenge">2V2 CS CHALLENGE</option>
                                  <option value="lone wolf">LONE WOLF</option>
                                  <option value="sniper only br">SNIPER ONLY BR</option>
                                  <option value="booyah only br">BOOYAH ONLY BR</option>
                <input name="slot" placeholder="Slot Time (e.g., 08:00 PM)" required>
                <input name="room_id" placeholder="Room ID" required>
                <input name="password" placeholder="Password" required>
                                  </select>

                <button>CREATE</button>

            </form>

        </div>

    </div>
    """)

#create room backend
@app.route("/admin/create_room", methods=["POST"])
@admin_required
def create_room():
    if "admin" not in session:
        return redirect("/admin")

    mode = request.form["mode"]
    slot = auto_format_slot(request.form["slot"])
    room_id = request.form["room_id"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO matches(mode,slot,room_id,password,status)
        VALUES(?,?,?,?,?)
    """,(mode,slot,room_id,password,"LIVE"))

    conn.commit()
    conn.close()

    return "✅ ROOM CREATED"

# admin logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =========================================
# MODE PAGE
# =========================================

@app.route("/mode/<mode>")
def mode(mode):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(" SELECT room_id FROM admin_rooms WHERE mode=?",(mode,))
    room = c.fetchone()
    conn.close()    
    if "user" not in session:
        return redirect("/login")

    slots = generate_slots()

    entry_fee = get_entry_fee(mode)

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>{{mode.upper()}}</h1>

        <h3>💸 Entry Fee : ₹{{entry_fee}}</h3>

        {% for s in slots %}

        <div class="info">

            ⏰ {{s}}

            <br><br>

            entry fee : {{entry_fee}}
            <br><br>
            {% if "cs" in mode or "lone wolf" in mode %}
                                  winner reward : 40
            {% else %}
                                  per kill reward :7
            {% endif %}

            👥 Players : {{get_count(mode,s)}} / {{get_max_players(mode)}}

            <br><br>

            {% if get_count(mode,s) < get_max_players(mode) %}
                                  <a href="{{ url_for('join',mode=mode,slot=s)}}">JOIN MATCH</a>
                                  {% else %}
                                  <b style="color:red;">MATCH FULL</b>
                                  {% endif %}

        </div>

        {% endfor %}

        <a href="/">BACK</a>

    </div>

    """,
    room=room,
    mode=mode,
    slots=slots,
    entry_fee=entry_fee,
    get_count=get_count,
    get_max_players=get_max_players
    )
#max players(mode)
def get_max_players(mode):
    mode = mode.lower()
    if mode == "solo br":
        return 48
    elif mode == "duo br":
        return 48
    elif mode == "sniper only br":
        return 48
    elif mode == "booyah only br":
        return 48
    elif mode == "lone wolf":
        return 2
    elif mode == "1v1 cs challenge":
        return 2
    elif mode == "2v2 cs challenge":
        return 4
    elif mode == "4v4 cs challenge":
        return 8
    else :
        return 48
# =========================================
# JOIN MATCH
# =========================================

@app.route("/join/<mode>/<path:slot>")
def join(mode, slot):
    slot = slot.replace("%20"," ")

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    entry_fee = get_entry_fee(mode)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "SELECT balance FROM wallet WHERE username=?",
        (username,)
    )

    bal = c.fetchone()
    entry_fee = get_entry_fee(mode)
    if not bal or bal[0] < entry_fee:
        conn.close()
        return "❌ LOW BALANCE"

    c.execute("""
    SELECT * FROM tournament
    WHERE username=? AND mode=? AND slot=? AND match_id IS NULL
    """,(username,mode,slot))

    if c.fetchone():
        conn.close()
        return "❌ ALREADY JOINED"

    c.execute("""
              SELECT COUNT(*) FROM tournament WHERE mode=? AND slot=? AND match_id IS NULL
              """,(mode,slot))
    count = c.fetchone()[0]
    if count >= get_max_players(mode):
        conn.close()
        return"match full"


    c.execute(
        "UPDATE wallet SET balance = balance - ? WHERE username=?",
        (entry_fee,username)
    )

    c.execute("""
INSERT INTO tournament(username,mode,slot,status,match_id)
VALUES(?,?,?,?,NULL)
""",(username,mode,slot,"UPCOMING"))

# referral completed
    c.execute("""
UPDATE referrals
SET status='COMPLETED'
WHERE referred_username=? AND status='PENDING'
""", (session["user"],))

    conn.commit()
    conn.close()

    return redirect(url_for("room",mode=mode,slot=slot))


#match status
def get_match_status(mode,slot):
    conn =sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(
        """ SELECT status FROM matches WHERE mode=? AND slot=?""",(mode,slot)
    )
    data = c.fetchone()
    conn.close()
    if data:
      return data[0]
    return "UPCOMING"

#auto match status

def update_match_status():
     conn = sqlite3.connect("database.db")
     c = conn.cursor()

     c.execute("SELECT mode, slot FROM matches")
     matches = c.fetchall()
     now = datetime.now()
     for m in matches:
        m_mode =m[0]
        m_slot_time = m[1]

        try:
            slot_dt = datetime.strptime(m_slot_time, "%I:%M %p")
            now_dt = datetime.strptime(now.strftime("%I:%M %p"), "%I:%M %p")

            diff = (slot_dt - now_dt).total_seconds() / 60

            if diff > 0:
                status = "UPCOMING"
            elif -120 <= diff <= 0:
                status = "LIVE"
            else:
                status = "ENDED"

            c.execute("""
                UPDATE matches
                SET status=?
                WHERE TRIM(mode)=TRIM(?) AND TRIM(slot)=TRIM(?)
            """, (status, m_mode, m_slot_time))

        except:
            continue

     conn.commit()
     conn.close()


#room
@app.route("/room/<mode>/<slot>")
def room(mode, slot):
    slot = normalize_slot(slot)

    if "user" not in session:
        return redirect("/login")

    update_match_status()
    status = get_match_status(mode, slot)

    count = get_count(mode, slot)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "SELECT tournament.username,users.game_name FROM tournament JOIN users ON tournament.username = users.username WHERE tournament.mode=? AND tournament.slot=? AND tournament.match_id IS NULL",
        (mode,slot,)
    )

    players = c.fetchall()

    c.execute(
        "SELECT room_id,password FROM admin_rooms WHERE LOWER(TRIM(mode))=LOWER(TRIM(?)) AND LOWER(TRIM(slot))=LOWER(TRIM(?))",
        (mode,slot)
    )

    data = c.fetchone()
    created_by = ""
    if not data:
     room_id = "NOT AVAILABLE"
     password = "NOT AVAILABLE"
     status = "UPCOMING"
    else:
        room_id = data[0]
        password = data[1]

    conn.close()

    # =========================
    # SHOW ROOM ONLY 10 MIN BEFORE
    # =========================

    try:

        slot_time = datetime.strptime(
            slot,
            "%I:%M %p"
        )

        now = datetime.now()

        slot_time = slot_time.replace(
            year=now.year,
            month=now.month,
            day=now.day
        )

        diff = (slot_time - now).total_seconds() / 60

    except:
        diff = 999

    if data:

        if diff <= 10:

            room_id = data[0]
            password = data[1]

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>🎮 {{mode.upper()}} ROOM</h1>

        <div class="info">
            ⏰ SLOT : {{slot}}
        </div>

        <div class="info">
            📡 STATUS : {{status}}
        </div>

        <div class="info">
            👥 PLAYERS : {{count}} / 48
        </div>

        <div class="info">
            🆔 ROOM ID : {{room_id}}
        </div>

        <div class="info">
            🔑 PASSWORD : {{password}}
        </div>

        {% if room_id == "NOT AVAILABLE" %}

        <h3 style="color:yellow;">
            ROOM DETAILS WILL SHOW
            10 MIN BEFORE MATCH
        </h3>

        {% endif %}

        <h2>🔥 JOINED PLAYERS</h2>

        <ul>

        {% for p in players %}

            <li>{{p[0]}} - {{p[1]}}</li>

        {% endfor %}

        </ul>

        <br>
        <a class="mode-btn" href="/">
            BACK
        </a>

    </div>

    """,

    mode=mode,
    slot=slot,
    room_id=room_id,
    password=password,
    status=status,
    count=count,
    players=players,
    created_by = created_by,
    session_user=session["user"]
    )


# =========================================
# RECHARGE
# =========================================
@app.route("/recharge", methods=["GET", "POST"])
def recharge():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    if request.method == "POST":

        amount = int(request.form["amount"])

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        # =================================
        # GET REFERRER FROM REFERRALS TABLE
        # =================================

        c.execute("""
SELECT referrer_username
FROM referrals
WHERE referred_username=? AND status='COMPLETED'
""", (username,))

        ref_data = c.fetchone()

        referral_user = None

        if ref_data:
          referral_user = ref_data[0]

        # =================================
        # ENSURE WALLET EXISTS
        # =================================

        c.execute("""
        SELECT balance
        FROM wallet
        WHERE username=?
        """,(username,))

        data = c.fetchone()

        if data is None:

            c.execute("""
            INSERT INTO wallet(username,balance)
            VALUES(?,?)
            """,(username,0))

        # =================================
        # USER RECHARGE
        # =================================

        c.execute("""
        UPDATE wallet
        SET balance = balance + ?
        WHERE username=?
        """,(amount,username))

        # =================================
        # REFERRAL REWARD
        # =================================

        if referral_user:

         reward = round(amount * 0.05, 2)

         c.execute("""
    UPDATE wallet
    SET balance = balance + ?
    WHERE username=?
    """, (reward, referral_user))

         c.execute("""
    INSERT INTO notifications(message)
    VALUES(?)
    """, (f"🎁 Referral Bonus: {referral_user} got ₹{reward} because {username} added ₹{amount}",))

        # =================================
        # DAILY STREAK START
        # =================================

        c.execute("""
        SELECT recharge_active
        FROM daily_reward
        WHERE username=?
        """,(username,))

        streak = c.fetchone()

        if not streak:

            c.execute("""
            INSERT INTO daily_reward(
            username,
            current_day,
            last_claim,
            recharge_active
            )
            VALUES(?,?,?,?)
            """,(username,1,"",1))

        else:

            recharge_active = streak[0]

            if recharge_active == 0:

                c.execute("""
                UPDATE daily_reward
                SET current_day=?,
                    recharge_active=?
                WHERE username=?
                """,(1,1,username))

        conn.commit()

        # =================================
        # GET UPDATED BALANCE
        # =================================

        c.execute("""
        SELECT balance
        FROM wallet
        WHERE username=?
        """,(username,))

        balance = c.fetchone()[0]

        conn.close()

        return f"✅ RECHARGE SUCCESSFUL | NEW BALANCE: ₹{balance}"

    return render_template_string(STYLE + """

    <div class="overlay">

        <div class="box">

            <h1>💰 RECHARGE</h1>

            <form method="POST">

                <input name="amount"
                type="number"
                placeholder="Enter Amount"
                required>

                <button>ADD MONEY</button>

            </form>

            <br>

            <a href="/">BACK</a>

        </div>

    </div>

    """)

# =========================================
# WITHDRAWAL
# =========================================

@app.route("/withdrawal", methods=["GET","POST"])
def withdrawal():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    if request.method == "POST":

        amount = int(request.form["amount"])
        method = request.form["method"]
        details = request.form["details"].strip()
        qr_file = request.files.get("qr_code")
        qr_path = ""

        balance = get_balance(username)

        if amount <= 0:
            return "❌ Invalid amount"

        if amount > balance:
            return "❌ Low balance"
        valid_methods = [
            "UPI",
            "PAYTM",
            "PHONEPE",
            "GOOGLEPAY",
            "FAMPAY",
            "PLAYSTORE_REDEEM"
        ]

        payment_apps = ["UPI", "PAYTM", "PHONEPE", "GOOGLEPAY", "FAMPAY"]

        if method not in valid_methods:
            return "❌ Invalid withdrawal method"

        if method in payment_apps:
            if not qr_file or qr_file.filename == "":
                return "❌ QR Code required for this payment method"

            qr_filename = username + "_withdraw_qr_" + datetime.now().strftime("%Y%m%d%H%M%S") + "_" + qr_file.filename
            qr_path = os.path.join(UPLOAD_FOLDER, qr_filename)
            qr_file.save(qr_path)
           

        if method not in valid_methods:
            return "❌ Invalid withdrawal method"

        if details == "":
            return "❌ Payment details required"

        if method == "UPI":
            if "@" not in details or len(details) < 6:
                return "❌ Invalid UPI ID"

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        now = datetime.now()
        req_date = now.strftime("%d/%m/%Y")
        req_time = now.strftime("%I:%M %p")
        transaction_code = "WDR" + now.strftime("%Y%m%d%H%M%S") + str(random.randint(100, 999))

        c.execute("""
INSERT INTO withdrawal_requests(username, amount, method, details, status, date, time, transaction_code, qr_code)
VALUES(?,?,?,?,?,?,?,?,?)
""", (username, amount, method, details, "PENDING", req_date, req_time, transaction_code, qr_path))
        conn.commit()
        conn.close()

        return "✅ WITHDRAWAL REQUEST SENT"

    return render_template_string(STYLE + """

    <div class="overlay">

        <div class="box">

            <h1>💸 WITHDRAWAL</h1>

            <form method="POST" enctype="multipart/form-data">

                <input name="amount" type="number" placeholder="Amount" required>

                <select name="method" id="methodSelect" required>
                    <option value="">Select Method</option>
                    <option value="UPI">UPI ID</option>
                    <option value="PAYTM">Paytm</option>
                    <option value="PHONEPE">PhonePe</option>
                    <option value="GOOGLEPAY">Google Pay</option>
                    <option value="FAMPAY">FamPay</option>
                    <option value="PLAYSTORE_REDEEM">Play Store Redeem Code</option>
                </select>

                <input name="details"
                placeholder="UPI ID / Mobile Number / Redeem Code Request"
                required>
                                  <<div id="qrBox" style="display:none;">
    <p>📷 QR Code Upload</p>
    <input id="qrInput" name="qr_code" type="file" accept="image/*">
    <small>PhonePe / Google Pay / Paytm / UPI ke liye QR code upload karein.</small>
    <br><br>
</div>

                <button>REQUEST</button>
                                  <p style="color:#ffea00;">
    🎁 Redeem available on transaction history after admin approve
</p>
          <script>
const methodSelect = document.getElementById("methodSelect");
const qrBox = document.getElementById("qrBox");
const qrInput = document.getElementById("qrInput");

methodSelect.addEventListener("change", function() {
    const paymentApps = ["UPI", "PAYTM", "PHONEPE", "GOOGLEPAY", "FAMPAY"];

    if (paymentApps.includes(this.value)) {
        qrBox.style.display = "block";
        qrInput.required = true;
    } else {
        qrBox.style.display = "none";
        qrInput.required = false;
        qrInput.value = "";
    }
});
</script>
            </form>
                                  <br><br>

<a class="mode-btn" href="/withdrawal_pending">⏳ Pending</a>
<a class="mode-btn" href="/withdrawal_completed">✅ Completed</a>
<a class="mode-btn" href="/withdrawal_history">📜 History</a>

<a class="mode-btn" href="/">BACK</a>

        </div>

    </div>

    """)

@app.route("/withdrawal_pending")
def withdrawal_pending():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT amount, method, details, status, date, time, transaction_code
    FROM withdrawal_requests
    WHERE username=? AND status='PENDING'
    ORDER BY id DESC
    """, (username,))

    data = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>⏳ Pending Withdrawals</h1>

        {% if data %}
            {% for w in data %}
            <div class="mode-card">
                <h2>⏳ Pending Request</h2>
                💰 Amount : ₹{{w[0]}} <br><br>
                📅 Date : {{w[4] or 'N/A'}} <br><br>
                ⏰ Time : {{w[5] or 'N/A'}} <br><br>
                🧾 Transaction Code : {{w[6] or 'N/A'}} <br><br>
                🏦 Method : {{w[1]}} <br><br>
                📱 Details : {{w[2]}} <br><br>
                📢 Status : {{w[3]}}
            </div>
            {% endfor %}
        {% else %}
            <div class="info">No pending withdrawals.</div>
        {% endif %}

        <a class="mode-btn" href="/withdrawal">BACK</a>
    </div>
    """, data=data)


@app.route("/withdrawal_completed")
def withdrawal_completed():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT amount, method, details, status, date, time, transaction_code, processed_date, processed_time, redeem_code
    FROM withdrawal_requests
    WHERE username=? AND status='APPROVED'
    ORDER BY id DESC
    """, (username,))

    data = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>✅ Completed Withdrawals</h1>

        {% if data %}
            {% for w in data %}
            <div class="mode-card">
                <h2>✅ Withdrawal Completed</h2>
                💰 Amount : ₹{{w[0]}} <br><br>
                📅 Request Date : {{w[4] or 'N/A'}} <br><br>
                ⏰ Request Time : {{w[5] or 'N/A'}} <br><br>
                ✅ Completed Date : {{w[7] or 'N/A'}} <br><br>
                ✅ Completed Time : {{w[8] or 'N/A'}} <br><br>
                🧾 Transaction Code : {{w[6] or 'N/A'}} <br><br>
                                  {% if w[1] == 'PLAYSTORE_REDEEM' %}
    🎁 Redeem Code : {{w[9] or 'Available after admin approve'}} <br><br>
{% endif %}
                🏦 Method : {{w[1]}} <br><br>
                📱 Details : {{w[2]}} <br><br>
                📢 Status : COMPLETED
            </div>
            {% endfor %}
        {% else %}
            <div class="info">No completed withdrawals.</div>
        {% endif %}

        <a class="mode-btn" href="/withdrawal">BACK</a>
    </div>
    """, data=data)


@app.route("/withdrawal_history")
def withdrawal_history():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT amount, method, details, status, date, time, transaction_code, processed_date, processed_time, redeem_code
    FROM withdrawal_requests
    WHERE username=?
    ORDER BY id DESC
    """, (username,))

    data = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>📜 Withdrawal History</h1>

        {% if data %}
            {% for w in data %}
            <div class="mode-card">
                {% if w[3] == 'PENDING' %}
                    <h2>⏳ Pending</h2>
                {% elif w[3] == 'APPROVED' %}
                    <h2>✅ Completed</h2>
                {% elif w[3] == 'REJECTED' %}
                    <h2>❌ Rejected</h2>
                {% else %}
                    <h2>📜 {{w[3]}}</h2>
                {% endif %}

                💰 Amount : ₹{{w[0]}} <br><br>
                📅 Request Date : {{w[4] or 'N/A'}} <br><br>
                ⏰ Request Time : {{w[5] or 'N/A'}} <br><br>
                🧾 Transaction Code : {{w[6] or 'N/A'}} <br><br>
                                  {% if w[1] == 'PLAYSTORE_REDEEM' %}
    🎁 Redeem Code : {{w[9] or 'Available after admin approve'}} <br><br>
{% endif %}
                🏦 Method : {{w[1]}} <br><br>
                📱 Details : {{w[2]}} <br><br>
                📢 Status : {{w[3]}} <br><br>

                {% if w[3] != 'PENDING' %}
                    📅 Processed Date : {{w[7] or 'N/A'}} <br><br>
                    ⏰ Processed Time : {{w[8] or 'N/A'}} <br><br>
                {% endif %}
            </div>
            {% endfor %}
        {% else %}
            <div class="info">No withdrawal history.</div>
        {% endif %}

        <a class="mode-btn" href="/withdrawal">BACK</a>
    </div>
    """, data=data)

# =========================================
# DAILY REWARD
# =========================================

# =========================================
# DAILY REWARD
# =========================================

@app.route("/daily_reward")
def daily_reward():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT current_day,last_claim,recharge_active
    FROM daily_reward
    WHERE username=?
    """,(username,))

    data = c.fetchone()

    if not data:
        conn.close()
        return "❌ RECHARGE FIRST"

    current_day = data[0]
    last_claim = data[1]
    recharge_active = data[2]

    if recharge_active == 0:
        conn.close()
        return "❌ RECHARGE REQUIRED"

    today = datetime.now().strftime("%Y-%m-%d")

    if last_claim == today:
        conn.close()
        return "❌ ALREADY CLAIMED TODAY"

    # =========================
    # REWARD
    # =========================

    reward = current_day

    # ADD MONEY

    c.execute("""
    UPDATE wallet
    SET balance = balance + ?
    WHERE username=?
    """,(reward,username))

    # =========================
    # DAY 7 COMPLETE
    # =========================

    if current_day >= 7:

        c.execute("""
        UPDATE daily_reward
        SET current_day=?,
            last_claim=?,
            recharge_active=0
        WHERE username=?
        """,(1,today,username))

    else:

        c.execute("""
        UPDATE daily_reward
        SET current_day=current_day+1,
            last_claim=?
        WHERE username=?
        """,(today,username))

    conn.commit()
    conn.close()

    return f"🎁 DAY {current_day} CLAIMED ₹{reward}"


# =========================================
# RESULTS
# =========================================

@app.route("/results")
def results():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "SELECT username,mode,kills,reward FROM results"
    )

    data = c.fetchall()

    conn.close()

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>🏆 RESULTS</h1>

        <ul>

        {% for r in data %}

        <li>

            👤 {{r[0]}}

            <br><br>

            🎮 {{r[1]}}

            <br><br>

            🔫 {{r[2]}} Kills

            <br><br>

            💰 ₹{{r[3]}}

        </li>

        {% endfor %}

        </ul>

    </div>

    """,data=data)
#user declare result
@app.route("/submit_result/<int:match_id>", methods=["GET","POST"])
def submit_result(match_id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(""" SELECT mode, slot, entry_fee
FROM matches
WHERE id=? """, (match_id,))
    match = c.fetchone()

    if not match:
        conn.close()
        return "❌ Match not found"

    mode = match[0]
    slot = match[1]
    entry_fee = match[2]

    if request.method == "POST":

        usernames = request.form.getlist("username")
        kills_list = request.form.getlist("kills")
        screenshot = request.files.get("screenshot")

        if not screenshot or screenshot.filename == "":
          conn.close()
          return "❌ Screenshot required"

        filename = session["user"] + "_" + screenshot.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        screenshot.save(filepath)

        if len(usernames) == 0:
            conn.close()
            return "❌ No players found"

        for i in range(len(usernames)):

            username = usernames[i]
            kills = int(kills_list[i])

            mode_lower = mode.lower()

        if "cs" in mode_lower or "lone wolf" in mode_lower:
          total_winners = len(usernames)
          reward = (entry_fee * 80 / 100) / total_winners
        else:
          reward = kills * 8.75

        reward = round(reward, 2)

        c.execute("""
            INSERT INTO result_requests(
            username, mode, slot, kills, reward, screenshot, status, entry_fee, total_winners
            )
            VALUES(?,?,?,?,?,?,?,?,?)
            """, (username, mode, slot, kills, reward, filepath, "PENDING", entry_fee, len(usernames)))
        
        conn.commit()
        conn.close()

        return "✅ All player results submitted for approval"

    c.execute("""
SELECT tournament.username, users.game_name
FROM tournament
LEFT JOIN users ON tournament.username = users.username
WHERE tournament.match_id=?
ORDER BY tournament.id ASC
""", (match_id,))

    players = c.fetchall()
    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">
        <div class="box">

            <h1>🏆 SUBMIT PLAYER RESULTS</h1>

            {% if players|length == 0 %}
                <div class="info">
                    ❌ No players joined this match yet
                </div>
            {% endif %}

            <form method="POST" enctype="multipart/form-data">

                {% for p in players %}
                    <div class="info">
                        👤{{p[0]}} - {{p[1]}}
                        <input type="hidden" name="username" value="{{p[0]}}">
                        <input name="kills" type="number" placeholder="Kills" required>
                    </div>
                {% endfor %}
                 {% if players|length > 0 %}
    <input name="screenshot" type="file" accept="image/*" required>
{% endif %}
                {% if players|length > 0 %}
                    <button>SUBMIT ALL RESULTS</button>
                {% endif %}

            </form>

            <br>
            <a class="mode-btn" href="/join_custom_rooms">BACK</a>

        </div>
    </div>
    """, players=players)

# =========================================
# MY MATCHES
# =========================================

@app.route("/my_matches")
def my_matches():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT mode, slot
    FROM tournament
    WHERE username=?
    """, (username,))

    matches = c.fetchall()
    conn.close()

    now = datetime.now()

    upcoming = []
    live = []
    ended = []

    for m in matches:

        mode = m[0]
        slot = str(m[1]).strip()

        try:
            if "AM" in slot.upper() or "PM" in slot.upper():
                slot_time = datetime.strptime(slot, "%I:%M %p")
            else:
                slot_time = datetime.strptime(slot, "%H:%M")

            slot_time = slot_time.replace(
                year=now.year,
                month=now.month,
                day=now.day
            )

            diff = (slot_time - now).total_seconds() / 60

            if diff > 10:
                upcoming.append(m)

            elif -120 <= diff <= 10:
                live.append(m)

            else:
                ended.append(m)

        except:
            upcoming.append(m)

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🎮 MY MATCHES</h1>

        <div class="mode-card">
            <h2>🟡 UPCOMING MATCHES</h2>
            <br>

            {% for m in upcoming %}
                <a class="mode-btn" href="/room/{{m[0]}}/{{m[1]}}">
                    🎮 {{m[0].upper()}}
                    <br><br>
                    ⏰ {{m[1]}}
                </a>
                <br><br>
            {% endfor %}
        </div>

        <br>

        <div class="mode-card">
            <h2>🔴 LIVE MATCHES</h2>
            <br>

            {% for m in live %}
                <a class="mode-btn" href="/room/{{m[0]}}/{{m[1]}}">
                    🎮 {{m[0].upper()}}
                    <br><br>
                    ⏰ {{m[1]}}
                </a>
                <br><br>
            {% endfor %}
        </div>

        <br>

        <div class="mode-card">
            <h2>🏆 RESULTS</h2>
            <br>

            {% for m in ended %}
                <a class="mode-btn" href="/room/{{m[0]}}/{{m[1]}}">
                    🎮 {{m[0].upper()}}
                    <br><br>
                    ⏰ {{m[1]}}
                </a>
                <br><br>
            {% endfor %}
        </div>

        <br>

        <a class="mode-btn" href="/">
        ⬅ BACK
        </a>

    </div>
    """,
    upcoming=upcoming,
    live=live,
    ended=ended)
# =========================================
# PROFILE
# =========================================

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT username, phone, balance, referral_code FROM users WHERE username=?", (session["user"],))
    user = c.fetchone()

    conn.close()

    balance = get_balance(username)

    return render_template_string(STYLE + """

    <div class="overlay">

        <h1>👤 PROFILE</h1>

        <div class="info">

            👤 Username : {{user[0]}}

            <br><br>

            📱 Phone : {{user[1]}}

            <br><br>
                                  GAME NAME : {{user[2]}}
           <br><br>
            💰 Balance : ₹{{balance}}
            <p>🎁 Referral No: <b>{{user[3]}}</b></p>

            <a href="/refer" class="btn">Refer & Earn</a>
        </div>

    </div>

    """,
    user=user,
    balance=balance
    )

# =========================================
# SUPPORT
# =========================================

SUPPORT_INSTAGRAM = "https://www.instagram.com/vivek_singh_2m?igsh=YXk2ajNyZWhxZjdh"

@app.route("/support")
def support():

    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🎧 SUPPORT CENTER</h1>

        <div class="mode-card">

            <h2>👤 HELLO {{username}}</h2>

            <br>

            📞 Need Help With:
            <br><br>

            💰 Recharge Problem
            <br><br>

            🏆 Tournament Issue
            <br><br>

            🎮 Room ID Problem
            <br><br>

            💸 Withdrawal Problem
            <br><br>

            🚫 Ban / Report Issue

            <br><br><br>

            <a class="mode-btn"
            href="{{support_link}}"
            target="_blank">

            📩 CHAT ON INSTAGRAM

            </a>

        </div>

        <br>

        <a class="mode-btn" href="/">
        ⬅ BACK
        </a>

    </div>
    """,
    username=username,
    support_link=SUPPORT_INSTAGRAM
    )

# =========================================
# REPORT PLAYER
# =========================================

@app.route("/report", methods=["GET","POST"])
def report():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        reporter = session["user"]

        reported_player = request.form["reported_player"]

        reason = request.form["reason"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO reports(
        reporter,
        reported_player,
        reason,
        status
        )
        VALUES(?,?,?,?)
        """,(reporter,reported_player,reason,"PENDING"))

        conn.commit()
        conn.close()

        return "✅ REPORT SUBMITTED"

    return render_template_string(STYLE + """
    <div class="overlay">

        <div class="box">

            <h1>🚫 REPORT PLAYER</h1>

            <form method="POST">

                <input name="reported_player"
                placeholder="Player Username"
                required>

                <input name="reason"
                placeholder="Reason"
                required>

                <button>SUBMIT REPORT</button>

            </form>

        </div>

    </div>
    """)

#user notifications
@app.route("/notifications")
def notifications():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT message
    FROM notifications
    ORDER BY id DESC
    """)

    data = c.fetchall()

    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>📢 NOTIFICATIONS</h1>

        <ul>

        {% for n in data %}

        <li>
        🔔 {{n[0]}}
        </li>

        {% endfor %}

        </ul>

    </div>
    """,data=data)

@app.route("/privacy")
def privacy():
    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>Privacy Policy</h1>

        <div class="mode-card">
            <p>
                FireZone Esports users ki basic information jaise username, mobile number,
                wallet requests, match details aur result records app functionality ke liye store karta hai.
            </p>

            <p>
                Hum user data ko kisi third party ke saath sell nahi karte.
                User data sirf account, match, wallet request aur support purpose ke liye use hota hai.
            </p>

            <p>
                Agar kisi user ko account ya data related help chahiye, to contact page se support le sakta hai.
            </p>

            <br>
            <a href="/" class="btn">Back to Home</a>
        </div>
    </div>
    """)


@app.route("/terms")
def terms():
    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>Terms & Conditions</h1>

        <div class="mode-card">
            <p>
                FireZone Esports ek gaming/tournament platform hai. Users ko app use karte time
                fair play rules follow karne honge.
            </p>

            <p>
                Fake details, cheating, wrong result upload, abusive behavior ya multiple fake accounts
                par account block kiya ja sakta hai.
            </p>

            <p>
                Users ko app ke rules, match timing, result rules aur admin decision follow karna hoga.
            </p>

            <p>
                Real money/payment features public karne se pehle local laws, age rules aur compliance
                check karna user ki responsibility hai.
            </p>

            <br>
            <a href="/" class="btn">Back to Home</a>
        </div>
    </div>
    """)


@app.route("/contact")
def contact():
    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>Contact Support</h1>

        <div class="mode-card">
            <p>Support ke liye email karein:</p>

            <h3>support@firezoneesports.com</h3>

            <p>
                Issue bhejte time apna username, mobile number aur problem ka screenshot zaroor bhejein.
            </p>

            <br>
            <a href="/" class="btn">Back to Home</a>
        </div>
    </div>
    """)

@app.route("/refer")
def refer():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT referral_code FROM users WHERE username=?", (session["user"],))
    data = c.fetchone()
    conn.close()

    referral_code = data[0] if data and data[0] else "NO-CODE"

    app_link = "https://firezone-esports-92ff.onrender.com"
    message = f"Join FireZone Esports using my referral code: {referral_code} {app_link}"
    whatsapp_link = "https://wa.me/?text=" + message.replace(" ", "%20")

    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>🎁 Refer & Earn</h1>

        <div class="mode-card">
            <h2>Your Referral Code</h2>
            <h1>{{referral_code}}</h1>

            <p>Apne friends ko ye referral code bhejo.</p>

            <a href="{{whatsapp_link}}" class="btn">Share on WhatsApp</a>
            <br><br>

            <a href="/referral_history" class="btn">Referral History</a>
            <br><br>

            <a href="/profile" class="btn">Back to Profile</a>
        </div>
    </div>
    """, referral_code=referral_code, whatsapp_link=whatsapp_link)


@app.route("/referral_history")
def referral_history():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT referred_username, status, date 
    FROM referrals 
    WHERE referrer_username=?
    ORDER BY id DESC
    """, (session["user"],))

    refs = c.fetchall()
    conn.close()

    pending = [r for r in refs if r[1] == "PENDING"]
    completed = [r for r in refs if r[1] == "COMPLETED"]

    return render_template_string(STYLE + """
    <div class="overlay">
        <h1>📜 Referral History</h1>

        <div class="mode-card">
            <h2>⏳ Pending Refer</h2>

            {% if pending %}
                {% for r in pending %}
                    <p>👤 {{r[0]}} | {{r[2]}}</p>
                {% endfor %}
            {% else %}
                <p>No pending referrals.</p>
            {% endif %}
        </div>

        <div class="mode-card">
            <h2>✅ Completed Refer</h2>

            {% if completed %}
                {% for r in completed %}
                    <p>👤 {{r[0]}} | {{r[2]}}</p>
                {% endfor %}
            {% else %}
                <p>No completed referrals.</p>
            {% endif %}
        </div>

        <br>
        <a href="/refer" class="btn">Back</a>
    </div>
    """, pending=pending, completed=completed)

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app.run(debug=True)

