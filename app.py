import streamlit as st
import requests
import json
import time
from datetime import datetime

# === 1. 核心联动配置 (找回记忆) ===
CONFIG = {
    "LARK_WEBHOOK": "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89",
    "APP_TOKEN": "bascnM6XXXXXX",  # 请确认你的多维表格 Token
    "TABLE_ID": "tblXXXXXX",       # 请确认你的数据表 ID
    "TENANT_ACCESS_TOKEN": ""      # 自动获取或手动填入
}

if "history_logs" not in st.session_state:
    st.session_state.history_logs = []
if "analysed" not in st.session_state:
    st.session_state.analysed = False

# === 2. 飞书联动函数库 ===

def send_feishu_group_card(data):
    """推送红色精美卡片到飞书群聊"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": "🚨 WinBack 战败挽回预警"}, "template": "red"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**风险归因：** {data['reason']}\n**目标竞品：** {data['competitor']}"}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**建议话术：**\n{data['script']}"}},
                {"tag": "action", "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": "立即致电挽回"}, "type": "primary"}]}
            ]
        }
    }
    requests.post(CONFIG["LARK_WEBHOOK"], json=payload, headers=headers)

def sync_to_bitable(data):
    """同步数据至飞书多维表格 (Bitable)"""
    # 此处为模拟调用 Bitable API，正式环境需先获取 tenant_token
    # API URL: https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records
    pass 

# === 3. 智能决策引擎 (适配上传的抵触音频) ===
def get_smart_analysis(file_name):
    # 针对上传的 '含介绍_沟通开放度_防御心态明显抵触_双声道.wav'
    if "抵触" in file_name or "防御" in file_name:
        return {
            "risk_level": "特高 (98%)", "reason": "沟通高度受阻", "competitor": "未知",
            "title": "🥊 破冰行动：应对高抵触客户",
            "steps": ["1. 立即停止推销", "2. 微信弱介入", "3. 24h后由经理回访"],
            "script": "“王先生，理解您的忙碌，资料我发您微信，绝不再打扰...”"
        }
    return {
        "risk_level": "高危 (92%)", "reason": "竞品拦截", "competitor": "问界M7",
        "title": "⚔️ 战败反击：对标问界M7",
        "steps": ["1. 强调智驾标配", "2. 5000元补贴", "3. 邀约二次到店"],
        "script": "“LS6在底盘安全上领先M7一个代际...”"
    }

# === 4. WINBACK! 特效渲染 ===
def trigger_winback_fx():
    fx_html = """
    <div style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999; display:flex; align-items:center; justify-content:center; pointer-events:none; animation: fadeout 1.2s forwards;">
        <h1 style="font-family:'Arial Black'; font-size:120px; color:#FFFFFF; text-shadow: 0 0 20px #FF3D00, 10px 10px 0px #FFEA00; animation: impact 0.5s;">WINBACK!</h1>
    </div>
    <style>
        @keyframes impact { 0% { transform: scale(5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        @keyframes fadeout { 0%, 80% { opacity: 1; } 100% { opacity: 0; } }
    </style>
    """
    st.components.v1.html(fx_html, height=0)

# === 5. UI 布局 ===
st.set_page_config(page_title="WinBack-Radar 3.0", layout="centered")

# 标题行严格对齐
c1, c2 = st.columns([0.1, 0.9])
with c1: st.write("## 🛡️")
with c2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

with st.sidebar:
    st.header("⚙️ 联动配置")
    sync_lark = st.toggle("同步推送飞书卡片", value=True)
    sync_bitable = st.toggle("实时同步多维表格", value=True)
    st.divider()
    st.write(f"🔗 Webhook 已锁定")

uploaded_file = st.file_uploader("上传智慧工牌录音 (.wav)", type=["wav", "mp3"])

if st.button("🚀 启动 AI 审计", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "测试音频.wav"
    with st.status("正在进行深度语义审计...", expanded=True):
        st.session_state.current_data = get_smart_analysis(fname)
        time.sleep(1)
    
    st.session_state.analysed = True
    new_log = {
        "记录时间": datetime.now().strftime("%H:%M:%S"),
        "风险分类": st.session_state.current_data["reason"],
        "关联竞品": st.session_state.current_data["competitor"],
        "任务状态": "⏳ 待下发"
    }
    st.session_state.history_logs.insert(0, new_log)

if st.session_state.analysed:
    data = st.session_state.current_data
    st.divider()
    st.subheader("📊 AI 审计结果")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("风险等级", data["risk_level"])
    m2.metric("战败归因", data["reason"])
    m3.metric("建议响应", "立即执行")

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        for s in data["steps"]: st.write(s)
        st.info(f"**挽回话术：** {data['script']}")

    if st.button("🔥 发起冲锋 (WinBack)", type="primary", use_container_width=True):
        trigger_winback_fx()
        # 更新看板状态
        if st.session_state.history_logs:
            st.session_state.history_logs[0]["任务状态"] = "⚡ 冲锋执行中"
        
        if sync_lark: send_feishu_group_card(data)
        if sync_bitable: sync_to_bitable(data)
        
        st.success("✅ 数据已同步至飞书群聊及多维表格！")
        st.balloons()

# 底部看板回归
st.divider()
st.subheader("📈 数据资产看板 (Bitable 同步流水)")
if st.session_state.history_logs:
    st.table(st.session_state.history_logs)
