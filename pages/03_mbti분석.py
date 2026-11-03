import streamlit as st
import csv
from pathlib import Path

# --------------------------------
# 1. 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="MBTI 진로 추천소",
    page_icon="🎯",
    layout="wide"
)

# --------------------------------
# 2. MBTI별 진로 데이터
# --------------------------------
career_data = {
    "ISTJ": [
        {
            "job": "회계사 💰",
            "major": "경영학과, 회계학과, 경제학과",
            "personality": "꼼꼼하고 책임감이 강하며 정확하게 일하는 것을 좋아하는 사람",
            "salary": "약 4,000만~7,000만 원"
        },
        {
            "job": "품질관리 전문가 🔍",
            "major": "산업공학과, 식품공학과, 화학공학과",
            "personality": "규칙을 잘 지키고 작은 오류도 놓치지 않는 사람",
            "salary": "약 3,500만~5,500만 원"
        }
    ],
    "ISFJ": [
        {
            "job": "영양사 🥗",
            "major": "식품영양학과, 영양학과",
            "personality": "다른 사람을 배려하고 꼼꼼하게 계획하는 사람",
            "salary": "약 2,800만~4,500만 원"
        },
        {
            "job": "초등학교 교사 🍎",
            "major": "초등교육과",
            "personality": "인내심이 있고 다른 사람을 세심하게 챙기는 사람",
            "salary": "약 3,500만~6,000만 원"
        }
    ],
    "INFJ": [
        {
            "job": "심리상담사 🧠",
            "major": "심리학과, 상담심리학과",
            "personality": "공감 능력이 뛰어나고 다른 사람의 이야기를 잘 들어주는 사람",
            "salary": "약 3,000만~5,000만 원"
        },
        {
            "job": "사회복지사 🤝",
            "major": "사회복지학과, 아동복지학과",
            "personality": "따뜻한 마음을 가지고 사회에 도움을 주고 싶은 사람",
            "salary": "약 2,800만~4,000만 원"
        }
    ],
    "INTJ": [
        {
            "job": "식품공학 연구원 🧪",
            "major": "식품공학과, 식품생명공학과, 생명공학과",
            "personality": "분석적이고 논리적이며 새로운 기술을 연구하는 것을 좋아하는 사람",
            "salary": "약 3,500만~6,000만 원"
        },
        {
            "job": "데이터 분석가 💻",
            "major": "통계학과, 컴퓨터공학과, 데이터사이언스학과",
            "personality": "논리적으로 문제를 해결하고 자료를 분석하는 사람",
            "salary": "약 3,500만~6,500만 원"
        }
    ],
    "ISTP": [
        {
            "job": "기계공학 기술자 ⚙️",
            "major": "기계공학과, 자동차공학과",
            "personality": "실용적이고 기계를 다루거나 문제를 해결하는 것을 좋아하는 사람",
            "salary": "약 3,500만~5,500만 원"
        },
        {
            "job": "소프트웨어 개발자 💻",
            "major": "컴퓨터공학과, 소프트웨어학과",
            "personality": "독립적으로 생각하고 문제의 원인을 분석하는 사람",
            "salary": "약 3,500만~6,500만 원"
        }
    ],
    "ISFP": [
        {
            "job": "시각디자이너 🎨",
            "major": "시각디자인학과, 산업디자인학과",
            "personality": "감각적이고 창의적이며 자신만의 표현을 좋아하는 사람",
            "salary": "약 2,800만~4,500만 원"
        },
        {
            "job": "파티시에 🧁",
            "major": "제과제빵과, 호텔조리학과, 식품조리학과",
            "personality": "손재주가 좋고 섬세하며 새로운 디저트를 만드는 것을 좋아하는 사람",
            "salary": "약 2,800만~4,500만 원"
        }
    ],
    "INFP": [
        {
            "job": "작가 ✍️",
            "major": "문예창작학과, 국어국문학과",
            "personality": "상상력이 풍부하고 자신의 생각을 글로 표현하는 것을 좋아하는 사람",
            "salary": "약 2,500만~5,000만 원"
        },
        {
            "job": "심리상담 전문가 💗",
            "major": "심리학과, 상담심리학과",
            "personality": "공감 능력이 뛰어나고 사람의 감정에 관심이 많은 사람",
            "salary": "약 3,000만~5,000만 원"
        }
    ],
    "INTP": [
        {
            "job": "과학 연구원 🔬",
            "major": "생명과학과, 화학과, 물리학과",
            "personality": "호기심이 많고 새로운 지식을 탐구하는 것을 좋아하는 사람",
            "salary": "약 3,500만~6,000만 원"
        },
        {
            "job": "프로그래머 🖥️",
            "major": "컴퓨터공학과, 소프트웨어학과",
            "personality": "논리적 사고력이 뛰어나고 복잡한 문제를 해결하는 사람",
            "salary": "약 3,500만~6,500만 원"
        }
    ],
    "ESTP": [
        {
            "job": "스포츠 지도자 🏃",
            "major": "체육학과, 스포츠과학과",
            "personality": "활동적이고 도전하는 것을 좋아하며 상황 대처 능력이 좋은 사람",
            "salary": "약 2,800만~4,500만 원"
        },
        {
            "job": "마케팅 전문가 📢",
            "major": "경영학과, 광고홍보학과, 마케팅학과",
            "personality": "적극적이고 사람들과 소통하는 것을 좋아하는 사람",
            "salary": "약 3,000만~5,500만 원"
        }
    ],
    "ESFP": [
        {
            "job": "이벤트 기획자 🎉",
            "major": "광고홍보학과, 이벤트학과, 문화콘텐츠학과",
            "personality": "사람들과 어울리는 것을 좋아하고 분위기를 즐겁게 만드는 사람",
            "salary": "약 3,000만~5,000만 원"
        },
        {
            "job": "호텔 서비스 전문가 🏨",
            "major": "호텔경영학과, 관광학과",
            "personality": "친화력이 좋고 밝은 에너지로 사람들을 대하는 사람",
            "salary": "약 2,800만~4,500만 원"
        }
    ],
    "ENFP": [
        {
            "job": "광고 기획자 💡",
            "major": "광고홍보학과, 미디어커뮤니케이션학과",
            "personality": "아이디어가 풍부하고 새로운 도전을 즐기는 사람",
            "salary": "약 3,000만~5,500만 원"
        },
        {
            "job": "콘텐츠 크리에이터 🎬",
            "major": "영상학과, 미디어학과, 콘텐츠학과",
            "personality": "창의적이고 표현력이 좋으며 다양한 주제에 관심이 많은 사람",
            "salary": "약 2,500만~5,000만 원"
        }
    ],
    "ENTP": [
        {
            "job": "창업 기획자 🚀",
            "major": "경영학과, 창업학과, 경제학과",
            "personality": "새로운 아이디어를 내고 다양한 방법으로 문제를 해결하는 사람",
            "salary": "약 3,000만~6,000만 원"
        },
        {
            "job": "제품 기획자 📱",
            "major": "산업공학과, 경영학과, 산업디자인학과",
            "personality": "호기심이 많고 새로운 제품과 서비스를 기획하는 것을 좋아하는 사람",
            "salary": "약 3,500만~6,000만 원"
        }
    ],
    "ESTJ": [
        {
            "job": "경영 관리자 📊",
            "major": "경영학과, 경제학과",
            "personality": "계획적이고 조직을 이끌며 목표를 달성하는 것을 좋아하는 사람",
            "salary": "약 4,000만~7,000만 원"
        },
        {
            "job": "공무원 🏛️",
            "major": "행정학과, 법학과, 정치외교학과",
            "personality": "책임감이 있고 체계적으로 업무를 처리하는 사람",
            "salary": "약 3,000만~5,500만 원"
        }
    ],
    "ESFJ": [
        {
            "job": "인사 담당자 🤝",
            "major": "경영학과, 행정학과, 심리학과",
            "personality": "협동심이 강하고 사람들과 원활하게 소통하는 사람",
            "salary": "약 3,000만~5,000만 원"
        },
        {
            "job": "간호사 🩺",
            "major": "간호학과",
            "personality": "책임감이 강하고 다른 사람을 세심하게 돌보는 사람",
            "salary": "약 3,500만~5,000만 원"
        }
    ],
    "ENFJ": [
        {
            "job": "교사 📚",
            "major": "교육학과, 사범대학 관련 학과",
            "personality": "다른 사람의 성장을 돕고 소통과 협력을 중요하게 생각하는 사람",
            "salary": "약 3,500만~6,000만 원"
        },
        {
            "job": "홍보 전문가 📣",
            "major": "광고홍보학과, 미디어커뮤니케이션학과",
            "personality": "설득력이 있고 사람들과 관계를 맺는 것을 좋아하는 사람",
            "salary": "약 3,000만~5,500만 원"
        }
    ],
    "ENTJ": [
        {
            "job": "기업 경영자 👔",
            "major": "경영학과, 경제학과",
            "personality": "목표 지향적이고 리더십이 있으며 결정을 내리는 것을 좋아하는 사람",
            "salary": "약 4,000만~8,000만 원 이상"
        },
        {
            "job": "변호사 ⚖️",
            "major": "법학과, 법학전문대학원",
            "personality": "논리적이고 분석력이 뛰어나며 자신의 의견을 명확하게 전달하는 사람",
            "salary": "약 5,000만~1억 원 이상"
        }
    ]
}

