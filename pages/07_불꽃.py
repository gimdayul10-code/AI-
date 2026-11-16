import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# 페이지 설정
st.set_page_config(page_title="Iris 품종 예측 및 비교 앱", page_icon="🌸", layout="centered")

st.title("🌸 Iris(붓꽃) 품종 예측 및 비교 앱")
st.write("사용자가 입력한 특성을 바탕으로 **3가지 머신러닝 알고리즘의 예측 결과를 한눈에 비교**해 드립니다!")

# 데이터 로드 및 모델 학습 함수
@st.cache_resource
def load_data_and_models():
    try:
        df = pd.read_csv('Iris.csv', encoding='cp949')
    except:
        df = pd.read_csv('Iris.csv', encoding='utf-8')
    
    y = df['품종']
    
    # 1) 꽃잎 특성 모델 (꽃잎 길이, 꽃잎너비)
    X_petal = df[['꽃잎 길이', '꽃잎너비']]
    models_petal = {
        "랜덤 포레스트 (Random Forest)": RandomForestClassifier(random_state=42),
        "서포트 벡터 머신 (SVM)": SVC(probability=True, random_state=42),
        "K-최근접 이웃 (KNN)": KNeighborsClassifier(n_neighbors=5)
    }
    for m in models_petal.values():
        m.fit(X_petal, y)
        
    # 2) 꽃받침 특성 모델 (꽃받침 길이, 꽃받침 너비)
    X_sepal = df[['꽃받침 길이', '꽃받침 너비']]
    models_sepal = {
        "랜덤 포레스트 (Random Forest)": RandomForestClassifier(random_state=42),
        "서포트 벡터 머신 (SVM)": SVC(probability=True, random_state=42),
        "K-최근접 이웃 (KNN)": KNeighborsClassifier(n_neighbors=5)
    }
    for m in models_sepal.values():
        m.fit(X_sepal, y)
        
    return df, models_petal, models_sepal

df, models_petal, models_sepal = load_data_and_models()

# 알고리즘 설명 데이터
algo_info = {
    "랜덤 포레스트 (Random Forest)": {
        "desc": "여러 개의 의사결정나무(Decision Tree)를 만들어 종합적인 판단을 내리는 **앙상블(Ensemble)** 알고리즘입니다.",
        "principle": "무작위로 샘플을 뽑아 수많은 나무를 학습시킨 뒤, 새로운 데이터가 들어오면 **다수결(투표)**로 최종 품종을 결정합니다. 과적합에 강하고 정확도가 높습니다."
    },
    "서포트 벡터 머신 (SVM)": {
        "desc": "데이터 공간에서 서로 다른 품종을 가장 잘 구분하는 **경계선(결정 경계)**을 찾는 알고리즘입니다.",
        "principle": "품종 데이터 그룹 사이의 간격(마진)이 **최대가 되도록 하는 최적의 경계선**을 찾습니다. 선형 및 비선형 분류에 모두 강력합니다."
    },
    "K-최근접 이웃 (KNN)": {
        "desc": "새로운 데이터가 들어왔을 때, 가장 거리가 가까운 기존 데이터들을 참고하여 분류하는 **거리 기반** 알고리즘입니다.",
        "principle": "입력값과 유클리드 거리가 **가장 가까운 K개(5개)의 이웃**을 찾아, 그 이웃들 중 가장 많은 품종으로 최종 분류합니다."
    }
}

# 탭 생성
tab1, tab2 = st.tabs(["🍃 탭 1: 꽃잎 크기 (비교 분석)", "🌿 탭 2: 꽃받침 크기 (비교 분석)"])

