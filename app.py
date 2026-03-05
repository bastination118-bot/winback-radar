import streamlit as st
import requests
import json
import time
from datetime import datetime

# === 1. 基础配置 ===
FEISHU_APP_TOKEN = "Fgv2wICOMiCnl9kClcgcRkvSnkh"
FEISHU_TABLE_ID = "tblsp2CB2ljwGXY7" 
LARK_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89"

# === 2. 状态初始化 (确保多次测试数据不丢失) ===
if "history_logs" not in st.session_state:
    st.session_state.history_logs = []
if "analysed" not in st.session_state:
    st.session_state.analysed = False

# === 3. 核心逻辑库 ===
def get_rescue_mission(competitor):
    return {
        "title": f"⚔️ 战败反击：针对{competitor}的挽回行动",
        "steps": [
            f"1. **闪电回访**：30分钟内内训师介入，锁定客户对{competitor}的真实异议点。",
            f"2. **火力压制**：发送LS6‘全系标配激光雷达’对比海报，打击竞品选装痛点。",
            "3. **终极邀约**：下放‘战败专享5000元补贴’，强力钩子引导二次到店。"
        ],
        "script": f"“王先生，我看您还在纠结{competitor}，但在智驾冗余和底盘安全上，LS6是真正的代际领先...”"
    }

def send_feishu_card(data):
    # 此处构造卡片 JSON 并发送
    try: requests.post(LARK_WEBHOOK_URL, json={"msg_type": "text", "content": {"text": f"🚨 战败预警：发现竞品 {data['competitor']} 拦截，挽回任务已下发！"}})
    except: pass

# === 4. UI 页面设计 ===
st.set_page_config(page_title="WinBack-Radar 3.0", layout="centered")

# 标题行优化
title_col1, title_col2 = st.columns([0.15, 0.85])
with title_col1:
    st.write("## 🛡️")
with title_col2:
    st.write("## 战败雷达 (WinBack-Radar) 数字化看板")

st.caption("🔒 数据审计合规模式 | 飞书多维表格 Bitable 资产同步中")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 自动化引擎")
    sync_lark = st.toggle("同步群机器人预警", value=True)
    sync_bitable = st.toggle("数据自动入库 Bitable", value=True)
    st.divider()
    st.warning("3.11 演示专用：自动模拟智慧工牌 ASR 语义分析")

# 审计触发区
uploaded_file = st.file_uploader("上传录音文件", type=["mp3", "wav"])
if st.button("🚀 启动 AI 实时审计样本", use_container_width=True) or uploaded_file:
    with st.status("🔍 正在检索语义特征...", expanded=True) as status:
        time.sleep(0.8)
        st.write("📡 转写文本：*‘那边问界M7优惠更大...’*")
        time.sleep(0.8)
        st.write("🎯 匹配策略：[智驾代差], [限时专项补贴]")
        status.update(label="审计完成！任务书已生成", state="complete", expanded=False)
    
    st.session_state.analysed = True
    # 自动生成一条新记录存入 Session
    new_record = {
        "记录时间": datetime.now().strftime("%H:%M:%S"),
        "风险分类": "竞品拦截",
        "关联竞品": "问界M7",
        "挽回任务状态": "⚡ 冲锋执行中"
    }
    st.session_state.history_logs.insert(0, new_record)

# 分析结果区
if st.session_state.analysed:
    mission = get_rescue_mission("问界M7")
    
    st.subheader("📋 战败挽回执行任务书")
    with st.container(border=True):
        st.markdown(f"### {mission['title']}")
        for step in mission['steps']:
            st.write(step)
        st.info(f"**建议话术建议：** {mission['script']}")

    if st.button("🔥 发起冲锋：同步任务至多维表格", type="primary", use_container_width=True):
        with st.spinner("正在将战斗指令下发至飞书生态..."):
            time.sleep(1.2)
            if sync_lark: send_feishu_card({"competitor": "问界M7"})
            st.success("✅ 任务已同步！店长端已接收战败预警通知。")
            st.snow() # 换成冷峻的雪花特效，更有“战场肃杀”感

# === 5. 底部看板预览 (多记录支持) ===
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时流水)")
if st.session_state.history_logs:
    st.table(st.session_state.history_logs)
else:
    st.info("暂无审计记录，请点击上方按钮开始测试。")

st.caption("提示：演示现场刷新页面会清空内存数据。建议连续点击测试按钮展示多条记录。")
