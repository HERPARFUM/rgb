import streamlit as st
import numpy as np
from PIL import Image
from streamlit_cropper import st_cropper

st.set_page_config(page_title="手动框选颜色分析", layout="wide")

st.title("手动框选区域颜色分析")
st.markdown("上传图片 -> 调整红框位置 -> 实时获取框内颜色均值")

# 1. 上传图片
uploaded_file = st.file_uploader("请上传图片", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    img = Image.open(uploaded_file)
    
    # 布局：左边放图，右边放数据
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("1. 在此处调整红框")
        # --- 核心组件：框选器 ---
        # realtime_update=True 表示拖动时实时计算
        # box_color 指定框的颜色
        cropped_img = st_cropper(img, realtime_update=True, box_color='#FF0000', aspect_ratio=None)

    with col2:
        st.subheader("2. 选区分析结果")
        
        if cropped_img:
            # 显示截取的小图
            st.image(cropped_img, caption="当前选中的区域", width=150)
            
            # --- 数据计算 ---
            # 将图片转为数组
            img_array = np.array(cropped_img)
            
            # 计算平均值 (axis=0,1 表示计算长宽方向的平均)
            # 结果顺序：R, G, B
            mean_color = np.mean(img_array, axis=(0, 1))
            
            r = int(mean_color[0])
            g = int(mean_color[1])
            b = int(mean_color[2])
            
            # 计算亮度 (标准公式: 0.299R + 0.587G + 0.114B)
            brightness = int(0.299*r + 0.587*g + 0.114*b)
            
            # --- 显示数据卡片 ---
            st.divider()
            
            # 显示颜色块
            st.markdown(f"""
            <div style="
                width: 100%; 
                height: 50px; 
                background-color: rgb({r}, {g}, {b}); 
                border-radius: 10px; 
                border: 2px solid #ddd;
                margin-bottom: 20px;">
            </div>
            """, unsafe_allow_html=True)

            st.metric(label="平均亮度 (0-255)", value=brightness)
            st.metric(label="Red (红)", value=r)
            st.metric(label="Green (绿)", value=g)
            st.metric(label="Blue (蓝)", value=b)
            
            st.code(f"RGB: ({r}, {g}, {b})")
            
else:
    st.info("请先上传一张图片。")