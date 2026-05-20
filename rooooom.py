import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 기본 설정 및 스타일
st.set_page_config(page_title="방구석 거지방", page_icon="💸", layout="centered")

# CSS로 거지방 특유의 B급 감성 한 스푼 넣기
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; }
    .post-box { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 15px; }
    .beggar-tier { font-size: 20px; font-weight: bold; color: #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 저장소 초기화 (Streamlit 세션 상태 활용)
# 원래는 DB를 써야 하지만, 테스트용으로 세션 상태를 DB처럼 씁니다.
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {
            "id": 1,
            "time": "2026-05-20 14:00",
            "nickname": "익명의 자취생",
            "item": "스타벅스 자바칩 프라푸치노",
            "price": 6800,
            "reason": "점심 먹고 너무 졸려서 뇌에 설탕 주입함..",
            "good": 2,
            "bad": 15,
            "comments": ["정신 차려라", "졸리면 뒤구르기를 해라", "6800원이면 국밥이 한 그릇"]
        },
        {
            "id": 2,
            "time": "2026-05-20 14:30",
            "nickname": "절약왕이될상",
            "item": "편의점 도시락",
            "price": 4500,
            "reason": "약속 취소하고 편의점 털었습니다.",
            "good": 24,
            "bad": 1,
            "comments": ["훌륭하다 인간", "통장 리스펙"]
        }
    ]

# 3. 사이드바 - 내 정보 & 거지 티어 측정
st.sidebar.title("💰 나의 거지방 프로필")
my_nickname = st.sidebar.text_input("닉네임 설정", value="방구석거지")

# 이번 달 지출 계산 시뮬레이션
total_spent = sum([p['price'] for p in st.session_state.posts if p['nickname'] == my_nickname])
st.sidebar.metric(label="내가 쓴 총금액", value=f"{total_spent:,} 원")

if total_spent == 0:
    tier = "💎 무소유 마스터 (지출 없음)"
elif total_spent < 10000:
    tier = "🥉 자취방 흙수저"
elif total_spent < 50000:
    tier = "🥈 평범한 월급노예"
else:
    tier = "🚨 파산 직전의 베짱이"

st.sidebar.markdown(f"현재 나의 등급:<br><span class='beggar-tier'>{tier}</span>", unsafe_allow_html=True)


# 4. 메인 화면 - 타이틀 및 소비 등록
st.title("💸 방구석 거지방")
st.caption("서로의 지갑을 지켜주는 눈물겨운 익명 소비 절약 커뮤니티")

with st.form(key="expense_form", clear_on_submit=True):
    st.subheader("📝 나의 소비 내역 고발하기")
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("소비 항목 (예: 아메리카노, 배달치킨)", placeholder="뭘 샀나요?")
    with col2:
        price = st.number_input("금액 (원)", min_value=0, step=1000)
        
    reason = st.text_area("변명 혹은 사유", placeholder="안 사면 죽을 것 같았던 이유를 대보세요.")
    submit_button = st.form_submit_button(label="거지방에 고발하기 🚨")

    if submit_button:
        if item and price > 0:
            new_post = {
                "id": len(st.session_state.posts) + 1,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "nickname": my_nickname,
                "item": item,
                "price": price,
                "reason": reason,
                "good": 0,
                "bad": 0,
                "comments": []
            }
            # 최신 글이 위로 오도록 앞에 삽입
            st.session_state.posts.insert(0, new_post)
            st.success("고발 완료! 이제 동료 거지들의 심판을 기다리세요.")
        else:
            st.error("항목과 금액을 올바르게 입력해주세요!")

st.write("---")

# 5. 메인 화면 - 거지방 타임라인 (심판 구역)
st.subheader("🔥 실시간 대기 중인 소비 심판소")

for idx, post in enumerate(st.session_state.posts):
    # 각 포스트를 깔끔한 박스 형태로 표현
    st.markdown(f"""
    <div class='post-box'>
        <span style='color:gray; font-size:12px;'>{post['time']} | <b>{post['nickname']}</b></span>
        <h4 style='margin: 5px 0;'>🛒 {post['item']} - <span style='color:#ff4b4b;'>{post['price']:,}원</span></h4>
        <p style='color:#495057; background:#f1f3f5; padding:10px; border-radius:5px;'>💬 "{post['reason']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 투표 및 댓글 기능 구현 (버튼은 밖으로 빼야 Streamlit에서 정상 작동함)
    col_g, col_b, col_empty = st.columns([1, 1, 4])
    
    with col_g:
        if st.button(f"👍 참음 ({post['good']})", key=f"good_{post['id']}_{idx}"):
            post['good'] += 1
            st.rerun()
            
    with col_b:
        if st.button(f"👎 때찌 ({post['bad']})", key=f"bad_{post['id']}_{idx}"):
            post['bad'] += 1
            st.rerun()
            
    # 잔소리(댓글) 달기
    with st.expander(f"🤬 잔소리 {len(post['comments'])}개 보기"):
        for comment in post['comments']:
            st.write(f"- {comment}")
            
        # 댓글 입력
        comment_input = st.text_input("정신 차리라고 한마디 하기", key=f"cmt_input_{post['id']}_{idx}")
        if st.button("잔소리 투척", key=f"cmt_btn_{post['id']}_{idx}"):
            if comment_input:
                post['comments'].append(comment_input)
                st.rerun()
                
    st.write("")
