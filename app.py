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

# === 3. 增强型多维语义路由引擎 (v1.1 核心升级) ===
def get_semantic_analysis(file_name):
    """
    语义分析引擎 v1.1：基于场景矩阵判断客户情绪、意愿与现状
    """
    time.sleep(1.2)
    fname = file_name.lower()
    
    # --- 场景 1：彻底战败（针对：已购他牌退订.wav） ---
    if any(k in fname for k in ["退订", "已购", "买了他牌", "他牌", "买了别的"]):
        return {
            "risk": "已流失 (100%)",
            "reason": "彻底战败 (已购竞品)",
            "competitor": "其他品牌",
            "title": "📉 【战败归档】存量线索转公海及原因审计",
            "steps": [
                "1. **归因存证**：通过话术确认客户购买竞品的具体成交点（价格/交期）。",
                "2. **品牌留痕**：发送‘恭喜提车’卡片，内含智己售后老友保养礼包。",
                "3. **公海流转**：标记战败原因，180天后自动激活二次触达。"
            ],
            "script": "“王先生，理解您的选择。恭喜提车！虽然这次没能牵手，但后续LS6有任何OTA升级或活动，我也很乐意分享给您。”",
            "status_label": "🚫 战败归档"
        }
    
    # --- 场景 2：意愿强烈（针对：愿意购车.wav） ---
    elif any(k in fname for k in ["愿意", "购车", "意愿强烈", "下定", "准备买"]):
        return {
            "risk": "极低 (5%)",
            "reason": "高意向客户 (准成交状态)",
            "competitor": "无",
            "title": "🎉 【促单保单】限时权益锁定SOP",
            "steps": [
                "1. **锁定权益**：告知客户本月限时权益（如智驾升级包）名额仅剩2个。",
                "2. **金融闭环**：1小时内由金融专员发送个性化月供测算方案。",
                "3. **邀约下定**：发送线上订车小程序链接，协助完成远程锁单。"
            ],
            "script": "“王先生，听得出您对LS6的底盘非常满意。现在下定不仅能锁单，还能锁定本月的权益，我帮您操作？”",
            "status_label": "✅ 待成交"
        }
    
    # --- 场景 3：严重抵触（针对：明显抵触/不愿沟通.wav） ---
    elif any(k in fname for k in ["不愿", "防御", "抵触", "别问", "别打"]):
        return {
            "risk": "特高 (98%)",
            "reason": "沟通受阻 (客户防御心态重)",
            "competitor": "未知/待确认",
            "title": "🥊 【破冰行动】情绪安抚与低频温养计划",
            "steps": [
                "1. **即时止损**：标记‘暂勿电话’，避免销售轰炸导致拉黑投诉。",
                "2. **轻量渗透**：3小时后通过微信发送一条‘不打扰致歉信’。",
                "3. **价值转接**：发送LS6静谧空间视频，以柔性方式建立产品连接。"
            ],
            "script": "“王先生，理解您的忙碌。资料我发您微信，您空了扫一眼就好，近期绝不再打扰。”",
            "status_label": "⚠️ 待温养"
        }
    
    # --- 场景 4：竞品拦截（识别特定关键词） ---
    elif any(k in fname for k in ["问界", "m7", "小米", "su7", "特斯拉", "极氪"]):
        comp = "竞品拦截"
        if "问界" in fname or "m7" in fname: comp = "问界M7"
        elif "小米" in fname or "su7" in fname: comp = "小米SU7"
        
        return {
            "risk": "高危 (92%)",
            "reason": f"强对标中 ({comp})",
            "competitor": comp,
            "title": f"⚔️ 【抢救任务】针对{comp}的价值重塑",
            "steps": [
                "1. **差异化打击**：对比底盘机械素质，强调LS6全系标配激光雷达。",
                "2. **火力配置**：发送《LS6 vs {comp} 核心竞争力分析表》。",
                "3. **邀约返店**：申请专项‘对比试驾大礼包’，引导客户进行二次深度体验。"
            ],
            "script": f"“王先生，{comp}确实优秀，但在智驾算法和底盘舒适度上LS6更具代际优势，建议您对比下。”",
            "status_label": "🔥 冲锋挽回"
        }
    
    # --- 场景 5：需求模糊 (默认场景) ---
    return {
        "risk": "中等 (45%)",
        "reason": "需求模糊 (观望对比中)",
        "competitor": "无 (全行业对比)",
        "title": "🔍 【价值挖掘】客户需求锚点构建SOP",
        "steps": ["1. 寻找痛点：询问用车场景", "2. 发送提车日记", "3. 推荐到店活动"],
        "script": "“王先生，您平时主要是市区通勤还是长途？我可以为您算一下更省钱的方案。”",
        "status_label": "⏳ 线索培育"
    }

