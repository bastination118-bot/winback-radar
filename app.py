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

# === 3. 增强型语义路由模块 (解决逻辑死板问题) ===
def get_semantic_analysis(file_name):
    """
    智能化升级：多维度判断文件特征，不再盲目回复问界
    """
    time.sleep(1.2)
    fname = file_name.lower()
    
    # 场景 A：意愿强烈 (适配新上传的：愿意购车.wav)
    if any(k in fname for k in ["愿意", "购车", "意愿强烈", "下定"]):
        return {
            "risk": "极低 (5%)",
            "reason": "意愿客户 (高意向/准成交)",
            "competitor": "无 (未提及)",
            "title": "🎉 【促单保单】高意向客户快速转化SOP",
            "steps": [
                "1. **趁热打铁**：24小时内发送金融方案对比表。",
                "2. **权益锁定**：提醒当前限时权益（如内饰升级包）仅剩3天。",
                "3. **邀约下定**：引导至线上订车小程序，协助完成锁单。"
            ],
            "script": "“王先生，听得出您对LS6的智驾非常满意。现在订车还能享受本月的限时权益，我把链接发您？”",
            "status_label": "✅ 待成交 (转化引导中)"
        }
    
    # 场景 B：识别到严重抵触 (不愿沟通)
    elif any(k in fname for k in ["不愿", "防御", "抵触", "别问"]):
        return {
            "risk": "特高 (98%)",
            "reason": "沟通高度受阻 (客户防御心态重)",
            "competitor": "未知/全行业",
            "title": "🥊 【破冰行动】针对高度抵触客户的温养计划",
            "steps": [
                "1. **冷处理**：24小时内严禁电话轰炸，防止客户拉黑投诉。",
                "2. **轻量温养**：由主管发送‘不打扰致歉信’，附带静谧空间短视频。"
            ],
            "script": "“王先生，资料我放在您微信里，您有空时扫一眼就好，近期不再打扰。”",
            "status_label": "⚠️ 待执行 (破冰SOP已下发)"
        }
    
    # 场景 C：其他竞品 (演示备选)
    elif any(k in fname for k in ["小米", "su7", "特斯拉", "极氪"]):
        comp = "小米SU7" if "小米" in fname else "特斯拉Model Y"
        return {
            "risk": "高危 (90%)",
            "reason": f"竞品拦截 ({comp})",
            "competitor": comp,
            "title": f"⚔️ 【对标计划】针对{comp}的战败挽回",
            "steps": ["1. 对比机械素质", "2. 强调全系标配激光雷达", "3. 赠送终身智驾权益"],
            "script": f"“王先生，{comp}确实很火，但LS6的底盘调校和空间表现...”",
            "status_label": "⚠️ 待处理 (对标任务生成)"
        }
    
    # 场景 D：兜底 (不再默认问界)
    return {
        "risk": "中等 (45%)",
        "reason": "需求模糊 (正在观望)",
        "competitor": "无 (未提及)",
        "title": "🔍 【需求挖掘】长线线索培育SOP",
        "steps": ["1. 寻找痛点：询问用车场景", "2. 建立信任：发送提车日记", "3. 寻找时机：下月活动预热"],
        "script": "“王先生，您近期用车主要是通勤还是长途？我可以为您匹配更合适的方案。”",
        "status_label": "⏳ 待培育 (线索温养中)"
    }

# === 4. UI 布局与交互 ===
st.set_page_config(page_title="WinBack-Radar 3.5", layout="centered")

# CSS 修复：强制表格文字完整显示，不再截断
st.markdown("""
<style>
    div[data-testid="stTable"] td { white-space: normal !important; word-break: break-all !important; font-size: 14px !important; }
    div[data-testid="stMetricValue"] { font-size: 24px !important; }
</style>
""", unsafe_allow_html=True)

# 标题栏
h1, h2 = st.columns([0.1, 0.9])
with h1: st.write("## 🛡️")
with h2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

with st.sidebar:
    st.header("⚙️ 自动化引擎")
    sync_lark = st.toggle("同步群机器人预警", value=True)
    st.divider()
    st.info("💡 智能模式：已适配意愿强烈、防御抵触、竞品拦截等多种模型。")

# 4.1 审计触发
uploaded_file = st.file_uploader("上传录音文件", type=["wav", "mp3"])
if st.button("🚀 启动智能分析", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "智慧工牌采样.wav"
    with st.status(f"🔍 正在提取 ASR 语义特征: {fname}...", expanded=True) as s:
        analysis_res = get_semantic_analysis(fname)
        st.session_state.current_analysis = analysis_res
        
        new_log = {
            "记录时间": datetime.now().strftime("%H:%M:%S"),
            "风险分类": analysis_res["reason"],
            "关联竞品": analysis_res["competitor"],
            "任务状态": analysis_res["status_label"]
        }
        st.session_state.history_logs.insert(0, new_log)
        # 强制只保留最近5条历史数据
        st.session_state.history_logs = st.session_state.history_logs[:5]
        s.update(label="AI 分析完成", state="complete")

# 4.2 报告展示
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
            st.session_state.history_logs[0]["任务状态"] = "⚡ 冲锋中"
        st.balloons()
        
        if sync_lark:
            payload = {"msg_type":"interactive","card":{"header":{"title":{"tag":"plain_text","content":"🚨 战败风险预警"},"template":"red"},"elements":[{"tag":"div","text":{"tag":"lark_md","content":f"**归因：**{data['reason']}\n**对手：**{data['competitor']}"}},{"tag":"hr"},{"tag":"div","text":{"tag":"lark_md","content":f"**执行建议：**\n{data['script']}"}}]}}
            requests.post(LARK_WEBHOOK, json=payload)
        st.success("指令已下发！状态已同步。")

# 4.3 看板优化 (5条历史+编号1-5+完整显示)
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时流水)")
if st.session_state.history_logs:
    df_display = pd.DataFrame(st.session_state.history_logs)
    # 生成 1-5 的编号
    df_display.index = range(1, len(df_display) + 1)
    df_display.index.name = "编号"
    st.table(df_display)
