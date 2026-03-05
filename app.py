import streamlit as st
import requests
import json
import time
from datetime import datetime

# === 基础配置 ===
FEISHU_APP_TOKEN = "Fgv2wICOMiCnl9kClcgcRkvSnkh"
# 修正：Table_ID 只保留 ID 部分，去掉 view 后缀
FEISHU_TABLE_ID = "tblsp2CB2ljwGXY7" 
LARK_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89"

# === 模拟业务逻辑：基于文档的话术库 ===
KNOWLEDGE_BASE = {
    "问界M7": "重点强调智己LS6的‘全画幅数字驾舱’与‘声纹分离技术’，对比M7的内饰风格，突显LS6的年轻化与科技感。利用FAB法则：Feature-一体式屏，Advantage-视野无盲区，Benefit-驾驶更安全。",
    "理想L6": "对标其智驾方案。智己LS6全系配备激光雷达+英伟达Orin X芯片，强调‘城市NOA’的开通速度与算法领先性，而不只是‘沙发大电视’。",
    "价格异议": "执行《售前路径》中的‘风险逆转’逻辑：告知目前的金融贴息政策及‘保价协议’，拆解每日用车成本仅需一杯咖啡钱。"
}

# === 逻辑：挽回计划生成器 ===
def get_rescue_mission(competitor):
    return {
        "title": f"【紧急】针对{competitor}的战败挽回任务",
        "steps": [
            f"1. **立即响应**：30分钟内由内训师陪同销售拨打挽回电话，确认客户对{competitor}的犹豫点。",
            "2. **价值重塑**：发送智己LS6对比视频，强调智驾全系标配，而竞品需选装。",
            "3. **邀约返店**：告知‘战败客户专项补贴’仅剩3名，锁定二次到店意向。"
        ],
        "script_short": f"“王先生，关于您看的{competitor}，我帮您做了深度对比，LS6在底盘安全上领先一个代际...”"
    }

# === 核心函数：发送飞书卡片 ===
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
    try:
        requests.post(LARK_WEBHOOK_URL, json=card_content)
    except:
        pass

def sync_to_bitable(data):
    st.toast(f"✅ 数据已加密同步至多维表格资产库")

# === Streamlit 网页设计 ===
st.set_page_config(page_title="WinBack-Radar 模拟器", layout="centered")

st.title("🛡️ 战败雷达 (WinBack-Radar) 模拟器")
st.caption("基于飞书 OpenClaw & 智己 LS6 销售赋能文档驱动 | 演示版 v3.1")

with st.sidebar:
    st.header("⚙️ 推送配置")
    sync_lark = st.toggle("同步触发飞书卡片", value=True)
    sync_bitable = st.toggle("自动写入多维表格", value=True)
    st.info("状态：3.11 演示模式已开启")

# 1. 上传区
uploaded_file = st.file_uploader("上传智慧工牌录音文件 (.mp3, .wav)", type=["mp3", "wav"])

# 初始化状态
if "analysed" not in st.session_state:
    st.session_state.analysed = False

if st.button("🚀 使用模拟样本进行测试") or uploaded_file:
    with st.status("🔍 AI 正在进行语义审计...", expanded=True) as status:
        time.sleep(1)
        st.write("转写文本：*‘你们的智己LS6不错，但我下午约了问界M7的试驾，那边优惠好像更大...’*")
        time.sleep(1)
        st.write("检测到敏感词：[问界M7], [优惠], [下午约了]")
        time.sleep(1)
        st.write("正在检索《竞品分析》及《售前路径》...")
        status.update(label="分析完成！已生成挽回执行路径", state="complete", expanded=False)
    st.session_state.analysed = True

# 2. 结果展示区
if st.session_state.analysed:
    res_data = {
        "pain_point": "客户存在价格异议，且正在对比竞品问界M7的优惠力度。",
        "competitor": "问界M7",
        "script": KNOWLEDGE_BASE["问界M7"]
    }
    # 生成挽回计划
    mission = get_rescue_mission(res_data["competitor"])

    st.subheader("📊 AI 审计报告")
    col1, col2 = st.columns(2)
    col1.metric("风险等级", "高危 (92%)", delta="需立即干预")
    col2.metric("战败归因", "竞品拦截 (问界M7)")

    # 挽回计划展示 (新增功能体现)
    with st.expander("📋 战败挽回执行任务书 (SOP)", expanded=True):
        st.markdown(f"#### {mission['title']}")
        for step in mission['steps']:
            st.write(s = step)
        st.info(f"**建议话术：** {mission['script_short']}")

    if st.button("✅ 确认执行并推送飞书"):
        if sync_lark:
            send_feishu_card(res_data)
            st.success("飞书卡片已推送至店长端！")
        if sync_bitable:
            sync_to_bitable(res_data)
        st.balloons()

# === 3. 底部看板预览 (增加任务书体现) ===
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时同步)")
mock_data = {
    "记录时间": [datetime.now().strftime("%H:%M:%S")],
    "风险分类": ["竞品拦截"],
    "关联竞品": ["问界M7"],
    "挽回任务状态": ["⚠️ 待致电 (任务书已生成)"]
}
st.table(mock_data)
