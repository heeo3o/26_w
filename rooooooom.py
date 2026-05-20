import streamlit as st
import pandas as pd
from datetime import datetime
import random

# 1. 페이지 기본 설정
st.set_page_config(page_title="방구석 거지방 Pro", page_icon="💸", layout="centered")

# CSS 스타일 (캐릭터 박스 및 말풍선용)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; }
    .post-box { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 15px; }
    .character-box { background-color: #fff9db; padding: 15px; border-radius: 10px; border: 2px dashed #fcc419; text-align: center; margin-bottom: 20px; }
    .chat-box { background-color: #eaeaea; padding: 15px; border-radius: 10px; max-height: 250px; overflow-y: auto; margin-bottom: 15px; }
    .chat-msg { background-color: white; padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 저장소 초기화 (세션 상태)
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {"id": 1, "time": "2026-05-20 14:00", "nickname": "익명의 자취생", "item": "스타벅스 프라푸치노", "price": 6800, "reason": "뇌에 설탕 주입함..", "good": 2, "bad": 15, "comments": ["정신 차려라", "물이나 마셔라"]},
        {"id": 2, "time": "2026-05-20 14:30", "nickname": "절약왕이될상", "item": "편의점 도시락", "price": 4500, "reason": "약속 취소하고 편의점 털었습니다.", "good": 24, "bad": 1, "comments": ["훌륭하다 인간"]}
    ]

# 실시간 단톡방용 가상 데이터
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"user": "무소유마스터", "msg": "오늘 무지출 챌린지 3일차 성공 지립니닷"},
        {"user": "지갑전사", "msg": "방금 치킨 결제하려다가 손가락 부러뜨렸습니다 휴..."},
        {"user": "치킨유혹꾼", "msg": "치킨 냄새 장난아닌데 참으시네 독하다 독해"}
    ]

# 3. 사이드바 - 내 정보 & 거지 티어 & [추가] 거지 캐릭터 키우기
st.sidebar.title("💰 나의 거지방 프로필")
my_nickname = st.sidebar.text_input("닉네임 설정", value="방구석거지")

# 이번 달 지출 계산
total_spent = sum([p['price'] for p in st.session_state.posts if p['nickname'] == my_nickname])
st.sidebar.metric(label="내가 오늘 지른 금액", value=f"{total_spent:,} 원")

# 지출에 따른 캐릭터 상태 및 등급 변화
if total_spent == 0:
    tier = "💎 무소유 마스터"
    char_avatar = "🧘"
    char_status = "체력 만땅! 통장이 두둑하여 마음이 평화롭습니다."
elif total_spent < 15000:
    tier = "🥈 평범한 월급노예"
    char_avatar = "🚶"
    char_status = "약간의 지출이 있었지만 아직까진 걸어 다닐 만합니다."
elif total_spent < 50000:
    tier = "🥉 자취방 흙수저"
    char_avatar = "🧎"
    char_status = "무릎을 꿇기 시작했습니다. 삼각김밥으로 연명해야 합니다."
else:
    tier = "🚨 파산 직전의 베짱이"
    char_avatar = "💀"
    char_status = " 영혼이 가출했습니다. 지갑이 폭발하여 숨만 쉬고 있습니다."

# 캐릭터 UI 렌더링
st.sidebar.markdown(f"""
<div class='character-box'>
    <div style='font-size: 50px;'>{char_avatar}</div>
    <div style='font-weight: bold; margin-top:5px;'>등급: {tier}</div>
    <div style='font-size: 12px; color: #666; margin-top:5px;'>{char_status}</div>
</div>
""", unsafe_allow_html=True)


# 4. 메인 화면 - 타이틀 및 소비 등록
st.title("💸 방구석 거지방 Pro")
st.caption("서로의 지갑을 지켜주는 눈물겨운 익명 소비 절약 커뮤니티")

