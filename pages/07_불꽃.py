import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

# 페이지 설정
st.set_page_config(page_title="Iris 품종 예측 앱", page_icon="🌸", layout="centered")

st.title("🌸 Iris(붓꽃) 품종 예측 앱")
st.write("사용자가 입력한 **꽃잎 길이**와 **꽃잎 너비**를 바탕으로 머신러닝(랜덤 포레스트) 모델이 붓꽃의 품종을 예측해 드립니다!")

# 데이터 로드 및 모델 학습 함수
@st.cache_resource
def load_data_and_model():
    try:
        df = pd.read_csv('Iris.csv', encoding='cp949')
    except:
        df = pd.read_csv('Iris.csv', encoding='utf-8')
    
    # 특성과 타겟 설정 (꽃잎 길이, 꽃잎너비 사용)
    X = df[['꽃잎 길이', '꽃잎너비']]
    y = df['품종']
    
    # 가장 적합한 분류 알고리즘인 랜덤 포레스트 모델 학습
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    
    return df, model

df, model = load_data_and_model()

# 3. 사용자가 입력할 수 있는 값의 범위 안내
st.subheader("📌 입력 가능한 값의 범위 (데이터셋 기준)")
min_len, max_len = float(df['꽃잎 길이'].min()), float(df['꽃잎 길이'].max())
min_wid, max_wid = float(df['꽃잎너비'].min()), float(df['꽃잎너비'].max())

st.info(
    f"- **꽃잎 길이 (Petal Length):** {min_len} cm ~ {max_len} cm\n"
    f"- **꽃잎 너비 (Petal Width):** {min_wid} cm ~ {max_wid} cm"
)

# 2. 사용자 입력 받기 (꽃잎 길이, 꽃잎 너비)
st.subheader("🎛️ 꽃잎 크기 입력")
col1, col2 = st.columns(2)
with col1:
    petal_length = st.number_input(
        "꽃잎 길이 (cm)", 
        min_value=min_len, 
        max_value=max_len, 
        value=float(df['꽃잎 길이'].mean()),
        step=0.1
    )
with col2:
    petal_width = st.number_input(
        "꽃잎 너비 (cm)", 
        min_value=min_wid, 
        max_value=max_wid, 
        value=float(df['꽃잎너비'].mean()),
        step=0.1
    )

# 예측 실행 버튼
if st.button("품종 예측하기", type="primary"):
    input_data = pd.DataFrame([[petal_length, petal_width]], columns=['꽃잎 길이', '꽃잎너비'])
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    st.success(f"🎉 예측된 품종은 **{prediction}** 입니다!")
    
    # 예측 확률 표시
    st.write("### 📊 품종별 예측 확률")
    for idx, class_name in enumerate(model.classes_):
        st.progress(float(probabilities[idx]), text=f"{class_name}: {probabilities[idx]*100:.1f}%")

# 5. 그래프 시각화 (사용자 입력값을 초록별로 표시)
st.subheader("📈 데이터 분포 및 내 입력 위치 시각화")
fig, ax = plt.subplots(figsize=(8, 6))

# 기존 데이터 산점도
sns.scatterplot(
    data=df, 
    x='꽃잎 길이', 
    y='꽃잎너비', 
    hue='품종', 
    palette='Set2', 
    style='품종',
    s=70, 
    ax=ax
)

# 사용자가 입력한 값을 초록색 별표(*)로 표시
ax.scatter(
    [petal_length], 
    [petal_width], 
    color='green', 
    marker='*', 
    s=250, 
    label='내 입력값', 
    zorder=5
)

ax.set_title("Iris Petal Length vs Petal Width")
ax.set_xlabel("꽃잎 길이 (cm)")
ax.set_ylabel("꽃잎 너비 (cm)")
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)
