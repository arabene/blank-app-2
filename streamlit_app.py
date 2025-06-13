import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.title("전기차 충전소 현황")

# 1. 데이터 로드
try:
    df = pd.read_csv("charger_20230531.csv", encoding='cp949')
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.stop()
except Exception as e:
    st.error(f"CSV 파일을 읽는 중 오류 발생: {e}")
    st.stop()

# 2. 위도경도 분리
if '위도경도' in df.columns:
    df[['위도', '경도']] = df['위도경도'].str.split(',', expand=True)
    df['위도'] = pd.to_numeric(df['위도'].str.strip(), errors='coerce')
    df['경도'] = pd.to_numeric(df['경도'].str.strip(), errors='coerce')
else:
    st.error("'위도경도' 컬럼이 존재하지 않습니다.")
    st.stop()

# 3. 결측치 제거
df1 = df[['충전소명', '주소', '위도', '경도']].dropna(subset=['위도', '경도'])

# 4. 지도 생성
m = folium.Map(location=[df1['위도'].mean(), df1['경도'].mean()], zoom_start=11)
marker_cluster = MarkerCluster().add_to(m)

for idx, row in df1.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['충전소명']
    ).add_to(marker_cluster)

folium_static(m)