# ==================== [탭 1] 꽃잎 분석 및 비교 ====================
with tab1:
    st.header("🍃 꽃잎(Petal) 속성 기반 3개 알고리즘 비교")
    
    with st.expander("📖 사용된 3가지 알고리즘 설명 및 원리 보기", expanded=False):
        for name, info in algo_info.items():
            st.markdown(f"### **{name}**")
            st.markdown(f"- **설명:** {info['desc']}")
            st.markdown(f"- **원리:** {info['principle']}")
            st.divider()

    min_len_p, max_len_p = float(df['꽃잎 길이'].min()), float(df['꽃잎 길이'].max())
    min_wid_p, max_wid_p = float(df['꽃잎너비'].min()), float(df['꽃잎너비'].max())
    
    st.info(f"- **꽃잎 길이 범위:** {min_len_p} cm ~ {max_len_p} cm\n- **꽃잎 너비 범위:** {min_wid_p} cm ~ {max_wid_p} cm")
    
    col1, col2 = st.columns(2)
    with col1:
        p_len = st.number_input("꽃잎 길이 (cm)", min_value=min_len_p, max_value=max_len_p, value=float(df['꽃잎 길이'].mean()), step=0.1, key="p_len")
    with col2:
        p_wid = st.number_input("꽃잎 너비 (cm)", min_value=min_wid_p, max_value=max_wid_p, value=float(df['꽃잎너비'].mean()), step=0.1, key="p_wid")
        
    if st.button("꽃잎 기준으로 3개 모델 예측 결과 비교하기", type="primary", key="btn_p"):
        input_data = pd.DataFrame([[p_len, p_wid]], columns=['꽃잎 길이', '꽃잎너비'])
        
        st.subheader("📊 3개 알고리즘 예측 결과 비교")
        comparison_results = []
        
        for name, model in models_petal.items():
            pred = model.predict(input_data)[0]
            probs = model.predict_proba(input_data)[0]
            max_prob = max(probs) * 100
            comparison_results.append({
                "알고리즘": name,
                "예측 품종": pred,
                "확신도(최고 확률)": f"{max_prob:.1f}%"
            })
            
        # 표 형식으로 비교 제공
        st.table(pd.DataFrame(comparison_results))
        
        # 상세 확률 바 표시
        for name, model in models_petal.items():
            pred = model.predict(input_data)[0]
            probs = model.predict_proba(input_data)[0]
            with st.container():
                st.markdown(f"**🤖 {name}** (예측: **{pred}**)")
                cols = st.columns(len(model.classes_))
                for idx, c_name in enumerate(model.classes_):
                    cols[idx].metric(label=c_name, value=f"{probs[idx]*100:.1f}%")
                st.divider()
            
    st.subheader("📈 꽃잎 데이터 분포 및 내 입력 위치")
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df, x='꽃잎 길이', y='꽃잎너비', hue='품종', palette='Set2', style='품종', s=70, ax=ax1)
    ax1.scatter([p_len], [p_wid], color='green', marker='*', s=300, edgecolor='black', label='My Input', zorder=5)
    ax1.set_title("Petal Length vs Petal Width")
    ax1.set_xlabel("Petal Length (cm)")
    ax1.set_ylabel("Petal Width (cm)")
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig1)

# ==================== [탭 2] 꽃받침 분석 및 비교 ====================
with tab2:
    st.header("🌿 꽃받침(Sepal) 속성 기반 3개 알고리즘 비교")
    
    with st.expander("📖 사용된 3가지 알고리즘 설명 및 원리 보기", expanded=False):
        for name, info in algo_info.items():
            st.markdown(f"### **{name}**")
            st.markdown(f"- **설명:** {info['desc']}")
            st.markdown(f"- **원리:** {info['principle']}")
            st.divider()
        
    min_len_s, max_len_s = float(df['꽃받침 길이'].min()), float(df['꽃받침 길이'].max())
    min_wid_s, max_wid_s = float(df['꽃받침 너비'].min()), float(df['꽃받침 너비'].max())
    
    st.info(f"- **꽃받침 길이 범위:** {min_len_s} cm ~ {max_len_s} cm\n- **꽃받침 너비 범위:** {min_wid_s} cm ~ {max_wid_s} cm")
    
    col3, col4 = st.columns(2)
    with col3:
        s_len = st.number_input("꽃받침 길이 (cm)", min_value=min_len_s, max_value=max_len_s, value=float(df['꽃받침 길이'].mean()), step=0.1, key="s_len")
    with col4:
        s_wid = st.number_input("꽃받침 너비 (cm)", min_value=min_wid_s, max_value=max_wid_s, value=float(df['꽃받침 너비'].mean()), step=0.1, key="s_wid")
        
    if st.button("꽃받침 기준으로 3개 모델 예측 결과 비교하기", type="primary", key="btn_s"):
        input_data_s = pd.DataFrame([[s_len, s_wid]], columns=['꽃받침 길이', '꽃받침 너비'])
        
        st.subheader("📊 3개 알고리즘 예측 결과 비교")
        comparison_results_s = []
        
        for name, model in models_sepal.items():
            pred = model.predict(input_data_s)[0]
            probs = model.predict_proba(input_data_s)[0]
            max_prob = max(probs) * 100
            comparison_results_s.append({
                "알고리즘": name,
                "예측 품종": pred,
                "확신도(최고 확률)": f"{max_prob:.1f}%"
            })
            
        st.table(pd.DataFrame(comparison_results_s))
        
        for name, model in models_sepal.items():
            pred = model.predict(input_data_s)[0]
            probs = model.predict_proba(input_data_s)[0]
            with st.container():
                st.markdown(f"**🤖 {name}** (예측: **{pred}**)")
                cols = st.columns(len(model.classes_))
                for idx, c_name in enumerate(model.classes_):
                    cols[idx].metric(label=c_name, value=f"{probs[idx]*100:.1f}%")
                st.divider()
            
    st.subheader("📈 꽃받침 데이터 분포 및 내 입력 위치")
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df, x='꽃받침 길이', y='꽃받침 너비', hue='품종', palette='Set1', style='품종', s=70, ax=ax2)
    ax2.scatter([s_len], [s_wid], color='green', marker='*', s=300, edgecolor='black', label='My Input', zorder=5)
    ax2.set_title("Sepal Length vs Sepal Width")
    ax2.set_xlabel("Sepal Length (cm)")
    ax2.set_ylabel("Sepal Width (cm)")
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig2)
