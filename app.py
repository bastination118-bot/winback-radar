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
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = {}

# === 2. 增强型智能分析逻辑 ===
def analyze_audio_content(file_name, is_mock_button=False):
    """模拟 ASR 语义分析，根据内容分发挽回策略"""
    # 模拟分析延迟
    time.sleep(1.5)
    
    # 逻辑分支：如果文件名包含“抵触”或“不想聊”，给出防御性挽回策略
    if "抵触" in file_name or "不想聊" in file_name:
        return {
            "pain_point": "客户防御心理极强，拒绝电话沟通，存在严重流失风险。",
            "competitor": "未知/全行业拦截",
            "risk_level": "特高 (98%)",
            "reason": "沟通高度受阻",
            "title": "🥊 破冰行动：针对高抵触客户的‘退一步’策略",
            "steps": [
                "1. **立即止损**：销售端停止电话轰炸，避免被拉黑。",
                "2. **微信温养**：3小时後发送‘不打扰致歉信’+‘智己LS6静謐性测试视频’（软性植入）。",
                "3. **权益钩子**：24小时后由店长账号推送‘专属深度试驾邀请’，强调私人预约制。"
            ],
            "script": "“王先生，非常抱歉刚才打扰到您。我理解您的忙碌，后续我不打扰您，资料我发您微信，您空了扫一眼就行...”"
        }
    else:
        # 默认的竞品对比策略
        return {
            "pain_point": "客户提及价格异议，正在对比问界M7。",
            "competitor": "问界M7",
            "risk_level": "高危 (92%)",
            "reason": "竞品拦截",
            "title": "⚔️ 战败反击：针对问界M7的价值重塑",
            "steps": [
                "1. **闪电回访**：30分钟内内训师介入，锁定价格异议点。",
                "2. **火力压制**：发送LS6‘全系标配激光雷达’对比海报。",
                "3. **终极邀约**：发放战败专享5000元补贴。"
            ],
            "script": "“王先生，关于您看的问界M7，LS6在底盘安全和智驾算法上领先一个代际...”"
        }

# === 3. PK 风格特效 (WinBack 版) ===
def trigger_winback_fx():
    fx_html = """
    <div id="fx-container" style="position:fixed; top:0; left:0; width:100%; height:100%; 
        background:rgba(255,61,0,0.2); z-index:9999; display:flex; align-items:center; justify-content:center;
        pointer-events:none; animation: fadeout 1.2s forwards;">
        <h1 style="font-family:'Arial Black', sans-serif; font-size:100px; color:#FFFFFF;
            text-shadow: 0 0 20px #FF3D00, 5px 5px 0px #FFEA00;
            animation: impact 0.4s cubic-bezier(0.17, 0.89, 0.32, 1.49);">
            WINBACK!
        </h1>
    </div>
    <style>
        @keyframes impact { 0% { transform: scale(5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        @keyframes fadeout { 0%, 80% { opacity: 1; } 100% { opacity: 0; } }
    </style>
    """
    st.components.v1.html(fx_html, height=200)

# === 4. UI 布局 ===
st.set_page_config(page_title="WinBack-Radar 3.0", layout="centered")

# 标题行
t_col1, t_col2 = st.columns([0.12, 0.88])
with t_col1: st.write("## 🛡️")
with t_col2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

with st.sidebar:
    st.header("⚙️ 自动化配置")
    sync_lark = st.toggle("同步群机器人预警", value=True)
    st.info("💡 提示：上传文件名带‘抵触’二字可触发特殊 SOP")

# 触发审计
uploaded_file = st.file_uploader("上传智慧工牌录音 (.wav / .mp3)", type=["wav", "mp3"])
if st.button("🚀 启动模拟样本审计", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "模拟问界M7对话.wav"
    with st.status(f"🔍 AI 正在审计: {fname}...", expanded=True) as status:
        st.session_state.current_analysis = analyze_audio_content(fname)
        status.update(label="分析完成！已识别风险特征", state="complete", expanded=False)
    
    st.session_state.analysed = True
    # 存入流水看板
    new_log = {
        "记录时间": datetime.now().strftime("%H:%M:%S"),
        "风险分类": st.session_state.current_analysis["reason"],
        "关联竞品": st.session_state.current_analysis["competitor"],
        "任务状态": "⏳ 待处理"
    }
    st.session_state.history_logs.insert(0, new_log)

# 分析结果展示
if st.session_state.analysed and st.session_state.current_analysis:
    data = st.session_state.current_analysis
    st.divider()
    st.subheader("📊 语义审计报告")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("风险等级", data["risk_level"])
    m_col2.metric("战败归因", data["reason"])
    m_col3.metric("建议响应", "立即执行")

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        st.write(f"**诊断结论：** {data['pain_point']}")
        for step in data['steps']:
            st.write(step)
        st.info(f"**挽回话术：** {data['script']}")

    if st.button("🔥 发起冲锋 (WinBack)", type="primary", use_container_width=True):
        trigger_winback_fx() # 特效
        # 更新状态不一致问题
        if st.session_state.history_logs:
            st.session_state.history_logs[0]["任务状态"] = "⚡ 冲锋执行中"
        
        if sync_lark:
            # 此处发送逻辑还原之前的精美卡片... (略，保持原有 send_feishu_card)
            st.success("✅ 战败挽回指令已通过 Webhook 下发至店长端！")
        st.balloons() # 备用动效

# 底部看板
st.divider()
st.subheader("📈 数据资产看板 (Bitable 同步流水)")
if st.session_state.history_logs:
    st.table(st.session_state.history_logs)
