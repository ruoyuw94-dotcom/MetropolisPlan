import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import folium
from streamlit_folium import st_folium

# ===================== 配置区 =====================
# True=模拟AI输出(比赛演示，不需要API Key)；False=调用真实OpenAI LLM
SIMULATE_LLM = True
OPENAI_API_KEY = ""  # 填入你的key，SIMULATE_LLM设为False才生效
# ==================================================

# ---------------------- 知识库：来自北都/新田科技城官方文档 ----------------------
knowledge_base = """
# ========== 北部都会区 - 新田科技城 规划知识库 ==========
## 专案背景
新田科技城是北部都会区「创新科技地带」核心项目，包含河套港深创新及科技园，定位打造「南金融、北创科」，与深圳福田科创园区协同发展。整个北部都会区目标提供50万住宅单位、创造50万个就业岗位；新田科技城总开发面积约626公顷，预计提供50000‑54000个住宅单位，人才公寓6400个，就业岗位217000个。
新田科技城提供约300公顷创科用地，总楼面面积可达700万平方米，涵盖研发、中试、先进制造、人才公寓、商业配套。

## 核心规划原则【强制约束，方案必须遵守】
1. 发展与保育并存原则：开发建设不能忽视米埔拉姆萨尔湿地（国际重要湿地）生态保护。
2. 城乡共融：保留原有乡村聚落；邻近乡村地块要降低建筑密度、设置景观缓冲带，保留通风廊、景观视廊。
3. 15分钟生活圈：住宅、创科园区需要配套公共休憩、政府机构社区设施。
4. 海绵城市、蓝绿网络：采用蓄洪设施、活化排水河道，应对极端暴雨、气候变化，实现气候韧性。
5. 阶梯式建筑高度：靠近湿地保育区方向建筑高度逐步递减，保护鸟类飞行廊道。

## 生态保育硬性规范（土地评估最重要依据）
1. 三宝树湿地保育公园：约338公顷，作为新田科技城开发的生态补偿，实现湿地生态功能「无净损失」原则。
2. 必须保护米埔村、米埔陇村鹭鸟林；预留鸟类飞行廊道、野生动物通行廊道；设置非建筑用地(NBA)作生态缓冲。
3. 临近湿地的地块执行阶梯式高度轮廓，由内陆向湿地方向由高往低下降；湿地边缘划设至少35米阔非建筑景观缓冲地带。
4. 部分鱼塘会因发展填平，但政府会透过三宝树湿地公园弥补生态损失；环评报告要求开发不得对拉姆萨尔湿地带来不可接受的生态破坏。
5. 蓝绿网络：串联河道、蓄洪池、休憩用地、湿地，提升生物多样性，同时做防洪调蓄。

## 土地用途与发展参考参数
### 用地配比参考（来自公众参与报告）
1. 高密度方案：住宅45%、创科用地30%，压缩生态缓冲带，适合远离湿地的内陆地块；风险：生态压力高，需要严格管控建筑高度，保留鸟类廊道。
2. 生态优先方案：住宅22%、创科用地15%，大面积连续生态缓冲廊道；适合紧邻三宝树湿地保育公园地块；缺点：住宅、产业供应量下降。
3. 均衡综合方案（政府推荐方向）：住宅约34%、创科用地24%，预留足够生态缓冲空间，平衡房屋供应、创科发展与生态保护。

### 建筑地积比率参考
- 创科用地最高地积比率可达6，但**仅适用于远离湿地及乡村的东南部地块**。
- 邻近湿地、乡村聚落地块，必须降低地积比率，采用低‑中密度开发。

## 交通与基础设施约束
1. 北环主线、北环支线为骨干，连接落马洲、河套创科园；新皇岗口岸重建，强化深港跨境联系。
2. 规划完善行人及单车网络，实现15分钟生活圈。
3. 基建包含区域供冷系统、再造水设施，蓄洪设施，落实智慧绿色韧性城市。

## 社会人文约束
1. 保留乡村式发展地带；邻近村庄的开发，需要设休憩、美化市容地带作缓冲，维持通风廊。
2. 保护区内历史建筑、庙宇、风水树等本地文化资源。
3. 公屋私营房屋参考比例70:30，属于规划假设，实施阶段可以弹性调整。

## 五大评估维度参考标准（对应你网页雷达图5个维度）
1. **生态保育**：与湿地保育区距离、是否预留鸟类/野生动物廊道、非建筑缓冲带面积、是否遵守阶梯式建筑高度、对鱼塘与栖息地影响。
2. **气候韧性**：海绵城市/蓄洪设施布局、蓝绿网络覆盖、极端降雨防洪能力、城市热岛缓解效果。
3. **低碳开发**：绿化覆盖率、建筑开发碳排放、再生能源潜力、区域供冷、绿色出行配套。
4. **社区宜居**：公共休憩空间、GIC政府机构社区设施覆盖、15分钟生活圈可达性、与周边乡村共融设计。
5. **跨境协同**：距离铁路口岸距离、创科用地与河套/深圳科创园的产业联动潜力、人才公寓配套数量。

## 重要限制（AI生成方案禁止违反）
❌ 禁止建议直接占用拉姆萨尔湿地核心区进行开发
❌ 不允许忽略鸟类飞行廊道、非建筑缓冲地带
❌ 邻近湿地地块不可以直接使用最高6倍地积比率
✅ AI输出方案需要写明适合哪一类地块（靠近湿地 / 内陆远离湿地），同时标明风险与缓解措施
"""

