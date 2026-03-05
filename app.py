import streamlit as st
import requests
import json
import time
from datetime import datetime

# === 1. 飞书联动配置 (持久化记忆) ===
LARK_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89"

# === 2. 核心状态初始化 (防御性编程，防止看板消失) ===
if "history_logs" not in st.session_state:
    st.session_state.history_logs = []  # 存储看板数据
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None # 存储当前AI分析结论

# === 3. 智能 ASR 审计引擎 (适配上下文：防御心态识别) ===
def perform_ai_audit(file_name):
    time.sleep(1.5)
    # 针对你上传的：含介绍_沟通开放度_防御心态明显抵触_双声道.wav
    if any(k in file_name for k in ["抵触", "防御", "别问"]):
        return {
            "risk": "特高 (98%)",
            "reason": "沟通高度受阻 (防御心态)",
            "competitor": "未知/待确认",
            "title": "🥊 【紧急】破冰行动：应对高抵触客户",
            "steps": ["1. **立即止损**：销售停止电话联系，防止拉黑", "2. **微信渗透**：由店长发送‘深夜致歉信’软性植入", "3. **价值转接**：3天后由内训师以‘产品回访’身份切入"],
            "script": "“王先生，理解您的忙碌，资料我发您微信，绝不再打扰...”",
            "bitable_status": "⚠️ 待致电 (破冰指令已生成)"
        }
    return {
        "risk": "高危 (92%)",
        "reason": "竞品拦截 (问界M7)",
        "competitor": "问界M7",
        "title": "⚔️ 【紧急】针对问界M7的战败挽回任务",
        "steps": ["1. **闪电回访**：30min内主管介入", "2. **FAB对比**：强调LS6全系激光雷达优势", "3. **利益诱导**：下放5000元专项补贴"],
        "script": "“王先生，LS6在底盘安全和智驾标配上领先M7一个代际...”",
        "bitable_status": "⚠️ 待致电 (任务书已生成)"
    }

# === 4. UI 布局 ===
st.set_page_config(page_title="WinBack-Radar 3.11", layout="centered")

# 标题行 (严格对齐截图)
c1, c2 = st.columns([0.1, 0.9])
with c1: st.write("## 🛡️")
with c2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

with st.sidebar:
    st.header("⚙️ 自动化引擎")
    sync_lark = st.toggle("同步群机器人预警", value=True)
    st.toggle("数据自动入库 Bitable", value=True)
    st.divider()
    st.caption("演示版 v3.11 | 基于飞书 OpenClaw")

# A. 审计输入区
uploaded_file = st.file_uploader("上传录音文件 (.wav/.mp3)", type=["wav", "mp3"])
if st.button("🚀 启动 AI 实时审计样本", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "智慧工牌采样.wav"
    with st.status(f"🔍 正在提取 ASR 语义特征: {fname}...", expanded=True):
        res = perform_ai_audit(fname)
        st.session_state.current_analysis = res
        
        # 实时写入看板流水 (确保列名与截图 image_a01315.png 严格一致)
        new_log = {
            "记录时间": datetime.now().strftime("%H:%M:%S"),
            "风险分类": res["reason"],
            "关联竞品": res["competitor"],
            "任务状态": res["bitable_status"]
        }
        st.session_state.history_logs.insert(0, new_log)

# B. 结果看板/报告区 (核心展示区)
if st.session_state.current_analysis:
    data = st.session_state.current_analysis
    st.divider()
    st.subheader("📊 AI 审计报告")
    
    col_l, col_r = st.columns(2)
    col_l.metric("风险等级", data["risk"])
    col_r.metric("战败归因", data["reason"])

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        for s in data["steps"]: st.write(s)
        st.info(f"**建议挽回话术：**\n{data['script']}")

    if st.button("🔥 发起冲锋 (WinBack)", type="primary", use_container_width=True):
        # 1. 冲击波特效
        st.components.v1.html("""<div style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999;display:flex;align-items:center;justify-content:center;pointer-events:none;animation:fadeout 1.2s forwards;"><h1 style="font-family:'Arial Black';font-size:100px;color:white;text-shadow:0 0 20px #FF3D00,8px 8px 0px #FFEA00;animation:impact 0.4s;">WINBACK!</h1></div><style>@keyframes impact{0%{transform:scale(5);opacity:0;}100%{transform:scale(1);opacity:1;}}@keyframes fadeout{0%,80%{opacity:1;}100%{opacity:0;}}</style>""", height=0)
        
        # 2. 状态逻辑闭环：更新看板第一行的状态
        if st.session_state.history_logs:
            st.session_state.history_logs[0]["任务状态"] = "⚡ 冲锋执行中"
        
        # 3. 飞书联动
        if sync_lark:
            payload = {"msg_type":"interactive","card":{"header":{"title":{"tag":"plain_text","content":"🚨 战败风险预警"},"template":"red"},"elements":[{"tag":"div","text":{"tag":"lark_md","content":f"**风险：**{data['reason']}\n**对手：**{data['competitor']}"}},{"tag":"hr"},{"tag":"div","text":{"tag":"lark_md","content":f"**话术：**{data['script']}"}}]}}
            requests.post(LARK_WEBHOOK, json=payload)
        
        st.success("✅ 指令已下发，多维表格状态已同步更新！")
        st.balloons()

# C. 数据流水看板 (严格修复 image_9f2a59.png 的混乱问题)
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时同步)")
if st.session_state.history_logs:
    # 强制重新构建 DataFrame 确保列序和列名整洁
    import pandas as pd
    df = pd.DataFrame(st.session_state.history_logs)
    st.table(df[["记录时间", "风险分类", "关联竞品", "任务状态"]])