# --------------------------------
# 3. 제목 및 소개
# --------------------------------
st.title("🎯 MBTI 진로 추천소")
st.subheader("나의 MBTI에 어울리는 미래 직업은?")
st.write(
    "16가지 MBTI 중 나의 유형을 선택하고 "
    "나에게 어울리는 진로 2가지를 찾아보자! ✨"
)

st.info(
    "💡 MBTI는 진로를 결정하는 정답이 아니야! "
    "나의 흥미와 적성을 알아보는 참고 자료로 활용해 줘."
)

# --------------------------------
# 4. MBTI 선택
# --------------------------------
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

st.markdown("### 🔍 나의 MBTI를 선택해 줘!")

selected_mbti = st.selectbox(
    "MBTI 유형",
    mbti_list,
    index=0
)

st.divider()

# --------------------------------
# 5. 선택한 MBTI 결과
# --------------------------------
st.header(f"✨ {selected_mbti}에게 추천하는 진로 TOP 2")

jobs = career_data[selected_mbti]

col1, col2 = st.columns(2)

for i, (col, job) in enumerate(zip([col1, col2], jobs)):
    with col:
        st.subheader(f"🏆 추천 진로 {i+1}")
        st.markdown(f"### {job['job']}")

        st.write("🎓 **관련 학과**")
        st.write(job["major"])

        st.write("🌟 **적합한 성격**")
        st.write(job["personality"])

        st.write("💰 **평균 연봉 참고 범위 (세전)**")
        st.success(job["salary"])

