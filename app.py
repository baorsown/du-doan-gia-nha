import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="Dự đoán & So sánh giá nhà",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Ứng dụng dự đoán & so sánh giá nhà")

# ===============================
# LOAD DATA GỐC
# ===============================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data_vn_day_du_co_quan.csv")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df

df = load_data(DATA_PATH)

# ===============================
# UPLOAD CSV / EXCEL
# ===============================
st.sidebar.header("📂 Thêm dữ liệu")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV hoặc Excel",
    type=["csv", "xlsx"]
)

if uploaded_file:
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
st.caption(f"Tổng số dòng: {len(df)}")
st.dataframe(df.head(50), use_container_width=True)

# ===============================
# CHUẨN HÓA CỘT (SAFE)
# ===============================
df_model = df.copy()

num_cols = [
    "DienTichLot",
    "TinhTrangTongThe",
    "NamXayDung",
    "NamSuaChua",
    "BsmtFinSF2",
    "TongSoBsmtSF",
    "GiaBan"
]

for col in num_cols:
    if col not in df_model.columns:
        df_model[col] = 0

cat_cols = ["LoaiNha", "PhanVung", "Quan", "LoaiToaNha", "VatLieuNgoai"]
encode_maps = {}

for col in cat_cols:
    if col not in df_model.columns:
        df_model[col] = "KhongXacDinh"

    df_model[col] = df_model[col].astype("category")
    encode_maps[col] = {
        v: k for k, v in enumerate(df_model[col].cat.categories)
    }
    df_model[col] = df_model[col].map(encode_maps[col])

# ===============================
# TRAIN MODEL
# ===============================
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
        "Quan",
        "LoaiToaNha",
        "VatLieuNgoai"
    ]
]

y = df_model["GiaBan"]

model = LinearRegression()
model.fit(X, y)

def safe_encode(value, mapping):
    return mapping.get(value, 0)

# ===============================
# INPUT DỰ ĐOÁN
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

    loainha = st.selectbox(
        "Loại nhà",
        df["LoaiNha"].unique() if "LoaiNha" in df.columns else ["KhongXacDinh"]
    )

    phanvung = st.selectbox(
        "Khu vực",
        df["PhanVung"].unique() if "PhanVung" in df.columns else ["KhongXacDinh"]
    )

    if "Quan" in df.columns and "PhanVung" in df.columns:
        quan_list = df[df["PhanVung"] == phanvung]["Quan"].unique()
        if len(quan_list) == 0:
            quan_list = ["KhongXacDinh"]
    else:
        quan_list = ["KhongXacDinh"]

    quan = st.selectbox("Quận", quan_list)

    loaitoanha = st.selectbox(
        "Loại tòa nhà",
        df["LoaiToaNha"].unique() if "LoaiToaNha" in df.columns else ["KhongXacDinh"]
    )

    vatlieu = st.selectbox(
        "Vật liệu ngoài",
        df["VatLieuNgoai"].unique() if "VatLieuNgoai" in df.columns else ["KhongXacDinh"]
    )

# ===============================
# BUTTON DỰ ĐOÁN
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
        "Quan": safe_encode(quan, encode_maps["Quan"]),
        "LoaiToaNha": safe_encode(loaitoanha, encode_maps["LoaiToaNha"]),
        "VatLieuNgoai": safe_encode(vatlieu, encode_maps["VatLieuNgoai"]),
    }])

    price = model.predict(input_data)[0]
    st.success(f"💰 Giá dự đoán: {price:,.0f} VNĐ")

    st.subheader("📊 So sánh giá theo khu vực")

    if "PhanVung" in df.columns:
        khu_df = df.groupby("PhanVung", as_index=False)["GiaBan"].mean()
        st.bar_chart(khu_df.set_index("PhanVung"), height=400)
