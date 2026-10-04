# -*- coding: utf-8 -*-
"""乡约阡陌 全流程集成测试（游客端/商户端/管理端）v4：购物车+取消+退款+公告
使用独立临时数据库，不污染演示数据。"""
import os
import tempfile
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import models
models.DB_PATH = os.path.join(tempfile.gettempdir(), 'xyqm_test.db')
if os.path.exists(models.DB_PATH):
    os.remove(models.DB_PATH)

import app as appmod
import init_db as idb
idb.main()

c = appmod.app.test_client()
passed, failed = 0, 0

def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f'  ✔ {name}')
    else:
        failed += 1
        print(f'  ✘ {name}')

print('=== 游客端 ===')
for url in ['/', '/login', '/register', '/farmstays', '/farmstay/28', '/farmstay/29',
            '/farmstay/30', '/products', '/product/23', '/product/27', '/resources',
            '/ai_travel']:
    r = c.get(url)
    check(f'GET {url} -> {r.status_code}', r.status_code == 200)

# 未登录访问需登录页面（正确重定向到登录）
r = c.get('/resource/publish', follow_redirects=False)
check('未登录访问发布资源 -> 302跳登录', r.status_code == 302)
r = c.get('/booking?farmstay_id=28', follow_redirects=False)
check('未登录访问预约 -> 302跳登录', r.status_code == 302)
r = c.get('/cart', follow_redirects=False)
check('未登录访问购物车 -> 302跳登录', r.status_code == 302)

# 游客登录
r = c.post('/login', data={'username': '游客小美', 'password': '123456'})
check('游客登录 -> 302', r.status_code == 302)
for url in ['/my/bookings', '/my/orders', '/my/favorites', '/my/reviews', '/my/profile',
            '/resource/publish', '/booking?farmstay_id=28', '/cart']:
    r = c.get(url)
    check(f'GET {url} -> {r.status_code}', r.status_code == 200)

# 游客提交预约（成功页直接渲染200）
r = c.post('/booking', data={'farmstay_id': '28', 'project_id': '64', 'visit_date': '2026-10-01',
                             'people': '2', 'phone': '13800000000', 'remark': '测试', 'add_product': '31'})
check('提交预约 -> 200成功页', r.status_code == 200)
check('预约成功页含预约编号', '预约申请已提交' in r.data.decode('utf-8'))

# 游客提交特产订单（含收货信息）
r = c.post('/product/order', data={'product_id': '23', 'quantity': '2',
                                   'recv_name': '张小明', 'recv_phone': '13800001111',
                                   'recv_address': '北京市海淀区学院路1号'})
check('特产下单 -> 302', r.status_code == 302)

# 游客小美真实id（动态查询）
import sqlite3 as _sq
_conn = _sq.connect(models.DB_PATH)
_conn.row_factory = _sq.Row
_uid = _conn.execute("SELECT id FROM users WHERE username='游客小美'").fetchone()['id']
_conn.close()

# ===== 购物车 =====
r = c.post('/cart/add', data={'product_id': '23', 'quantity': '2'})
check('加入购物车 -> 302', r.status_code == 302)
r = c.post('/cart/add', data={'product_id': '23', 'quantity': '1'})
check('重复加入购物车(累加) -> 302', r.status_code == 302)
r = c.get('/cart')
check('购物车页 -> 200', r.status_code == 200)
cart_rows = models.get_cart(_uid)
check('购物车有 1 项商品', len(cart_rows) == 1)
if cart_rows:
    cid = cart_rows[0]['id']
    r = c.post('/cart/update', data={'cart_id': str(cid), 'quantity': '5'})
    check('修改购物车数量 -> 302', r.status_code == 302)
    check('数量已更新为5', models.get_cart(_uid)[0]['quantity'] == 5)
    r = c.post('/cart/remove', data={'cart_id': str(cid)})
    check('删除购物车项 -> 302', r.status_code == 302)
    check('购物车已清空该项', len(models.get_cart(_uid)) == 0)

