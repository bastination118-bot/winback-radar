import streamlit as st
st.write("Hello! I am WinBack-Radar.") # 这一句是用来测试网页是否活着的
import streamlit as st
import requests
import json
import time
from datetime import datetime

# === 基础配置 ===
FEISHU_APP_TOKEN = "Fgv2wICOMiCnl9kClcgcRkvSnkh"  # 你的多维表格 Token
FEISHU_TABLE_ID = "tblsp2CB2ljwGXY7&view=vewRNwgk1o" # [需填入] 浏览器地址栏 table= 后面的部分
LARK_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89" # [需填入] 你的飞书群机器人Webhook
# === 新增：挽回计划逻辑库 ===
def get_rescue_mission(competitor):
    return {
        "title": f"【紧急】针对{competitor}的战败挽回任务",
        "steps": [
            f"1. **立即响应**：30分钟内由内训师陪同销售拨打挽回电话，确认客户对{competitor}的犹豫点。",
            "2. **价值重塑**：发送智己LS6对比视频，强调智驾全系标配，而竞品需选装。",
            "3. **邀约返店**：告知‘战败客户专项补贴’仅剩3名，锁定二次到店意向。"
        ],
        "script": f"“王先生，关于您看的{competitor}，我帮您做了深度对比，LS6在底盘安全上领先一个代际...”"
    }

# === 模拟业务逻辑：基于文档的话术库 ===
KNOWLEDGE_BASE = {
    "问界M7": "重点强调智己LS6的‘全画幅数字驾舱’与‘声纹分离技术’，对比M7的内饰风格，突显LS6的年轻化与科技感。利用FAB法则：Feature-一体式屏，Advantage-视野无盲区，Benefit-驾驶更安全。",
    "理想L6": "对标其智驾方案。智己LS6全系配备激光雷达+英伟达Orin X芯片，强调‘城市NOA’的开通速度与算法领先性，而不只是‘沙发大电视’。",
    "价格异议": "执行《售前路径》中的‘风险逆转’逻辑：告知目前的金融贴息政策及‘保价协议’，拆解每日用车成本仅需一杯咖啡钱。"
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
    # 模拟发送（若未配置Webhook则打印）
    if "xxxx" not in LARK_WEBHOOK_URL:
        return requests.post(LARK_WEBHOOK_URL, json=card_content)
    return None

# === 核心函数：同步至多维表格 ===
def sync_to_bitable(data):
    # 此处逻辑需配合飞书自建应用的 tenant_access_token 调用，演示版做逻辑模拟
    st.toast(f"✅ 数据已同步至多维表格: {FEISHU_APP_TOKEN}")

# === Streamlit 网页设计 ===
st.set_page_config(page_title="WinBack-Radar 模拟器", layout="centered")

st.title("🛡️ 战败雷达 (WinBack-Radar) 模拟器")
st.caption("基于飞书 OpenClaw & 智己 LS6 销售赋能文档驱动")

with st.sidebar:
    st.header("⚙️ 推送配置")
    sync_lark = st.toggle("同步触发飞书卡片", value=True)
    sync_bitable = st.toggle("自动写入多维表格", value=True)
    st.info("配置生效中：3.11 演示模式已开启")

# 1. 上传区
uploaded_file = st.file_uploader("上传智慧工牌录音文件 (.mp3, .wav)", type=["mp3", "wav"])

# 模拟按钮（防止没有录音文件时的测试）
if st.button("使用模拟 ASR 样本进行测试") or uploaded_file:
    
    # 模拟 ASR 识别过程
    with st.status("🔍 AI 正在进行语义审计...", expanded=True) as status:
        time.sleep(1)
        st.write("转写文本：*‘你们的智己LS6不错，但我下午约了问界M7的试驾，那边优惠好像更大...’*")
        time.sleep(1)
        st.write("检测到敏感词：[问界M7], [优惠], [下午约了]")
        time.sleep(1)
        st.write("正在检索《竞品分析》及《售前路径》...")
        status.update(label="分析完成！", state="complete", expanded=False)

# 2. 结果分析展示
    res_data = {
        "pain_point": "客户存在价格异议，且正在对比竞品问界M7的优惠力度。",
        "competitor": "问界M7",
        "script": KNOWLEDGE_BASE["问界M7"]
    }

    st.subheader("📊 AI 分析报告")
    col1, col2 = st.columns(2)
    col1.metric("风险等级", "高危 (85%)", delta="需立即干预")
    col2.metric("战败归因", "竞品拦截")

    st.info(f"**建议挽回话术：**\n\n{res_data['script']}")

    # 3. 触发联动
    if sync_lark:
        send_feishu_card(res_data)
        st.success("飞书卡片已推送至店长端！")
    
    if sync_bitable:
        sync_to_bitable(res_data)

# === 底部看板预览 ===
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时同步)")
st.caption("最近 5 条抢救任务记录")
mock_data = {
    "时间": [datetime.now().strftime("%H:%M:%S")],
    "销售": ["张三"],
    "原因": ["竞品拦截"],
    "状态": ["待抢救"]
}
st.table(mock_data))