# ---------------------- 多国语言词库（✅ 全部key改为普通减号 zh-CN 修复KeyError） ----------------------
lang_dict = {
    "zh-CN": {
        "title_main": "MetropolisPlan AI",
        "subtitle_main": "北部都会区可持续土地规划决策辅助网页平台",
        "sidebar_title": "🧭 MetropolisPlan AI",
        "sidebar_sub": "北部都会区土地规划决策辅助平台",
        "lang_select": "选择语言",
        "nav_home": "🏠 首页",
        "nav_input": "📝 地块参数输入",
        "nav_dashboard": "📊 土地评估仪表板",
        "nav_ai": "💡 AI开发方案建议",
        "nav_map": "🗺️ 空间可视化地图",
        "nav_report": "📄 导出报告",
        "home_intro_title": "专案简介",
        "home_intro": "针对香港北部都会区，为政府规划部门提供**土地可持续评估、AI开发方案生成、空间可视化**一站式决策辅助工具。平衡住宅、创科用地开发与米埔湿地、海岸生态保育，协助达成SDG11可持续城市社区目标。",
        "home_module_title": "三大核心模组",
        "home_module_list": "- ✅ 多维度土地可持续评估\n- ✅ 生成式AI产生多套开发方案建议\n- ✅ 用地布局可视化对比",
        "home_info": "✅ 赛道：Sustainable Northern Metropolis\n✅ 主要SDG：SDG11 可持续城市和社区\n✅ 使用对象：香港规划署 / 北部都会区统筹办事处",
        "home_note": "原型版本：界面框架演示，指标与AI方案可以调用LLM生成，可接入大型语言模型与GIS真实数据",
        "input_title": "📝 地块开发参数登记",
        "input_site_name": "地块名称",
        "input_site_default": "新田示范地块 A",
        "input_area": "地块总面积（公顷）",
        "input_location": "地块所属片区",
        "input_loc_options": ["新田科技城周边", "落马洲", "河套创科园", "流浮山白泥片区"],
        "input_resi_ratio": "住宅用地占比 %",
        "input_tech_ratio": "创科产业用地占比 %",
        "input_buffer": "生态缓冲带预留面积（公顷）",
        "input_warn": "已登记地块：{site}，总面积 {area} 公顷，住宅{resi}%，创科用地{tech}%，生态缓冲带 {buffer} 公顷",
        "input_submit": "提交参数，开始评估",
        "input_success": "✅ 参数提交成功！前往【土地评估仪表板】查看评估结果",
        "dash_title": "📊 多维度土地可持续评估",
        "dash_dim": ["生态保育", "气候韧性", "低碳开发", "社区宜居", "跨境协同"],
        "dash_score_title": "各项指标得分",
        "dash_radar_title": "雷达图可视化",
        "dash_comment_title": "✍️ AI评估解读（模拟输出，可调用LLM）",
        "dash_comment": "> 本地块整体评估表现良好，社区宜居、跨境协同维度得分较高；生态保育得分偏低，主要原因距离湿地保护区较近，建议进一步扩大生态廊道预留面积，降低栖息地破碎化风险。洪涝风险属中等水平，建议增加海绵城市、雨水滞留空间的布局。",
        "ai_title": "💡 生成式AI 三套可选开发方案",
        "ai_btn_run": "🚀 调用LLM生成开发方案（基于官方知识库）",
        "ai_tab1": "方案A｜高密度开发",
        "ai_tab2": "方案B｜生态优先",
        "ai_tab3": "方案C｜均衡综合方案",
        "aiA_title": "方案A：高密度开发（优先住宅+创科用地）",
        "aiA_content": "- 住宅用地占比：45%｜创科用地：30%\n- 生态缓冲带：12公顷\n- ✅ 优点：可提供大量住宅单位，配合新田创科园就业人口的居住需求\n- ⚠️ 风险：生态压力高，需要严格管控建筑范围，减少对周边湿地的干扰",
        "aiB_title": "方案B：生态优先方案",
        "aiB_content": "- 住宅用地占比：22%｜创科用地：15%\n- 生态缓冲带：42公顷，预留连续生态廊道\n- ✅ 优点：大幅降低对米埔湿地、本土生物栖息地的干扰，抵御洪涝能力强\n- ⚠️ 风险：住宅、产业用地供应量减少，土地开发强度较低",
        "aiC_title": "方案C｜均衡综合方案（推荐）",
        "aiC_content": "- 住宅用地占比：34%｜创科用地：24%\n- 生态缓冲带：22公顷\n- ✅ 优点：住宅、产业用地供应充足，同时预留足够生态缓冲空间，各项指标综合最均衡，适合北部都会区新城开发。",
        "map_title": "🗺️ 用地布局可视化（Folium / Leaflet地图）",
        "map_select_plan": "选择查看方案",
        "map_info": "目前检视：{plan} 用地布局示意图",
        "map_legend": "🟫 住宅用地｜🟦 创科产业用地｜🟩 绿地/生态缓冲带｜🟢 湿地保护区",
        "map_note": "> 地图说明：粗略示意边界，仅用于Hackathon原型演示；正式项目接入真实GIS GeoJSON边界文件",
        "report_title": "📄 评估报告导出",
        "report_sub": "AI生成评估报告（中英双语版本）",
        "report_preview": "报告预览",
        "report_download": "下载报告 (txt)",
        "report_filename": "northern_metropolis_land_report.txt",
    },
    "zh-TW": {
        "title_main": "MetropolisPlan AI",
        "subtitle_main": "北部都會區可持續土地規劃決策輔助網頁平台",
        "sidebar_title": "🧭 MetropolisPlan AI",
        "sidebar_sub": "北部都會區土地規劃決策輔助平台",
        "lang_select": "選擇語言",
        "nav_home": "🏠 首頁",
        "nav_input": "📝 地塊參數輸入",
        "nav_dashboard": "📊 土地評估儀表板",
        "nav_ai": "💡 AI開發方案建議",
        "nav_map": "🗺️ 空間可視化地圖",
        "nav_report": "📄 匯出報告",
        "home_intro_title": "專案簡介",
        "home_intro": "針對香港北部都會區，為政府規劃部門提供**土地可持續評估、AI開發方案生成、空間可視化**一站式決策輔助工具。平衡住宅、創科用地開發與米埔濕地、海岸生態保育，協助達成SDG11可持續城市社區目標。",
        "home_module_title": "三大核心模組",
        "home_module_list": "- ✅ 多維度土地可持續評估\n- ✅ 生成式AI產生多套開發方案建議\n- ✅ 用地佈局可視化對比",
        "home_info": "✅ 賽道：Sustainable Northern Metropolis\n✅ 主要SDG：SDG11 可持續城市和社區\n✅ 使用對象：香港規劃署 / 北部都會區統籌辦事處",
        "home_note": "原型版本：介面框架示範，指標與AI方案可呼叫LLM生成，可接入大型語言模型與GIS真實數據",
        "input_title": "📝 地塊開發參數登記",
        "input_site_name": "地塊名稱",
        "input_site_default": "新田示範地塊 A",
        "input_area": "地塊總面積（公頃）",
        "input_location": "地塊所屬片區",
        "input_loc_options": ["新田科技城周邊", "落馬洲", "河套創科園", "流浮山白泥片區"],
        "input_resi_ratio": "住宅用地佔比 %",
        "input_tech_ratio": "創科產業用地佔比 %",
        "input_buffer": "生態緩衝帶預留面積（公頃）",
        "input_warn": "已登記地塊：{site}，總面積 {area} 公頃，住宅{resi}%，創科用地{tech}%，生態緩衝帶 {buffer} 公頃",
        "input_submit": "提交參數，開始評估",
        "input_success": "✅ 參數提交成功！前往【土地評估儀表板】查看評估結果",
        "dash_title": "📊 多維度土地可持續評估",
        "dash_dim": ["生態保育", "氣候韌性", "低碳開發", "社區宜居", "跨境協同"],
        "dash_score_title": "各項指標得分",
        "dash_radar_title": "雷達圖可視化",
        "dash_comment_title": "✍️ AI評估解讀（模擬輸出，可呼叫LLM）",
        "dash_comment": "> 本地塊整體評估表現良好，社區宜居、跨境協同維度得分較高；生態保育得分偏低，主要原因距離濕地保護區較近，建議進一步擴大生態廊道預留面積，降低棲息地破碎化風險。洪澇風險屬中等水平，建議增加海綿城市、雨水滯留空間的佈局。",
        "ai_title": "💡 生成式AI 三套可選開發方案",
        "ai_btn_run": "🚀 呼叫LLM生成開發方案（基於官方知識庫）",
        "ai_tab1": "方案A｜高密度開發",
        "ai_tab2": "方案B｜生態優先",
        "ai_tab3": "方案C｜均衡綜合方案",
        "aiA_title": "方案A：高密度開發（優先住宅+創科用地）",
        "aiA_content": "- 住宅用地佔比：45%｜創科用地：30%\n- 生態緩衝帶：12公頃\n- ✅ 優點：可提供大量住宅單位，配合新田創科園就業人口的居住需求\n- ⚠️ 風險：生態壓力高，需要嚴格管控施工範圍，減少對周邊濕地的干擾",
        "aiB_title": "方案B：生態優先方案",
        "aiB_content": "- 住宅用地佔比：22%｜創科用地：15%\n- 生態緩衝帶：42公頃，預留連續生態廊道\n- ✅ 優點：大幅降低對米埔濕地、本土生物棲息地的干擾，抵禦洪澇能力強\n- ⚠️ 風險：住宅、產業用地供應量減少，土地開發強度較低",
        "aiC_title": "方案C｜均衡綜合方案（推薦）",
        "aiC_content": "- 住宅用地佔比：34%｜創科用地：24%\n- 生態緩衝帶：22公頃\n- ✅ 優點：住宅、產業用地供應充足，同時預留足夠生態緩衝空間，各項指標綜合最均衡，適合北部都會區新城開發。",
        "map_title": "🗺️ 用地佈局可視化（Folium / Leaflet地圖）",
        "map_select_plan": "選擇查看方案",
        "map_info": "目前檢視：{plan} 用地佈局示意圖",
        "map_legend": "🟫 住宅用地｜🟦 創科產業用地｜🟩 綠地/生態緩衝帶｜🟢 濕地保護區",
        "map_note": "> 地圖備註：粗略示意邊界，僅用於Hackathon原型演示；正式項目接入真實GIS GeoJSON邊界檔案",
        "report_title": "📄 評估報告匯出",
        "report_sub": "AI生成評估報告（中英雙語版本）",
        "report_preview": "報告預覽",
        "report_download": "下載報告 (txt)",
        "report_filename": "northern_metropolis_land_report.txt",
    },
    "en": {
        "title_main": "MetropolisPlan AI",
        "subtitle_main": "Sustainable Land Planning Decision Support Platform for Northern Metropolis",
        "sidebar_title": "🧭 MetropolisPlan AI",
        "sidebar_sub": "Land Planning Assistant for Northern Metropolis",
        "lang_select": "Select Language",
        "nav_home": "🏠 Home",
        "nav_input": "📝 Site Parameter Input",
        "nav_dashboard": "📊 Land Assessment Dashboard",
        "nav_ai": "💡 AI Development Proposals",
        "nav_map": "🗺️ Spatial Visualization Map",
        "nav_report": "📄 Export Report",
        "home_intro_title": "Project Introduction",
        "home_intro": "For Hong Kong Northern Metropolis, we provide an one‑stop decision support platform for government planning departments, including sustainable land evaluation, AI proposal generation and spatial visualization. Balancing residential & tech land development with Mai Po wetland and coastal ecological conservation to achieve SDG11.",
        "home_module_title": "Three Core Modules",
        "home_module_list": "- ✅ Multi‑dimensional Sustainable Land Assessment\n- ✅ Generative AI for multiple development proposals\n- ✅ Visual comparison of land layout",
        "home_info": "✅ Track: Sustainable Northern Metropolis\n✅ Target SDG: SDG11 Sustainable Cities and Communities\n✅ Target User: Planning Department / Northern Metropolis Coordination Office",
        "home_note": "Prototype Demo: Framework showcase. Indicators and AI outputs can be generated via LLM, can connect with real‑world GIS datasets.",
        "input_title": "📝 Site Development Parameter Registration",
        "input_site_name": "Site Name",
        "input_site_default": "San Tin Demo Site A",
        "input_area": "Total Site Area (Hectare)",
        "input_location": "Site Location",
        "input_loc_options": ["San Tin Tech City Surrounding", "Lok Ma Chau", "Lok Ma Chau Loop InnoPark", "Lau Fau Shan Pak Nai"],
        "input_resi_ratio": "Residential Land %",
        "input_tech_ratio": "Tech Industry Land %",
        "input_buffer": "Ecological Buffer Area (Hectare)",
        "input_warn": "Registered Site: {site}, Total Area {area} ha, Residential {resi}%, Tech Land {tech}%, Ecological Buffer {buffer} ha",
        "input_submit": "Submit Parameters & Start Assessment",
        "input_success": "✅ Parameters submitted successfully! Go to Land Assessment Dashboard to view results.",
        "dash_title": "📊 Multi‑dimensional Sustainable Land Assessment",
        "dash_dim": ["Ecology Conservation", "Climate Resilience", "Low Carbon Development", "Liveable Community", "Cross‑boundary Synergy"],
        "dash_score_title": "Indicator Scores",
        "dash_radar_title": "Radar Chart Visualization",
        "dash_comment_title": "✍️ AI Assessment Interpretation (Simulated, LLM to be integrated)",
        "dash_comment": "> This site achieves an overall good score. Liveable community and cross‑boundary synergy perform well. Ecology conservation score is relatively low because of proximity to wetland reserve. Suggest expanding ecological corridor to reduce habitat fragmentation. Flood risk is moderate, sponge city facilities are recommended.",
        "ai_title": "💡 3 Optional Development Proposals by Generative AI",
        "ai_btn_run": "🚀 Run LLM to generate proposals (Based on official knowledge base)",
        "ai_tab1": "Plan A｜High Density Development",
        "ai_tab2": "Plan B｜Ecology First",
        "ai_tab3": "Plan C｜Balanced Mixed Plan (Recommended)",
        "aiA_title": "Plan A: High Density (Priority for Residential + Tech Land)",
        "aiA_content": "- Residential: 45%｜Tech Land:30%\n- Ecological Buffer:12 ha\n- ✅ Advantage: Supply large amount of residential units for San Tin InnoPark workforce\n- ⚠️ Risk: High ecological pressure. Strict construction boundary control required to minimise wetland disturbance.",
        "aiB_title": "Plan B: Ecology First",
        "aiB_content": "- Residential: 22%｜Tech Land:15%\n- Ecological Buffer:42 ha, continuous ecological corridor reserved\n- ✅ Advantage: Minimise disturbance to Mai Po wetland & native habitat, strong flood resistance\n- ⚠️ Risk: Less residential & industrial land supply, lower development intensity",
        "aiC_title": "Plan C｜Balanced Mixed Plan (Recommended)",
        "aiC_content": "- Residential:34%｜Tech Land:24%\n- Ecological Buffer:22 ha\n- ✅ Advantage: Sufficient residential and tech land, enough ecological buffer. Best overall balanced indicators for Northern Metropolis new town.",
        "map_title": "🗺️ Land Layout Visualization (Folium / Leaflet Map)",
        "map_select_plan": "Select Plan to View",
        "map_info": "Currently viewing: {plan} land layout sketch",
        "map_legend": "🟫 Residential Land｜🟦 Tech Industrial Land｜🟩 Green / Ecological Buffer｜🟢 Wetland Reserve",
        "map_note": "> Map note: Rough boundary sketch only for Hackathon demo. Full version import real GIS GeoJSON boundary.",
        "report_title": "📄 Export Assessment Report",
        "report_sub": "AI‑generated Assessment Report",
        "report_preview": "Report Preview",
        "report_download": "Download Report (txt)",
        "report_filename": "northern_metropolis_land_report.txt",
    }
}