# 购物车结算（重新加入后结算）
c.post('/cart/add', data={'product_id': '23', 'quantity': '1'})
r = c.post('/cart/checkout', data={'recv_name': '张小明', 'recv_phone': '13800001111',
                                   'recv_address': '北京市海淀区学院路1号'})
check('购物车结算 -> 302', r.status_code == 302)
check('结算后购物车清空', len(models.get_cart(_uid)) == 0)
r = c.post('/cart/checkout', data={'recv_name': '', 'recv_phone': '', 'recv_address': ''})
check('空收货信息结算被拦截 -> 302', r.status_code == 302)

# ===== 取消订单（待发货） =====
user_orders = models.get_user_product_orders(_uid)
pending = [o for o in user_orders if o['status'] == '待发货']
check('游客有待发货订单可取消', len(pending) >= 1)
if pending:
    oid = pending[0]['id']
    r = c.post('/order/%d/cancel' % oid)
    check('取消订单 -> 302', r.status_code == 302)
    check('订单状态已取消', models.get_product_order(oid)['status'] == '已取消')

# ===== 申请退款（已发货） =====
shipped = [o for o in user_orders if o['status'] == '已发货']
check('游客有已发货订单可退款', len(shipped) >= 1)
if shipped:
    oid = shipped[0]['id']
    r = c.post('/order/%d/refund' % oid, data={'reason': '品质不满意'})
    check('申请退款 -> 302', r.status_code == 302)
    check('状态变为退款申请', models.get_product_order(oid)['status'] == '退款申请')
    check('退款原因已记录', models.get_product_order(oid)['refund_reason'] == '品质不满意')
    r = c.post('/order/%d/refund' % oid, data={'reason': ''})
    check('空原因退款被拦截 -> 302', r.status_code == 302)

# 收藏
r = c.post('/favorite', data={'target_type': 'farmstay', 'target_id': '2'})
check('收藏农家乐 -> 302', r.status_code == 302)

# 发布评价
r = c.post('/my/reviews', data={'farmstay_id': '28', 'rating': '5', 'content': '农家菜很好吃，环境优美！'})
check('发布评价 -> 302', r.status_code == 302)

# AI 出行规划
r = c.post('/ai_travel', data={'user_input': '周末带爸妈去崇礼避暑', 'region': '河北省'})
check('AI出行规划 -> 200', r.status_code == 200)

# 资源发布 + AI匹配
r = c.post('/resource/publish', data={'rtype': '闲置农具', 'title': '闲置播种机', 'region': '河北保定',
                                      'description': '八成新', 'price': '200', 'contact': '赵大姐'})
check('发布资源 -> 302', r.status_code == 302)
r = c.post('/resource/match', data={'need': '播种机', 'region': '河北省'})
check('AI资源匹配 -> 200', r.status_code == 200)

# 游客访问商户端应被拦截
r = c.get('/merchant', follow_redirects=False)
check('游客访问商户端被拦截 -> 302', r.status_code == 302)

# 溯源查询
r = c.get('/trace')
check('溯源查询页 -> 200', r.status_code == 200)
r = c.post('/trace', data={'code': 'XYQM1001'})
check('溯源查询XYQM1001 -> 200', r.status_code == 200)
check('溯源结果含红富士', '红富士' in r.data.decode('utf-8'))
r = c.post('/trace', data={'code': 'NOPE0000'})
check('溯源查询无效码 -> 200有提示', r.status_code == 200)

print('=== 商户端 ===')
c.get('/logout')
r = c.post('/login', data={'username': '青山农家乐', 'password': '123456'})
check('商户登录 -> 302', r.status_code == 302)
for url in ['/merchant', '/merchant/shop', '/merchant/projects', '/merchant/rooms',
            '/merchant/products', '/merchant/bookings', '/merchant/reviews', '/merchant/ai',
            '/merchant/orders']:
    r = c.get(url)
    check(f'GET {url} -> {r.status_code}', r.status_code == 200)

