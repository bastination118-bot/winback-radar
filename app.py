import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime

# === 1. 配置与初始化 ===
LARK_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89"

if "history_logs" not in st.session_state:
    st.session_state.history_logs = []
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None

# === 2. 增强型语义路由 (拒绝假 AI) ===
def get_semantic_analysis(file_name):
    """
    智能化升级：识别文件关键词，动态生成报告内容
    """
    time.sleep(1.2)
    fname = file_name.lower()
    
    # 场景 1：意愿强烈 (针对：愿意购车.wav)
    if any(k in fname for k in ["愿意", "购车", "意愿", "下定"]):
        return {
            "risk": "极低 (5%)",
            "reason": "意愿客户 (高意向/准成交)",
            "competitor": "无 (未提及)",
            "title": "🎉 【促单保单】高意向客户快速转化SOP",
            "steps": ["1. **权益锁定**：提醒限时优惠", "2. **金融方案**：发送月供对比", "3. **协助下定**：引导小程序"],
            "script": "“王先生，听得出您对智驾非常满意。现在订车能锁定本月5000元权益，我把链接发您？”",
            "status_label": "✅ 待成交 (转化中)"
        }
    # 场景 2：严重抵触 (针对：明显抵触.wav)
    elif any(k in fname for k in ["不愿", "抵触", "防御", "别问"]):
        return {
            "risk": "特高 (98%)",
            "reason": "沟通受阻 (客户防御心态重)",
            "competitor": "未知/全行业",
            "title": "🥊 【破冰行动】针对高抵触客户温养",
            "steps": ["1. **冷处理**：严禁继续拨打", "2. **轻介入**：发送产品静谧视频"],
            "script": "“王先生，资料我放您微信，您有空看一眼就好，近期不再打扰。”",
            "status_label": "⚠️ 待温养 (破冰中)"
        }
    # 场景 3：兜底 (观望中)
    return {
        "risk": "中等 (45%)",
        "reason": "需求模糊 (正在观望)",
        "competitor": "无 (未提及)",
        "title": "🔍 【需求挖掘】长线培育SOP",
        "steps": ["1. 寻找痛点", "2. 发送提车日记"],
        "script": "“王先生，您用车主要是通勤还是长途？我可以为您匹配更合适的方案。”",
        "status_label": "⏳ 待培育"
    }

# === 3. UI 布局与样式修复 ===
st.set_page_config(page_title="WinBack-Radar 3.6", layout="centered")

# CSS 深度修复：解决字体截断和表格错乱
st.markdown("""
<style>
    /* 修复字体显示不全 */
    .stMetric label, .stMetric div { overflow: visible !important; white-space: nowrap !important; }
    /* 强制表格样式 */
    div[data-testid="stTable"] { border-radius: 10px; overflow: hidden; }
    div[data-testid="stTable"] td { white-space: normal !important; word-break: break-all !important; }
</style>
""", unsafe_allow_html=True)

h1, h2 = st.columns([0.1, 0.9])
with h1: st.write("## 🛡️")
with h2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

# 4.1 审计触发
uploaded_file = st.file_uploader("上传录音文件", type=["wav", "mp3"])
if st.button("🚀 启动智能分析", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "智慧工牌采样.wav"
    with st.status(f"🔍 语义审计中: {fname}...") as s:
        res = get_semantic_analysis(fname)
        st.session_state.current_analysis = res
        
        # 核心：存入时只保留标准的 4 个 Key，防止多列并排
        new_entry = {
            "记录时间": datetime.now().strftime("%H:%M:%S"),
            "风险分类": res["reason"],
            "关联竞品": res["competitor"],
            "任务状态": res["status_label"]
        }
        st.session_state.history_logs.insert(0, new_entry)
        # 强制只留 5 行
        st.session_state.history_logs = st.session_state.history_logs[:5]
        s.update(label="AI 分析完成", state="complete")

# 4.2 报告展示 (修复显示不全)
if st.session_state.current_analysis:
    data = st.session_state.current_analysis
    st.divider()
    st.subheader("📊 AI 审计报告")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("风险等级", data["risk"])
    col_b.metric("战败归因", data["reason"])
    col_c.metric("建议响应", "执行 SOP")

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        for step in data["steps"]: st.write(step)
        st.info(f"**建议话术：**\n{data['script']}")

    if st.button("🔥 发起冲锋 (WinBack)", type="primary", use_container_width=True):
        if st.session_state.history_logs:
            st.session_state.history_logs[0]["任务状态"] = "⚡ 冲锋执行中"
        st.balloons()
        st.success("指令下发成功！")

# 4.3 看板清洗 (解决截图 2 的 NaN 和错位问题)
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时流水)")
if st.session_state.history_logs:
    # 强制将 List 转为干净的 DataFrame
    raw_df = pd.DataFrame(st.session_state.history_logs)
    
    # 【核心修复】：强制只选取这 4 列，彻底隔离 NaN 和旧数据列
    clean_columns = ["记录时间", "风险分类", "关联竞品", "任务状态"]
    # 如果有的行缺失某些列，自动填补“/”，防止错位
    df_display = raw_df.reindex(columns=clean_columns).fillna("/")
    
    # 插入编号列 (1-5)
    df_display.insert(0, "编号", range(1, len(df_display) + 1))
    
    # 去掉 DataFrame 默认索引展示
    st.table(df_display)