# ---------------------- LLM 调用函数 ----------------------
def call_llm(site_name, area, residential_ratio, tech_ratio, buffer_zone):
    prompt = f"""
你是香港北部都会区土地规划专家，严格只参考下面官方规划知识库的内容，禁止编造不存在政策与数据。
=====官方知识库=====
{knowledge_base}
=====用户输入地块参数=====
地块名称：{site_name}
总面积(公顷)：{area}
住宅用地占比：{residential_ratio}%
科创用地占比：{tech_ratio}%
生态缓冲带：{buffer_zone} 公顷

你的任务：
1. 先做该地块五大维度（生态保育、气候韧性、低碳开发、社区宜居、跨境协同）简要评估
2. 生成最多3套可行土地开发建议方案，每套方案要写明：用地配比、适用场景、优点、潜在风险以及缓解措施
3. 输出风格正式，适合香港政府规划人员阅读，输出Markdown格式。
"""
    if SIMULATE_LLM:
        return """### 📋 模拟LLM输出（演示模式，未调用真实大模型）
> 提示：切换 SIMULATE_LLM=False 并填入OPENAI_API_KEY即可获得真实AI生成结果

**地块基础资讯**
地块：{site_name}，面积 {area}公顷，住宅{residential_ratio}%，创科{tech_ratio}%，生态缓冲带 {buffer_zone}公顷

#### 1.综合评估
本地块位于新田科技城范围，需要重点关注邻近米埔/三宝树湿地的生态约束；当前生态缓冲带规模需要检查是否满足35米非建筑缓冲的规划要求。气候韧性方面建议配置海绵城市蓄洪设施；社区层面落实15分钟生活圈；跨境层面可依托北环线实现和河套创科园联动。

#### 方案A｜高密度开发
用地配比：住宅45%，创科用地30%，生态缓冲12公顷
适用场景：地块远离湿地保育区内陆区域
优点：提供充足住宅与创科土地，满足产业就业人口居住需求
风险：生态压力大，必须严格执行阶梯建筑高度，保护鸟类飞行廊道。

#### 方案B｜生态优先
用地配比：住宅22%，创科用地15%，生态缓冲42公顷
适用场景：紧邻三宝树湿地保育公园的地块
优点：大规模连续生态廊道，降低湿地干扰，提升防洪能力
风险：住宅及产业供应规模收缩。

#### 方案C｜均衡综合方案（推荐）
用地配比：住宅34%，创科用地24%，生态缓冲22公顷
适用场景：大多数新田科技城普通地块
优点：平衡房屋、产业发展和生态保育，符合政府规划导向。
风险：需要做好乡村共融、通风廊、景观缓冲带设计。
""".format(site_name=site_name, area=area, residential_ratio=residential_ratio, tech_ratio=tech_ratio, buffer_zone=buffer_zone)
    else:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0.3
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"⚠️ LLM调用失败：{str(e)}，请检查API Key与网络。"

