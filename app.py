# -*- coding: utf-8 -*-
"""
乡约阡陌 —— AI赋能全国乡村农旅体验与助农服务平台（主程序）
技术栈：Python Flask + SQLite + 国产大模型API
角色：0游客 / 1商户 / 3平台管理员
运行：python app.py → 浏览器 http://127.0.0.1:5000
"""

import os
import datetime
import sys
from functools import wraps
from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash)

import models
import ai_helper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _resource_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


RESOURCE_DIR = _resource_dir()

app = Flask(__name__,
            template_folder=os.path.join(RESOURCE_DIR, 'templates'),
            static_folder=os.path.join(RESOURCE_DIR, 'static'))
app.secret_key = 'xiangyueqianmo-2026-secret-key'
app.config['SESSION_PERMANENT'] = False


# ================= 登录与权限 =================

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                flash('请先登录', 'warning')
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash('您没有权限访问该页面', 'danger')
                return redirect(url_for('index'))
            return view(*args, **kwargs)
        return wrapped
    return decorator


def get_user():
    if 'user_id' in session:
        return models.get_user_by_id(session['user_id'])
    return None


@app.context_processor
def inject_globals():
    u = get_user()
    return {'cart_count': models.get_cart_count(u['id']) if u else 0}


ROLE_NAMES = {0: '游客', 1: '商户', 3: '平台管理员'}


# ================= 公共：登录/注册 =================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        # 前端选择身份作为意向（游客0/商户1），后端以数据库真实角色为准
        user = models.get_user_by_name(username)
        if user and user['password'] == password:
            if user['status'] == '禁用':
                flash('账号已被禁用，请联系平台管理员', 'danger')
                return render_template('login.html')
            if user['role'] == 1 and user['status'] == '待审核':
                flash('商户入驻申请审核中，审核通过前请以游客身份使用', 'warning')
                return render_template('login.html')
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            # 按角色跳转
            if user['role'] == 1:
                return redirect(url_for('merchant_dashboard'))
            if user['role'] == 3:
                return redirect(url_for('admin_overview'))
            return redirect(url_for('index'))
        flash('用户名或密码错误', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        utype = request.form.get('utype', 'tourist')   # tourist游客 / merchant商户
        phone = request.form.get('phone', '').strip()
        region = request.form.get('region', '').strip()
        if not username or not password:
            flash('用户名和密码不能为空', 'danger')
        elif len(password) < 6:
            flash('密码至少6位', 'danger')
        elif utype == 'merchant':
            shop_name = request.form.get('shop_name', '').strip()
            shop_type = request.form.get('shop_type', '农户体验点')
            if not shop_name:
                flash('商户请填写店铺名称', 'danger')
            else:
                ok = models.create_user(username, password, role=1, phone=phone, region=region,
                                        shop_name=shop_name, shop_type=shop_type,
                                        shop_address=request.form.get('shop_address', ''),
                                        shop_desc=request.form.get('shop_desc', ''),
                                        status='待审核')
                if ok:
                    flash('商户入驻申请已提交，等待平台管理员审核', 'success')
                    return redirect(url_for('login'))
                flash('用户名已存在', 'danger')
        else:
            ok = models.create_user(username, password, role=0, phone=phone, region=region)
            if ok:
                flash('注册成功，请登录', 'success')
                return redirect(url_for('login'))
            flash('用户名已存在，请换一个', 'danger')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('login'))


# ================= 游客端 =================

@app.route('/')
def index():
    banners = models.list_banners()
    farmstays = models.list_farmstays()[:8]
    products = models.list_products()[:8]
    resources = models.list_resources()[:4]
    month = datetime.datetime.now().strftime('%m')
    notices = models.list_notices('启用')
    return render_template('index.html', banners=banners, farmstays=farmstays, month=month,
                           products=products, resources=resources, user=get_user(),
                           notices=notices, active='home')


@app.route('/farmstays')
def farmstay_list():
    region = request.args.get('region', '')
    category = request.args.get('category', '')
    keyword = request.args.get('keyword', '')
    sort = request.args.get('sort', '')
    rows = models.list_farmstays(region=region, category=category, keyword=keyword)
    if sort == 'price_asc':
        rows = sorted(rows, key=lambda r: r['price_min'])
    elif sort == 'price_desc':
        rows = sorted(rows, key=lambda r: r['price_min'], reverse=True)
    elif sort == 'score':
        rows = sorted(rows, key=lambda r: r['score'], reverse=True)
    categories = ['采摘体验', '农家住宿', '农家餐饮', '农耕研学', '非遗体验']
    # 全国地区筛选列表（从农旅数据提取 省-市）
    regions = []
    _seen = set()
    for _r in models.list_farmstays():
        _parts = (_r['region'] or '').split('-')
        if len(_parts) >= 2:
            _key = _parts[0] + '-' + _parts[1]
            if _key not in _seen:
                _seen.add(_key)
                regions.append({'value': _parts[1].replace('市', ''), 'label': _key})
    regions.sort(key=lambda x: x['label'])
    return render_template('farmstay_list.html', rows=rows, region=region,
                           category=category, keyword=keyword, categories=categories,
                           regions=regions,
                           user=get_user(), active='farmstays')


@app.route('/farmstay/<int:fid>')
def farmstay_detail(fid):
    fs = models.get_farmstay(fid)
    if not fs:
        flash('该农家乐不存在或已下架', 'warning')
        return redirect(url_for('farmstay_list'))
    models.inc_view(fid)
    fs = models.get_farmstay(fid)
    projects = models.list_projects(fid)
    rooms = models.list_rooms(fid)
    products = models.list_products(fid)
    reviews = models.list_reviews(fid)
    ai_knowledge = ai_helper.local_knowledge(fs['name'], fs['region'], fs['category'])
    merchant = models.get_user_by_id(fs['merchant_id'])
    months = ai_helper.month_season(int(datetime.datetime.now().strftime('%m')))
    geo = ai_helper.geo_products(fs['region'])
    tab = request.args.get('tab', 'projects')
    return render_template('farmstay_detail.html', fs=fs, projects=projects,
                           rooms=rooms, products=products, reviews=reviews,
                           ai_knowledge=ai_knowledge, merchant=merchant, user=get_user(),
                           months=months, geo=geo, tab=tab, active='farmstays')


