import streamlit as st
from database import supabase

st.title("🛏️ Đặt phòng")

room = st.selectbox(
    "Chọn phòng",
    ["201","202","203","204","301","302","303","304"]
)

name = st.text_input("Tên khách")
phone = st.text_input("Số điện thoại")
cccd = st.text_input("CCCD")

deposit = st.number_input(
    "Tiền cọc",
    min_value=0,
    step=100000
)

if st.button("Lưu đặt phòng"):

    data = {
        "room_number": room,
        "customer_name": name,
        "phone": phone,
        "cccd": cccd,
        "deposit": deposit
    }

    supabase.table("bookings").insert(data).execute()

    supabase.table("rooms").update({
        "status": "Đang thuê"
    }).eq("room_number", room).execute()

    st.success(f"Đã lưu đặt phòng {room}")