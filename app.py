import streamlit as st

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Dự đoán giá ",
    page_icon="🏠",
    layout="wide"
)

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
body {
    background-color: #f6f7fb;
}
.block-container {
    padding-top: 1.5rem;
}
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}
.big-title {
    font-size: 36px;
    font-weight: 700;
}
.subtitle {
    color: #6b7280;
}
.price {
    font-size: 32px;
    font-weight: bold;
    color: #16a34a;
}
.stButton>button {
    width: 100%;
    height: 48px;
    font-size: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
st.markdown("""
<div class="card">
    <div class="big-title">🏠 DỰ ĐOÁN GIÁ NHÀ TPHCM</div>
    <div class="subtitle">Ứng dụng AI hỗ trợ tham khảo giá bất động sản</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ===============================
# MAIN LAYOUT
# ===============================
col1, col2 = st.columns([1, 1])

# ===============================
# LEFT - INPUT CARD
# ===============================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📌 Thông tin căn nhà")

    area = st.number_input("Diện tích (m²)", 20, 1000, 60)
    bedrooms = st.selectbox("Số phòng ngủ", [1, 2, 3, 4, 5])
    bathrooms = st.selectbox("Số phòng vệ sinh", [1, 2, 3])
    floor = st.selectbox("Tầng", [1, 2, 3, 4, 5])
    huong=st.selectbox("Hướng",["Đông","Tây","Nam","Bắc"])
    district = st.selectbox(
        "Quận",
        ["Quận 1", "Quận 3", "Quận 7", "Bình Thạnh", "Thủ Đức"]
    )
    ward=st.selectbox(
        "Phường",
        ["Phường 1", "Phường 2", "Phường 3", "Phường 4", "Phường 5"]
    )
    house_type = st.radio(
        "Loại nhà",
        ["Nhà phố", "Chung cư", "Biệt thự"],
        horizontal=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# RIGHT - RESULT CARD
# ===============================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Kết quả dự đoán")

    if st.button("🔮 Dự đoán giá"):
        st.markdown('<div class="price">3.200.000.000 VNĐ</div>', unsafe_allow_html=True)
        
        st.success("Dự đoán thành công")
        st.info("Giá chỉ mang tính tham khảo")

    else:
        st.markdown('<div class="price">---</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.write("")

