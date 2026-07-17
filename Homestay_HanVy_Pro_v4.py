
import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, timedelta
from hashlib import sha256

st.set_page_config(page_title="Homestay Hàn Vỹ Pro", layout="wide")

DB="hanvy_pro.db"
conn=sqlite3.connect(DB,check_same_thread=False)

def init_db():
    c=conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS rooms(
    room_number TEXT PRIMARY KEY,
    room_type TEXT,
    price INTEGER,
    status TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT,
    guest_name TEXT,
    phone TEXT,
    cccd TEXT,
    checkin TEXT,
    checkout TEXT,
    deposit INTEGER,
    room_price INTEGER,
    total_room INTEGER,
    status TEXT DEFAULT 'Đã đặt'
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS services(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    service_name TEXT,
    qty INTEGER,
    unit_price INTEGER,
    total INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date TEXT,
    category TEXT,
    amount INTEGER,
    note TEXT
    )""")

    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0]==0:
        c.execute(
            "INSERT INTO users VALUES (?,?)",
            ("admin", sha256("admin123".encode()).hexdigest())
        )

    if c.execute("SELECT COUNT(*) FROM rooms").fetchone()[0]==0:
        rooms=[
            ("201","Đơn",450000,"Trống"),
            ("202","Đơn",450000,"Trống"),
            ("203","Đôi",550000,"Trống"),
            ("204","Đơn",450000,"Trống"),
            ("301","Đơn",450000,"Trống"),
            ("302","Đơn",450000,"Trống"),
            ("303","Đôi",550000,"Trống"),
            ("304","Đơn",450000,"Trống"),
        ]
        c.executemany("INSERT INTO rooms VALUES (?,?,?,?)",rooms)

    conn.commit()

init_db()

if "auth" not in st.session_state:
    st.session_state.auth=False

if not st.session_state.auth:
    st.title("🏡 HOMESTAY HÀN VỸ PRO")
    u=st.text_input("Tài khoản")
    p=st.text_input("Mật khẩu",type="password")
    if st.button("Đăng nhập"):
        hp=sha256(p.encode()).hexdigest()
        ok=conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u,hp)
        ).fetchone()
        if ok:
            st.session_state.auth=True
            st.rerun()
        else:
            st.error("Sai thông tin")
    st.stop()

st.title("🏡 HOMESTAY HÀN VỸ PRO")

rooms=pd.read_sql("SELECT * FROM rooms",conn)
bookings=pd.read_sql("SELECT * FROM bookings",conn)

revenue = bookings["total_room"].sum() if not bookings.empty else 0

c1,c2,c3,c4=st.columns(4)
c1.metric("Tổng phòng",8)
c2.metric("Phòng trống",len(rooms[rooms.status=="Trống"]))
c3.metric("Đang thuê",len(rooms[rooms.status!="Trống"]))
c4.metric("Doanh thu",f"{revenue:,.0f} đ")

tabs=st.tabs([
"📅 Đặt phòng",
"🏠 Phòng",
"🛎️ Dịch vụ",
"💸 Thu chi",
"📊 Báo cáo"
])

with tabs[0]:
    st.subheader("Tạo booking")

    free_rooms=rooms["room_number"].tolist()

    with st.form("booking_form"):
        room=st.selectbox("Phòng",free_rooms)
        guest=st.text_input("Tên khách")
        phone=st.text_input("SĐT")
        cccd=st.text_input("CCCD")
        ci=st.date_input("Checkin",date.today())
        co=st.date_input("Checkout",date.today()+timedelta(days=1))
        deposit=st.number_input("Tiền cọc",0,100000000,0)

        submit=st.form_submit_button("Lưu")

        if submit:
            price=int(
                rooms.loc[rooms.room_number==room,"price"].iloc[0]
            )
            nights=max((co-ci).days,1)
            total=price*nights

            conn.execute("""
            INSERT INTO bookings(
            room_number,guest_name,phone,cccd,
            checkin,checkout,deposit,
            room_price,total_room,status)
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,(room,guest,phone,cccd,
                 str(ci),str(co),deposit,
                 price,total,"Đang ở"))

            conn.execute(
                "UPDATE rooms SET status='Đang thuê' WHERE room_number=?",
                (room,)
            )
            conn.commit()
            st.success("Đã tạo booking")

    st.dataframe(pd.read_sql("SELECT * FROM bookings ORDER BY id DESC",conn))

with tabs[1]:
    st.dataframe(pd.read_sql("SELECT * FROM rooms",conn),use_container_width=True)

    active=pd.read_sql(
        "SELECT id,room_number,guest_name FROM bookings WHERE status='Đang ở'",
        conn
    )

    if not active.empty:
        bid=st.selectbox("Checkout Booking",active["id"])
        if st.button("Checkout"):
            room=conn.execute(
                "SELECT room_number FROM bookings WHERE id=?",
                (int(bid),)
            ).fetchone()[0]

            conn.execute(
                "UPDATE bookings SET status='Checkout' WHERE id=?",
                (int(bid),)
            )
            conn.execute(
                "UPDATE rooms SET status='Trống' WHERE room_number=?",
                (room,)
            )
            conn.commit()
            st.success("Checkout thành công")

with tabs[2]:
    bks=pd.read_sql(
        "SELECT id,guest_name,room_number FROM bookings",
        conn
    )

    if not bks.empty:
        bid=st.selectbox("Booking",bks["id"])

        sname=st.text_input("Tên dịch vụ")
        qty=st.number_input("SL",1,100,1)
        price=st.number_input("Đơn giá",0,10000000,0)

        if st.button("Thêm dịch vụ"):
            conn.execute("""
            INSERT INTO services(
            booking_id,service_name,qty,unit_price,total)
            VALUES(?,?,?,?,?)
            """,(int(bid),sname,qty,price,qty*price))
            conn.commit()
            st.success("Đã thêm")

    st.dataframe(pd.read_sql("SELECT * FROM services",conn))

with tabs[3]:
    category=st.text_input("Khoản chi")
    amount=st.number_input("Số tiền",0,100000000,0)
    note=st.text_input("Ghi chú")

    if st.button("Lưu chi phí"):
        conn.execute(
            "INSERT INTO expenses(expense_date,category,amount,note) VALUES(?,?,?,?)",
            (str(date.today()),category,amount,note)
        )
        conn.commit()

    st.dataframe(pd.read_sql("SELECT * FROM expenses",conn))

with tabs[4]:
    services=pd.read_sql("SELECT * FROM services",conn)
    expenses=pd.read_sql("SELECT * FROM expenses",conn)

    service_rev=services["total"].sum() if not services.empty else 0
    expense=expenses["amount"].sum() if not expenses.empty else 0

    total=revenue+service_rev
    profit=total-expense

    st.metric("Doanh thu phòng",f"{revenue:,.0f} đ")
    st.metric("Doanh thu dịch vụ",f"{service_rev:,.0f} đ")
    st.metric("Chi phí",f"{expense:,.0f} đ")
    st.metric("Lợi nhuận",f"{profit:,.0f} đ")

st.caption("Admin mặc định: admin / admin123")
