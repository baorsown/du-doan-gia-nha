import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="Dự đoán & So sánh giá nhà",
    page_icon="🏠",
    layout="wide"
)

# ===============================
# LOAD DATA
# ===============================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data_vn.csv")

@st.cache_data
def load_base_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    return df

df = load_base_data()

# ===============================
# UPLOAD CSV / EXCEL
# ===============================
st.sidebar.subheader("📂 Thêm dữ liệu từ file")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV hoặc Excel",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df_new = pd.read_csv(uploaded_file)
    else:
        df_new = pd.read_excel(uploaded_file)

    df_new.columns = df_new.columns.str.strip()
    df = pd.concat([df, df_new], ignore_index=True)
    st.sidebar.success(f"✅ Đã thêm {len(df_new)} dòng dữ liệu")

# ===============================
# HIỂN THỊ DỮ LIỆU
# ===============================
st.subheader("📋 Dữ liệu hiện có")
st.caption(f"Tổng số dòng dữ liệu: {len(df)}")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

# ===============================
# ENCODE + TRAIN MODEL
# ===============================
df_model = df.copy()

cat_cols = ["LoaiNha", "PhanVung", "LoaiToaNha", "VatLieuNgoai"]
encode_maps = {}

for col in cat_cols:
    df_model[col] = df_model[col].astype("category")
    encode_maps[col] = {
        v: k for k, v in enumerate(df_model[col].cat.categories)
    }
    df_model[col] = df_model[col].map(encode_maps[col])

X = df_model[
    [
        "DienTichLot",
        "TinhTrangTongThe",
        "NamXayDung",
        "NamSuaChua",
        "BsmtFinSF2",
        "TongSoBsmtSF",
        "LoaiNha",
        "PhanVung",
        "LoaiToaNha",
        "VatLieuNgoai"
    ]
]

y = df_model["GiaBan"]

model = LinearRegression()
model.fit(X, y)

def safe_encode(value, mapping):
    return mapping.get(value, -1)

# ===============================
# DỰ ĐOÁN
# ===============================
st.subheader("🔮 Dự đoán giá nhà")

c1, c2 = st.columns(2)

with c1:
    dientich = st.number_input("Diện tích lô (m²)", 20, 500, 120)
    tinhtrang = st.slider("Tình trạng tổng thể", 1, 10, 7)
    namxay = st.slider("Năm xây dựng", 1990, 2024, 2015)
    namsua = st.slider("Năm sửa chữa", 1990, 2024, 2018)
    bsmt2 = st.number_input("BsmtFinSF2", 0, 300, 40)

with c2:
    tongbsmt = st.number_input("Tổng Bsmt", 0, 400, 80)
    loainha = st.selectbox("Loại nhà", df["LoaiNha"].unique())
    phanvung = st.selectbox("Khu vực", df["PhanVung"].unique())
    loaitoanha = st.selectbox("Loại tòa nhà", df["LoaiToaNha"].unique())
    vatlieu = st.selectbox("Vật liệu ngoài", df["VatLieuNgoai"].unique())

# ===============================
# BUTTON DỰ ĐOÁN + BIỂU ĐỒ
# ===============================
if st.button("🔮 Dự đoán giá & So sánh"):
    input_data = pd.DataFrame([{
        "DienTichLot": dientich,
        "TinhTrangTongThe": tinhtrang,
        "NamXayDung": namxay,
        "NamSuaChua": namsua,
        "BsmtFinSF2": bsmt2,
        "TongSoBsmtSF": tongbsmt,
        "LoaiNha": safe_encode(loainha, encode_maps["LoaiNha"]),
        "PhanVung": safe_encode(phanvung, encode_maps["PhanVung"]),
        "LoaiToaNha": safe_encode(loaitoanha, encode_maps["LoaiToaNha"]),
        "VatLieuNgoai": safe_encode(vatlieu, encode_maps["VatLieuNgoai"]),
    }])

    price = model.predict(input_data)[0]
    st.success(f"💰 Giá dự đoán: {price:,.0f} VNĐ")

    # ===============================
    # BIỂU ĐỒ SO SÁNH THEO KHU
    # ===============================
    st.subheader("📊 So sánh giá nhà theo khu vực")

    compare_df = (
        df.groupby("PhanVung", as_index=False)["GiaBan"]
        .mean()
    )

    compare_df.loc[
        compare_df["PhanVung"] == phanvung,
        "GiaBan"
    ] = price

    fig, ax = plt.subplots()

    bars = ax.bar(
        compare_df["PhanVung"],
        compare_df["GiaBan"]
    )

    for bar, zone in zip(bars, compare_df["PhanVung"]):
        if zone == phanvung:
            bar.set_color("red")

    avg_city = df["GiaBan"].mean()
    ax.axhline(avg_city, linestyle="--", label="Giá trung bình toàn khu vực")
    ax.legend()

    ax.set_xlabel("Khu vực")
    ax.set_ylabel("Giá (VNĐ)")

    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h,
            f"{h:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    st.pyplot(fig)


