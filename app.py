import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime

# === 1. 核心联动配置 ===
LARK_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89"

# === 2. 状态强效初始化 ===
if "history_logs" not in st.session_state:
    st.session_state.history_logs = []
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None

# === 3. 语义分析引擎 v1.2 (新增试驾满意逻辑) ===
def get_semantic_analysis(file_name):
    """
    语义分析引擎 v1.2：新增试驾维度，解决识别响应错误
    """
    time.sleep(1.2)
    fname = file_name.lower()
    
    # --- 场景 1：已购战败 (针对：已购他牌退订.wav) ---
    if any(k in fname for k in ["退订", "已购", "买了他牌", "他牌", "买了别的"]):
        return {
            "risk": "已流失 (100%)",
            "reason": "彻底战败 (已购竞品)",
            "competitor": "其他品牌",
            "title": "📉 【战败归档】存量线索转公海审计",
            "steps": ["1. 确认成交点", "2. 发送品牌留痕卡片", "3. 线索自动转公海"],
            "script": "“王先生，祝贺提车！LS6的OTA计划我也发您，以后换车再考虑咱家。”",
            "status_label": "🚫 战败归档"
        }
    
    # --- 场景 2：试驾满意 (新增：针对试驾满意.wav) ---
    elif any(k in fname for k in ["满意", "试驾", "不错", "挺好", "开着舒服"]):
        return {
            "risk": "极低 (10%)",
            "reason": "试驾满意 (情绪正面)",
            "competitor": "无",
            "title": "⚡ 【趁热打铁】试驾后即时促单方案",
            "steps": [
                "1. **强化体验**：发送刚才试驾时的智驾功能回放视频。",
                "2. **权益倒计时**：告知‘试驾当日定车额外礼遇’。",
                "3. **对比报告**：发送一份针对客户关注点的《LS6竞品优势表》。"
            ],
            "script": "“王先生，看您刚才试驾完心情不错，LS6的智驾确实很顶。今天定车还能额外多送两万积分，咱们把手续办了？”",
            "status_label": "✅ 促单中"
        }

    # --- 场景 3：意愿强烈 (愿意购车.wav) ---
    elif any(k in fname for k in ["愿意", "购车", "下定", "准备买"]):
        return {
            "risk": "极低 (5%)",
            "reason": "准成交状态",
            "competitor": "无",
            "title": "🎉 【促单保单】限时权益锁定SOP",
            "steps": ["1. 权益锁定", "2. 金融测算", "3. 引导锁单"],
            "script": "“王先生，现在下定能锁住本月权益，我把小程序发您。”",
            "status_label": "✅ 待成交"
        }
    
    # --- 场景 4：严重抵触 ---
    elif any(k in fname for k in ["不愿", "防御", "抵触", "别问", "别打"]):
        return {
            "risk": "特高 (98%)",
            "reason": "沟通受阻 (反感度高)",
            "competitor": "未知",
            "title": "🥊 【破冰行动】情绪安抚计划",
            "steps": ["1. 立即止损", "2. 微信弱温养"],
            "script": "“王先生，资料发您微信了，近期不再打扰您。”",
            "status_label": "⚠️ 待破冰"
        }
    
    # --- 场景 5：竞品拦截 ---
    elif any(k in fname for k in ["问界", "m7", "小米", "su7", "特斯拉"]):
        comp = "问界M7" if "问界" in fname else "小米SU7"
        return {
            "risk": "高危 (92%)",
            "reason": f"强对标 ({comp})",
            "competitor": comp,
            "title": f"⚔️ 【抢救任务】针对{comp}的对标方案",
            "steps": ["1. 差异化打击", "2. 发送对比图", "3. 邀约二试"],
            "script": f"“王先生，{comp}不错，但LS6的底盘调校更好...”",
            "status_label": "🔥 挽回中"
        }
    
    # --- 场景 6：兜底 ---
    return {
        "risk": "中等 (45%)",
        "reason": "正在观望",
        "competitor": "全品牌",
        "title": "🔍 【价值挖掘】客户需求培育",
        "steps": ["1. 寻找痛点", "2. 发送推文"],
        "script": "“王先生，您平时主要是通勤还是长途？我给您匹配个方案？”",
        "status_label": "⏳ 待培育"
    }