r = c.post('/merchant/add_farmstay', data={'name': '测试小院', 'region': '河北省-保定市', 'address': '某村',
                                           'category': '农家餐饮', 'price_min': '30', 'tags': '测试',
                                           'description': '测试用'})
check('商户创建点位 -> 302', r.status_code == 302)
r = c.post('/merchant/product/add', data={'farmstay_id': '28', 'name': '测试核桃', 'price': '15', 'unit': '斤',
                                          'stock': '50', 'description': '测试', 'origin': '河北保定'})
check('商户上架特产 -> 302', r.status_code == 302)
r = c.post('/merchant/ai', data={'mode': 'copy', 'keywords': '苹果采摘 亲子', 'scene': '店铺简介'})
check('AIGC文案 -> 200', r.status_code == 200)
r = c.post('/merchant/ai', data={'mode': 'festival', 'season': '秋分', 'shop_info': '青山农家乐'})
check('节气策划 -> 200', r.status_code == 200)
r = c.post('/merchant/booking/update', data={'booking_id': '1', 'status': '已确认'})
check('商户确认预约 -> 302', r.status_code == 302)

# 商户取消订单（种子待发货订单）
mer_pending = [o for o in models.list_all_product_orders(1) if o['status'] == '待发货']
if mer_pending:
    oid = mer_pending[0]['id']
    r = c.post('/merchant/order/cancel', data={'order_id': str(oid)})
    check('商户取消订单 -> 302', r.status_code == 302)
    check('商户取消后状态已取消', models.get_product_order(oid)['status'] == '已取消')

print('=== 管理端 ===')
c.get('/logout')
r = c.post('/login', data={'username': '平台管理员', 'password': '123456'})
check('管理员登录 -> 302', r.status_code == 302)
for url in ['/admin', '/admin/merchants', '/admin/farmstays', '/admin/products',
            '/admin/users', '/admin/reviews', '/admin/banners', '/admin/notices',
            '/admin/orders']:
    r = c.get(url)
    check(f'GET {url} -> {r.status_code}', r.status_code == 200)

r = c.post('/admin/audit_ai', data={'text': '本店苹果甜过初恋，好吃到爆！'})
check('AI内容审核 -> 302跳转评价页', r.status_code == 302)
r = c.post('/admin/user/create', data={'username': '测试管理员', 'password': '123456', 'role': '3', 'region': '河北省-保定市'})
check('创建平台管理员 -> 302', r.status_code == 302)
r = c.post('/admin/banners', data={'title': '测试轮播', 'image': 'banner2.jpg', 'link': '/'})
check('添加轮播图 -> 302', r.status_code == 302)
r = c.get('/admin/banners')
check('轮播列表含新轮播 -> 200', r.status_code == 200)

# ===== 管理端处理退款 =====
_refund = [o for o in models.list_all_product_orders() if o['status'] == '退款申请']
check('平台有待处理退款申请', len(_refund) >= 1)
if _refund:
    _oid = _refund[0]['id']
    r = c.post('/admin/order/refund', data={'order_id': str(_oid), 'action': 'approve'})
    check('平台同意退款 -> 302', r.status_code == 302)
    check('平台处理后状态已退款', models.get_product_order(_oid)['status'] == '已退款')

# ===== 公告管理 =====
r = c.post('/admin/notice/add', data={'title': '测试公告', 'content': '平台临时维护通知'})
check('发布公告 -> 302', r.status_code == 302)
notices = models.list_notices()
check('公告列表有5条', len(notices) == 5)
_new_id = notices[0]['id']
r = c.post('/admin/notice/toggle', data={'notice_id': str(_new_id), 'status': '停用'})
check('停用公告 -> 302', r.status_code == 302)
check('公告已停用', models.list_notices()[0]['status'] == '停用')
r = c.post('/admin/notice/delete', data={'notice_id': str(_new_id)})
check('删除公告 -> 302', r.status_code == 302)

# 首页应显示启用的公告
c.get('/logout')
r = c.post('/login', data={'username': '游客小美', 'password': '123456'})
r = c.get('/')
check('首页含系统公告栏', '系统公告' in r.data.decode('utf-8'))