# ---------------------- Folium Leaflet 地图绘制函数 ----------------------
def create_san_tin_map(selected_plan_name):
    # 新田科技城中心经纬度
    center_lat, center_lng = 22.5145, 114.0625
    m = folium.Map(location=[center_lat, center_lng], zoom_start=12, tiles="CartoDB Positron")

    # 新田科技城 粗略外框多边形（示意）
    san_tin_boundary = [
        [22.542, 114.041],
        [22.544, 114.086],
        [22.496, 114.090],
        [22.493, 114.038],
        [22.542, 114.041]
    ]
    folium.Polygon(
        locations=san_tin_boundary,
        color="#222222", weight=2, fill=False,
        popup="新田科技城边界（示意）"
    ).add_to(m)

    # 米埔 + 三宝树湿地保育区 多边形示意
    wetland_zone = [
        [22.536, 114.039],
        [22.539, 114.061],
        [22.510, 114.060],
        [22.507, 114.036],
        [22.536, 114.039]
    ]
    folium.Polygon(
        locations=wetland_zone,
        color="#006400", weight=1, fill_color="#339933", fill_opacity=0.45,
        popup="米埔 / 三宝树湿地保育公园"
    ).add_to(m)

    # 用户示范地块位置
    demo_site = [
        [22.518, 114.056],
        [22.518, 114.070],
        [22.506, 114.070],
        [22.506, 114.056],
        [22.518, 114.056]
    ]

    # 根据选择方案绘制色块
    if selected_plan_name in ["方案A｜高密度开发","Plan A｜High Density Development"]:
        # 高密度：大面积住宅+创科，小面积生态缓冲
        resi_poly = [[22.518,114.056],[22.518,114.064],[22.506,114.064],[22.506,114.056]]
        tech_poly = [[22.518,114.064],[22.518,114.070],[22.506,114.070],[22.506,114.064]]
        eco_poly = []
    elif selected_plan_name in ["方案B｜生态优先","Plan B｜Ecology First"]:
        # 生态优先：绝大部分地块都是生态绿地
        resi_poly = [[22.518,114.056],[22.518,114.059],[22.513,114.059],[22.513,114.056]]
        tech_poly = [[22.511,114.067],[22.511,114.070],[22.506,114.070],[22.506,114.067]]
        eco_poly = [[22.518,114.059],[22.518,114.070],[22.506,114.070],[22.506,114.059]]
    else:
        # 方案C 均衡综合方案（默认推荐）
        resi_poly = [[22.518,114.056],[22.518,114.062],[22.506,114.062],[22.506,114.056]]
        tech_poly = [[22.518,114.062],[22.518,114.067],[22.506,114.067],[22.506,114.062]]
        eco_poly = [[22.518,114.067],[22.518,114.070],[22.506,114.070],[22.506,114.067]]

    # 画住宅 棕色
    if len(resi_poly) > 0:
        folium.Polygon(locations=resi_poly, color="#662200", fill_color="#8B4513", fill_opacity=0.7, popup="住宅用地").add_to(m)
    # 画创科 蓝色
    if len(tech_poly) >0:
        folium.Polygon(locations=tech_poly, color="#113388", fill_color="#4169E1", fill_opacity=0.7, popup="创科产业用地").add_to(m)
    # 画生态缓冲 绿色
    if len(eco_poly) >0:
        folium.Polygon(locations=eco_poly, color="#117722", fill_color="#3CB371", fill_opacity=0.65, popup="生态缓冲绿地").add_to(m)

    return m