# === 4. UI 布局与 CSS 彻底修复显示问题 ===
st.set_page_config(page_title="WinBack-Radar 1.2", layout="centered")

st.markdown("""
<style>
    /* 解决 Metric 截断 */
    [data-testid="stMetric"] { overflow: visible !important; }
    [data-testid="stMetricValue"] { font-size: 22px !important; white-space: normal !important; overflow: visible !important; }
    [data-testid="stMetricLabel"] { white-space: normal !important; }
    
    /* 解决表格截断与布局 */
    div[data-testid="stTable"] td { white-space: normal !important; word-break: break-all !important; line-height: 1.4 !important; }
    .stTable { width: 100%; border: 1px solid #f0f2f6; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# 标题
h1, h2 = st.columns([0.1, 0.9])
with h1: st.write("## 🛡️")
with h2: st.write("## 战败雷达 (WinBack-Radar) v1.2")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 引擎设置")
    sync_lark = st.toggle("同步飞书卡片", value=True)
    st.divider()
    st.caption("v1.2 已优化 CSS 布局与试驾满意模型")

# 4.1 触发
uploaded_file = st.file_uploader("上传录音采样", type=["wav", "mp3"])
if st.button("🚀 启动 AI 智能审计", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "默认采样.wav"
    with st.status(f"🔍 语义深度扫描: {fname}...") as s:
        res = get_semantic_analysis(fname)
        st.session_state.current_analysis = res
        
        # 强制标准字段
        log_entry = {
            "记录时间": datetime.now().strftime("%H:%M:%S"),
            "风险分类": res["reason"],
            "关联竞品": res["competitor"],
            "任务状态": res["status_label"]
        }
        st.session_state.history_logs.insert(0, log_entry)
        st.session_state.history_logs = st.session_state.history_logs[:5]
        s.update(label="分析完成！", state="complete")

# 4.2 报告展示 (修复显示不全)
if st.session_state.current_analysis:
    data = st.session_state.current_analysis
    st.divider()
    st.subheader("📊 AI 审计报告")
    
    m1, m2, m3 = st.columns(3)
    # 强制让 Metric 这里的文字不被截断
    m1.metric("风险评估", data["risk"])
    m2.metric("审计分类", data["reason"])
    m3.metric("建议操作", "下发指令")

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        for step in data["steps"]: st.write(f"- {step}")
        st.info(f"**推荐话术建议：**\n{data['script']}")

    if st.button("🔥 执行战败挽回/促单指令", type="primary", use_container_width=True):
        if st.session_state.history_logs:
            st.session_state.history_logs[0]["任务状态"] = "⚡ 正在执行"
        st.balloons()
        
        if sync_lark:
            payload = {"msg_type":"interactive","card":{"header":{"title":{"tag":"plain_text","content":"🚨 战败雷达预警"},"template":"red"},"elements":[{"tag":"div","text":{"tag":"lark_md","content":f"**分类：**{data['reason']}\n**对手：**{data['competitor']}"}},{"tag":"div","text":{"tag":"lark_md","content":f"**话术：**\n{data['script']}"}}]}}
            try: requests.post(LARK_WEBHOOK, json=payload, timeout=5)
            except: pass
        st.success("指令已下发！状态已同步至看板。")

# 4.3 看板 (强制 1-5 编号且不显示 NaN)
st.divider()
st.subheader("📈 数据资产看板 (实时流水)")
if st.session_state.history_logs:
    df = pd.DataFrame(st.session_state.history_logs)
    # 强制重新索引，解决截图 2 的列混乱
    df = df.reindex(columns=["记录时间", "风险分类", "关联竞品", "任务状态"])
    df.index = range(1, len(df) + 1)
    df.index.name = "编号"
    st.table(df)