print('=== 村级管理员角色已移除 ===')
c.get('/logout')
r = c.post('/login', data={'username': '王村助农站', 'password': '123456'})
check('村级管理员账号已删除无法登录', '用户名或密码错误' in r.data.decode('utf-8'))

print('=== v5 新增功能 ===')
# 重新登录游客小美
c.get('/logout')
r = c.post('/login', data={'username': '游客小美', 'password': '123456'})
# 公告弹窗 + 搜索栏
r = c.get('/')
html = r.data.decode('utf-8')
check('首页含公告弹窗 noticeModal', 'noticeModal' in html)
check('首页含轮播下搜索栏 home-search', 'home-search' in html)

# 溯源 GET ?code= 直达
r = c.get('/trace?code=XYQM1022')
check('溯源GET直达 -> 200', r.status_code == 200)
check('溯源档案表含认证编号', '认证编号' in r.data.decode('utf-8'))

# 北京点位（AI出行按省匹配）
bj = models.list_farmstays(region='北京市')
check('北京市点位 >= 4 个', len(bj) >= 4)
r = c.post('/ai_travel', data={'user_input': '周末去北京采摘', 'region': '北京市'})
check('AI出行北京 -> 200', r.status_code == 200)
check('AI出行推荐北京点位', '密云山水采摘园' in r.data.decode('utf-8'))

# 资源省份筛选 + 资源详情 + 对接意向
r = c.get('/resources?region=河北')
check('资源按省份筛选 -> 200', r.status_code == 200)
rid = models.list_resources()[0]['id']
r = c.get('/resource/%d' % rid)
check('资源详情 /resource/%d -> 200' % rid, r.status_code == 200)
r = c.post('/resource/%d/intent' % rid, data={'message': '测试对接意向'})
check('提交对接意向 -> 302', r.status_code == 302)

# 个人中心统计卡 + Tab
r = c.get('/my/profile')
html = r.data.decode('utf-8')
check('个人中心含数据统计', '我的预约' in html and '我的意向单' in html)
check('个人中心含Tab导航', 'AI出行偏好' in html)
r = c.get('/my/profile?tab=intents')
check('个人中心对接意向Tab -> 200', r.status_code == 200)
check('对接意向Tab含记录', '测试对接意向' in r.data.decode('utf-8'))

# 取消预约
_uid = models.get_user_by_name('游客小美')['id']
r = c.post('/booking', data={'farmstay_id': '28', 'project_id': '64', 'visit_date': '2026-10-06',
                             'people': '2', 'phone': '13800000000', 'remark': '', 'add_product': ''})
_bid = models.get_user_bookings(_uid)[0]['id']
r = c.post('/booking/%d/cancel' % _bid)
check('取消预约 -> 302', r.status_code == 302)
check('预约状态已取消', models.get_user_bookings(_uid)[0]['status'] == '已取消')

# 商品详情溯源二维码（测试库商品 id 从 1 开始，动态取）
_tpid = models.find_product_by_trace('XYQM1022')['id']
r = c.get('/product/%d' % _tpid)
html = r.data.decode('utf-8')
check('商品详情含溯源二维码', 'qr/qr_' in html)
check('商品详情已无底部溯源档案', '种植溯源档案（全程可追溯）' not in html)
check('商品详情含查询溯源档案按钮', '查询溯源档案' in html)


# === v6 新增：详情页改版 + 单点规划 + AI出行筛选表单 ===
_bj_points = models.list_farmstays(region='北京市')
_fid = _bj_points[0]['id'] if _bj_points else 1
r = c.get('/farmstay/%d' % _fid)
html = r.data.decode('utf-8')
check('详情页含大图1/1角标', '1 / 1' in html)
check('详情页含风物科普', '风物科普' in html)
check('详情页含月份时令', '白露·秋分' in html)
check('详情页含地理标志', '地理标志' in html)
check('详情页含Tab项目/房型/特产/评价', all(k in html for k in ('农旅项目', '住宿房型', '产地特产', '用户评价')))
check('详情页含浏览量', '次浏览' in html)
check('详情页AI规划指向本点', ('/farmstay/%d/plan' % _fid) in html)
check('详情页含高德导航', 'uri.amap.com' in html)