# ---------------------- 页面初始化 ----------------------
st.set_page_config(page_title="MetropolisPlan AI", layout="wide")

# session_state 存储用户输入参数
if "site_name" not in st.session_state:
    st.session_state.site_name = "新田示范地块 A"
if "area" not in st.session_state:
    st.session_state.area = 120
if "residential_ratio" not in st.session_state:
    st.session_state.residential_ratio = 35
if "tech_ratio" not in st.session_state:
    st.session_state.tech_ratio = 25
if "buffer_zone" not in st.session_state:
    st.session_state.buffer_zone = 20
if "ai_result" not in st.session_state:
    st.session_state.ai_result = ""

# 语言切换
lang_options = {"简体中文":"zh-CN", "繁體中文":"zh-TW", "English":"en"}
selected_lang_name = st.sidebar.selectbox(lang_dict["zh-CN"]["lang_select"], list(lang_options.keys()), index=1)
lang = lang_options[selected_lang_name]
text = lang_dict[lang]

nav_list = [text["nav_home"], text["nav_input"], text["nav_dashboard"], text["nav_ai"], text["nav_map"], text["nav_report"]]
page = st.sidebar.radio("", nav_list)
st.sidebar.title(text["sidebar_title"])
st.sidebar.subheader(text["sidebar_sub"])