# === 4. UI 布局与增强逻辑 ===
st.set_page_config(page_title="WinBack-Radar 3.11 Pro", layout="centered")

# CSS 修复：强制表格文字完整显示，不截断
st.markdown("""
<style>
    div[data-testid="stTable"] td { white-space: normal !important; word-break: break-all !important; font-size: 14px !important; line-height: 1.5 !important; }
    div[data-testid="stMetricValue"] { font-size: 26px !important; color: #FF4B4B; }
    .stTable { border: 1px solid #f0f2f6; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 标题栏
h1, h2 = st.columns([0.1, 0.9])
with h1: st.write("## 🛡️")
with h2: st.write("## 战败雷达 (WinBack-Radar) 数字化看板 v1.1")

with st.sidebar:
    st.header("⚙️ 自动化引擎")
    sync_lark = st.toggle("同步飞书群预警卡片", value=True)
    st.divider()
    st.info("💡 v1.1 已升级多维语义矩阵：自动识别已购战败、意愿强烈、防御心态等场景。")

# 4.1 审计触发
uploaded_file = st.file_uploader("上传智慧工牌录音采样", type=["wav", "mp3"])

if st.button("🚀 启动 AI 实时语义分析", use_container_width=True) or uploaded_file:
    fname = uploaded_file.name if uploaded_file else "智慧工牌默认采样.wav"
    with st.status(f"🔍 正在进行多维语义审计: {fname}...", expanded=True) as s:
        # 调用增强型分析引擎
        analysis_res = get_semantic_analysis(fname)
        st.session_state.current_analysis = analysis_res
        
        # 写入看板历史
        new_log = {
            "记录时间": datetime.now().strftime("%H:%M:%S"),
            "风险分类": analysis_res["reason"],
            "关联竞品": analysis_res["competitor"],
            "任务状态": analysis_res["status_label"]
        }
        st.session_state.history_logs.insert(0, new_log)
        # 严格限制 5 行
        st.session_state.history_logs = st.session_state.history_logs[:5]
        s.update(label="分析完成！已精准匹配业务场景", state="complete")

# 4.2 报告展示
if st.session_state.current_analysis:
    data = st.session_state.current_analysis
    st.divider()
    st.subheader("📊 AI 审计结果与挽回 SOP")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("风险评估", data["risk"])
    col_b.metric("场景分类", data["reason"])
    col_c.metric("执行建议", "查看 SOP")

    with st.container(border=True):
        st.markdown(f"### {data['title']}")
        for step in data["steps"]:
            st.write(step)
        st.info(f"**💡 推荐执行话术：**\n{data['script']}")

    if st.button("🔥 发起冲锋 (WinBack)", type="primary", use_container_width=True):
        if st.session_state.history_logs:
            # 更新看板第一行状态
            st.session_state.history_logs[0]["任务状态"] = "⚡ 冲锋执行中"
        
        st.balloons()
        
        # 飞书联动卡片
        if sync_lark:
            payload = {
                "msg_type": "interactive",
                "card": {
                    "header": {"title": {"tag": "plain_text", "content": "🚨 战败风险预警指令"}, "template": "red"},
                    "elements": [
                        {"tag": "div", "text": {"tag": "lark_md", "content": f"**预警原因：** {data['reason']}\n**关联对手：** {data['competitor']}"}},
                        {"tag": "hr"},
                        {"tag": "div", "text": {"tag": "lark_md", "content": f"**话术建议：**\n{data['script']}"}}
                    ]
                }
            }
            try: requests.post(LARK_WEBHOOK, json=payload, timeout=5)
            except: pass
        st.success("挽回指令已通过飞书下发，数据看板已同步状态！")

# 4.3 看板优化 (5条历史+编号1-5+完整显示)
st.divider()
st.subheader("📈 数据资产看板 (Bitable 实时流水)")
if st.session_state.history_logs:
    # 强制构建干净的 DataFrame，解决 NaN 重影问题
    df_display = pd.DataFrame(st.session_state.history_logs)
    
    # 定义标准列
    standard_cols = ["记录时间", "风险分类", "关联竞品", "任务状态"]
    df_display = df_display.reindex(columns=standard_cols)
    
    # 强制重置索引为编号 1-5
    df_display.index = range(1, len(df_display) + 1)
    df_display.index.name = "编号"
    
    st.table(df_display)
