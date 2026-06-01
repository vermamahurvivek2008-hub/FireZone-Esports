#===========================================
#firezone - esport
#===========================================
import random
import requests
from flask import Flask
from flask import flash, render_template_string, request, redirect, url_for, session
import sqlite3
import hashlib
from datetime import datetime, timedelta
from functools  import wraps

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
app.secret_key = "firezone_secret"

ADMIN_USER = "admin"
ADMIN_PASS = "vivek123"

START_HOUR = 8
END_HOUR = 23
GAP_MINUTES = 30

# =========================================

# STYLE

# =========================================

STYLE = """

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


# =========================================
# DATABASE
# =========================================

def init_db():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE users ADD COLUMN banned INTEGER DEFAULT 0")
    except:
        pass

    c.execute("""
     CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    phone TEXT UNIQUE,
    referral_by TEXT
     )
      """)
    
    try:
        c.execute("ALTER TABLE users ADD COLUMN banned INTEGER DEFAULT 0")
    except:
        pass

    c.execute("""
    CREATE TABLE IF NOT EXISTS wallet(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
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
              winning_prize INTEGER
    )
    """)
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

    c.execute("""
    CREATE TABLE IF NOT EXISTS withdrawal_requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        amount INTEGER,
        upi TEXT,
        status TEXT
    )
    """)
   

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
                c.execute(
                    "DELETE FROM matches WHERE id=?",
                    (match_id,)
                )

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

    c.execute(
        "SELECT COUNT(*) FROM tournament WHERE mode=? AND slot=?",
        (mode, slot)
    )

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
    delete_old_matches
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
    if session["user"] !="admin":
        return "ACCESS DENIED"

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

            <div class="mode-title">
                <a href="/mode/duo br">
                    ENTER DUO BR
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
            <div class="mode-title">
                <a href="/mode/1v1 cs challenge">
                    ENTER 1V1 CS CHALLENGE
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
            <div class="mode-title">
                <a href="/mode/2v2 cs">
                    ENTER 2V2 CS
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
            <div class="mode-title">
                <a href="/mode/4v4 cs">
                    ENTER 4V4 CS
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
            <div class="mode-title">
                <a href="/mode/lone wolf">
                    ENTER LONE WOLF
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

            <div class="mode-title">
                <a href="/mode/sniper only br">
                    ENTER SNIPER MODE
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

            <div class="mode-title">
                <a href="/mode/booyah only br">
                    ENTER BOOYAH MODE
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
    SELECT id, username, mode, slot
    FROM tournament
    ORDER BY id DESC
    """)

    data = c.fetchall()

    conn.close()

    return render_template_string(STYLE + """
    <div class="overlay">

        <h1>🏆 AUTO RESULT SYSTEM</h1>

        {% for t in data %}

        <div class="info">

            👤 Username : {{t[1]}}

            <br><br>

            🎮 Mode : {{t[2]}}

            <br><br>

            🎯 Slot : {{t[3]}}

            <br><br>

            <form method="POST"
            action="/admin/add_kills/{{t[0]}}">

                <input
                type="number"
                name="kills"
                placeholder="Enter Kills"
                required>

                <br><br>

                <button type="submit">
                SUBMIT RESULT
                </button>

            </form>

        </div>

        {% endfor %}

    </div>
    """, data=data)
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

        mode = request.form["mode"]

        slot = auto_format_slot(request.form["slot"])

        winning_prize = request.form["winning_prize"]


        conn = sqlite3.connect("database.db")

        c = conn.cursor()

        c.execute("""

        INSERT INTO matches(

            mode,
            slot,
            status,
            entry_fee,
            winning_prize

        )

        VALUES(?,?,?,?,?)

        """,(

            mode,
            slot,
            "UPCOMING",
            0,
            winning_prize

        ))

        conn.commit()

        conn.close()


        return render_template_string(STYLE + """

        <div class="overlay">

            <div class="box">

                <h1>🚨 FREE MATCH CREATED</h1>

                <br><br>

                <h2>JOIN FAST ⚡</h2>

                <br>

                🎮 Mode : {{mode.upper()}}

                <br><br>

                💸 Entry Fee : FREE

                <br><br>

                🏆 Prize : ₹{{winning_prize}}

                <br><br>

                LIMITED SLOTS AVAILABLE 🔥

            </div>

        </div>

        """,

        mode=mode,

        winning_prize=winning_prize
        )


    return render_template_string(STYLE + """

    <div class="overlay">

        <div class="box">

            <h1>🎁 CREATE FREE MATCH</h1>

            <form method="POST">

                <input name="mode"
                placeholder="Mode"
                required>

                <input name="slot"
                placeholder="Slot"
                required>

                <input name="winning_prize"
                placeholder="Prize"
                required>

                <button>CREATE</button>

            </form>

        </div>

    </div>

    """)

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

    SELECT id,mode,slot,winning_prize

    FROM matches

    WHERE entry_fee=0

    ORDER BY id DESC

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

            🏆 Prize : ₹{{m[3]}}

            <br><br>

            <a class="mode-btn"
            href="/user_custom_room/{{m[0]}}">

            JOIN MATCH

            </a>

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

    SELECT id,mode,slot,entry_fee,winning_prize,status
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
                                  <a class="mode-btn" href="/custom_room/{{m[0]}}">
                                  JOIN TOURNAMENT
                                  </a>

        </div>
                                  <br>

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
                                  <a class="mode-btn" href="/join/{{mode}}/{{slot}}">
                                  JOIN TOURNAMENT
                                  </a>
                                  <a class="mode-btn" href="/join_custom_rooms">
                                  BACK
                                  </a>
        </div>

    </div>

    """,mode=mode,slot=slot,status=status, entry_fee=entry_fee,winning_prize=winning_prize,
      data=data)
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
        winning_prize

    )

    VALUES(?,?,?,?,?)

    """, (

        mode,
        slot,
        "UPCOMING",
        entry_fee,
        winning_prize

    ))

    conn.commit()
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
    slot=slot
    )

