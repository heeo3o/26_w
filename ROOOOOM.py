import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="방구석 거지방 Pro", page_icon="💸", layout="centered")

# CSS 스타일 수정 (버튼 및 박스 가독성 업그레이드)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .post-box { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 5px; }
    .character-box { background-color: #fff9db; padding: 15px; border-radius: 10px; border: 2px dashed #fcc419; text-align: center; margin-bottom: 20px; }
    .chat-box { background-color: #eaeaea; padding: 15px; border-radius: 10px; max-height: 250px; overflow-y: auto; margin-bottom: 15px; }
    .chat-msg { background-color: white; padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# 2. 발표용 풍부한 초기 데이터 (5개 세팅)
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {
            "id": 1, "time": "2026-05-20 15:00", "nickname": "월급은통장을스칠뿐", 
            "item": "엽기떡볶이 + 모듬튀김 + 중국당면", "price": 24000, 
            "reason": "회사에서 부장님한테 한 소리 듣고 스트레스 받아서 나도 모르게 배민 결제함.. 살려주세요.", 
            "good": 3, "bad": 42, "comments": ["스트레스는 운동으로 푸세요", "떡볶이에 2만 4천원은 유죄"]
        },
        {
            "id": 2, "time": "2026-05-20 14:45", "nickname": "헤르미온느", 
            "item": "아이패드 프로 13인치", "price": 1490000, 
            "reason": "이걸로 인터넷 강의 들으면서 갓생 살려고 지질렀습니다. 공부할 거니까 투자 맞죠?", 
            "good": 1, "bad": 185, "comments": ["유튜브 머신 예약", "당근마켓에서 뵙겠습니다"]
        },
        {
            "id": 3, "time": "2026-05-20 14:30", "nickname": "절약왕이될상", 
            "item": "편의점 혜자도시락", "price": 4500, 
            "reason": "오늘 친구들 술자리 유혹 뿌리치고 편의점에서 혼밥했습니다. 칭찬해줘요.", 
            "good": 98, "bad": 2, "comments": ["와 이건 진짜 리스펙", "당신이 이 방의 왕입니다"]
        },
        {
            "id": 4, "time": "2026-05-20 13:10", "nickname": "참새와방앗간", 
            "item": "탕후루 2개", "price": 6000, 
            "reason": "지나가는데 설탕 냄새가 너무 달콤해서 정신 차려보니 입에 꼬치가 들려있었음", 
            "good": 12, "bad": 56, "comments": ["치과 의사선생님이 좋아합니다", "설탕물에 6천원을 태워?"]
        },
        {
            "id": 5, "time": "2026-05-20 12:05", "nickname": "무소유꿈나무", 
            "item": "헬스장 12개월 회원권", "price": 480000, 
            "reason": "오늘부터 진짜 다이어트합니다. 장기 결제해야 싸서 1년 치 끊었어요!", 
            "good": 35, "bad": 38, "comments": ["기부천사 방지 위원회에서 나왔습니다", "제발 한 달 뒤에도 가시길"]
        }
    ]

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"user": "무소유마스터", "msg": "오늘 무지출 챌린지 3일차 성공 지립니닷"},
        {"user": "지갑전사", "msg": "방금 치킨 결제하려다가 손가락 부러뜨렸습니다 휴..."},
        {"user": "치킨유혹꾼", "msg": "치킨 냄새 장난아닌데 참으시네 독하다 독해"}
    ]

# 3. 사이드바 - 프로필 & 캐릭터
st.sidebar.title("💰 나의 거지방 프로필")
my_nickname = st.sidebar.text_input("닉네임 설정", value="방구석거지")

total_spent = sum([p['price'] for p in st.session_state.posts if p['nickname'] == my_nickname])
st.sidebar.metric(label="내가 오늘 지른 금액", value=f"{total_spent:,} 원")

if total_spent == 0:
    tier, char_avatar, char_status = "💎 무소유 마스터", "🧘", "통장이 두둑하여 마음이 평화롭습니다."
elif total_spent < 15000:
    tier, char_avatar, char_status = "🥈 평범한 월급노예", "🚶", "약간의 지출이 있지만 걸어 다닐 만합니다."
elif total_spent < 50000:
    tier, char_avatar, char_status = "🥉 자취방 흙수저", "🧎", "무릎을 꿇었습니다. 삼김으로 연명하세요."
else:
    tier, char_avatar, char_status = "🚨 파산 직전의 베짱이", "💀", "지갑 폭발! 숨만 쉬고 사세요."

st.sidebar.markdown(f"""
<div class='character-box'>
    <div style='font-size: 50px;'>{char_avatar}</div>
    <div style='font-weight: bold; margin-top:5px;'>등급: {tier}</div>
    <div style='font-size: 12px; color: #666; margin-top:5px;'>{char_status}</div>
</div>
""", unsafe_allow_html=True)


# 4. 메인 화면
st.title("💸 방구석 거지방 Pro")
st.caption("서로의 지갑을 지켜주는 눈물겨운 익명 소비 절약 커뮤니티")

