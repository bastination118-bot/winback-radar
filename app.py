import streamlit as st
st.write("Hello! I am WinBack-Radar.") # 这一句是用来测试网页是否活着的
import time
import requests
from datetime import datetime

# === 1. 基础配置 ===
# 请手动填入你的 Webhook，演示前确认包含关键词“战败”
LARK_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx" 
BITABLE_INFO = {
    "app_token": "Fgv2wICOMiCnl9kClcgcRkvSnkh",
    "table_id": "tblsp2CB2ljwGXY7"
}

# === 2. 核心逻辑：执行路径生成器 ===
def get_rescue_plan(competitor):
    return {
        "歸因": f"遭竞品【{competitor}】价格策略拦截",
        "路径": [
            {"阶段": "1. 立即响应", "行动": "30分钟内由内训师陪同销售回访，确认客户对竞品的真实犹豫点。"},
            {"阶段": "2. 价值重塑", "行动": f"发送智己LS6对比{competitor}的‘全系标配激光雷达’差异表，突显智驾代差。"},
            {"阶段": "3. 诱饵锁定", "行动": "申请专项‘对比试驾礼’，以5000元限时补贴为由邀约二次返店。"}
        ],
        "话术": f"“王先生，关于您下午看的{competitor}，我刚才帮您做了对比，LS6在智驾算法上领先一个代际，这关乎长期安全...”"
    }

# === 3. UI 页面设计 ===
st.set_page_config(page_title="WinBack-Radar 3.0", layout="wide")

# 自定义 CSS 让页面更专业
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_stdio=True)

# 顶部标题栏
st.title("🛡️ 战败雷达 (WinBack-Radar) 模拟器 v3.0")
st.caption("基于飞书 OpenClaw & 智己销售赋能文档 | 已开启数据脱敏模式")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 自动化配置")
    sync_lark = st.toggle("同步触发飞书任务卡片", value=True)
    sync_bitable = st.toggle("写入多维表格资产", value=True)
    st.divider()
    st.info("💡 3.11 演示模式：点击下方按钮模拟工牌音频录入。")

# 第一行：数据输入与审计状态
col_input, col_status = st.columns([1, 2])

with col_input:
    st.subheader("📥 音频输入")
    uploaded_file = st.file_uploader("上传工牌录音 (.mp3, .wav)", type=["mp3", "wav"])
    test_btn = st.button("🚀 使用模拟样本进行审计", use_container_width=True)

if test_btn or uploaded_file:
    with col_status:
        with st.status("🔍 AI 正在进行语义审计...", expanded=True) as status:
            time.sleep(1)
            st.write("已提取关键词：[问界M7], [配置对比], [价格犹豫]")
            time.sleep(1)
            st.write("正在检索《竞品分析》及《售前路径》...")
            time.sleep(1)
            status.update(label="审计完成！已生成挽回任务", state="complete")

    st.divider()

    # 第二行：仪表盘数据展示
    plan = get_rescue_plan("问界M7")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("风险等级", "高危 (92%)", delta="需立即干预")
    with m_col2:
        st.metric("战败归因", "竞品拦截", delta="价格/配置异议", delta_color="inverse")
    with m_col3:
        st.metric("建议响应时间", "30分钟内")

    # 第三行：核心挽回任务书
    st.subheader("📋 战败挽回执行任务书")
    
    t_col1, t_col2 = st.columns([1.5, 1])
    
    with t_col1:
        st.write("#### **第一阶段：执行路径**")
        for item in plan['path']:
            with st.expander(f"📌 {item['阶段']}", expanded=True):
                st.write(item['行动'])
    
    with t_col2:
        st.write("#### **金牌挽回话术**")
        st.info(plan['话术'])
        
        if st.button("✅ 确认生成并同步任务"):
            with st.spinner("正在同步至飞书生态..."):
                time.sleep(1.5)
                # 提示成功
                st.success("🎉 同步成功！")
                st.toast(f"已存入 Bitable: {BITABLE_INFO['table_id']}")
                st.balloons()
                
                # 如果填了 Webhook，这里可以加入发送逻辑
                # requests.post(LARK_WEBHOOK, json=...)

# 底部数据看板预览
st.divider()
st.subheader("📈 数据资产看板 (模拟同步效果)")
mock_data = {
    "时间": [datetime.now().strftime("%H:%M")],
    "销售员": ["销售 A (脱敏)"],
    "关联竞品": ["问界M7"],
    "状态": ["已下派任务"]
}
st.table(mock_data)