@app.route('/farmstay/<int:fid>/plan', methods=['GET', 'POST'])
def farmstay_plan_page(fid):
    fs = models.get_farmstay(fid)
    if not fs:
        flash('该农旅点不存在或已下架', 'warning')
        return redirect(url_for('farmstay_list'))
    projects = models.list_projects(fid)
    rooms = models.list_rooms(fid)
    products = models.list_products(fid)
    merchant = models.get_user_by_id(fs['merchant_id'])
    result = None
    days, people = 1, 2
    interests = []
    if request.method == 'POST':
        days = int(request.form.get('days', 1))
        people = int(request.form.get('people', 2))
        interests = request.form.getlist('interests')
        result = ai_helper.farmstay_plan(fs, projects, rooms, products, merchant,
                                         days=days, people=people, interests=interests)
    months = ai_helper.month_season(int(datetime.datetime.now().strftime('%m')))
    geo = ai_helper.geo_products(fs['region'])
    return render_template('farmstay_plan.html', fs=fs, projects=projects,
                           rooms=rooms, products=products, merchant=merchant,
                           result=result, days=days, people=people, interests=interests,
                           months=months, geo=geo, user=get_user(), active='farmstays')


@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    if request.method == 'POST':
        fid = int(request.form.get('farmstay_id'))
        project_id = int(request.form.get('project_id') or 0)
        visit_date = request.form.get('visit_date', '')
        people = int(request.form.get('people', 1))
        phone = request.form.get('phone', '')
        remark = request.form.get('remark', '')
        add_product = 1 if request.form.get('add_product') else 0
        if not visit_date or not phone:
            flash('请填写出行日期和联系电话', 'danger')
            return redirect(url_for('farmstay_detail', fid=fid))
        no = models.create_booking(session['user_id'], fid, project_id, visit_date,
                                   people, phone, remark, add_product)
        # AI 出行备忘录
        fs = models.get_farmstay(fid)
        memo = ai_helper.local_travel_plan(f'去{fs["name"]} {visit_date} 共{people}人', fs['region'])
        return render_template('booking_success.html', booking_no=no,
                               memo=memo, fs=fs, user=get_user(), active='bookings')
    fid = request.args.get('farmstay_id', type=int)
    fs = models.get_farmstay(fid) if fid else None
    if not fs:
        flash('请选择要预约的农家乐', 'warning')
        return redirect(url_for('farmstay_list'))
    projects = models.list_projects(fid)
    return render_template('booking.html', fs=fs, projects=projects, user=get_user(),
                           active='bookings')


@app.route('/products')
def product_list():
    keyword = request.args.get('keyword', '')
    products = models.list_products(keyword=keyword)
    return render_template('product_list.html', products=products, keyword=keyword,
                           user=get_user(), active='products')


@app.route('/product/<int:pid>')
def product_detail(pid):
    p = models.get_product(pid)
    if not p:
        flash('商品不存在', 'warning')
        return redirect(url_for('product_list'))
    traces = models.get_trace_records(pid)
    fs = models.get_farmstay(p['farmstay_id'])
    return render_template('product_detail.html', p=p, traces=traces, fs=fs,
                           user=get_user(), active='products')


@app.route('/trace', methods=['GET', 'POST'])
def trace_query():
    """独立溯源码查询入口（游客可扫码/输码查看全程溯源）"""
    result = None
    code = ''
    if request.method == 'POST':
        code = request.form.get('code', '').strip().upper()
    else:
        code = request.args.get('code', '').strip().upper()
    if code:
        p = models.find_product_by_trace(code)
        if p:
            traces = models.get_trace_records(p['id'])
            farm = models.get_farmstay(p['farmstay_id']) if p['farmstay_id'] else None
            result = {'product': p, 'traces': traces, 'farm': farm}
        else:
            flash('未找到该溯源码对应的商品，请核对后重试', 'warning')
    return render_template('trace.html', result=result, code=code, user=get_user(),
                           active='trace')


@app.route('/product/order', methods=['POST'])
@login_required
def product_order():
    pid = int(request.form.get('product_id'))
    qty = int(request.form.get('quantity', 1))
    recv_name = request.form.get('recv_name', '').strip()
    recv_phone = request.form.get('recv_phone', '').strip()
    recv_address = request.form.get('recv_address', '').strip()
    if not (recv_name and recv_phone and recv_address):
        flash('请填写完整的收货人、联系电话与收货地址', 'danger')
        return redirect(url_for('product_detail', pid=pid))
    no = models.create_product_order(session['user_id'], pid, qty,
                                     recv_name=recv_name, recv_phone=recv_phone,
                                     recv_address=recv_address)
    flash(f'订单提交成功！订单号：{no}（产地直供演示，不涉及真实支付）', 'success')
    return redirect(url_for('my_orders'))


# ================= 购物车 =================
@app.route('/cart')
@login_required
def cart():
    items = models.get_cart(session['user_id'])
    total = sum((i['price'] or 0) * i['quantity'] for i in items if i['price'])
    return render_template('cart.html', items=items, total=total, user=get_user())


@app.route('/cart/add', methods=['POST'])
@login_required
def cart_add():
    pid = int(request.form.get('product_id'))
    qty = max(1, int(request.form.get('quantity', 1)))
    models.add_cart(session['user_id'], pid, qty)
    flash('已加入购物车', 'success')
    return redirect(request.referrer or url_for('product_detail', pid=pid))


@app.route('/cart/update', methods=['POST'])
@login_required
def cart_update():
    cid = int(request.form.get('cart_id'))
    qty = max(1, int(request.form.get('quantity', 1)))
    models.update_cart_qty(cid, qty)
    return redirect(url_for('cart'))


@app.route('/cart/remove', methods=['POST'])
@login_required
def cart_remove():
    cid = int(request.form.get('cart_id'))
    models.remove_cart_item(cid)
    return redirect(url_for('cart'))


