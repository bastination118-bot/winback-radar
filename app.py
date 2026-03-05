import streamlit as st
import requests
import json
import time
from datetime import datetime

# === 1. 初始化与配置 (找回飞书联动灵魂) ===
LARK_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89"

# 变量安全初始化，彻底解决 AttributeError
if "history_logs" not in st.session_state:
    st.session_state.history_logs = []
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None
if "analysed" not in st.session_state:
    st.session_state.analysed = False

# === 2. 飞书联动核心函数 ===
def send_lark_card(data):
    """推送红色高危预警卡片至飞书群聊"""
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": "🚨 WinBack 战败抢救指令"}, "template": "red"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**预警原因：** {data['reason']}\n**关联对手：** {data['competitor']}"}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**💡 执行话术：**\n{data['script']}"}},
                {"tag": "action", "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": "立即回访"}, "type": "primary"}]}
            ]
        }
    }
    try:
        requests.post(LARK_WEBHOOK, json=payload, timeout=5)
    except:
        pass

# === 3. 智能决策引擎 (针对性适配上传音频) ===
def get_ai_analysis(file_name):
    """模拟语义审计，识别抵触情绪或竞品拦截"""
    time.sleep(1.2)
    # 针对你上传的：含介绍_沟通开放度_防御心态明显抵触_双声道.wav
    if any(k in file_name for k in ["抵触", "防御", "不想聊"]):
        return {
            "risk_level": "特高 (98%)",
            "reason": "沟通高度受阻",
            "competitor": "未知/全行业",
            "title": "🥊 破冰行动：应对高抵触客户温养SOP",
            "steps": ["1. **立即止损**：停止电话轰炸，防止投诉拉黑", "2. **微信渗透**：3h后发送‘不打扰致歉信’", "3. **价值钩子**：24h后推送‘静谧性’专题视频"],
            "script": "“王先生，理解您的忙碌。资料我发您微信，您空了扫一眼就行，绝不再打扰...”"
        }
    else:
        return {
            "risk_level": "高危 (92%)",
            "reason": "竞品拦截",
            "competitor": "问界M7",
            "title": "⚔️ 战败反击：针对问界M7的价值重塑",
            "steps": ["1. **闪电回访**：内训师30min内介入", "2. **火力压制**：发送‘全系标配激光雷达’对比图", "3. **限时钩子**：下放5000元战败专项补贴"],
            "script": "“王先生，LS6在底盘安全和智驾算法上领先问界M7一个代际...”"
        }

# === 4. UI 视觉组件 ===
def trigger_winback_fx():
    st.components.v1.html("""
    <div style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:9999; display:flex; align-items:center; justify-content:center; pointer-events:none; animation: fadeout 1.2s forwards;">
        <h1 style="font-family:'Arial Black'; font-size:100px; color:white; text-shadow: 0 0 20px #FF3D00, 8px 8px 0px #FFEA00; animation: impact 0.4s;">WINBACK!</h1>
    </div>
    <style>
        @keyframes impact { 0% { transform: scale(5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        @keyframes fadeout { 0%, 80% { opacity: 1; } 100% { opacity: 0; } }
    </style>
    """, height=0)

# === 5. 页面布局开始 ===
st.set_page_config(page_title="WinBack-Radar 3.11", layout="centered")

# 标题对齐 [0.1, 0.9]
t_col1, t_col2 = st.columns([0.1, 0.9])
with t_col1: st.write("## 🛡️")
with t_col2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

with st.sidebar:
    st.header("⚙️ 联动配置")
    sync_lark = st.toggle("同步群机器人预警", value=True)
    st.info("💡 状态：演示模式 v3.11 已开启")
    st.write(f"🔗 Webhook: 已锁定")

# 1. 触发审计
uploaded_file = st.file_uploader("上传智慧工牌录音 (.wav / .mp3)", type=["wav", "mp3"])
if st.button("🚀 启动 AI 实时审计样本", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "模拟对话.wav"
    with st.status(f"🔍 正在进行语义审计: {fname}...", expanded=True) as s:
        st.session_state.current_analysis = get_ai_analysis(fname)
        st.session_state.analysed = True
        s.update(label="审计完成！已识别战败风险", state="complete")
    
    # 存入流水 (规范化字段，解决看板混乱)
    new_log = {
        "记录时间": datetime.now().strftime("%H:%M:%S"),
        "风险分类": st.session_state.current_analysis["reason"],
        "关联竞品": st.session_state.current_analysis["competitor"],
        "任务状态": "⏳ 待下发"
    }
    st.session_state.history_logs.insert(0, new_log)

# 2. 报告展示
if st.session_state.analysed and st.session_state.current_analysis:
    data = st.session_state.current_analysis
    st.divider()
    st.subheader("📊 AI 分析报告")
    
    # 指标栏
    m1, m2, m3 = st.columns(3)
    m1.metric("风险等级", data["risk_level"])
    m2.metric("战败归因", data["reason"])
    m3.metric("挽回建议", "立即发起冲锋")

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        for step in data['steps']: st.write(step)
        st.info(f"**建议挽回话术：** {data['script']}")

    # 冲锋联动按钮
    if st.button("🔥 发起冲锋 (WinBack)", type="primary", use_container_width=True):
        trigger_winback_fx()
        # 实时更新看板第一行的状态
        if st.session_state.history_logs:
            st.session_state.history_logs[0]["任务状态"] = "⚡ 冲锋执行中"
        
        if sync_lark:
            send_lark_card(data)
            st.success("✅ 挽回指令已通过飞书卡片实时下发至店长端！")
        st.balloons()

# 3. 数据看板回归 (简洁版)
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时流水)")
if st.session_state.history_logs:
    st.table(st.session_state.history_logs)
