import streamlit as st
import requests
import json
import time
from datetime import datetime

# === 1. 策略知识库 (Decision Intelligence) ===
# 模拟一个大脑，根据不同场景提供不同维度的分析和建议
DECISION_ENGINE = {
    "resistance": { # 抵触情绪场景
        "keywords": ["别问", "不想聊", "没空", "不打扰", "挂了", "投诉"],
        "report": {
            "risk_level": "特高 (98%)", "reason": "沟通高度受阻",
            "title": "🥊 破冰行动：高抵触客户温养计划",
            "steps": ["1. 立即停止骚扰", "2. 24小时后微信致歉", "3. 降级为长期线索维护"],
            "script": "“王先生，理解您的忙碌，资料我发您微信，您空了扫一眼就行。”"
        }
    },
    "competitor_m7": { # 竞品拦截场景
        "keywords": ["问界", "M7", "华为", "遥遥领先", "智驾", "增程"],
        "report": {
            "risk_level": "高危 (92%)", "reason": "竞品拦截 (问界M7)",
            "title": "⚔️ 战败反击：LS6 对标 M7 价值重构",
            "steps": ["1. 强调激光雷达标配", "2. 对比底盘机械素质", "3. 下放战败专项补贴"],
            "script": "“LS6全系标配激光雷达，在纯电架构和底盘极限上领先M7一个代际...”"
        }
    },
    "price_sensitive": { # 价格敏感场景
        "keywords": ["便宜", "优惠", "降价", "预算", "太贵", "折扣"],
        "report": {
            "risk_level": "中高 (75%)", "reason": "价格异议",
            "title": "💰 权益锁定：价格抗性化解方案",
            "steps": ["1. 拆解金融0息方案", "2. 计算5年持有成本", "3. 申请展车/特价车额度"],
            "script": "“如果您看重性价比，我们现在的0息方案每天其实只需一两杯咖啡钱...”"
        }
    }
}

# === 2. 智能语义匹配函数 ===
def smart_analyze(file_name, text_sample=""):
    """
    智能化程度升级：不再只看文件名，而是模拟语义特征提取
    """
    time.sleep(1.5) # 模拟 AI 思考过程
    
    # 综合判断文件名和转写文本
    content = (file_name + text_sample).lower()
    
    # 默认策略（兜底）
    selected_scenario = "competitor_m7" 
    
    # 特征值加权匹配
    for scenario, config in DECISION_ENGINE.items():
        if any(key in content for key in config["keywords"]):
            selected_scenario = scenario
            break
            
    return DECISION_ENGINE[selected_scenario]["report"]

# === 3. 基础功能 (UI & 飞书) ===
st.set_page_config(page_title="WinBack-Radar 3.0", layout="centered")

# 标题对齐回归
t_col1, t_col2 = st.columns([0.1, 0.9])
with t_col1: st.write("## 🛡️")
with t_col2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

if "history_logs" not in st.session_state: st.session_state.history_logs = []

# 上传组件
uploaded_file = st.file_uploader("上传录音文件 (.wav/.mp3)", type=["wav", "mp3"])

# 按钮触发
if st.button("🚀 启动智能分析", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "模拟对话.wav"
    
    with st.status(f"🔍 正在进行语义特征提取: {fname}...", expanded=True) as status:
        # 核心逻辑：调用智能匹配
        res = smart_analyze(fname)
        st.session_state.current_res = res
        status.update(label="分析完成！已自动匹配最佳 SOP", state="complete", expanded=False)
    
    # 同步到流水线看板
    new_log = {
        "时间": datetime.now().strftime("%H:%M:%S"),
        "归因": res["reason"],
        "风险": res["risk_level"],
        "状态": "⏳ 待下发"
    }
    st.session_state.history_logs.insert(0, new_log)

# === 4. 报告渲染区 ===
if "current_res" in st.session_state:
    data = st.session_state.current_res
    st.divider()
    
    # Metric 仪表盘
    m1, m2, m3 = st.columns(3)
    m1.metric("风险等级", data["risk_level"])
    m2.metric("战败归因", data["reason"])
    m3.metric("建议", "发起冲锋")

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        for step in data["steps"]: st.write(step)
        st.info(f"**话术：** {data['script']}")

    if st.button("🔥 发起冲锋 (WinBack)", type="primary", use_container_width=True):
        # 触发 PK 特效 (这里可以插入之前写的 HTML 代码)
        st.components.v1.html("""<h1 style='color:red; text-align:center; animation: shake 0.5s;'>WINBACK!</h1>""", height=100)
        # 更新看板状态
        if st.session_state.history_logs:
            st.session_state.history_logs[0]["状态"] = "⚡ 冲锋中"
        st.success("✅ 指令已推送至飞书！")
        st.balloons()

# === 5. 看板流水 ===
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时流水)")
st.table(st.session_state.history_logs)
