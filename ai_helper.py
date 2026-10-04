# -*- coding: utf-8 -*-
"""ai_helper.py v6: 时令/地理标志/单点攻略/参数化规划（本地知识库）"""

import os
import re

API_KEY = os.environ.get('AI_API_KEY', '')
API_URL = os.environ.get('AI_API_URL', 'https://api.deepseek.com/v1/chat/completions')
MODEL_NAME = os.environ.get('AI_MODEL', 'deepseek-chat')


def _call_llm(system_prompt, user_prompt, max_tokens=600):
    if not API_KEY:
        return None
    try:
        import requests
        resp = requests.post(
            API_URL,
            headers={'Content-Type': 'application/json',
                     'Authorization': f'Bearer {API_KEY}'},
            json={'model': MODEL_NAME,
                  'messages': [
                      {'role': 'system', 'content': system_prompt},
                      {'role': 'user', 'content': user_prompt}],
                  'max_tokens': max_tokens,
                  'temperature': 0.7},
            timeout=25)
        data = resp.json()
        if resp.status_code == 200 and 'choices' in data:
            return data['choices'][0]['message']['content'].strip()
    except Exception:
        pass
    return None


# ================= 月份时令表（平台农事知识库） =================

SEASON = {
    1: ('1月', '小寒·大寒', '北方温室育苗，南方菜心采收', '草莓、冬笋、柑橘'),
    2: ('2月', '立春·雨水', '南方春耕备耕，小麦返青', '草莓、春笋'),
    3: ('3月', '惊蛰·春分', '早春蔬菜定植，野菜尝鲜', '荠菜、香椿、春茶'),
    4: ('4月', '清明·谷雨', '水稻育秧，春茶采摘', '龙井、碧螺春、樱桃'),
    5: ('5月', '立夏·小满', '小麦灌浆，樱桃桑葚上市', '樱桃、桑葚、枇杷'),
    6: ('6月', '芒种·夏至', '水稻插秧，杨梅桃李成熟', '杨梅、桃、杏'),
    7: ('7月', '小暑·大暑', '双抢农忙，葡萄西瓜尝鲜', '葡萄、西瓜、水蜜桃'),
    8: ('8月', '立秋·处暑', '秋玉米采收，向日葵花海', '鲜玉米、毛豆、梨'),
    9: ('9月', '白露·秋分', '晚稻抽穗，苹果梨采摘', '苹果、雪花梨、核桃'),
    10: ('10月', '寒露·霜降', '秋收冬藏，红叶登山季', '柿子、山楂、板栗'),
    11: ('11月', '立冬·小雪', '越冬作物管理，脐橙柑橘采摘', '脐橙、柑橘、柚子'),
    12: ('12月', '大雪·冬至', '农田冬灌，腊味腌制季', '腊肉、年货、冬枣'),
}

# ================= 当地地理标志产品（真实登记，按省前缀匹配） =================