@app.route('/cart/checkout', methods=['POST'])
@login_required
def cart_checkout():
    items = models.get_cart(session['user_id'])
    if not items:
        flash('购物车为空', 'danger')
        return redirect(url_for('cart'))
    recv_name = request.form.get('recv_name', '').strip()
    recv_phone = request.form.get('recv_phone', '').strip()
    recv_address = request.form.get('recv_address', '').strip()
    if not (recv_name and recv_phone and recv_address):
        flash('请填写完整的收货人、联系电话与收货地址', 'danger')
        return redirect(url_for('cart'))
    no_list = []
    for it in items:
        if not it['price']:
            continue
        no = models.create_product_order(session['user_id'], it['product_id'], it['quantity'],
                                         recv_name=recv_name, recv_phone=recv_phone,
                                         recv_address=recv_address)
        no_list.append(no)
    models.clear_cart(session['user_id'])
    flash('结算成功，共生成 %d 个订单（产地直供演示，不涉及真实支付）' % len(no_list), 'success')
    return redirect(url_for('my_orders'))


@app.route('/order/<int:oid>/cancel', methods=['POST'])
@login_required
def order_cancel(oid):
    order = models.get_product_order(oid)
    if order and order['user_id'] == session['user_id']:
        models.cancel_product_order(oid)
        flash('订单已取消', 'success')
    else:
        flash('订单不存在', 'danger')
    return redirect(url_for('my_orders'))


@app.route('/order/<int:oid>/refund', methods=['POST'])
@login_required
def order_refund(oid):
    order = models.get_product_order(oid)
    reason = request.form.get('reason', '').strip()
    if order and order['user_id'] == session['user_id'] and reason:
        models.apply_refund_product_order(oid, reason)
        flash('退款申请已提交，等待商家处理', 'success')
    else:
        flash('请填写退款原因', 'danger')
    return redirect(url_for('my_orders'))


@app.route('/merchant/order/cancel', methods=['POST'])
@role_required(1)
def merchant_order_cancel():
    oid = int(request.form.get('order_id'))
    models.cancel_product_order(oid)
    flash('订单已取消', 'success')
    return redirect(url_for('merchant_orders'))


@app.route('/merchant/order/refund', methods=['POST'])
@role_required(1)
def merchant_order_refund():
    oid = int(request.form.get('order_id'))
    action = request.form.get('action', 'reject')
    models.process_refund_product_order(oid, approve=(action == 'approve'))
    flash('退款申请已处理' if action == 'approve' else '已驳回退款申请', 'success')
    return redirect(url_for('merchant_orders'))


@app.route('/admin/order/refund', methods=['POST'])
@role_required(3)
def admin_order_refund():
    oid = int(request.form.get('order_id'))
    action = request.form.get('action', 'reject')
    models.process_refund_product_order(oid, approve=(action == 'approve'))
    flash('退款申请已处理' if action == 'approve' else '已驳回退款申请', 'success')
    return redirect(url_for('admin_orders'))


# ================= 系统公告 =================
@app.route('/admin/notices')
@role_required(3)
def admin_notices():
    rows = models.list_notices()
    return render_template('admin/notices.html', rows=rows, user=get_user())


@app.route('/admin/notice/add', methods=['POST'])
@role_required(3)
def admin_notice_add():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    if title and content:
        models.add_notice(title, content)
        flash('公告已发布', 'success')
    else:
        flash('请填写公告标题与内容', 'danger')
    return redirect(url_for('admin_notices'))


@app.route('/admin/notice/delete', methods=['POST'])
@role_required(3)
def admin_notice_delete():
    nid = int(request.form.get('notice_id'))
    models.delete_notice(nid)
    flash('公告已删除', 'success')
    return redirect(url_for('admin_notices'))


@app.route('/admin/notice/toggle', methods=['POST'])
@role_required(3)
def admin_notice_toggle():
    nid = int(request.form.get('notice_id'))
    status = request.form.get('status', '启用')
    models.toggle_notice(nid, status)
    return redirect(url_for('admin_notices'))


@app.route('/resources')
def resource_list():
    rtype = request.args.get('rtype', '')
    keyword = request.args.get('keyword', '')
    region = request.args.get('region', '')
    rows = models.list_resources(rtype=rtype, keyword=keyword, region=region)
    region_opts = []
    _seen = set()
    for _r in models.list_resources():
        _p = (_r['region'] or '').split('-')[0]
        if _p and _p not in _seen:
            _seen.add(_p)
            region_opts.append(_p)
    region_opts.sort()
    return render_template('resource_list.html', rows=rows, rtype=rtype,
                           keyword=keyword, region=region, region_opts=region_opts,
                           user=get_user(), active='resources')


@app.route('/resource/<int:rid>')
def resource_detail(rid):
    r = models.get_resource(rid)
    if not r:
        flash('该资源不存在或已下架', 'warning')
        return redirect(url_for('resource_list'))
    same = models.list_resources(rtype=r['rtype'])[:4]
    same = [x for x in same if x['id'] != r['id']]
    nearby = models.list_resources(region=r['region'][:3])[:4]
    nearby = [x for x in nearby if x['id'] != r['id']]
    return render_template('resource_detail.html', r=r, same=same, nearby=nearby,
                           user=get_user(), active='resources')


@app.route('/resource/<int:rid>/intent', methods=['POST'])
@login_required
def resource_intent(rid):
    message = request.form.get('message', '').strip()
    models.add_resource_intent(rid, session['user_id'], message)
    flash('对接意向已提交，平台将协助您与发布者对接', 'success')
    return redirect(url_for('resource_detail', rid=rid))


@app.route('/resource/publish', methods=['GET', 'POST'])
@login_required
def resource_publish():
    if request.method == 'POST':
        rtype = request.form.get('rtype', '闲置农具')
        title = request.form.get('title', '').strip()
        region = request.form.get('region', '').strip()
        description = request.form.get('description', '').strip()
        price = float(request.form.get('price', 0))
        contact = request.form.get('contact', '').strip()
        if not title:
            flash('请填写资源标题', 'danger')
        else:
            models.add_resource(session['user_id'], rtype, title, region,
                                description, price, contact)
            flash('资源发布成功！AI匹配已启用', 'success')
            return redirect(url_for('resource_list'))
    return render_template('resource_publish.html', user=get_user(), active='resources')


@app.route('/resource/match', methods=['POST'])
def resource_match():
    need = request.form.get('need', '').strip()
    region = request.form.get('region', '').strip()
    if not need:
        flash('请输入您的需求', 'warning')
        return redirect(url_for('resource_list'))
    result = ai_helper.resource_match(need, region)
    rows = models.list_resources(keyword=need)
    return render_template('resource_list.html', rows=rows, match_result=result,
                           need=need, user=get_user(), active='resources')


