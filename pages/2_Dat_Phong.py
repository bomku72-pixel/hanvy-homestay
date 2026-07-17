from database import supabase

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