st.caption(
    "※ 연봉은 국내 직업의 대략적인 참고 추정 범위이며, "
    "경력·기업 규모·근무 지역 등에 따라 달라질 수 있어."
)

st.divider()

# --------------------------------
# 6. CSV 파일 활용
# --------------------------------
st.header("🌍 세계 MBTI 분포도")

st.write(
    f"선택한 {selected_mbti} 유형이 "
    "국가별로 어느 정도 분포하는지 확인해 보자!"
)

csv_path = Path(__file__).parent / "countriesMBTI_16types.csv"

if csv_path.exists():
    try:
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        if rows and selected_mbti in rows[0]:
            ranking = []

            for row in rows:
                try:
                    value = float(row[selected_mbti])
                    ranking.append({
                        "country": row["Country"],
                        "value": value * 100
                    })
                except (ValueError, KeyError):
                    continue

            ranking.sort(
                key=lambda x: x["value"],
                reverse=True
            )

            st.subheader(
                f"🌎 {selected_mbti} 비율이 높은 국가 TOP 5"
            )

            for i, item in enumerate(ranking[:5], start=1):
                st.write(
                    f"**{i}위. {item['country']}**"
                    f" — {item['value']:.2f}%"
                )
                st.progress(
                    min(max(item["value"] / 100, 0.0), 1.0)
                )

            st.caption(
                "※ 국가별 비율은 업로드한 CSV 원본 데이터를 기준으로 해."
            )

        else:
            st.warning("CSV 파일에서 MBTI 열을 찾을 수 없어.")

    except (OSError, csv.Error, KeyError, ValueError) as e:
        st.warning(f"CSV 파일을 읽는 중 문제가 발생했어: {e}")

else:
    st.warning(
        "countriesMBTI_16types.csv 파일을 "
        "app.py와 같은 폴더에 넣어 줘!"
    )

# --------------------------------
# 7. 마무리
# --------------------------------
st.divider()

st.markdown("### 💖 나의 가능성을 발견해 보자!")

st.write(
    "MBTI로 알아본 진로는 여러 선택지 중 하나일 뿐이야. "
    "내가 좋아하는 것과 잘하는 것을 함께 생각하면서 "
    "나만의 멋진 미래를 만들어 보자! 🌈"
)

st.caption("🎯 MBTI 진로 추천소 | 나의 미래를 찾아가는 첫걸음")
