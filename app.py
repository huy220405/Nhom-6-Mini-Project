import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cấu hình trang
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")

# Tiêu đề
st.title("🛍️ Dashboard Phân Cụm Khách Hàng (Shopping Analysis)")
st.markdown("**Nhóm 6 - Mini Project Data Mining**")
st.write("---")

# Cột bên trái: Upload file
with st.sidebar:
    st.header("📂 Tải dữ liệu")
    uploaded_file = st.file_uploader("Chọn file 'customer_clusters_from_rules.csv'", type=["csv"])
    st.write("💡 *Mẹo: File nằm trong thư mục data/processed*")

# Phần chính
if uploaded_file is not None:
    # 1. Đọc dữ liệu
    df = pd.read_csv(uploaded_file)
    
    # 2. Hiển thị KPI tổng quan
    st.header("1. Tổng quan dữ liệu")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số khách hàng", f"{df.shape[0]:,}")
    col2.metric("Số lượng cụm (Nhóm)", df['cluster'].nunique())
    col3.metric("Doanh thu trung bình", f"{df['Monetary'].mean():.2f}")

    st.write("---")

    # 3. Phân tích cụm (Biểu đồ)
    st.header("2. Phân tích hành vi theo cụm")
    
    # Chia 2 cột để vẽ biểu đồ
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📊 Tỷ lệ phân bố khách hàng")
        # Vẽ biểu đồ tròn
        fig1, ax1 = plt.subplots()
        cluster_counts = df['cluster'].value_counts()
        ax1.pie(cluster_counts, labels=[f"Cụm {i}" for i in cluster_counts.index], 
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        ax1.axis('equal')  # Để biểu đồ tròn
        st.pyplot(fig1)

    with chart_col2:
        st.subheader("💰 So sánh chi tiêu (Monetary)")
        # Vẽ biểu đồ cột
        fig2, ax2 = plt.subplots()
        sns.barplot(data=df, x='cluster', y='Monetary', ax=ax2, palette="viridis", errorbar=None)
        ax2.set_xlabel("Cụm khách hàng")
        ax2.set_ylabel("Chi tiêu trung bình")
        st.pyplot(fig2)

    # 4. Bảng số liệu chi tiết RFM
    st.subheader("🔍 Chỉ số RFM trung bình từng cụm")
    rfm_summary = df.groupby('cluster')[['Recency', 'Frequency', 'Monetary']].mean().round(2)
    st.table(rfm_summary)

    # 5. Gợi ý chiến lược (Dựa trên phân tích của bạn lúc nãy)
    st.write("---")
    st.header("3. Đề xuất chiến lược Marketing")
    
    for cluster_id in sorted(df['cluster'].unique()):
        with st.expander(f"Chiến lược cho Cụm {cluster_id}", expanded=True):
            avg_monetary = df[df['cluster'] == cluster_id]['Monetary'].mean()
            if avg_monetary < 2000: # Giả định ngưỡng thấp là nhóm 0
                st.info(f"**Nhóm Khách Vãng Lai / Ngủ Đông (Cụm {cluster_id}):** Chi tiêu thấp, ít quay lại.")
                st.markdown("- **Hành động:** Gửi mã giảm giá kích cầu, email 'We miss you'.")
            else: # Nhóm cao là nhóm 1
                st.success(f"**Nhóm Khách VIP / Trung Thành (Cụm {cluster_id}):** Chi tiêu cao, mua nhiều.")
                st.markdown("- **Hành động:** Bán chéo (Cross-sell) combo sản phẩm, tặng quà tri ân, chăm sóc đặc biệt.")

else:
    st.info("👈 Vui lòng tải file kết quả (.csv) ở thanh bên trái để xem báo cáo.")