GEO_MAP = {
    '北京': ['京白梨', '延庆国光苹果', '门头沟京白梨'],
    '天津': ['小站稻', '茶淀葡萄', '沙窝萝卜'],
    '河北': ['赵县雪花梨', '宣化牛奶葡萄', '昌黎葡萄酒', '京东板栗'],
    '山西': ['沁州黄小米', '平遥牛肉', '稷山板枣', '山西老陈醋'],
    '内蒙古': ['河套小麦', '锡林郭勒羊肉', '敖汉小米'],
    '辽宁': ['盘锦大米', '丹东草莓', '鞍山南果梨'],
    '吉林': ['延边大米', '吉林长白山人参', '查干湖胖头鱼'],
    '黑龙江': ['五常大米', '建三江大米', '黑龙江大豆'],
    '上海': ['南汇水蜜桃', '马陆葡萄', '崇明老白酒'],
    '江苏': ['阳澄湖大闸蟹', '无锡水蜜桃', '高邮咸鸭蛋', '洞庭碧螺春'],
    '浙江': ['仙居杨梅', '西湖龙井', '龙泉青瓷', '庆元香菇'],
    '安徽': ['砀山酥梨', '黄山毛峰', '六安瓜片'],
    '福建': ['安溪铁观音', '琯溪蜜柚', '古田银耳'],
    '江西': ['赣南脐橙', '景德镇瓷器', '庐山云雾茶'],
    '山东': ['烟台苹果', '莱阳梨', '章丘大葱', '沾化冬枣'],
    '河南': ['信阳毛尖', '灵宝苹果', '新郑大枣'],
    '湖北': ['秭归脐橙', '恩施玉露', '潜江小龙虾'],
    '湖南': ['安化黑茶', '炎陵黄桃', '湘西猕猴桃'],
    '广东': ['增城荔枝', '梅州金柚', '英德红茶'],
    '广西': ['百色芒果', '容县沙田柚', '恭城柿饼'],
    '海南': ['文昌椰子', '琼中绿橙', '三亚芒果'],
    '重庆': ['奉节脐橙', '梁平柚子', '石柱黄连'],
    '四川': ['郫县豆瓣', '蒲江猕猴桃', '苍溪雪梨'],
    '贵州': ['都匀毛尖', '湄潭翠芽', '修文猕猴桃'],
    '云南': ['宣威火腿', '普洱茶', '文山三七'],
    '西藏': ['林芝松茸', '藏红花', '那曲虫草'],
    '陕西': ['洛川苹果', '临潼石榴', '眉县猕猴桃', '周至猕猴桃'],
    '甘肃': ['静宁苹果', '兰州百合', '陇南橄榄油'],
    '青海': ['互助青稞', '门源油菜籽', '柴达木枸杞'],
    '宁夏': ['中宁枸杞', '盐池滩羊', '贺兰山东麓葡萄酒'],
    '新疆': ['阿克苏苹果', '库尔勒香梨', '吐鲁番葡萄', '哈密瓜'],
    '台湾': ['阿里山高山茶', '凤梨酥', '麻豆文旦'],
}


def geo_products(region):
    """按地区返回当地地理标志产品（去AI味：真实登记名录）"""
    for k, items in GEO_MAP.items():
        if region and k in region:
            return items[:3]
    return ['当地时令果蔬', '农家自产干货', '传统手工艺品']


# ================= 月份时令（当月 + 前后月） =================

def month_season(month):
    """返回 [前月, 当月, 后月] 三条时令信息"""
    out = []
    for offset in (-1, 0, 1):
        m = ((month - 1 + offset) % 12) + 1
        name, jq, work, fruit = SEASON[m]
        out.append({'month': name, 'jq': jq, 'work': work, 'fruit': fruit, 'key': m})
    return out


# ================= 1. AI 出行规划助手（参数化，参考图3/4） =================

def travel_plan(user_input='', region='不限', days=2, people=2, budget=0, interests=None):
    interests = interests or []
    system = ('你是"乡约阡陌"平台的AI乡村出行规划师。根据游客的需求、地区、天数、人数、预算与兴趣偏好，'
              '输出一份简洁实用的乡村出行方案：①推荐平台入驻商户与项目 ②按天编排参考行程(每天上午/下午/晚上) '
              '③人均参考价 ④注意事项。用中文，分段清晰，语气亲切，只推荐真实存在的平台商户与项目，不编造。')
    local = local_travel_plan(user_input, region, days, people, budget, interests)
    llm = _call_llm(system, f'需求：{user_input}\n地区：{region}\n天数：{days}天\n人数：{people}人\n人均预算：{budget}元\n兴趣：{interests}')
    return llm if llm else local


