import streamlit as st
import requests
import json
import time
from datetime import datetime

# === 1. 基础配置 ===
LARK_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89"

if "history_logs" not in st.session_state:
    st.session_state.history_logs = []
if "analysed" not in st.session_state:
    st.session_state.analysed = False

# === 2. 核心逻辑 ===
KNOWLEDGE_BASE = {
    "问界M7": "重点强调智己LS6的‘全画幅数字驾舱’与‘声纹分离技术’，对比M7的内饰风格，突显LS6的年轻化与科技感。利用FAB法则：Feature-一体式屏，Advantage-视野无盲区，Benefit-驾驶更安全。"
}

def get_rescue_mission(competitor):
    return {
        "title": f"⚔️ 战败反击：针对{competitor}的挽回行动",
        "steps": [
            f"1. **闪电回访**：30分钟内由内训师陪同销售拨打，确认客户对{competitor}的异议点。",
            f"2. **火力压制**：发送LS6‘全系标配激光雷达’对比海报，打击竞品选装痛点。",
            "3. **终极邀约**：下放‘战败专享5000元补贴’，强力钩子引导二次到店。"
        ],
        "script": f"“王先生，关于您看的{competitor}，LS6在底盘安全和智驾算法上领先一个代际...”"
    }

def send_feishu_card(data):
    headers = {"Content-Type": "application/json"}
    card_content = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": "🚨 战败风险实时预警"}, "template": "red"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**客户痛点：** {data['pain_point']}\n**对应竞品：** {data['competitor']}"}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**💡 抢救话术建议：**\n{data['script']}"}},
                {"tag": "action", "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": "立即致电客户"}, "type": "primary"}]}
            ]
        }
    }
    try: requests.post(LARK_WEBHOOK_URL, json=card_content, headers=headers)
    except: pass

# === 3. PK 特效 CSS 定义 ===
def trigger_winback_fx():
    fx_html = """
    <div id="fx-container" style="position:fixed; top:0; left:0; width:100%; height:100%; 
        background:rgba(0,0,0,0.3); z-index:9999; display:flex; align-items:center; justify-content:center;
        pointer-events:none; animation: fadeout 1.5s forwards;">
        <h1 style="font-family:'Arial Black', sans-serif; font-size:120px; color:#FF3D00;
            text-shadow: 5px 5px #FFEA00, 10px 10px #D50000;
            animation: impact 0.5s cubic-bezier(0.17, 0.89, 0.32, 1.49);">
            WINBACK!
        </h1>
    </div>
    <style>
        @keyframes impact {
            0% { transform: scale(5); opacity: 0; }
            50% { transform: scale(1); opacity: 1; }
            70% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        @keyframes fadeout {
            0% { opacity: 1; }
            80% { opacity: 1; }
            100% { opacity: 0; display:none; }
        }
    </style>
    """
    st.components.v1.html(fx_html, height=0)

# === 4. UI 页面设计 ===
st.set_page_config(page_title="WinBack-Radar 3.0", layout="centered")

# 标题行对齐回归
title_col1, title_col2 = st.columns([0.1, 0.9])
with title_col1:
    st.write("## 🛡️")
with title_col2:
    st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

st.caption("基于飞书 OpenClaw & 智驾赋能文档驱动 | 演示版 v3.3")

with st.sidebar:
    st.header("⚙️ 自动化引擎")
    sync_lark = st.toggle("同步群机器人预警", value=True)
    sync_bitable = st.toggle("数据自动入库 Bitable", value=True)
    st.divider()
    st.info("3.11 演示专用：已开启脱敏审计模式")

uploaded_file = st.file_uploader("上传录音文件", type=["mp3", "wav"])
if st.button("🚀 启动 AI 实时审计样本", use_container_width=True) or uploaded_file:
    with st.status("🔍 AI 正在进行语义审计...", expanded=True) as status:
        time.sleep(0.8)
        st.write("📡 转写文本：*‘问界M7优惠更大...’*")
        time.sleep(0.8)
        status.update(label="分析完成！", state="complete", expanded=False)
    
    st.session_state.analysed = True
    new_record = {
        "记录时间": datetime.now().strftime("%H:%M:%S"),
        "风险分类": "竞品拦截",
        "关联竞品": "问界M7",
        "任务状态": "⚡ 冲锋执行中"
    }
    st.session_state.history_logs.insert(0, new_record)

if st.session_state.analysed:
    st.divider()
    st.subheader("📊 AI 审计报告")
    
    # 仪表盘
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("风险等级", "高危 (92%)", delta="需立即干预")
    m_col2.metric("战败归因", "竞品拦截", delta="问界M7", delta_color="inverse")
    m_col3.metric("建议响应", "30分钟内")

    res_data = {"pain_point": "客户对比问界M7。", "competitor": "问界M7", "script": KNOWLEDGE_BASE["问界M7"]}
    mission = get_rescue_mission(res_data["competitor"])

    with st.expander("📋 战败挽回执行任务书 (SOP)", expanded=True):
        st.markdown(f"#### {mission['title']}")
        for step in mission['steps']:
            st.write(step)
        st.info(f"**建议话术建议：** {mission['script']}")

    # --- 冲锋按钮 & PK 特效 ---
    if st.button("🔥 发起冲锋：同步任务至飞书生态", type="primary", use_container_width=True):
        trigger_winback_fx() # 触发自定义 PK 动效
        with st.spinner("指令下发中..."):
            time.sleep(1.2)
            if sync_lark: send_feishu_card(res_data)
            st.success("✅ 任务已同步！店长端已接收精美预警卡片。")

# 底部看板流水
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时流水)")
if st.session_state.history_logs:
    st.table(st.session_state.history_logs)