@app.route('/ai_travel', methods=['GET', 'POST'])
def ai_travel():
    import random
    import re
    result = None
    user_input = ''
    picked = '不限'
    days, people, budget = 2, 2, 0
    interests = []
    quick = request.args.get('quick', '')
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        picked = request.form.get('region', '不限')
        days = int(request.form.get('days', 2) or 2)
        people = int(request.form.get('people', 2) or 2)
        budget = int(request.form.get('budget', 0) or 0)
        interests = request.form.getlist('interests')
        # ===== 自由文本智能解析：从一句话出行想法中识别省份/天数/预算/兴趣 =====
        if user_input:
            # 1) 省份识别
            for kw, prov in [('北京', '北京市'), ('天津', '天津市'), ('上海', '上海市'),
                             ('重庆', '重庆市'), ('广东', '广东省'), ('浙江', '浙江省'),
                             ('江苏', '江苏省'), ('山东', '山东省'), ('四川', '四川省'),
                             ('云南', '云南省'), ('陕西', '陕西省'), ('湖南', '湖南省'),
                             ('湖北', '湖北省'), ('河南', '河南省'), ('河北', '河北省'),
                             ('辽宁', '辽宁省'), ('吉林', '吉林省'), ('黑龙江', '黑龙江省'),
                             ('安徽', '安徽省'), ('福建', '福建省'), ('江西', '江西省'),
                             ('海南', '海南省'), ('贵州', '贵州省'), ('甘肃', '甘肃省'),
                             ('青海', '青海省'), ('山西', '山西省'), ('广西', '广西省'),
                             ('新疆', '新疆省'), ('西藏', '西藏'), ('内蒙古', '内蒙古'),
                             ('宁夏', '宁夏'), ('台湾', '台湾'), ('香港', '香港'), ('澳门', '澳门')]:
                if kw in user_input:
                    picked = prov
                    break
            # 2) 天数识别（如“2天”“两天”“3天2晚”）
            m = re.search(r'(\d+)\s*天', user_input)
            if not m:
                cn = {'一': 1, '两': 2, '二': 2, '三': 3, '四': 4, '五': 5,
                      '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
                m2 = re.search(r'([一两二三四五六七八九十]+)\s*天', user_input)
                if m2:
                    w = m2.group(1)
                    days = cn.get(w, sum(cn.get(c, 0) for c in w) or 2)
                    days = min(max(days, 1), 10)
            else:
                days = min(max(int(m.group(1)), 1), 10)
            # 3) 预算识别（如“800元”“预算800”“800块钱”“800左右”）
            m = re.search(r'(\d+)\s*(?:元|块钱|块|左右|以内)', user_input)
            if not m:
                m = re.search(r'预算\s*(\d+)', user_input)
            if m:
                budget = min(int(m.group(1)), 5000)
            # 4) 兴趣识别
            for it in ['采摘', '亲子', '研学', '团建', '民宿', '非遗', '草原',
                       '梯田', '美食', '康养', '星空', '露营', '古镇', '山水']:
                if it in user_input and it not in interests:
                    interests.append(it)
        result = ai_helper.travel_plan(user_input, picked, days, people, budget, interests)
    # 按地区+预算+兴趣推荐真实商户（去AI味：只推平台登记商户）
    spots = models.list_farmstays(region=picked if picked != '不限' else '')
    _cat_map = {'采摘': '采摘体验', '研学': '农耕研学', '民宿': '农家住宿',
                '非遗': '非遗体验', '美食': '农家餐饮'}
    _cat = [_cat_map[i] for i in interests if i in _cat_map]
    if _cat:
        filtered = [x for x in spots if x['category'] in _cat]
        if filtered:
            spots = filtered
    if budget and budget > 0:
        spots = [x for x in spots if x['price_min'] <= budget]
    # 随机推荐优先从地区匹配点位中选（参考图4商户卡）
    hot = None
    if spots:
        hot = random.choice(spots)
    if len(spots) < 4:
        others = models.list_farmstays()
        seen = {x['id'] for x in spots}
        for x in others:
            if x['id'] not in seen:
                spots.append(x)
                seen.add(x['id'])
            if len(spots) >= 6:
                break
    spots = spots[:6]
    if hot is None and spots:
        hot = random.choice(spots)
    regions_all = [r['region'].split('-')[0] for r in models.list_farmstays() if r['region']]
    regions = sorted(set(regions_all))
    return render_template('ai_travel.html', result=result, user_input=user_input,
                           spots=spots, picked=picked, days=days, people=people,
                           budget=budget, interests=interests, hot=hot, quick=quick,
                           regions=regions, user=get_user(), active='ai')


@app.route('/my/bookings')
@login_required
def my_bookings():
    rows = models.get_user_bookings(session['user_id'])
    return render_template('my_bookings.html', rows=rows, user=get_user(), active='bookings')


@app.route('/booking/<int:bid>/cancel', methods=['POST'])
@login_required
def cancel_booking(bid):
    models.cancel_booking(bid, session['user_id'])
    flash('预约已取消', 'success')
    return redirect(url_for('my_bookings'))


@app.route('/my/orders')
@login_required
def my_orders():
    rows = models.get_user_product_orders(session['user_id'])
    return render_template('my_orders.html', rows=rows, user=get_user(), active='orders')


@app.route('/my/favorites')
@login_required
def my_favorites():
    favs = models.get_user_favorites(session['user_id'])
    items = []
    for f in favs:
        if f['target_type'] == 'farmstay':
            fs = models.get_farmstay(f['target_id'])
            if fs:
                items.append(('农家乐', fs['name'], fs['region'], f'/farmstay/{fs["id"]}'))
        else:
            p = models.get_product(f['target_id'])
            if p:
                items.append(('特产', p['name'], p['origin'], f'/product/{p["id"]}'))
    return render_template('my_favorites.html', items=items, user=get_user(), active='favorites')


@app.route('/favorite', methods=['POST'])
@login_required
def favorite():
    target_type = request.form.get('target_type', 'farmstay')
    target_id = int(request.form.get('target_id'))
    added = models.toggle_favorite(session['user_id'], target_type, target_id)
    flash('已加入收藏' if added else '已取消收藏', 'success')
    return redirect(request.referrer or url_for('index'))


@app.route('/my/reviews', methods=['GET', 'POST'])
@login_required
def my_reviews():
    if request.method == 'POST':
        fid = int(request.form.get('farmstay_id'))
        rating = int(request.form.get('rating', 5))
        content = request.form.get('content', '').strip()
        if content:
            models.add_review(session['user_id'], fid, rating, content)
            flash('评价发布成功', 'success')
            return redirect(url_for('my_reviews'))
    rows = models.list_reviews()
    mine = [r for r in rows if r['user_id'] == session['user_id']]
    farmstays = models.list_farmstays()
    return render_template('my_reviews.html', rows=mine, farmstays=farmstays,
                           user=get_user(), active='reviews')


@app.route('/my/profile', methods=['GET', 'POST'])
@login_required
def my_profile():
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        region = request.form.get('region', '').strip()
        models.update_user(session['user_id'], phone=phone, region=region)
        flash('个人资料已更新', 'success')
        return redirect(url_for('my_profile'))
    stats = models.count_user_data(session['user_id'])
    bookings = models.get_user_bookings(session['user_id'])
    favs = models.get_user_favorites(session['user_id'])
    items = []
    for f in favs:
        if f['target_type'] == 'farmstay':
            fs = models.get_farmstay(f['target_id'])
            if fs:
                items.append(('农家乐', fs['name'], fs['region'], '/farmstay/%d' % fs['id']))
        else:
            p = models.get_product(f['target_id'])
            if p:
                items.append(('特产', p['name'], p['origin'], '/product/%d' % p['id']))
    rows = models.list_reviews()
    mine = [r for r in rows if r['user_id'] == session['user_id']]
    intents = models.list_user_intents(session['user_id'])
    return render_template('my_profile.html', user=get_user(), active='profile',
                           stats=stats, bookings=bookings, favorites=items,
                           reviews=mine, intents=intents,
                           tab=request.args.get('tab', 'bookings'))


# ================= 商户端 =================

@app.route('/merchant')
@role_required(1)
def merchant_dashboard():
    stats = models.merchant_stats(session['user_id'])
    bookings = models.list_all_bookings(merchant_id=session['user_id'])
    order_stats = models.merchant_order_stats(session['user_id'])
    booking_stats = {}
    for b in bookings:
        booking_stats[b['status']] = booking_stats.get(b['status'], 0) + 1
    # 近7日趋势（商户：按最近7天新增订单——商户数据少，直接用全量明细演示）
    trend = models.order_daily_trend(7)
    return render_template('merchant/dashboard.html', stats=stats,
                           bookings=bookings[:5], user=get_user(),
                           order_stats=order_stats, booking_stats=booking_stats,
                           trend=trend)


@app.route('/merchant/orders')
@role_required(1)
def merchant_orders():
    rows = models.list_all_product_orders(merchant_id=session['user_id'])
    import datetime
    now = (datetime.date.today() + datetime.timedelta(days=3)).strftime('%Y-%m-%d')
    return render_template('merchant/orders.html', rows=rows, user=get_user(), now=now)


@app.route('/merchant/order/ship', methods=['POST'])
@role_required(1)
def merchant_order_ship():
    oid = int(request.form.get('order_id'))
    company = request.form.get('company_name', '').strip() or '顺丰快递'
    tracking = request.form.get('tracking_number', '').strip() or ('SF' + ''.join(__import__('random').choices('0123456789', k=10)))
    arrival = request.form.get('expected_arrival', '').strip()
    models.ship_product_order(oid, company, tracking, arrival)
    flash('发货成功，物流轨迹已生成', 'success')
    return redirect(url_for('merchant_orders'))


@app.route('/merchant/order/sign', methods=['POST'])
@role_required(1)
def merchant_order_sign():
    oid = int(request.form.get('order_id'))
    models.sign_product_order(oid)
    flash('已标记签收', 'success')
    return redirect(url_for('merchant_orders'))


@app.route('/admin/orders')
@role_required(3)
def admin_orders():
    rows = models.list_all_product_orders()
    return render_template('admin/orders.html', rows=rows, user=get_user())


@app.route('/order/<int:oid>/logistics')
@login_required
def order_logistics(oid):
    order = models.get_product_order(oid)
    if not order:
        flash('订单不存在', 'danger')
        return redirect(url_for('my_orders'))
    tracks = models.get_logistics_tracks(oid)
    return render_template('logistics.html', order=order, tracks=tracks, user=get_user())


@app.route('/merchant/shop')
@role_required(1)
def merchant_shop():
    user = get_user()
    farmstays = models.list_farmstays(merchant_id=user['id'])
    return render_template('merchant/shop.html', user=user, farmstays=farmstays)


@app.route('/merchant/shop/save', methods=['POST'])
@role_required(1)
def merchant_shop_save():
    shop_name = request.form.get('shop_name', '').strip()
    shop_address = request.form.get('shop_address', '').strip()
    shop_desc = request.form.get('shop_desc', '').strip()
    phone = request.form.get('phone', '').strip()
    models.update_user(session['user_id'], shop_name=shop_name,
                       shop_address=shop_address, shop_desc=shop_desc, phone=phone)
    flash('店铺信息已保存', 'success')
    return redirect(url_for('merchant_shop'))


@app.route('/merchant/add_farmstay', methods=['POST'])
@role_required(1)
def merchant_add_farmstay():
    name = request.form.get('name', '').strip()
    region = request.form.get('region', '').strip()
    address = request.form.get('address', '').strip()
    category = request.form.get('category', '采摘体验')
    price_min = float(request.form.get('price_min', 0))
    tags = request.form.get('tags', '').strip()
    description = request.form.get('description', '').strip()
    if not name:
        flash('请填写点位名称', 'danger')
    else:
        models.add_farmstay(session['user_id'], name, region, address, category,
                            price_min, tags, description)
        flash('农旅点位创建成功', 'success')
    return redirect(url_for('merchant_shop'))


@app.route('/merchant/projects')
@role_required(1)
def merchant_projects():
    user = get_user()
    farmstays = models.list_farmstays(merchant_id=user['id'])
    projects = []
    for fs in farmstays:
        for pj in models.list_projects(fs['id']):
            projects.append({'pj': pj, 'fs': fs})
    return render_template('merchant/projects.html', projects=projects,
                           farmstays=farmstays, user=get_user())


@app.route('/merchant/project/add', methods=['POST'])
@role_required(1)
def merchant_project_add():
    fid = int(request.form.get('farmstay_id'))
    name = request.form.get('name', '').strip()
    price = float(request.form.get('price', 0))
    unit = request.form.get('unit', '人/次')
    open_time = request.form.get('open_time', '全天')
    if name and price > 0:
        models.add_project(fid, name, price, unit, open_time)
        flash('项目已添加', 'success')
    else:
        flash('请填写完整项目信息', 'danger')
    return redirect(url_for('merchant_projects'))


@app.route('/merchant/project/update', methods=['POST'])
@role_required(1)
def merchant_project_update():
    pid = int(request.form.get('project_id'))
    status = request.form.get('status', '上架')
    models.update_project(pid, status=status)
    flash('项目状态已更新', 'success')
    return redirect(url_for('merchant_projects'))


@app.route('/merchant/project/edit', methods=['POST'])
@role_required(1)
def merchant_project_edit():
    pid = int(request.form.get('project_id'))
    fid = int(request.form.get('farmstay_id'))
    name = request.form.get('name', '').strip()
    price = float(request.form.get('price', 0))
    unit = request.form.get('unit', '人/次')
    open_time = request.form.get('open_time', '全天')
    status = request.form.get('status', '上架')
    if name and price > 0:
        models.update_project(pid, farmstay_id=fid, name=name, price=price,
                              unit=unit, open_time=open_time, status=status)
        flash('项目内容已更新', 'success')
    else:
        flash('请填写完整项目信息', 'danger')
    return redirect(url_for('merchant_projects'))


@app.route('/merchant/project/delete', methods=['POST'])
@role_required(1)
def merchant_project_delete():
    pid = int(request.form.get('project_id'))
    models.delete_project(pid)
    flash('项目已删除', 'success')
    return redirect(url_for('merchant_projects'))


@app.route('/merchant/rooms')
@role_required(1)
def merchant_rooms():
    user = get_user()
    farmstays = models.list_farmstays(merchant_id=user['id'])
    rooms = []
    for fs in farmstays:
        for rm in models.list_rooms(fs['id']):
            rooms.append({'rm': rm, 'fs': fs})
    return render_template('merchant/rooms.html', rooms=rooms, farmstays=farmstays,
                           user=get_user())


@app.route('/merchant/room/add', methods=['POST'])
@role_required(1)
def merchant_room_add():
    fid = int(request.form.get('farmstay_id'))
    name = request.form.get('name', '').strip()
    beds = int(request.form.get('beds', 1))
    price = float(request.form.get('price', 0))
    stock = int(request.form.get('stock', 1))
    if name and price > 0:
        models.add_room(fid, name, beds, price, stock)
        flash('房型已添加', 'success')
    return redirect(url_for('merchant_rooms'))


@app.route('/merchant/room/update', methods=['POST'])
@role_required(1)
def merchant_room_update():
    rid = int(request.form.get('room_id'))
    status = request.form.get('status', '上架')
    models.update_room(rid, status=status)
    flash('房型状态已更新', 'success')
    return redirect(url_for('merchant_rooms'))


@app.route('/merchant/room/edit', methods=['POST'])
@role_required(1)
def merchant_room_edit():
    rid = int(request.form.get('room_id'))
    fid = int(request.form.get('farmstay_id'))
    name = request.form.get('name', '').strip()
    beds = int(request.form.get('beds', 1))
    price = float(request.form.get('price', 0))
    stock = int(request.form.get('stock', 1))
    status = request.form.get('status', '上架')
    if name and price > 0:
        models.update_room(rid, farmstay_id=fid, name=name, beds=beds,
                           price=price, stock=stock, status=status)
        flash('房型内容已更新', 'success')
    else:
        flash('请填写完整房型信息', 'danger')
    return redirect(url_for('merchant_rooms'))


@app.route('/merchant/room/delete', methods=['POST'])
@role_required(1)
def merchant_room_delete():
    rid = int(request.form.get('room_id'))
    models.delete_room(rid)
    flash('房型已删除', 'success')
    return redirect(url_for('merchant_rooms'))


@app.route('/merchant/products')
@role_required(1)
def merchant_products():
    user = get_user()
    farmstays = models.list_farmstays(merchant_id=user['id'])
    products = []
    for fs in farmstays:
        for pd in models.list_products(fs['id']):
            products.append({'pd': pd, 'fs': fs})
    return render_template('merchant/products.html', products=products,
                           farmstays=farmstays, user=get_user())


@app.route('/merchant/product/add', methods=['POST'])
@role_required(1)
def merchant_product_add():
    fid = int(request.form.get('farmstay_id'))
    name = request.form.get('name', '').strip()
    price = float(request.form.get('price', 0))
    unit = request.form.get('unit', '斤')
    stock = int(request.form.get('stock', 0))
    description = request.form.get('description', '').strip()
    origin = request.form.get('origin', '').strip()
    if name and price > 0:
        pid, code = models.add_product(fid, name, price, unit, stock, description, origin)
        # 默认溯源记录
        for stage, loc, detail, rec in [
            ('种植', origin, '农家肥种植，不使用化学农药。', '农户'),
            ('采摘', origin, '成熟期人工采摘，精选优质品。', '农户'),
            ('检测', '县级质检站', '农残检测合格。', '质检站'),
            ('上架', '乡约阡陌平台', '产地直供，溯源完整。', '平台'),
        ]:
            models.add_trace_record(pid, stage, loc, detail, rec)
        flash(f'特产上架成功！溯源码：{code}', 'success')
    else:
        flash('请填写完整商品信息', 'danger')
    return redirect(url_for('merchant_products'))


@app.route('/merchant/product/update', methods=['POST'])
@role_required(1)
def merchant_product_update():
    pid = int(request.form.get('product_id'))
    status = request.form.get('status', '上架')
    models.update_product(pid, status=status)
    flash('商品状态已更新', 'success')
    return redirect(url_for('merchant_products'))


@app.route('/merchant/product/edit', methods=['POST'])
@role_required(1)
def merchant_product_edit():
    pid = int(request.form.get('product_id'))
    fid = int(request.form.get('farmstay_id'))
    name = request.form.get('name', '').strip()
    price = float(request.form.get('price', 0))
    unit = request.form.get('unit', '斤')
    stock = int(request.form.get('stock', 0))
    description = request.form.get('description', '').strip()
    origin = request.form.get('origin', '').strip()
    status = request.form.get('status', '上架')
    if name and price > 0:
        models.update_product(pid, farmstay_id=fid, name=name, price=price,
                              unit=unit, stock=stock, description=description,
                              origin=origin, status=status)
        flash('商品内容已更新', 'success')
    else:
        flash('请填写完整商品信息', 'danger')
    return redirect(url_for('merchant_products'))


@app.route('/merchant/product/delete', methods=['POST'])
@role_required(1)
def merchant_product_delete():
    pid = int(request.form.get('product_id'))
    models.delete_product(pid)
    flash('商品已删除', 'success')
    return redirect(url_for('merchant_products'))


@app.route('/merchant/trace/add', methods=['POST'])
@role_required(1)
def merchant_trace_add():
    pid = int(request.form.get('product_id'))
    stage = request.form.get('stage', '').strip()
    location = request.form.get('location', '').strip()
    detail = request.form.get('detail', '').strip()
    if stage and detail:
        models.add_trace_record(pid, stage, location, detail, session['username'])
        flash('溯源记录已添加', 'success')
    return redirect(url_for('merchant_products'))


@app.route('/merchant/bookings')
@role_required(1)
def merchant_bookings():
    rows = models.list_all_bookings(merchant_id=session['user_id'])
    return render_template('merchant/bookings.html', rows=rows, user=get_user())


@app.route('/merchant/booking/update', methods=['POST'])
@role_required(1)
def merchant_booking_update():
    bid = int(request.form.get('booking_id'))
    status = request.form.get('status', '待审核')
    models.update_booking(bid, status=status)
    flash('预约状态已更新', 'success')
    return redirect(url_for('merchant_bookings'))


@app.route('/merchant/reviews')
@role_required(1)
def merchant_reviews():
    user = get_user()
    farmstays = models.list_farmstays(merchant_id=user['id'])
    fids = [f['id'] for f in farmstays]
    rows = []
    for fid in fids:
        rows += models.list_reviews(farmstay_id=fid)
    return render_template('merchant/reviews.html', rows=rows, user=get_user())


@app.route('/merchant/review/reply', methods=['POST'])
@role_required(1)
def merchant_review_reply():
    rid = int(request.form.get('review_id'))
    reply = request.form.get('reply', '').strip()
    models.update_review(rid, reply=reply)
    flash('回复已发布', 'success')
    return redirect(url_for('merchant_reviews'))


@app.route('/merchant/ai', methods=['GET', 'POST'])
@role_required(1)
def merchant_ai():
    result = None
    mode = request.form.get('mode', '')
    if request.method == 'POST':
        if mode == 'copy':
            kw = request.form.get('keywords', '').strip()
            scene = request.form.get('scene', '店铺简介')
            if kw:
                result = ai_helper.gen_copy(kw, scene)
        elif mode == 'festival':
            season = request.form.get('season', '').strip()
            shop = request.form.get('shop_info', '').strip()
            if season:
                result = ai_helper.festival_plan(season, shop)
        elif mode == 'review':
            reviews = request.form.get('reviews_text', '').strip()
            if reviews:
                result = ai_helper.review_analysis(reviews)
    return render_template('merchant/ai.html', result=result, user=get_user())


# ================= 管理端 =================

@app.route('/admin')
@role_required(3)
def admin_overview():
    stats = models.platform_stats()
    order_stats = models.order_status_stats()
    trend = models.order_daily_trend(7)
    # 农旅分类分布
    cats = {}
    for f in models.list_farmstays():
        cats[f['category']] = cats.get(f['category'], 0) + 1
    # 用户角色分布
    roles = {}
    for r in models.list_users():
        roles[r['role']] = roles.get(r['role'], 0) + 1
    # 预约状态分布
    bstats = {}
    for b in models.list_all_bookings():
        bstats[b['status']] = bstats.get(b['status'], 0) + 1
    return render_template('admin/overview.html', stats=stats, user=get_user(),
                           order_stats=order_stats, trend=trend, cat_stats=cats,
                           role_stats=roles, booking_stats=bstats)


@app.route('/admin/merchants')
@role_required(3)
def admin_merchants():
    rows = models.list_users(role=1)
    return render_template('admin/merchants.html', rows=rows, user=get_user())


@app.route('/admin/merchant/audit', methods=['POST'])
@role_required(3)
def admin_merchant_audit():
    uid = int(request.form.get('user_id'))
    action = request.form.get('action', '正常')
    status = '正常' if action == 'pass' else '驳回'
    models.update_user(uid, status=status)
    flash('审核操作完成', 'success')
    return redirect(url_for('admin_merchants'))


@app.route('/admin/farmstays')
@role_required(3)
def admin_farmstays():
    rows = models.list_all_admin_farmstays()
    return render_template('admin/farmstays.html', rows=rows, user=get_user())


@app.route('/admin/farmstay/update', methods=['POST'])
@role_required(3)
def admin_farmstay_update():
    fid = int(request.form.get('farmstay_id'))
    status = request.form.get('status', '上架')
    models.update_farmstay(fid, status=status)
    flash('内容状态已更新', 'success')
    return redirect(url_for('admin_farmstays'))


@app.route('/admin/farmstay/add', methods=['POST'])
@role_required(3)
def admin_farmstay_add():
    name = request.form.get('name', '').strip()
    if not name:
        flash('点位名称不能为空', 'danger')
        return redirect(url_for('admin_farmstays'))
    region = request.form.get('region', '').strip() or '待定'
    address = request.form.get('address', '').strip()
    category = request.form.get('category', '采摘体验').strip()
    try:
        price_min = float(request.form.get('price_min', 0) or 0)
    except ValueError:
        price_min = 0
    tags = request.form.get('tags', '').strip()
    description = request.form.get('description', '').strip()
    image = request.form.get('image', '').strip() or 'farm_default.jpg'
    merchant_id = int(request.form.get('merchant_id', 1) or 1)
    models.add_farmstay(merchant_id, name, region, address, category, price_min,
                        tags, description, image=image)
    flash(f'点位「{name}」已新增', 'success')
    return redirect(url_for('admin_farmstays'))


@app.route('/admin/farmstay/edit', methods=['POST'])
@role_required(3)
def admin_farmstay_edit():
    fid = int(request.form.get('farmstay_id'))
    name = request.form.get('name', '').strip()
    if not name:
        flash('点位名称不能为空', 'danger')
        return redirect(url_for('admin_farmstays'))
    try:
        price_min = float(request.form.get('price_min', 0) or 0)
    except ValueError:
        price_min = 0
    models.update_farmstay(
        fid, name=name, region=request.form.get('region', '').strip() or '待定',
        address=request.form.get('address', '').strip(),
        category=request.form.get('category', '采摘体验').strip(),
        price_min=price_min,
        tags=request.form.get('tags', '').strip(),
        description=request.form.get('description', '').strip(),
        image=request.form.get('image', '').strip() or 'farm_default.jpg',
        status=request.form.get('status', '上架'))
    flash('点位信息已更新', 'success')
    return redirect(url_for('admin_farmstays'))


@app.route('/admin/farmstay/delete', methods=['POST'])
@role_required(3)
def admin_farmstay_delete():
    fid = int(request.form.get('farmstay_id'))
    models.delete_farmstay(fid)
    flash('点位已删除', 'success')
    return redirect(url_for('admin_farmstays'))


@app.route('/admin/products')
@role_required(3)
def admin_products():
    rows = models.list_products()
    return render_template('admin/products.html', rows=rows, user=get_user())


@app.route('/admin/product/update', methods=['POST'])
@role_required(3)
def admin_product_update():
    pid = int(request.form.get('product_id'))
    status = request.form.get('status', '上架')
    models.update_product(pid, status=status)
    flash('商品状态已更新', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/product/add', methods=['POST'])
@role_required(3)
def admin_product_add():
    name = request.form.get('name', '').strip()
    if not name:
        flash('特产名称不能为空', 'danger')
        return redirect(url_for('admin_products'))
    try:
        farmstay_id = int(request.form.get('farmstay_id', 1) or 1)
        price = float(request.form.get('price', 0) or 0)
        stock = int(request.form.get('stock', 100) or 100)
    except ValueError:
        flash('价格或库存格式不正确', 'danger')
        return redirect(url_for('admin_products'))
    unit = request.form.get('unit', '份').strip() or '份'
    origin = request.form.get('origin', '').strip() or '待定'
    description = request.form.get('description', '').strip()
    trace_code = request.form.get('trace_code', '').strip().upper()
    image = request.form.get('image', '').strip() or 'product_default.jpg'
    pid = models.add_product(farmstay_id, name, price, unit, stock, description,
                             origin, trace_code=trace_code, image=image)
    # 若填写了溯源码，自动生成对应二维码
    if trace_code:
        try:
            models.gen_qr('https://466e522f.r1.cpolar.top/trace?code=' + trace_code,
                          'static/qr/qr_%d.png' % pid)
        except Exception:
            pass
    flash(f'特产「{name}」已新增并生成溯源码', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/product/edit', methods=['POST'])
@role_required(3)
def admin_product_edit():
    pid = int(request.form.get('product_id'))
    name = request.form.get('name', '').strip()
    if not name:
        flash('特产名称不能为空', 'danger')
        return redirect(url_for('admin_products'))
    try:
        price = float(request.form.get('price', 0) or 0)
        stock = int(request.form.get('stock', 100) or 100)
    except ValueError:
        flash('价格或库存格式不正确', 'danger')
        return redirect(url_for('admin_products'))
    models.update_product(
        pid, name=name, price=price, unit=request.form.get('unit', '份').strip() or '份',
        stock=stock, origin=request.form.get('origin', '').strip() or '待定',
        description=request.form.get('description', '').strip(),
        status=request.form.get('status', '上架'))
    flash('特产信息已更新', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/product/delete', methods=['POST'])
@role_required(3)
def admin_product_delete():
    pid = int(request.form.get('product_id'))
    models.delete_product(pid)
    flash('特产已删除', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/users')
@role_required(3)
def admin_users():
    rows = models.list_users()
    return render_template('admin/users.html', rows=rows, user=get_user())


@app.route('/admin/user/update', methods=['POST'])
@role_required(3)
def admin_user_update():
    uid = int(request.form.get('user_id'))
    status = request.form.get('status', '正常')
    models.update_user(uid, status=status)
    flash('账号状态已更新', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/user/create', methods=['POST'])
@role_required(3)
def admin_user_create():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '123456')
    role = int(request.form.get('role', 0))
    region = request.form.get('region', '').strip()
    if username:
        ok = models.create_user(username, password, role=role, region=region)
        flash('管理员账号创建成功' if ok else '用户名已存在', 'success' if ok else 'danger')
    return redirect(url_for('admin_users'))


@app.route('/admin/reviews')
@role_required(3)
def admin_reviews():
    rows = models.list_reviews()
    return render_template('admin/reviews.html', rows=rows, user=get_user())


@app.route('/admin/review/update', methods=['POST'])
@role_required(3)
def admin_review_update():
    rid = int(request.form.get('review_id'))
    status = request.form.get('status', '正常')
    models.update_review(rid, status=status)
    flash('评价状态已更新', 'success')
    return redirect(url_for('admin_reviews'))


@app.route('/admin/banners', methods=['GET', 'POST'])
@role_required(3)
def admin_banners():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        link = request.form.get('link', '/')
        image = request.form.get('image', 'banner1.jpg')
        if title:
            models.add_banner(title, image, link)
            flash('轮播图已添加', 'success')
        return redirect(url_for('admin_banners'))
    rows = models.list_banners()
    return render_template('admin/banners.html', rows=rows, user=get_user())


@app.route('/admin/audit_ai', methods=['POST'])
@role_required(3)
def admin_audit_ai():
    text = request.form.get('text', '').strip()
    result = ai_helper.content_check(text) if text else '请输入待检测内容'
    flash('AI 检测结果：' + result, 'success')
    return redirect(url_for('admin_reviews'))


# ================= 启动 =================

if __name__ == '__main__':
    if not os.path.exists(models.DB_PATH):
        models.init_db()
        print('数据库不存在，写入演示数据...')
        import init_db
        init_db.main()
    import threading
    import webbrowser
    # 使用5001端口，避免与智农鲜链(5000)同时运行时冲突
    threading.Thread(target=lambda: (__import__('time').sleep(1.5),
                                     webbrowser.open('http://127.0.0.1:5001')),
                     daemon=True).start()
    app.run(host='127.0.0.1', port=5001, debug=False)
