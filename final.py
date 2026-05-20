import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="방구석 거지방 Pro Max", page_icon="💸", layout="centered")

# CSS 스타일 수정 (통계 카드 및 디자인 고도화)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .post-box { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 5px; }
    .character-box { background-color: #fff9db; padding: 15px; border-radius: 10px; border: 2px dashed #fcc419; text-align: center; margin-bottom: 20px; }
    .chat-box { background-color: #eaeaea; padding: 15px; border-radius: 10px; max-height: 250px; overflow-y: auto; margin-bottom: 15px; }
    .chat-msg { background-color: white; padding: 8px 12px; border-radius: 10px; margin-bottom: 8px; font-size: 14px; }
    .stat-card { background-color: #e8f7ff; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; border: 1px solid #b3e3ff; }
    </style>
""", unsafe_allow_html=True)

# 2. 초기 데이터 구성
if 'posts' not in st.session_state:
    st.session_state.posts = [
        {"id": 1, "time": "2026-05-20 15:00", "nickname": "월급은통장을스칠뿐", "item": "엽기떡볶이 세트", "price": 24000, "reason": "부장님한테 한 소리 듣고 스트레스 받아서 결제함..", "good": 3, "bad": 42, "comments": ["스트레스는 운동으로!", "떡볶이에 2만 원은 유죄"]},
        {"id": 2, "time": "2026-05-20 14:45", "nickname": "헤르미온느", "item": "아이패드 프로 13인치", "price": 1490000, "reason": "이걸로 인강 들으면서 갓생 살려고요. 투자 맞죠?", "good": 1, "bad": 185, "comments": ["유튜브 머신 예약", "당근마켓 키워드 알림 설정합니다"]},
        {"id": 3, "time": "2026-05-20 14:30", "nickname": "절약왕이될상", "item": "편의점 혜자도시락", "price": 4500, "reason": "술자리 유혹 뿌리치고 편의점 혼밥했습니다. 칭찬 조종해 주세요.", "good": 98, "bad": 2, "comments": ["와 리스펙", "당신이 이 방의 왕"]},
        {"id": 4, "time": "2026-05-20 13:10", "nickname": "참새와방앗간", "item": "탕후루 2개", "price": 6000, "reason": "설탕 냄새가 너무 달콤해서 정신 차려보니 입에 꼬치가...", "good": 12, "bad": 56, "comments": ["치과 의사선생님이 좋아합니다", "설탕물에 6천 원을?"]},
        {"id": 5, "time": "2026-05-20 12:05", "nickname": "무소유꿈나무", "item": "헬스장 12개월권", "price": 480000, "reason": "장기 결제해야 싸서 끊었습니다! 진짜 다이어트함", "good": 35, "bad": 38, "comments": ["기부천사 예약", "제발 다음 달에도 가시길"]}
    ]

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"user": "무소유마스터", "msg": "오늘 무지출 챌린지 성공 지립니닷"},
        {"user": "지갑전사", "msg": "방금 치킨 결제하려다가 손가락 부러뜨렸습니다 휴..."},
        {"user": "치킨유혹꾼", "msg": "치킨 냄새 장난아닌데 참으시네 독하다 독해"}
    ]

# 3. 사이드바 - 프로필 및 거지 캐릭터
st.sidebar.title("💰 나의 거지방 프로필")
my_nickname = st.sidebar.text_input("닉네임 설정", value="방구석거지")

total_spent = sum([p['price'] for p in st.session_state.posts if p['nickname'] == my_nickname])
st.sidebar.metric(label="내가 오늘 지른 금액", value=f"{total_spent:,} 원")

if total_spent == 0:
    tier, char_avatar, char_status = "💎 무소유 마스터", "🧘", "통장이 두둑하여 평화롭습니다."
elif total_spent < 15000:
    tier, char_avatar, char_status = "🥈 평범한 월급노예", "🚶", "아직까진 걸어 다닐 만합니다."
elif total_spent < 50000:
    tier, char_avatar, char_status = "🥉 자취방 흙수저", "🧎", "무릎 꿇었습니다. 삼김으로 연명하세요."
else:
    tier, char_avatar, char_status = "🚨 파산 직전의 베짱이", "💀", "지갑 폭발! 숨만 쉬고 사세요."

st.sidebar.markdown(f"""
<div class='character-box'>
    <div style='font-size: 50px;'>{char_avatar}</div>
    <div style='font-weight: bold; margin-top:5px;'>등급: {tier}</div>
    <div style='font-size: 12px; color: #666; margin-top:5px;'>{char_status}</div>
</div>
""", unsafe_allow_html=True)


# 4. 메인 화면 상단
st.title("💸 방구석 거지방 Pro Max")
st.caption("서로의 지갑을 지켜주는 눈물겨운 익명 소비 절약 커뮤니티")

# 대시보드 통계 구역 (발표용 핵심 비주얼)
st.write("### 📊 오늘의 거지방 동향")
total_goods = sum([p['good'] for p in st.
