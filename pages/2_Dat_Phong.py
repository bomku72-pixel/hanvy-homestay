import streamlit as st

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
    st.success(f"Đã lưu đặt phòng {room}")