# 소비 등록 Form
with st.form(key="expense_form", clear_on_submit=True):
    st.subheader("📝 나의 소비 내역 고발하기")
    col1, col2 = st.columns(2)
    with col1: item = st.text_input("소비 항목", placeholder="뭘 샀나요?")
    with col2: price = st.number_input("금액 (원)", min_value=0, step=1000)
    reason = st.text_area("변명 혹은 사유", placeholder="사유를 적어보세요.")
    submit_button = st.form_submit_button(label="거지방에 고발하기 🚨")

    if submit_button and item and price > 0:
        new_post = {"id": len(st.session_state.posts) + 1, "time": datetime.now().strftime("%Y-%m-%d %H:%M"), "nickname": my_nickname, "item": item, "price": price, "reason": reason, "good": 0, "bad": 0, "comments": []}
        st.session_state.posts.insert(0, new_post)
        if price >= 50000:
            st.error(f"🚨 [파산 경고] {price:,}원?! 제정신입니까?")
            st.balloons()
        else:
            st.info("💡 고발 완료! 심판을 기다리세요.")
        st.rerun()

st.write("---")

# 5. 탭 구성
tab1, tab2 = st.tabs(["🔥 소비 심판소 (타임라인)", "💬 실시간 거지 대화방"])

with tab1:
    st.subheader("🔥 실시간 대기 중인 소비 심판소")
    
    for idx, post in enumerate(st.session_state.posts):
        # 포스트 박스
        st.markdown(f"""
        <div class='post-box'>
            <span style='color:gray; font-size:12px;'>{post['time']} | <b>{post['nickname']}</b></span>
            <h4 style='margin: 5px 0;'>🛒 {post['item']} - <span style='color:#ff4b4b;'>{post['price']:,}원</span></h4>
            <p style='color:#495057; background:#f1f3f5; padding:10px; border-radius:5px;'>💬 "{post['reason']}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 투표 버튼 구역 (이펙트 추가)
        col_g, col_b, _ = st.columns([1.5, 1.5, 3])
        
        with col_g:
            # 참음 버튼 (성공 이펙트)
            if st.button(f"🟢 참음 대단해 ({post['good']})", key=f"good_{post['id']}_{idx}"):
                post['good'] += 1
                st.toast(f"🎉 {post['nickname']}님에게 칭찬을 건넸습니다! (참음 +1)", icon="👏")
                st.snow() # 화면에 이쁜 눈/스파크가 내리는 효과 (발표용으로 최고)
                time.sleep(0.5) # 이펙트를 보여주기 위한 잠깐의 딜레이
                st.rerun()
                
        with col_b:
            # 때찌 버튼 (경고 이펙트)
            if st.button(f"🔴 때찌 정신차려 ({post['bad']})", key=f"bad_{post['id']}_{idx}"):
                post['bad'] += 1
                st.toast(f"🤬 {post['nickname']}님의 등짝을 후려쳤습니다! (때찌 +1)", icon="🚨")
                st.error("🚨 등짝 스매싱! 소비 통제 불능 유저를 처단했습니다!") # 상단 경고 팝업으로 티 내기
                time.sleep(0.5)
                st.rerun()
                
        # 잔소리 댓글
        with st.expander(f"🤬 잔소리 {len(post['comments'])}개 보기"):
            for comment in post['comments']:
                st.write(f"- {comment}")
            comment_input = st.text_input("정신 차리라고 한마디 하기", key=f"cmt_input_{post['id']}_{idx}")
            if st.button("잔소리 투척", key=f"cmt_btn_{post['id']}_{idx}"):
                if comment_input:
                    post['comments'].append(comment_input)
                    st.rerun()
        st.write("<br>", unsafe_allow_html=True)

with tab2:
    st.subheader("💬 거지방 실시간 익명 수다")
    if random.random() < 0.3:
        bot_names = ["밥은먹고다니냐", "탕진잼", "무소유가꿈", "시골쥐"]
        bot_msgs = ["아 배고프다 물 마셔야지", "오늘 회사 동료가 커피 사줘서 방어 성공!", "택배 인출 금지령 내렸습니다", "내 지갑 눈 감아"]
        st.session_state.chat_messages.append({"user": random.choice(bot_names), "msg": random.choice(bot_msgs)})
        if len(st.session_state.chat_messages) > 10: st.session_state.chat_messages.pop(0)

    chat_html = "<div class='chat-box'>"
    for msg in st.session_state.chat_messages:
        chat_html += f"<div class='chat-msg'><b>{msg['user']}:</b> {msg['msg']}</div>"
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)
    
    chat_input = st.text_input("대화방에 한마디 던지기", placeholder="나 오늘 돈 너무 쓰고 싶다..")
    if st.button("전송 ✉️"):
        if chat_input:
            st.session_state.chat_messages.append({"user": my_nickname, "msg": chat_input})
            st.rerun()