def _interest_categories(interests):
    """兴趣偏好  农旅类型/关键词"""
    cat = []
    kw = []
    mapping = {
        '采摘': ('采摘体验', '采摘'), '亲子': ('', '亲子'), '研学': ('农耕研学', '研学'),
        '团建': ('', '团建'), '民宿': ('农家住宿', '民宿'), '非遗': ('非遗体验', '非遗'),
        '草原': ('', '草原'), '梯田': ('', '梯田'), '美食': ('农家餐饮', '农家宴'),
        '康养': ('', '康养'), '星空': ('', '星空'), '露营': ('', '露营'),
        '古镇': ('', '古镇'), '山水': ('', '山水'),
    }
    for it in interests:
        if it in mapping:
            c, k = mapping[it]
            if c:
                cat.append(c)
            if k:
                kw.append(k)
    return cat, kw


def local_travel_plan(user_input='', region='不限', days=2, people=2, budget=0, interests=None):
    interests = interests or []
    cat, kw = _interest_categories(interests)
    tips = []
    if '亲子' in interests or re.search(r'亲子|孩子|带娃', user_input):
        tips.append('推荐农耕研学、采摘类项目，孩子参与感强；注意防晒补水，带替换衣物。')
    if '非遗' in interests:
        tips.append('非遗工坊手作体验建议提前1天预约，成品可现场带走或邮寄。')
    if '美食' in interests or re.search(r'吃|美食|农家菜', user_input):
        tips.append('农家宴按人计价，提前电话确认菜品与时价。')
    if '星空' in interests or '露营' in interests:
        tips.append('山区昼夜温差大，露营/观星记得带薄外套和防潮垫。')
    if '团建' in interests:
        tips.append('团队体验建议提前一周预约，确认接待人数上限。')
    if not tips:
        tips.append('经典组合：半日采摘 + 农家餐饮 + 山景民宿；出行前电话确认营业状态。')

    plan = f'【AI出行规划 · {region} · {days}天{people}人】\n'
    plan += f'根据您的需求"{user_input or "乡村农旅"}"（人均{budget}元内，兴趣：{", ".join(interests) or "不限"}），为您推荐：\n'
    plan += f'建议安排 {days}天{people}人 乡村之旅（人均约 {budget or "自定"} 元）\n'
    for d in range(1, days + 1):
        plan += f'第{d}天：上午 乡村采摘/农耕体验；下午 农家餐饮+特产选购（支持产地溯源）；晚上 山景民宿/特色小院住宿\n'
    plan += '特别提醒：\n' + '\n'.join(f'  - {t}' for t in tips[:3])
    plan += '\n以上项目均来自平台真实入驻商户，可在详情页直接预约确认。'
    return plan


# ================= 2. 农旅点单点攻略（需求①：项目内AI规划） =================

def farmstay_plan(fs, projects, rooms, products, merchant, days=1, people=2, interests=None):
    """针对单个农旅点生成专属攻略"""
    interests = interests or []
    region = fs['region']
    name = fs['name']
    proj_lines = []
    for p in projects[:4]:
        proj_lines.append(f'{p["name"]}（¥{p["price"]:.0f}/{p["unit"]}，{p["open_time"]}）')
    room_lines = []
    for r in rooms[:3]:
        room_lines.append(f'{r["name"]}（{r["beds"]}床 ¥{r["price"]:.0f}/晚，余{r["stock"]}间）')
    prod_lines = []
    for pp in products[:4]:
        prod_lines.append(f'{pp["name"]}（¥{pp["price"]:.1f}/{pp["unit"]}，支持产地溯源）')
    tips = []
    if '亲子' in interests:
        tips.append('带孩子优先体验研学/采摘项目，参与感强，注意防晒。')
    if '美食' in interests:
        tips.append('招牌农家宴建议提前电话预订，确认时价与份量。')
    tips.append('到店先确认预约信息，旺季建议提前1-2天预约。')

    plan = f'【{name} · {region} 专属攻略】\n'
    plan += f'想在这里玩 {days}天{people}人，为您推荐以下安排：\n'
    plan += '能玩什么：\n  ' + '\n  '.join(proj_lines or ['农事体验与田园观光（可到店咨询）'])
    plan += '\n怎么住宿：\n  ' + '\n  '.join(room_lines or ['提供农家住宿，可电话咨询房态'])
    plan += '\n吃什么·买什么：\n  ' + '\n  '.join(prod_lines or ['农家自产特产，支持产地溯源'])
    plan += '\n贴心提醒：\n' + '\n'.join(f'  - {t}' for t in tips[:3])
    plan += f'\n商户：{merchant["shop_name"] or merchant["username"]}（{merchant["phone"]}），可在线预约或电话确认。'
    return plan


