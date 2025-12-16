import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import os

# ===============================
# LOAD DATA & TRAIN MODEL
# ===============================
@st.cache_data
def load_model():
    BASE_DIR = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(BASE_DIR, "data_nha.csv"))

    # Mã hóa quận
    district_map = {
        "Quận 1": 1,
        "Quận 7": 2,
        "Bình Thạnh": 3,
        "Thủ Đức": 4,
        "Quận 3": 5
    }

    # Mã hóa hướng
    huong_map = {
        "Đông": 1,
        "Tây": 2,
        "Nam": 3,
        "Bắc": 4
    }

    df["district_code"] = df["district"].map(district_map)
    df["huong_code"] = df["huong"].map(huong_map)

    X = df[[
        "area",
        "bedrooms",
        "bathrooms",
        "floor",
        "district_code",
        "huong_code"
    ]]
    y = df["price"]

    model = LinearRegression()
    model.fit(X, y)

    return model, district_map, huong_map


model, district_map, huong_map = load_model()

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Dự đoán giá nhà",
    page_icon="🏠",
    layout="wide"
)

# ===============================
# CUSTOM CSS
# ===============================
st.markdown("""
<style>
body { background-color: #f6f7fb; }
.block-container { padding-top: 1.5rem; }
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}
.big-title { font-size: 36px; font-weight: 700; }
.subtitle { color: #6b7280; }
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
col1, col2 = st.columns(2)

# ===============================
# LEFT - INPUT
# ===============================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📌 Thông tin căn nhà")

    area = st.number_input("Diện tích (m²)", 20, 300, 60)
    bedrooms = st.selectbox("Số phòng ngủ", [1, 2, 3, 4, 5])
    bathrooms = st.selectbox("Số phòng vệ sinh", [1, 2, 3])
    floor = st.selectbox("Số tầng", [1, 2, 3, 4, 5])

    district = st.selectbox("Quận", list(district_map.keys()))
    huong = st.selectbox("Hướng nhà", list(huong_map.keys()))

    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# RIGHT - RESULT
# ===============================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Kết quả dự đoán")

    if st.button("🔮 Dự đoán giá"):
        input_data = [[
            area,
            bedrooms,
            bathrooms,
            floor,
            district_map[district],
            huong_map[huong]
        ]]

        predicted_price = model.predict(input_data)[0]

        st.markdown(
            f'<div class="price">{predicted_price:,.0f} VNĐ</div>',
            unsafe_allow_html=True
        )

        st.success("Dự đoán thành công")
        st.info("Giá mang tính tham khảo")

    else:
        st.markdown('<div class="price">---</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
