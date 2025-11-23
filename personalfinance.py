import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

DB_PATH = 'finance.db'
CATEGORIES = [
    'Food', 'Transport', 'Rent', 'Utilities', 'Entertainment',
    'Education', 'Health', 'Shopping', 'Savings', 'Other'
]

# ------------------ DB Setup ------------------
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password_hash TEXT,
                    email TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS incomes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    source TEXT,
                    date TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    category TEXT,
                    note TEXT,
                    date TEXT)''')
    conn.commit()
    conn.close()


# ------------------ Auth ------------------
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()


def signup(username, password, email):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users(username, password_hash, email) VALUES (?, ?, ?)',
                    (username, hash_password(password), email))
        conn.commit()
        return True
    except:
        return False


def login(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, username, email FROM users WHERE username=? AND password_hash=?',
                (username, hash_password(password)))
    row = cur.fetchone()
    return row


# ------------------ Finance functions ------------------
def add_income(uid, amount, source, date):
    conn = get_conn()
    conn.execute('INSERT INTO incomes(user_id,amount,source,date) VALUES(?,?,?,?)',
                (uid, amount, source, date))
    conn.commit()


def add_expense(uid, amount, category, note, date):
    conn = get_conn()
    conn.execute('INSERT INTO expenses(user_id,amount,category,note,date) VALUES(?,?,?,?,?)',
                (uid, amount, category, note, date))
    conn.commit()


def get_summary(uid):
    conn = get_conn()
    total_inc = conn.execute('SELECT SUM(amount) FROM incomes WHERE user_id=?', (uid,)).fetchone()[0] or 0
    total_exp = conn.execute('SELECT SUM(amount) FROM expenses WHERE user_id=?', (uid,)).fetchone()[0] or 0
    cat = conn.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category', (uid,)).fetchall()
    return total_inc, total_exp, cat


def get_expense_df(uid):
    conn = get_conn()
    df = pd.read_sql_query('SELECT * FROM expenses WHERE user_id=?', conn, params=(uid,))
    return df


# ------------------ Prediction ------------------
def predict_next(uid):
    df = get_expense_df(uid)
    if df.empty:
        return None
    df['date'] = pd.to_datetime(df['date'])
    monthly = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
    monthly['month_num'] = np.arange(len(monthly))

    X = monthly[['month_num']]
    y = monthly['amount']

    poly = PolynomialFeatures(2, include_bias=False)
    Xp = poly.fit_transform(X)
    model = LinearRegression().fit(Xp, y)

    next_month = poly.transform([[len(monthly)]])
    return model.predict(next_month)[0]


# ------------------ Streamlit UI ------------------
init_db()
st.title('📊 Personal Finance Manager')

if 'user' not in st.session_state:
    st.session_state.user = None

# ---------- AUTH ----------
if st.session_state.user is None:
    tab1, tab2 = st.tabs(['Login', 'Sign Up'])

    with tab1:
        u = st.text_input('Username')
        p = st.text_input('Password', type='password')
        if st.button('Login'):
            user = login(u, p)
            if user:
                st.session_state.user = user
                st.success('Login successful!')
            else:
                st.error('Invalid credentials')

    with tab2:
        nu = st.text_input('New Username')
        npw = st.text_input('New Password', type='password')
        em = st.text_input('Email (optional)')
        if st.button('Create Account'):
            if signup(nu, npw, em):
                st.success('Account created. Login now.')
            else:
                st.error('Username already exists.')

else:
    uid = st.session_state.user[0]
    st.sidebar.title('Menu')
    opt = st.sidebar.radio('Select', ['Dashboard', 'Add Income', 'Add Expense', 'Prediction', 'View Data', 'Logout'])

    if opt == 'Dashboard':
        total_inc, total_exp, cat = get_summary(uid)
        st.subheader('📌 Summary')
        st.write(f"**Total Income:** {total_inc}")
        st.write(f"**Total Expense:** {total_exp}")
        st.write(f"**Balance:** {total_inc - total_exp}")

        df_cat = pd.DataFrame(cat, columns=['Category', 'Total'])
        if not df_cat.empty:
            st.subheader('Category-wise Expense')
            st.bar_chart(df_cat.set_index('Category'))

    if opt == 'Add Income':
        amt = st.number_input('Amount')
        src = st.text_input('Source')
        date = st.date_input('Date', datetime.now())
        if st.button('Add Income'):
            add_income(uid, amt, src, str(date))
            st.success('Income added!')

    if opt == 'Add Expense':
        amt = st.number_input('Amount')
        cat = st.selectbox('Category', CATEGORIES)
        note = st.text_input('Note')
        date = st.date_input('Date', datetime.now())
        if st.button('Add Expense'):
            add_expense(uid, amt, cat, note, str(date))
            st.success('Expense added!')

    if opt == 'Prediction':
        st.subheader('🧠 AI Prediction')
        pred = predict_next(uid)
        if pred:
            st.success(f"Next month estimated expense: ₹{pred:.2f}")
        else:
            st.warning('Not enough data to predict.')

    if opt == 'View Data':
        df = get_expense_df(uid)
        st.dataframe(df)

    if opt == 'Logout':
        st.session_state.user = None
        st.success('Logged out.')