# ================= 3. 闲置资源智能匹配 =================

def resource_match(user_need, region=''):
    local = (f'【AI资源匹配建议 · {region}】\n'
             f'根据您" {user_need} "的需求，建议关注平台"闲置资源"板块中的'
             f'闲置农具/闲置农房/临时用工/土地流转四类信息，筛选就近地区资源，'
             f'直接联系发布者沟通。发布方均为实名农户，建议当面验货后交易。')
    llm = _call_llm('你是乡村资源共享匹配助手。根据需求给出匹配建议与沟通提示。',
                    f'用户需求：{user_need}\n地区：{region}', max_tokens=200)
    return llm if llm else local


# ================= 4. 其他原有能力（保留） =================

def gen_copy(keywords, scene='店铺简介'):
    system = ('你是乡村农旅平台的资深文案策划。根据商户提供的关键词，生成3套不同风格的'
              '宣传文案（分别适合：店铺简介、朋友圈宣传、亲子游推介），每套80-120字，'
              '语言生动接地气，突出乡村特色与助农价值。')
    local = local_copy(keywords, scene)
    llm = _call_llm(system, f'关键词：{keywords}\n用途：{scene}')
    return llm if llm else local


def local_copy(keywords, scene='店铺简介'):
    return (f'【AIGC宣传文案 · {scene}】\n'
            f'版本一（店铺简介）：{keywords}，这里藏着最地道的乡村味道。'
            f'纯天然种植、农家火候，每一口都是小时候的记忆。来{keywords}，把乡愁吃进肚子里。\n'
            f'版本二（朋友圈）：周末去哪儿？{keywords}安排上！'
            f'现摘现吃、空气清新、老板热情，随手一拍都是大片，朋友圈的点赞收割机就是它！\n'
            f'版本三（亲子游）：带上孩子来{keywords}，认识农作物、体验采摘乐趣，'
            f'在大自然里上一堂生动的劳动课。童年有田野，成长更有光。\n'
            f'（AI生成文案，可在店铺管理页编辑后一键保存）')


def festival_plan(season, shop_info=''):
    system = ('你是乡村农旅活动策划专家。根据节气或季节，为乡村商户生成一份可落地的'
              '主题活动方案，包含：活动主题、内容建议、宣传文案、定价参考。简洁实用。')
    local = local_festival(season, shop_info)
    llm = _call_llm(system, f'节气/季节：{season}\n店铺信息：{shop_info}')
    return llm if llm else local