# ===================== 页面1：首页 =====================
if page == text["nav_home"]:
    st.title(text["title_main"])
    st.subheader(text["subtitle_main"])
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {text['home_intro_title']}")
        st.markdown(text["home_intro"])
        st.markdown(f"#### {text['home_module_title']}")
        st.markdown(text["home_module_list"])
    with col2:
        st.info(text["home_info"])
        st.success(text["home_note"])

# ===================== 页面2：地块参数输入 =====================
elif page == text["nav_input"]:
    st.title(text["input_title"])
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        site_name = st.text_input(text["input_site_name"], value=st.session_state.site_name)
        area = st.number_input(text["input_area"], min_value=10, max_value=500, value=st.session_state.area)
        location = st.selectbox(text["input_location"], text["input_loc_options"])
    with col2:
        residential_ratio = st.slider(text["input_resi_ratio"], 10, 60, value=st.session_state.residential_ratio)
        tech_ratio = st.slider(text["input_tech_ratio"], 5, 40, value=st.session_state.tech_ratio)
        buffer_zone = st.slider(text["input_buffer"], 5, 80, value=st.session_state.buffer_zone)

    st.warning(text["input_warn"].format(site=site_name, area=area, resi=residential_ratio, tech=tech_ratio, buffer=buffer_zone))
    if st.button(text["input_submit"], type="primary"):
        st.session_state.site_name = site_name
        st.session_state.area = area
        st.session_state.residential_ratio = residential_ratio
        st.session_state.tech_ratio = tech_ratio
        st.session_state.buffer_zone = buffer_zone
        st.session_state["input_done"] = True
        st.success(text["input_success"])