# 소비 등록 Form
with st.form(key="expense_form", clear_on_submit=True):
    st.subheader("📝 나의 소비 내역 고발하기")
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("소비 항목 (예: 아메리카노)", placeholder="뭘 샀나요?")
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
            st.session_state.posts.insert(0, new_post)
            
            # [추가] 과소비 시 잔소리 알림 팝업 (금액에 따른 분기)
            if price >= 50000:
                st.error(f"🚨 [파산 경고] {price:,}원이라니 제정신입니까? 캐릭터가 목숨을 위협받고 있습니다!")
                st.balloons() # 역설적인 풍선 날리기 효과
            elif price >= 10000:
                st.warning(f"⚠️ [잔소리] {item} 안 샀으면 국밥이 몇 그릇입니까? 다음 지출은 스톱하세요!")
            else:
                st.info("💡 [소소한 지출] 이 정도는 봐 드립니다만, 티끌 모아 파산입니다.")
                
            st.rerun()
        else:
            st.error("항목과 금액을 올바르게 입력해주세요!")

st.write("---")

# 5. [추가] 실시간 거지 대화방 (탭 분리하여 깔끔하게 제공)
tab1, tab2 = st.tabs(["🔥 소비 심판소 (타임라인)", "💬 실시간 거지 대화방"])

with tab1:
    st.subheader("실시간 대기 중인 소비 심판소")
    for idx, post in enumerate(st.session_state.posts):
        st.markdown(f"""
        <div class='post-box'>
            <span style='color:gray; font-size:12px;'>{post['time']} | <b>{post['nickname']}</b></span>
            <h4 style='margin: 5px 0;'>🛒 {post['item']} - <span style='color:#ff4b4b;'>{post['price']:,}원</span></h4>
            <p style='color:#495057; background:#f1f3f5; padding:10px; border-radius:5px;'>💬 "{post['reason']}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_g, col_b, _ = st.columns([1, 1, 4])
        with col_g:
            if st.button(f"👍 참음 ({post['good']})", key=f"good_{post['id']}_{idx}"):
                post['good'] += 1
                st.rerun()
        with col_b:
            if st.button(f"👎 때찌 ({post['bad']})", key=f"bad_{post['id']}_{idx}"):
                post['bad'] += 1
                st.rerun()
                
        with st.expander(f"🤬 잔소리 {len(post['comments'])}개 보기"):
            for comment in post['comments']:
                st.write(f"- {comment}")
            comment_input = st.text_input("정신 차리라고 한마디 하기", key=f"cmt_input_{post['id']}_{idx}")
            if st.button("잔소리 투척", key=f"cmt_btn_{post['id']}_{idx}"):
                if comment_input:
                    post['comments'].append(comment_input)
                    st.rerun()

with tab2:
    st.subheader("💬 거지방 실시간 익명 수다")
    st.caption("새로고침을 누르거나 글을 쓰면 봇들이 실시간(?)으로 반응합니다.")
    
    # 가짜 실시간 느낌을 주기 위해 유저가 탭을 볼 때마다 랜덤 봇 메시지 추가 가능
    if random.random() < 0.3: # 30% 확률로 다른 거지의 뻘글 추가
        bot_names = ["밥은먹고다니냐", "탕진잼", "무소유가꿈", "시골쥐"]
        bot_msgs = ["아 배고프다 물 마셔야지", "오늘 회사 동료가 커피 사줘서 방어 성공!", "택배 인출 금지령 내렸습니다", "내 지갑 눈 감아"]
        st.session_state.chat_messages.append({"user": random.choice(bot_names), "msg": random.choice(bot_msgs)})
        if len(st.session_state.chat_messages) > 10: # 메모리 관리용 10개 제한
            st.session_state.chat_messages.pop(0)

    # 채팅창 렌더링
    chat_html = "<div class='chat-box'>"
    for msg in st.session_state.chat_messages:
        chat_html += f"<div class='chat-msg'><b>{msg['user']}:</b> {msg['msg']}</div>"
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)
    
    # 내 채팅 전송
    chat_input = st.text_input("대화방에 한마디 던지기", placeholder="나 오늘 돈 너무 쓰고 싶다..")
    if st.button("전송 ✉️"):
        if chat_input:
            st.session_state.chat_messages.append({"user": my_nickname, "msg": chat_input})
            st.rerun()