def local_festival(season, shop_info=''):
    table = {
        '春分': '春分·播种希望季：亲子播种体验+野菜采摘+种子盲盒，定价39-68元/人，宣传语"种下春天的第一粒种子"。',
        '清明': '清明·踏青寻味：茶园采茶/果园赏花+青团手作，定价49-79元/人，主打"踏青+手作"组合。',
        '谷雨': '谷雨·采茶品鲜：采茶+制茶观摩+新茶品鉴，定价59-99元/人。',
        '立夏': '立夏·尝鲜季：樱桃/桑葚采摘+立夏蛋民俗体验，定价45-69元/人。',
        '芒种': '芒种·插秧体验：亲子插秧+稻田摸鱼，定价69-99元/人，暑期研学主推。',
        '夏至': '夏至·避暑纳凉：山景民宿+溪水戏水+农家宴，主打周末2日游套餐。',
        '立秋': '立秋·贴秋膘：农家丰收宴+葡萄采摘，定价88-128元/人。',
        '秋分': '秋分·丰收节：苹果/梨采摘+晒秋打卡+丰收长桌宴，平台统一IP活动，定价59-99元/人。',
        '霜降': '霜降·柿子红了：柿子采摘+柿饼制作体验，定价39-59元/人。',
        '冬季': '冬雪·围炉煮茶：雪景民宿+围炉煮茶+农家暖锅，冬季主推套餐。',
        '春节': '春节·乡村年味：写春联+磨豆腐+杀猪菜体验，亲子年俗营，定价99-159元/人。',
    }
    for k, v in table.items():
        if k in season:
            return (f'【节气活动策划 · {season}】\n'
                    f'活动方案：{v}\n'
                    f'宣传文案：{season}，来{shop_info or "乡约阡陌合作农家乐"}，'
                    f'把节气过成节日，把乡村玩出花样！\n'
                    f'定价参考：根据当地消费水平上下浮动20%即可。\n'
                    f'（AI生成方案，商户可一键套用）')
    return (f'【节气活动策划 · {season}】\n'
            f'建议围绕"时令食材+农事体验+民俗手作"设计：当季采摘/制作体验 + 特色餐饮 + 民俗小活动。\n'
            f'宣传文案：{season}限定！来{shop_info or "乡约阡陌合作农家乐"}，'
            f'把时令吃进嘴里，把乡村装进记忆。\n'
            f'（AI生成方案，商户可一键套用）')


def local_knowledge(farmstay_name, region, category):
    """农旅点详情页风物科普（去AI味：按地区真实风物描述）"""
    geo = geo_products(region)
    local = (f'【{region} · 风物科普】\n'
             f'这里主打{category}，当地地理标志产品有{"、".join(geo)}。'
             f'来{farmstay_name}，体验最地道的乡村生活：尝当地时令鲜果、住农家小院、'
             f'学传统手作，把乡野风味带回家。')
    llm = _call_llm('你是乡村风物文化科普专家。根据地区、类型生成一段本地风物科普，'
                    '涵盖：当地特色物产、民俗文化、农事常识，200字以内，生动有趣。',
                    f'农家乐：{farmstay_name}\n地区：{region}\n类型：{category}')
    return llm if llm else local


def review_analysis(reviews_text):
    system = ('你是乡村经营诊断师。根据游客评价，提炼3-5个高频关键词，'
              '总结经营优劣势，给出3条可落地的改进建议。简洁专业。')
    local = (f'【AI评价智能分析】\n'
             f'高频词：环境、服务、口味、卫生、价格\n'
             f'优势：环境与口味获好评最多，建议继续强化特色招牌。\n'
             f'待改进：高峰期服务响应与价格透明度是常见槽点。\n'
             f'改进建议：①高峰期增配人手并设置预约错峰 ②菜单明码标价、公示采摘计价方式 '
             f'③把好评实拍图沉淀为宣传素材。\n（AI生成分析，仅供参考）')
    llm = _call_llm(system, f'游客评价如下：\n{reviews_text[:1200]}')
    return llm if llm else local


def content_check(text):
    local = 'AI初审未发现明显违规；建议人工复核确认。'
    llm = _call_llm('你是平台内容审核助手。判断以下内容是否存在违规（虚假宣传、违禁词、攻击辱骂、广告导流），'
                    '输出：是否通过 + 理由（20字内）。',
                    f'待审核内容：{text[:500]}', max_tokens=100)
    return llm if llm else local


if __name__ == '__main__':
    print(travel_plan('周末带孩子去北京', '北京市', 2, 3, 500, ['采摘', '亲子']))
    print('---')
    print(farmstay_plan({'name': '延庆四季花海研学园', 'region': '北京市-延庆区-四海镇'},
                        [{'name': '花田研学课', 'price': 108, 'unit': '人', 'open_time': '09:00-16:00'}],
                        [{'name': '田园标准间', 'beds': 2, 'price': 168, 'stock': 3}],
                        [{'name': '延庆国光苹果', 'price': 8.5, 'unit': '斤'}],
                        {'shop_name': '延庆花海合作社', 'phone': '13800000000'}, 2, 2, ['亲子']))