# ===================== 页面3：土地评估仪表板 =====================
elif page == text["nav_dashboard"]:
    st.title(text["dash_title"])
    st.divider()
    score_data = {
        "评估维度": text["dash_dim"],
        "得分": [68, 75, 70, 82, 78]
    }
    df_score = pd.DataFrame(score_data)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(text["dash_score_title"])
        st.dataframe(df_score, use_container_width=True)
    with col2:
        st.subheader(text["dash_radar_title"])
        fig = go.Figure(data=go.Scatterpolar(
            r = df_score["得分"],
            theta = df_score["评估维度"],
            fill = "toself",
            name = text["title_main"]
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), height=400)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"### {text['dash_comment_title']}")
    st.write(text["dash_comment"])

# ===================== 页面4：AI开发方案建议（整合知识库+LLM呼叫） =====================
elif page == text["nav_ai"]:
    st.title(text["ai_title"])
    st.divider()
    # 按钮触发LLM
    if st.button(text["ai_btn_run"], type="primary"):
        with st.spinner("Generating..."):
            res = call_llm(
                st.session_state.site_name,
                st.session_state.area,
                st.session_state.residential_ratio,
                st.session_state.tech_ratio,
                st.session_state.buffer_zone
            )
            st.session_state.ai_result = res
    st.divider()
    if st.session_state.ai_result:
        st.markdown(st.session_state.ai_result)
    else:
        tab1, tab2, tab3 = st.tabs([text["ai_tab1"], text["ai_tab2"], text["ai_tab3"]])
        with tab1:
            st.subheader(text["aiA_title"])
            st.markdown(text["aiA_content"])
        with tab2:
            st.subheader(text["aiB_title"])
            st.markdown(text["aiB_content"])
        with tab3:
            st.subheader(text["aiC_title"])
            st.markdown(text["aiC_content"])

