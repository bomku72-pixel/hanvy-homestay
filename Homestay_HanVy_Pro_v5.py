import streamlit as st

st.set_page_config(
    page_title="Hàn Vỹ Homestay Pro",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 HÀN VỸ HOMESTAY PRO V5")

st.success("Kết nối Supabase thành công")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Tổng phòng", 8)

with col2:
    st.metric("Đang thuê", 0)

with col3:
    st.metric("Phòng trống", 8)

with col4:
    st.metric("Doanh thu tháng", "0 ₫")

st.divider()

st.info(
    """
    Menu chức năng nằm bên trái:

    • Dashboard
    • Đặt phòng
    • Dịch vụ
    • Thu chi
    • Báo cáo
    """
)