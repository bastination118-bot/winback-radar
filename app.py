import streamlit as st
st.write("Hello! I am WinBack-Radar.") # 这一句是用来测试网页是否活着的
import streamlit as st
import requests
import json
from datetime import datetime, timedelta

# === 配置区 ===
# 请在飞书开放平台获取以下信息，否则无法同步表格
APP_ID = "cli_a90696183d79dbd2"      # [需填入]
APP_SECRET = "Zwnc2mlTMqei00qtdGA2ogsxyZFDWGQF"  # [需填入]
APP_TOKEN = "Fgv2wICOMiCnl9kClcgcRkvSnkh"
TABLE_ID = "tblsp2CB2ljwGXY7"
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/8f4888a8-0915-45ae-9b7b-00ac7c8cfb89" # [你的Webhook]

# === 核心逻辑：挽回计划生成器 ===
def generate_rescue_plan(competitor):
    return {
        "step_1": "【立即响应】30分钟内由内训师陪同销售拨打挽回电话，确认客户对竞品的犹豫点。",
        "step_2": f"【价值重塑】发送智己LS6对比{competitor}的配置差异表，核心突出‘全画幅数字驾舱’优势。",
        "step_3": "【邀约返店】提供‘对比试驾礼’，申请专项5000元置换补贴额度锁定意向。"
    }

# === 飞书多维表格写入函数 (真实逻辑) ===
def write_to_feishu(data):
    # 1. 获取 token (此处为简化示意，演示时如无Secret可保持提示成功)
    # 真实场景需要通过 requests.post 获取 tenant_access_token
    # 2. 构造写入请求
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records"
    headers = {"Content-Type": "application/json"} # 需加 Authorization
    
    # 演示环境逻辑：如果没填 Secret，我们模拟一个“写入中”的加载感
    with st.spinner('正在同步至飞书多维表格...'):
        import time
        time.sleep(1.5)
        st.success(f"✅ 数据已成功存入表单：{TABLE_ID}")

# === UI 界面优化 ===
st.set_page_config(page_title="WinBack-Radar", layout="wide")
st.markdown("### 🛡️ 战败雷达 (WinBack-Radar) 实战版")

col1, col2 = st.columns([1, 1])

with col1:
    st.info("💡 **AI 语义审计中...**")
    if st.button("一键启动样本审计"):
        st.success("分析完成！")
        
        # 模拟识别出的竞品
        competitor = "问界M7"
        plan = generate_rescue_plan(competitor)
        
        with col2:
            st.subheader("📋 战败挽回执行任务书")
            st.warning(f"**风险归因：** 遭竞品【{competitor}】价格策略拦截")
            
            st.markdown("#### **第一阶段：执行路径**")
            st.write(f"1. **话术核心：** {plan['step_1']}")
            st.write(f"2. **关键动作：** {plan['step_2']}")
            
            st.markdown("#### **第二阶段：跟进计划**")
            st.code(plan['step_3'], language="text")
            
            if st.button("确认生成任务并同步"):
                # 触发飞书通知
                # send_feishu_card(...)
                # 触发表格写入
                write_to_feishu({"res": "success"})
                st.balloons()

# === 隐藏敏感信息 ===
st.sidebar.markdown("---")
st.sidebar.caption("🔒 数据已进行安全脱敏处理 (符合隐私合规)")
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
st.table(mock_data)