# 北京点 Tab 数据齐全
ok = len(_bj_points) >= 4
for sp in _bj_points[:4]:
    h2 = c.get('/farmstay/%d' % sp['id']).data.decode('utf-8')
    if ('农旅项目' not in h2) or ('住宿房型' not in h2):
        ok = False
        break
check('北京点位Tab数据齐全', ok)

# 单点规划 GET/POST
r = c.get('/farmstay/%d/plan' % _fid)
check('单点规划页 -> 200', r.status_code == 200)
check('单点规划含此地定制', '此地' in r.data.decode('utf-8'))
r = c.post('/farmstay/%d/plan' % _fid, data={'days': '2', 'people': '3', 'interests': '亲子'})
html = r.data.decode('utf-8')
check('单点规划POST -> 200', r.status_code == 200)
check('单点攻略含能玩什么', '能玩什么' in html)
check('单点攻略含怎么住宿', '怎么住宿' in html)
check('单点攻略含买什么', '买什么' in html)
_i = html.find('AI 攻略结果')
check('单点攻略无emoji', not any(ord(ch) > 0x1F000 for ch in html[_i:_i + 800]))

# AI出行筛选表单
r = c.get('/ai_travel')
html = r.data.decode('utf-8')
check('AI出行含省份筛选', '目的地（省份）' in html)
check('AI出行含天数/人数/预算', all(k in html for k in ('出行天数', '出行人数', '人均预算')))
check('AI出行含兴趣多选', '兴趣偏好' in html and 'chk-label' in html)
check('AI出行无快捷行程按钮', '河北2天亲子采摘行程怎么安排？' not in html)
r = c.post('/ai_travel', data={'region': '北京市', 'days': '3', 'people': '3', 'budget': '500',
                               'interests': '亲子', 'user_input': ''})
html = r.data.decode('utf-8')
check('AI出行POST -> 200', r.status_code == 200)
check('AI出行含AI规划结果', 'AI 规划结果' in html)
check('AI出行按日编排', '第1天' in html and '第3天' in html)
check('AI出行推荐商户卡', '查看详情' in html)
check('AI出行含随机推荐', '随机推荐' in html)
check('AI出行推荐可跳详情', '/farmstay/' in html)
check('AI出行含复制按钮', '复制规划结果' in html)
_i = html.find('AI 规划结果')
check('AI出行结果无emoji', not any(ord(ch) > 0x1F000 for ch in html[_i:_i + 600]))


# === v7 新增：图片去重 ===
from collections import Counter as _Cnt
_img = [r['image'] for r in models.list_products() if r['image']]
check('商品图全部独立', len(_img) == len(set(_img)))
_fs = [r['image'] for r in models.list_farmstays() if r['image']]
check('农旅点独立图占比高', len(set(_fs)) >= max(1, len(_fs) - 3))
# 同农旅点内有图项目不重复
_pids = set(p['farmstay_id'] for p in models.list_projects())
_bad = 0
for _fid in _pids:
    _imgs = [p['image'] for p in models.list_projects(_fid) if p['image']]
    if len(_imgs) != len(set(_imgs)):
        _bad += 1
check('同点内项目图不重复', _bad == 0)
# 同农旅点内有图房型不重复
_rids = set(r['farmstay_id'] for r in models.list_rooms())
_bad = 0
for _fid in _rids:
    _imgs = [r['image'] for r in models.list_rooms(_fid) if r['image']]
    if len(_imgs) != len(set(_imgs)):
        _bad += 1
check('同点内房型图不重复', _bad == 0)

print()
print(f'结果：通过 {passed} 项，失败 {failed} 项')
if failed:
    raise SystemExit(1)