#delete tournament
@app.route("/delete_tournament/<int:id>")
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
    entry_fee,winning_prize

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

        </div>

        <br>

        {% endfor %}

    </div>

    """, matches=matches)

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

            {% if "cs" in mode or mode == "lone wolf" %}

                🏆 Winning Prize : ₹{{winning_prize}}

            {% else %}

                🔫 Per Kill Reward : ₹{{winning_prize}}

            {% endif %}

            <br><br>

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




# =========================================
# SIGNUP
# =========================================

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()
        phone = request.form["phone"]
        referral = request.form["referral"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                  SELECT phone FROM users WHERE phone=?""",(phone,))
        phone_data = c.fetchone()
        if phone_data:
            conn.close()
            return " phone number already registered"
        referral = request.form["referral"]

        

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
        "referral": referral,
        "otp": otp
        }

        send_otp(phone,otp)
        return redirect("/verify_otp")


        # wallet safe insert
        c.execute("""
            INSERT OR IGNORE INTO wallet(username,balance)
            VALUES(?,0)
        """, (username,))

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
                                  <input name="referral" placeholder="referral username(optional)">

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
        INSERT INTO users(username,password,phone,referral_by)
        VALUES(?,?,?,?)
        """,(data["username"],data["password"],data["phone"],data["referral"]))

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
            WHERE username=? AND password=?
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
        <a class="mode-btn" href="/admin/withdrawals">WITHDRAW REQUESTS</a>
                                  <a class="mode-btn" href="/admin/notification">SEND NOTIFICATIONS</a>
                                  <a class="mode-btn" href="/admin/reports">VIEW REPORTS</a>
                                  <a class="mode-btn" href="/admin/banned_users">
                                  BANNED USERS </a>
                                  <a class="mode-btn" href="/admin/results">AUTO RESULTS</a>
        <a class="mode-btn" href="/logout">LOGOUT</a>

    </div>
    """)