# ===================== 页面5：🗺️ Folium Leaflet 空间可视化地图【新增！】 =====================
elif page == text["nav_map"]:
    st.title(text["map_title"])
    st.divider()
    plan_options = [text["ai_tab1"], text["ai_tab2"], text["ai_tab3"]]
    selected_plan = st.radio(text["map_select_plan"], plan_options, horizontal=True)
    st.info(text["map_info"].format(plan=selected_plan))
    st.markdown(text["map_legend"])
    st.markdown(text["map_note"])

    # 生成地图
    map_obj = create_san_tin_map(selected_plan)
    # streamlit渲染folium地图
    st_folium(map_obj, width=1000, height=600)

# ===================== 页面6：导出报告 =====================
elif page == text["nav_report"]:
    st.title(text["report_title"])
    st.divider()
    st.markdown(f"### {text['report_sub']}")
    report_text = f"""
# MetropolisPlan AI 土地評估報告
地塊名稱：{st.session_state.site_name}
總面積：{st.session_state.area} 公頃
住宅佔比：{st.session_state.residential_ratio}%
創科用地佔比：{st.session_state.tech_ratio}%
生態緩衝帶：{st.session_state.buffer_zone} 公頃

## AI分析結果
{st.session_state.ai_result if st.session_state.ai_result else "尚未執行AI方案生成，請前往AI開發方案建議頁面執行生成。"}
"""
    st.text_area(text["report_preview"], report_text, height=350)
    st.download_button(label=text["report_download"], data=report_text, file_name=text["report_filename"])
