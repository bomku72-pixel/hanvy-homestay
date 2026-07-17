import streamlit as st

st.title("📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tổng phòng", 8)
col2.metric("Đang thuê", 0)
col3.metric("Trống", 8)
col4.metric("Tiền cọc", "0 ₫")

st.divider()

st.write("Dashboard doanh thu sẽ được kết nối Supabase ở bước tiếp theo.")