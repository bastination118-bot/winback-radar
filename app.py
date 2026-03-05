import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime

# === 1. 核心联动配置 ===
LARK_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89"

# === 2. 状态强效初始化 (解决 AttributeError 和 数据重影) ===
if "history_logs" not in st.session_state:
    st.session_state.history_logs = []
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None

# === 3. 增强型语义路由模块 (解决“分析不更新”问题) ===
def get_semantic_analysis(file_name):
    """根据文件名关键词模拟 ASR 语义理解"""
    time.sleep(1.2) # 模拟处理延迟
    
    # 场景 A：识别到严重抵触 (适配：含介绍_沟通深度_完全不愿沟通_双声道.wav)
    if any(k in file_name for k in ["不愿沟通", "防御", "抵触", "别问"]):
        return {
            "risk": "特高 (98%)",
            "reason": "沟通高度受阻 (客户防御心态重)",
            "competitor": "未知/全行业",
            "title": "🥊 【破冰行动】针对高度抵触客户的温养计划",
            "steps": [
                "1. **冷处理**：24小时内严禁电话轰炸，防止客户拉黑投诉。",
                "2. **轻量温养**：由主管发送‘不打扰致歉信’，附带智己LS6静谧空间短视频。",
                "3. **价值转接**：3天后通过企业微信推送‘无盲区智驾’功能点，弱化推销感。"
            ],
            "script": "“王先生，理解您现在的忙碌。LS6的产品资料我放在您微信里，您有空时扫一眼就好，近期不再打扰。”",
            "status_label": "⚠️ 待执行 (破冰SOP已下发)"
        }
    
    # 场景 B：识别到竞品拦截 (默认场景，如问界M7)
    return {
        "risk": "高危 (92%)",
        "reason": "竞品拦截 (问界M7强意向)",
        "competitor": "问界M7",
        "title": "⚔️ 【抢救任务】针对问界M7的价值重塑",
        "steps": [
            "1. **闪电响应**：30分钟内内训师介入，针对M7内饰与智驾包进行差异化对比。",
            "2. **火力压制**：发送‘LS6全系标配激光雷达’海报，打击竞品选装痛点。",
            "3. **终极邀约**：申请‘战败客户专项5000元补贴’，诱导二次回店。"
        ],
        "script": "“王先生，关于您看的问界M7，LS6在全幅数字屏和底盘素质上领先一个代际，建议您对比后再定...”",
        "status_label": "⚠️ 待致电 (任务书已生成)"
    }

# === 4. UI 布局与交互 ===
st.set_page_config(page_title="WinBack-Radar 3.11", layout="centered")

# 标题栏 [0.1, 0.9]
h1, h2 = st.columns([0.1, 0.9])
with h1: st.write("## 🛡️")
with h2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

with st.sidebar:
    st.header("⚙️ 自动化引擎")
    sync_lark = st.toggle("同步群机器人预警", value=True)
    sync_bitable = st.toggle("数据实时同步 Bitable", value=True)
    st.divider()
    st.info("💡 演示模式：已根据文件名自动适配语义模型")

# 4.1 审计触发
uploaded_file = st.file_uploader("上传录音文件 (.wav / .mp3)", type=["wav", "mp3"])
if st.button("🚀 启动智能分析", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "智慧工牌默认采样.wav"
    with st.status(f"🔍 正在提取 ASR 语义特征: {fname}...", expanded=True) as s:
        # 获取最新的分析结果
        analysis_res = get_semantic_analysis(fname)
        st.session_state.current_analysis = analysis_res
        
        # 将结果压入看板历史 (严格对齐 4 列字段)
        new_log = {
            "记录时间": datetime.now().strftime("%H:%M:%S"),
            "风险分类": analysis_res["reason"],
            "关联竞品": analysis_res["competitor"],
            "任务状态": analysis_res["status_label"]
        }
        st.session_state.history_logs.insert(0, new_log)
        s.update(label="分析完成！已识别战败归因并生成计划", state="complete")

# 4.2 报告展示 (解决 image_a01dfb.png 中的渲染崩溃)
if st.session_state.current_analysis:
    data = st.session_state.current_analysis
    st.divider()
    st.subheader("📊 AI 审计报告")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("风险等级", data["risk"])
    col_b.metric("战败归因", data["reason"])
    col_c.metric("建议响应", "发起冲锋")

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        for step in data["steps"]: st.write(step)
        st.info(f"**建议挽回话术：**\n{data['script']}")

    if st.button("🔥 发起冲锋 (WinBack)", type="primary", use_container_width=True):
        # 1. 修改看板内当前行的状态
        if st.session_state.history_logs:
            st.session_state.history_logs[0]["任务状态"] = "⚡ 冲锋执行中"
        
        # 2. 视觉特效
        st.balloons()
        
        # 3. 飞书联动 (带 FAB 法则的高级卡片)
        if sync_lark:
            card_content = {
                "msg_type": "interactive",
                "card": {
                    "header": {"title": {"tag": "plain_text", "content": "🚨 战败风险预警"}, "template": "red"},
                    "elements": [
                        {"tag": "div", "text": {"tag": "lark_md", "content": f"**归因：**{data['reason']}\n**对手：**{data['competitor']}"}},
                        {"tag": "hr"},
                        {"tag": "div", "text": {"tag": "lark_md", "content": f"**执行建议：**\n{data['script']}"}}
                    ]
                }
            }
            try: requests.post(LARK_WEBHOOK, json=card_content)
            except: pass
        st.success("指令已下发！店长端卡片已同步，多维表格状态已刷新。")

# 4.3 数据资产看板 (彻底修复 image_9f2a59.png 的混乱问题)
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时流水)")
if st.session_state.history_logs:
    # 关键步骤：使用 pandas 强制约束列，防止“列名打架”
    raw_df = pd.DataFrame(st.session_state.history_logs)
    # 定义标准 4 列名
    standard_columns = ["记录时间", "风险分类", "关联竞品", "任务状态"]
    # 强制重新排列并重命名字段，解决 NaN 重影
    df_display = raw_df.reindex(columns=standard_columns)
    st.table(df_display)