#admin withdrawals
@app.route("/admin/withdrawals")
@admin_required
def admin_withdrawals():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT id, username, amount, upi, status
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

            📱 UPI : {{w[3]}}

            <br><br>

            📢 Status : {{w[4]}}

            <br><br>

            <form action="/admin/approve_withdraw/{{w[0]}}" method="GET">

                <button type="submit">
                    ✅ APPROVE
                </button>

            </form>

            <br>

            <form action="/admin/reject_withdraw/{{w[0]}}" method="GET">

                <button type="submit">
                    ❌ REJECT
                </button>

            </form>

        </div>

        {% endfor %}

    </div>
    """, data=data)
#admin approve withdrawals
@app.route("/admin/approve_withdraw/<int:id>")
@admin_required
def approve_withdraw(id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT username, amount
    FROM withdrawal_requests
    WHERE id=?
    """,(id,))

    data = c.fetchone()

    if not data:
        conn.close()
        return "❌ REQUEST NOT FOUND"

    username = data[0]
    amount = data[1]

    c.execute("""
    UPDATE withdrawal_requests
    SET status='APPROVED'
    WHERE id=?
    """,(id,))

    c.execute("""
    INSERT INTO notifications(message)
    VALUES(?)
    """,(f"✅ {username}, your withdrawal of ₹{amount} is APPROVED",))

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
    SELECT username, amount
    FROM withdrawal_requests
    WHERE id=?
    """,(id,))

    data = c.fetchone()

    if not data:
        conn.close()
        return "❌ REQUEST NOT FOUND"

    username = data[0]
    amount = data[1]

    c.execute("""
    UPDATE withdrawal_requests
    SET status='REJECTED'
    WHERE id=?
    """,(id,))

    c.execute("""
    INSERT INTO notifications(message)
    VALUES(?)
    """,(f"❌ {username}, your withdrawal of ₹{amount} is REJECTED",))

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
                <input name="time" placeholder="time (12:00 PM)" required>
                <input name="room_id" placeholder="Room ID" required>
                <input name="password" placeholder="Password" required>

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
    WHERE username=? AND mode=? AND slot=?
    """,(username,mode,slot))

    if c.fetchone():
        conn.close()
        return "❌ ALREADY JOINED"
    
    c.execute("""
              SELECT COUNT(*) FROM tournament WHERE mode=? AND slot=?
              """,(mode,slot))
    count = c.fetchone()[0]
    if count >= 48:
        conn.close()
        return"match full"


    c.execute(
        "UPDATE wallet SET balance = balance - ? WHERE username=?",
        (entry_fee,username)
    )

    c.execute("""
    INSERT INTO tournament(username,mode,slot,status)
VALUES(?,?,?,?)
    """,(username,mode,slot,"UPCOMING"))
    
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

            if diff > 10:
                status = "UPCOMING"
            elif -10 <= diff <= 10:
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

    if "user" not in session:
        return redirect("/login")
    
    update_match_status()
    status = get_match_status(mode, slot)

    count = get_count(mode, slot)

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        "SELECT username FROM tournament WHERE mode=? AND slot=?",
        (mode,slot)
    )

    players = c.fetchall()

    c.execute(
        "SELECT room_id,password,status FROM matches WHERE mode=? AND slot=?",
        (mode,slot)
    )

    data = c.fetchone()
    if not data:
     room_id = "NOT AVAILABLE"
     password = "NOT AVAILABLE"
     status = "UPCOMING"
    else:
        room_id = data[0]
        password = data[1]
        status = data[2]
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

            <li>{{p[0]}}</li>

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
    players=players
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
        # GET REFERRAL USER
        # =================================

        c.execute("""
        SELECT referral_by
        FROM users
        WHERE username=?
        """,(username,))

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

            reward = amount * 0.05

            c.execute("""
            UPDATE wallet
            SET balance = balance + ?
            WHERE username=?
            """,(reward,referral_user))

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
        upi = request.form["upi"]
        balance = get_balance(username)
        if amount > balance:
            return " low balance"

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO withdrawal_requests(username,amount,upi,status) VALUES(?,?,?,?)",
            (username,amount,upi,"PENDING")
        )

        conn.commit()
        conn.close()

        return "✅ REQUEST SENT"

    return render_template_string(STYLE + """

    <div class="overlay">

        <div class="box">

            <h1>💸 WITHDRAWAL</h1>

            <form method="POST">

                <input name="amount" type="number" placeholder="Amount">

                <input name="upi" placeholder="UPI ID">

                <button>REQUEST</button>

            </form>

        </div>

    </div>

    """)

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

    c.execute(
        "SELECT username,phone FROM users WHERE username=?",
        (username,)
    )

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

            💰 Balance : ₹{{balance}}

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


# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    app.run(debug=True)

