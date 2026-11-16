import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# 페이지 설정
st.set_page_config(page_title="Iris 품종 예측 앱", page_icon="🌸", layout="centered")

st.title("🌸 Iris(붓꽃) 품종 예측 앱")
st.write("사용자가 입력한 **꽃잎 길이**와 **꽃잎 너비**를 바탕으로 선택한 머신러닝 모델이 붓꽃의 품종을 예측해 드립니다!")

# 데이터 로드 및 3가지 모델 학습 함수
@st.cache_resource
def load_data_and_models():
    try:
        df = pd.read_csv('Iris.csv', encoding='cp949')
    except:
        df = pd.read_csv('Iris.csv', encoding='utf-8')
    
    X = df[['꽃잎 길이', '꽃잎너비']]
    y = df['품종']
    
    # 3가지 분류 알고리즘 정의 및 학습
    models = {
        "랜덤 포레스트 (Random Forest)": RandomForestClassifier(random_state=42),
        "서포트 벡터 머신 (SVM)": SVC(probability=True, random_state=42),
        "K-최근접 이웃 (KNN)": KNeighborsClassifier(n_neighbors=5)
    }
    
    for name, model in models.items():
        model.fit(X, y)
        
    return df, models

df, models = load_data_and_models()

# 1. 알고리즘 선택 UI
st.subheader("🤖 1. 예측 알고리즘 선택")
selected_algo = st.selectbox(
    "사용할 분류 알고리즘을 선택하세요:",
    list(models.keys())
)

# 2. 선택된 알고리즘에 대한 설명 및 원리 안내
algo_info = {
    "랜덤 포레스트 (Random Forest)": {
        "desc": "여러 개의 의사결정나무(Decision Tree)를 만들어 종합적인 판단을 내리는 **앙상블(Ensemble)** 알고리즘입니다.",
        "principle": "데이터에서 무작위로 샘플을 뽑아 수많은 의사결정나무를 각각 학습시킨 뒤, 새로운 데이터가 들어오면 모든 나무의 예측 결과를 모아 **다수결(투표)**로 최종 품종을 결정합니다. 단일 나무보다 과적합(Overfitting)에 강하고 정확도가 높습니다."
    },
    "서포트 벡터 머신 (SVM)": {
        "desc": "데이터 공간에서 서로 다른 품종을 가장 잘 구분하는 **경계선(결정 경계)**을 찾는 알고리즘입니다.",
        "principle": "각 품종 데이터 그룹 사이의 간격(마진, Margin)이 **최대가 되도록 하는 최적의 경계선**을 찾습니다. 경계선에 가장 가까이 위치한 데이터(서포트 벡터)들이 기준이 되며, 데이터가 비선형적으로 분포할 경우 커널(Kernel) 기법을 통해 고차원으로 매핑하여 깔끔하게 분리합니다."
    },
    "K-최근접 이웃 (KNN)": {
        "desc": "새로운 데이터가 들어왔을 때, 가장 거리가 가까운 기존 데이터들을 참고하여 분류하는 **거리 기반** 알고리즘입니다.",
        "principle": "별도의 복잡한 수식을 미리 학습하지 않고 데이터를 저장해 두었다가, 예측할 때 입력값과 유클리드 거리가 **가장 가까운 K개(여기서는 5개)의 이웃 데이터**를 찾습니다. 그 이웃들 중 가장 많이 속한 품종으로 최종 분류합니다."
    }
}

with st.expander(f"📖 '{selected_algo}' 설명 및 작동 원리 보기", expanded=True):
    st.markdown(f"**💡 알고리즘 설명:** {algo_info[selected_algo]['desc']}")
    st.markdown(f"**⚙️ 작동 원리:** {algo_info[selected_algo]['principle']}")

st.divider()

# 3. 사용자가 입력할 수 있는 값의 범위 안내
st.subheader("📌 2. 입력 가능한 값의 범위 (데이터셋 기준)")
min_len, max_len = float(df['꽃잎 길이'].min()), float(df['꽃잎 길이'].max())
min_wid, max_wid = float(df['꽃잎너비'].min()), float(df['꽃잎너비'].max())

st.info(
    f"- **꽃잎 길이 (Petal Length):** {min_len} cm ~ {max_len} cm\n"
    f"- **꽃잎 너비 (Petal Width):** {min_wid} cm ~ {max_wid} cm"
)

# 4. 사용자 입력 받기
st.subheader("🎛️ 3. 꽃잎 크기 입력")
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

# 예측 실행
model = models[selected_algo]

if st.button("품종 예측하기", type="primary"):
    input_data = pd.DataFrame([[petal_length, petal_width]], columns=['꽃잎 길이', '꽃잎너비'])
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    st.success(f"🎉 **{selected_algo}** 모델이 예측한 품종은 **{prediction}** 입니다!")
    
    # 예측 확률 표시
    st.write("### 📊 품종별 예측 확률")
    for idx, class_name in enumerate(model.classes_):
        st.progress(float(probabilities[idx]), text=f"{class_name}: {probabilities[idx]*100:.1f}%")

# 5. 그래프 시각화 (사용자 입력값을 초록별로 표시)
st.subheader("📈 4. 데이터 분포 및 내 입력 위치 시각화")
fig, ax = plt.subplots(figsize=(8, 6))

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
    s=300, 
    edgecolor='black',
    label='My Input', 
    zorder=5
)

ax.set_title(f"Iris Distribution & Prediction ({selected_algo.split()[0]})")
ax.set_xlabel("Petal Length (cm)")
ax.set_ylabel("Petal Width (cm)")
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)
