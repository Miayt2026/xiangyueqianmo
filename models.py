# -*- coding: utf-8 -*-
"""
乡约阡陌 —— 数据库模型模块
AI赋能全国乡村农旅体验与助农服务平台
技术栈：SQLite（零配置，数据保存在 data.db）
角色：0游客 / 1商户 / 3平台管理员
"""

import sqlite3
import os
import sys


def _app_dir():
    """获取程序运行时的真实目录（兼容PyInstaller打包）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = _app_dir()
DB_PATH = os.path.join(BASE_DIR, 'data.db')


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ================= 建表 =================

def init_db():
    conn = get_conn()
    c = conn.cursor()

    # 用户表（游客/商户/平台管理员）
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role INTEGER DEFAULT 0,            -- 0游客 1商户 3平台管理员
            status TEXT DEFAULT '正常',         -- 正常/待审核/驳回/禁用
            phone TEXT,
            region TEXT DEFAULT '',            -- 所在地区（省-市-县）
            avatar TEXT DEFAULT 'user.jpg',
            shop_name TEXT DEFAULT '',         -- 商户店铺名称
            shop_type TEXT DEFAULT '',         -- 正规农家乐/农户体验点/农村合作社
            shop_address TEXT DEFAULT '',
            shop_desc TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 农家乐/体验点（农旅资源）
    c.execute('''
        CREATE TABLE IF NOT EXISTS farmstays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_id INTEGER NOT NULL,      -- 所属商户
            name TEXT NOT NULL,
            region TEXT DEFAULT '',            -- 地区（省-市-县）
            address TEXT DEFAULT '',
            category TEXT DEFAULT '采摘体验',  -- 采摘体验/农家住宿/农家餐饮/农耕研学/非遗体验
            price_min REAL DEFAULT 0,          -- 最低参考价
            score REAL DEFAULT 5.0,            -- 评分
            tags TEXT DEFAULT '',              -- 特色标签（逗号分隔）
            description TEXT DEFAULT '',
            image TEXT DEFAULT 'farm_default.jpg',
            lng REAL DEFAULT 0,                -- 经度（高德地图导航）
            lat REAL DEFAULT 0,                -- 纬度（高德地图导航）
            status TEXT DEFAULT '上架',         -- 上架/下架
            views INTEGER DEFAULT 0,          -- 浏览量
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 农旅项目（采摘/餐饮/体验项目）
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmstay_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL DEFAULT 0,
            unit TEXT DEFAULT '人/次',
            open_time TEXT DEFAULT '全天',
            status TEXT DEFAULT '上架',
            category TEXT DEFAULT '',
            desc TEXT DEFAULT '',
            image TEXT DEFAULT ''
        )
    ''')

    # 住宿房型
    c.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmstay_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            beds INTEGER DEFAULT 1,
            price REAL DEFAULT 0,
            stock INTEGER DEFAULT 1,
            status TEXT DEFAULT '上架',
            image TEXT DEFAULT ''
        )
    ''')

    # 特色农产品（特产）
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmstay_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL DEFAULT 0,
            unit TEXT DEFAULT '斤',
            stock INTEGER DEFAULT 0,
            description TEXT DEFAULT '',
            origin TEXT DEFAULT '',
            image TEXT DEFAULT 'product_default.jpg',
            trace_code TEXT DEFAULT '',        -- 溯源码
            status TEXT DEFAULT '上架',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 溯源记录
    c.execute('''
        CREATE TABLE IF NOT EXISTS trace_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            stage TEXT DEFAULT '',
            location TEXT DEFAULT '',
            detail TEXT DEFAULT '',
            recorder TEXT DEFAULT '',
            record_time TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 预约订单（农旅预约）
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_no TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL,
            farmstay_id INTEGER NOT NULL,
            project_id INTEGER DEFAULT 0,
            visit_date TEXT DEFAULT '',
            people INTEGER DEFAULT 1,
            phone TEXT DEFAULT '',
            remark TEXT DEFAULT '',
            add_product INTEGER DEFAULT 0,     -- 是否加购特产
            status TEXT DEFAULT '待审核',       -- 待审核/已确认/已驳回/已完成/已取消
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 特产意向订单
    c.execute('''
        CREATE TABLE IF NOT EXISTS product_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            status TEXT DEFAULT '待发货',          -- 待发货/已发货/已签收/已取消/退款申请/已退款
            recv_name TEXT DEFAULT '',             -- 收货人
            recv_phone TEXT DEFAULT '',            -- 收货电话
            recv_address TEXT DEFAULT '',          -- 收货地址
            company_name TEXT DEFAULT '',          -- 快递公司
            tracking_number TEXT DEFAULT '',       -- 快递单号
            expected_arrival TEXT DEFAULT '',      -- 预计到达
            refund_reason TEXT DEFAULT '',         -- 退款申请原因
            refund_time TEXT DEFAULT '',           -- 退款处理时间
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    # 购物车
    c.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            UNIQUE(user_id, product_id)
        )
    ''')
    # 系统公告
    c.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT DEFAULT '',
            category TEXT DEFAULT '农旅活动',     -- 农旅活动/政策公告/平台通知
            status TEXT DEFAULT '启用',            -- 启用/停用
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    # 物流轨迹（时间线）
    c.execute('''
        CREATE TABLE IF NOT EXISTS logistics_tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            node TEXT DEFAULT '',                  -- 节点说明
            location TEXT DEFAULT '',              -- 地点
            track_time TEXT DEFAULT '',            -- 时间
            sort INTEGER DEFAULT 0
        )
    ''')

    # 闲置资源共享（农具/农房/用工/土地流转）
    c.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            rtype TEXT DEFAULT '闲置农具',      -- 闲置农具/闲置农房/临时用工/土地流转
            title TEXT NOT NULL,
            region TEXT DEFAULT '',
            description TEXT DEFAULT '',
            price REAL DEFAULT 0,
            contact TEXT DEFAULT '',
            image TEXT DEFAULT '',
            status TEXT DEFAULT '发布中',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS resource_intents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT DEFAULT '',
            status TEXT DEFAULT '待对接',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 用户评价
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            farmstay_id INTEGER NOT NULL,
            rating INTEGER DEFAULT 5,
            content TEXT DEFAULT '',
            reply TEXT DEFAULT '',
            status TEXT DEFAULT '正常',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 收藏
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target_type TEXT DEFAULT 'farmstay',  -- farmstay/product
            target_id INTEGER NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            UNIQUE(user_id, target_type, target_id)
        )
    ''')

    # 轮播图配置（首页运营）
    c.execute('''
        CREATE TABLE IF NOT EXISTS banners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT DEFAULT '',
            image TEXT DEFAULT 'banner1.jpg',
            link TEXT DEFAULT '/',
            sort INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


# ================= 用户 =================

def create_user(username, password, role=0, phone='', region='',
                shop_name='', shop_type='', shop_address='', shop_desc='', status='正常'):
    conn = get_conn()
    try:
        conn.execute(
            'INSERT INTO users (username, password, role, phone, region, shop_name, shop_type, shop_address, shop_desc, status) '
            'VALUES (?,?,?,?,?,?,?,?,?,?)',
            (username, password, role, phone, region, shop_name, shop_type, shop_address, shop_desc, status))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_name(username):
    conn = get_conn()
    row = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
    conn.close()
    return row


def get_user_by_id(uid):
    conn = get_conn()
    row = conn.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone()
    conn.close()
    return row


def update_user(uid, **fields):
    conn = get_conn()
    sets = ', '.join(f'{k}=?' for k in fields)
    conn.execute(f'UPDATE users SET {sets} WHERE id=?', (*fields.values(), uid))
    conn.commit()
    conn.close()


def list_users(role=None, keyword=''):
    conn = get_conn()
    sql = 'SELECT * FROM users WHERE 1=1'
    args = []
    if role is not None:
        sql += ' AND role=?'
        args.append(role)
    if keyword:
        sql += ' AND (username LIKE ? OR shop_name LIKE ?)'
        args += [f'%{keyword}%', f'%{keyword}%']
    sql += ' ORDER BY id'
    rows = conn.execute(sql, args).fetchall()
    conn.close()
    return rows


# ================= 农家乐 =================

def add_farmstay(merchant_id, name, region, address, category, price_min, tags, description, image='farm_default.jpg', lng=0, lat=0):
    conn = get_conn()
    cur = conn.execute(
        'INSERT INTO farmstays (merchant_id, name, region, address, category, price_min, tags, description, image, lng, lat) '
        'VALUES (?,?,?,?,?,?,?,?,?,?,?)',
        (merchant_id, name, region, address, category, price_min, tags, description, image, lng, lat))
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def list_farmstays(region='', category='', keyword='', merchant_id=None):
    conn = get_conn()
    sql = 'SELECT * FROM farmstays WHERE status="上架"'
    args = []
    if region:
        sql += ' AND region LIKE ?'
        args.append(f'%{region}%')
    if category:
        sql += ' AND category=?'
        args.append(category)
    if keyword:
        sql += ' AND (name LIKE ? OR description LIKE ? OR tags LIKE ?)'
        args += [f'%{keyword}%', f'%{keyword}%', f'%{keyword}%']
    if merchant_id:
        sql = 'SELECT * FROM farmstays WHERE merchant_id=?'
        args = [merchant_id]
    sql += ' ORDER BY id DESC'
    rows = conn.execute(sql, args).fetchall()
    conn.close()
    return rows


def get_farmstay(fid):
    conn = get_conn()
    row = conn.execute('SELECT * FROM farmstays WHERE id=?', (fid,)).fetchone()
    conn.close()
    return row


def list_all_admin_farmstays():
    """管理端查看全部农旅点位（含下架，含商户名）"""
    conn = get_conn()
    rows = conn.execute(
        'SELECT f.*, u.shop_name as merchant_name FROM farmstays f '
        'LEFT JOIN users u ON f.merchant_id=u.id ORDER BY f.id DESC').fetchall()
    conn.close()
    return rows


def update_farmstay(fid, **fields):
    conn = get_conn()
    sets = ', '.join(f'{k}=?' for k in fields)
    conn.execute(f'UPDATE farmstays SET {sets} WHERE id=?', (*fields.values(), fid))
    conn.commit()
    conn.close()


def delete_farmstay(fid):
    conn = get_conn()
    conn.execute('DELETE FROM farmstays WHERE id=?', (fid,))
    conn.commit()
    conn.close()


# ================= 农旅项目 =================

def add_project(farmstay_id, name, price, unit, open_time):
    conn = get_conn()
    conn.execute('INSERT INTO projects (farmstay_id, name, price, unit, open_time) VALUES (?,?,?,?,?)',
                 (farmstay_id, name, price, unit, open_time))
    conn.commit()
    conn.close()


def list_projects(farmstay_id=None):
    conn = get_conn()
    if farmstay_id:
        rows = conn.execute('SELECT * FROM projects WHERE farmstay_id=? ORDER BY id', (farmstay_id,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM projects ORDER BY id').fetchall()
    conn.close()
    return rows


def get_project(pid):
    conn = get_conn()
    row = conn.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
    conn.close()
    return row


def update_project(pid, **fields):
    conn = get_conn()
    sets = ', '.join(f'{k}=?' for k in fields)
    conn.execute(f'UPDATE projects SET {sets} WHERE id=?', (*fields.values(), pid))
    conn.commit()
    conn.close()


def delete_project(pid):
    conn = get_conn()
    conn.execute('DELETE FROM projects WHERE id=?', (pid,))
    conn.commit()
    conn.close()


# ================= 房型 =================

def add_room(farmstay_id, name, beds, price, stock):
    conn = get_conn()
    conn.execute('INSERT INTO rooms (farmstay_id, name, beds, price, stock) VALUES (?,?,?,?,?)',
                 (farmstay_id, name, beds, price, stock))
    conn.commit()
    conn.close()


def list_rooms(farmstay_id=None):
    conn = get_conn()
    if farmstay_id:
        rows = conn.execute('SELECT * FROM rooms WHERE farmstay_id=? ORDER BY id', (farmstay_id,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM rooms ORDER BY id').fetchall()
    conn.close()
    return rows


def get_room(rid):
    conn = get_conn()
    row = conn.execute('SELECT * FROM rooms WHERE id=?', (rid,)).fetchone()
    conn.close()
    return row


def update_room(rid, **fields):
    conn = get_conn()
    sets = ', '.join(f'{k}=?' for k in fields)
    conn.execute(f'UPDATE rooms SET {sets} WHERE id=?', (*fields.values(), rid))
    conn.commit()
    conn.close()


def delete_room(rid):
    conn = get_conn()
    conn.execute('DELETE FROM rooms WHERE id=?', (rid,))
    conn.commit()
    conn.close()


# ================= 特产 =================

def add_product(farmstay_id, name, price, unit, stock, description, origin, trace_code='', image='product_default.jpg'):
    conn = get_conn()
    if not trace_code:
        cur = conn.execute('SELECT COUNT(*) c FROM products').fetchone()['c']
        trace_code = f'XYQM{cur+1001:04d}'
    cur = conn.execute(
        'INSERT INTO products (farmstay_id, name, price, unit, stock, description, origin, trace_code, image) '
        'VALUES (?,?,?,?,?,?,?,?,?)',
        (farmstay_id, name, price, unit, stock, description, origin, trace_code, image))
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid, trace_code


def list_products(farmstay_id=None, keyword=''):
    conn = get_conn()
    if farmstay_id:
        rows = conn.execute('SELECT * FROM products WHERE farmstay_id=? ORDER BY id DESC', (farmstay_id,)).fetchall()
    else:
        sql = 'SELECT * FROM products WHERE status="上架"'
        args = []
        if keyword:
            sql += ' AND (name LIKE ? OR origin LIKE ?)'
            args += [f'%{keyword}%', f'%{keyword}%']
        sql += ' ORDER BY id DESC'
        rows = conn.execute(sql, args).fetchall()
    conn.close()
    return rows


def get_product(pid):
    conn = get_conn()
    row = conn.execute('SELECT * FROM products WHERE id=?', (pid,)).fetchone()
    conn.close()
    return row


def find_product_by_trace(code):
    conn = get_conn()
    row = conn.execute('SELECT * FROM products WHERE trace_code=?', (code,)).fetchone()
    conn.close()
    return row


def update_product(pid, **fields):
    conn = get_conn()
    sets = ', '.join(f'{k}=?' for k in fields)
    conn.execute(f'UPDATE products SET {sets} WHERE id=?', (*fields.values(), pid))
    conn.commit()
    conn.close()


def delete_product(pid):
    conn = get_conn()
    conn.execute('DELETE FROM products WHERE id=?', (pid,))
    conn.commit()
    conn.close()


# ================= 溯源 =================

def add_trace_record(product_id, stage, location, detail, recorder):
    conn = get_conn()
    conn.execute('INSERT INTO trace_records (product_id, stage, location, detail, recorder) VALUES (?,?,?,?,?)',
                 (product_id, stage, location, detail, recorder))
    conn.commit()
    conn.close()


def get_trace_records(product_id):
    conn = get_conn()
    rows = conn.execute('SELECT * FROM trace_records WHERE product_id=? ORDER BY id', (product_id,)).fetchall()
    conn.close()
    return rows


# ================= 预约 =================

def create_booking(user_id, farmstay_id, project_id, visit_date, people, phone, remark, add_product):
    import random
    no = 'XYQM' + ''.join(random.choices('0123456789', k=8))
    conn = get_conn()
    conn.execute(
        'INSERT INTO bookings (booking_no, user_id, farmstay_id, project_id, visit_date, people, phone, remark, add_product) '
        'VALUES (?,?,?,?,?,?,?,?,?)',
        (no, user_id, farmstay_id, project_id, visit_date, people, phone, remark, add_product))
    conn.commit()
    conn.close()
    return no


def get_user_bookings(user_id):
    conn = get_conn()
    rows = conn.execute(
        'SELECT b.*, f.name as farmstay_name FROM bookings b LEFT JOIN farmstays f ON b.farmstay_id=f.id '
        'WHERE b.user_id=? ORDER BY b.id DESC', (user_id,)).fetchall()
    conn.close()
    return rows


def list_all_bookings(merchant_id=None):
    conn = get_conn()
    if merchant_id:
        rows = conn.execute(
            'SELECT b.*, f.name as farmstay_name, u.username FROM bookings b '
            'LEFT JOIN farmstays f ON b.farmstay_id=f.id '
            'LEFT JOIN users u ON b.user_id=u.id '
            'WHERE f.merchant_id=? ORDER BY b.id DESC', (merchant_id,)).fetchall()
    else:
        rows = conn.execute(
            'SELECT b.*, f.name as farmstay_name, u.username FROM bookings b '
            'LEFT JOIN farmstays f ON b.farmstay_id=f.id '
            'LEFT JOIN users u ON b.user_id=u.id ORDER BY b.id DESC').fetchall()
    conn.close()
    return rows


def update_booking(bid, **fields):
    conn = get_conn()
    sets = ', '.join(f'{k}=?' for k in fields)
    conn.execute(f'UPDATE bookings SET {sets} WHERE id=?', (*fields.values(), bid))
    conn.commit()
    conn.close()


# ================= 特产订单 =================

def create_product_order(user_id, product_id, quantity, recv_name='', recv_phone='', recv_address=''):
    import random
    no = 'PO' + ''.join(random.choices('0123456789', k=8))
    conn = get_conn()
    conn.execute(
        'INSERT INTO product_orders (order_no, user_id, product_id, quantity, recv_name, recv_phone, recv_address) '
        'VALUES (?,?,?,?,?,?,?)',
        (no, user_id, product_id, quantity, recv_name, recv_phone, recv_address))
    conn.commit()
    conn.close()
    return no


def get_product_order(order_id):
    conn = get_conn()
    row = conn.execute(
        'SELECT o.*, p.name as product_name, p.price, p.image, u.username FROM product_orders o '
        'LEFT JOIN products p ON o.product_id=p.id '
        'LEFT JOIN users u ON o.user_id=u.id WHERE o.id=?', (order_id,)).fetchone()
    conn.close()
    return row


def list_all_product_orders(merchant_id=None):
    conn = get_conn()
    if merchant_id:
        rows = conn.execute(
            'SELECT o.*, p.name as product_name, p.price, u.username FROM product_orders o '
            'LEFT JOIN products p ON o.product_id=p.id '
            'LEFT JOIN farmstays f ON p.farmstay_id=f.id '
            'LEFT JOIN users u ON o.user_id=u.id '
            'WHERE f.merchant_id=? ORDER BY o.id DESC', (merchant_id,)).fetchall()
    else:
        rows = conn.execute(
            'SELECT o.*, p.name as product_name, p.price, u.username FROM product_orders o '
            'LEFT JOIN products p ON o.product_id=p.id '
            'LEFT JOIN users u ON o.user_id=u.id ORDER BY o.id DESC').fetchall()
    conn.close()
    return rows


def ship_product_order(order_id, company_name, tracking_number, expected_arrival=''):
    conn = get_conn()
    conn.execute(
        "UPDATE product_orders SET status='已发货', company_name=?, tracking_number=?, expected_arrival=? WHERE id=?",
        (company_name, tracking_number, expected_arrival, order_id))
    import datetime
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn.execute(
        "INSERT INTO logistics_tracks (order_id, node, location, track_time, sort) VALUES (?,?,?,?,1)",
        (order_id, '商家已发货，包裹已交给' + company_name, '发货地', now))
    conn.execute(
        "INSERT INTO logistics_tracks (order_id, node, location, track_time, sort) VALUES (?,?,?,?,2)",
        (order_id, '包裹已到达' + (company_name or '中转') + '分拨中心', '中转中心', now))
    conn.execute(
        "INSERT INTO logistics_tracks (order_id, node, location, track_time, sort) VALUES (?,?,?,?,3)",
        (order_id, '运输中，即将送达目的地', '运输途中', now))
    conn.commit()
    conn.close()


def sign_product_order(order_id):
    conn = get_conn()
    conn.execute("UPDATE product_orders SET status='已签收' WHERE id=?", (order_id,))
    import datetime
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn.execute(
        "INSERT INTO logistics_tracks (order_id, node, location, track_time, sort) VALUES (?,?,?,?,99)",
        (order_id, '包裹已签收，感谢您在乡约阡陌选购', '收货地址', now))
    conn.commit()
    conn.close()


def get_logistics_tracks(order_id):
    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM logistics_tracks WHERE order_id=? ORDER BY sort DESC, id DESC', (order_id,)).fetchall()
    conn.close()
    return rows


def order_status_stats():
    # 按物流/订单状态统计（全平台）
    conn = get_conn()
    rows = conn.execute(
        'SELECT status, COUNT(*) c FROM product_orders GROUP BY status').fetchall()
    conn.close()
    return {r['status']: r['c'] for r in rows}


def merchant_order_stats(merchant_id):
    # 商户订单状态统计
    conn = get_conn()
    rows = conn.execute(
        'SELECT o.status, COUNT(*) c FROM product_orders o '
        'LEFT JOIN products p ON o.product_id=p.id '
        'LEFT JOIN farmstays f ON p.farmstay_id=f.id '
        'WHERE f.merchant_id=? GROUP BY o.status',
        (merchant_id,)).fetchall()
    conn.close()
    return {r['status']: r['c'] for r in rows}


def order_daily_trend(days=7):
    # 近 N 天订单量趋势（全平台）
    import datetime
    conn = get_conn()
    trend = {}
    today = datetime.date.today()
    for i in range(days - 1, -1, -1):
        d = today - datetime.timedelta(days=i)
        key = d.strftime('%m-%d')
        trend[key] = 0
    rows = conn.execute(
        "SELECT date(created_at) d, COUNT(*) c FROM product_orders GROUP BY date(created_at)").fetchall()
    for r in rows:
        key = r['d'][5:] if r['d'] and len(r['d']) >= 10 else None
        if key in trend:
            trend[key] = r['c']
    conn.close()
    return trend


def get_user_product_orders(user_id):
    conn = get_conn()
    rows = conn.execute(
        'SELECT o.*, p.name as product_name, p.price FROM product_orders o '
        'LEFT JOIN products p ON o.product_id=p.id WHERE o.user_id=? ORDER BY o.id DESC', (user_id,)).fetchall()
    conn.close()
    return rows


# ================= 闲置资源 =================

def add_resource(user_id, rtype, title, region, description, price, contact, image=''):
    conn = get_conn()
    conn.execute('INSERT INTO resources (user_id, rtype, title, region, description, price, contact, image) VALUES (?,?,?,?,?,?,?,?)',
                 (user_id, rtype, title, region, description, price, contact, image))
    conn.commit()
    conn.close()


def list_resources(rtype='', keyword='', region=''):
    conn = get_conn()
    sql = 'SELECT r.*, u.username, u.region as user_region FROM resources r LEFT JOIN users u ON r.user_id=u.id WHERE 1=1'
    args = []
    if rtype:
        sql += ' AND r.rtype=?'
        args.append(rtype)
    if keyword:
        sql += ' AND (r.title LIKE ? OR r.description LIKE ?)'
        args += [f'%{keyword}%', f'%{keyword}%']
    if region:
        sql += ' AND r.region LIKE ?'
        args.append(f'%{region}%')
    sql += ' ORDER BY r.id DESC'
    rows = conn.execute(sql, args).fetchall()
    conn.close()
    return rows


def get_resource(rid):
    conn = get_conn()
    row = conn.execute('SELECT * FROM resources WHERE id=?', (rid,)).fetchone()
    conn.close()
    return row


# ================= 评价 =================

def add_review(user_id, farmstay_id, rating, content):
    conn = get_conn()
    conn.execute('INSERT INTO reviews (user_id, farmstay_id, rating, content) VALUES (?,?,?,?)',
                 (user_id, farmstay_id, rating, content))
    conn.commit()
    conn.close()


def list_reviews(farmstay_id=None, status=None):
    conn = get_conn()
    if farmstay_id:
        rows = conn.execute(
            'SELECT r.*, u.username, f.name as farmstay_name FROM reviews r '
            'LEFT JOIN users u ON r.user_id=u.id LEFT JOIN farmstays f ON r.farmstay_id=f.id '
            'WHERE r.farmstay_id=? ORDER BY r.id DESC', (farmstay_id,)).fetchall()
    else:
        sql = ('SELECT r.*, u.username, f.name as farmstay_name FROM reviews r '
               'LEFT JOIN users u ON r.user_id=u.id LEFT JOIN farmstays f ON r.farmstay_id=f.id WHERE 1=1')
        args = []
        if status:
            sql += ' AND r.status=?'
            args.append(status)
        sql += ' ORDER BY r.id DESC'
        rows = conn.execute(sql, args).fetchall()
    conn.close()
    return rows


def update_review(rid, **fields):
    conn = get_conn()
    sets = ', '.join(f'{k}=?' for k in fields)
    conn.execute(f'UPDATE reviews SET {sets} WHERE id=?', (*fields.values(), rid))
    conn.commit()
    conn.close()


# ================= 收藏 =================

def toggle_favorite(user_id, target_type, target_id):
    conn = get_conn()
    row = conn.execute('SELECT id FROM favorites WHERE user_id=? AND target_type=? AND target_id=?',
                       (user_id, target_type, target_id)).fetchone()
    if row:
        conn.execute('DELETE FROM favorites WHERE id=?', (row['id'],))
        conn.commit()
        conn.close()
        return False
    conn.execute('INSERT INTO favorites (user_id, target_type, target_id) VALUES (?,?,?)',
                 (user_id, target_type, target_id))
    conn.commit()
    conn.close()
    return True


def get_user_favorites(user_id):
    conn = get_conn()
    rows = conn.execute('SELECT * FROM favorites WHERE user_id=? ORDER BY id DESC', (user_id,)).fetchall()
    conn.close()
    return rows


# ================= 轮播图 =================

def list_banners():
    conn = get_conn()
    rows = conn.execute('SELECT * FROM banners ORDER BY sort').fetchall()
    conn.close()
    return rows


def add_banner(title, image, link):
    conn = get_conn()
    conn.execute('INSERT INTO banners (title, image, link) VALUES (?,?,?)', (title, image, link))
    conn.commit()
    conn.close()


# ================= 统计看板 =================

def platform_stats():
    conn = get_conn()
    users = conn.execute('SELECT COUNT(*) c FROM users WHERE role=0').fetchone()['c']
    merchants = conn.execute('SELECT COUNT(*) c FROM users WHERE role=1').fetchone()['c']
    farmstays = conn.execute('SELECT COUNT(*) c FROM farmstays').fetchone()['c']
    bookings = conn.execute('SELECT COUNT(*) c FROM bookings').fetchone()['c']
    products = conn.execute('SELECT COUNT(*) c FROM products').fetchone()['c']
    resources = conn.execute('SELECT COUNT(*) c FROM resources').fetchone()['c']
    conn.close()
    return {'users': users, 'merchants': merchants, 'farmstays': farmstays,
            'bookings': bookings, 'products': products, 'resources': resources}


def merchant_stats(merchant_id):
    conn = get_conn()
    fids = [r['id'] for r in conn.execute('SELECT id FROM farmstays WHERE merchant_id=?', (merchant_id,)).fetchall()]
    if not fids:
        conn.close()
        return {'farmstays': 0, 'projects': 0, 'rooms': 0, 'products': 0, 'bookings': 0, 'reviews': 0, 'pending': 0}
    placeholders = ','.join('?' * len(fids))
    fs = conn.execute(f'SELECT COUNT(*) c FROM farmstays WHERE merchant_id=?', (merchant_id,)).fetchone()['c']
    pj = conn.execute(f'SELECT COUNT(*) c FROM projects WHERE farmstay_id IN ({placeholders})', fids).fetchone()['c']
    rm = conn.execute(f'SELECT COUNT(*) c FROM rooms WHERE farmstay_id IN ({placeholders})', fids).fetchone()['c']
    pd = conn.execute(f'SELECT COUNT(*) c FROM products WHERE farmstay_id IN ({placeholders})', fids).fetchone()['c']
    bk = conn.execute(f'SELECT COUNT(*) c FROM bookings WHERE farmstay_id IN ({placeholders})', fids).fetchone()['c']
    rv = conn.execute(f'SELECT COUNT(*) c FROM reviews WHERE farmstay_id IN ({placeholders})', fids).fetchone()['c']
    pend = conn.execute(f'SELECT COUNT(*) c FROM bookings WHERE farmstay_id IN ({placeholders}) AND status="待审核"', fids).fetchone()['c']
    conn.close()
    return {'farmstays': fs, 'projects': pj, 'rooms': rm, 'products': pd, 'bookings': bk, 'reviews': rv, 'pending': pend}


# ================= 购物车 =================

def add_cart(user_id, product_id, quantity=1):
    conn = get_conn()
    row = conn.execute('SELECT id, quantity FROM carts WHERE user_id=? AND product_id=?',
                       (user_id, product_id)).fetchone()
    if row:
        conn.execute('UPDATE carts SET quantity=quantity+? WHERE id=?', (quantity, row['id']))
    else:
        conn.execute('INSERT INTO carts (user_id, product_id, quantity) VALUES (?,?,?)',
                     (user_id, product_id, quantity))
    conn.commit()
    conn.close()


def get_cart(user_id):
    conn = get_conn()
    rows = conn.execute(
        'SELECT c.id, c.product_id, c.quantity, p.name, p.price, p.image, p.stock, p.status, '
        'p.farmstay_id, f.name as farmstay_name FROM carts c '
        'LEFT JOIN products p ON c.product_id=p.id '
        'LEFT JOIN farmstays f ON p.farmstay_id=f.id '
        'WHERE c.user_id=? ORDER BY c.id DESC', (user_id,)).fetchall()
    conn.close()
    return rows


def get_cart_count(user_id):
    conn = get_conn()
    r = conn.execute('SELECT COUNT(*) c FROM carts WHERE user_id=?', (user_id,)).fetchone()
    conn.close()
    return r['c']


def update_cart_qty(cart_id, quantity):
    conn = get_conn()
    conn.execute('UPDATE carts SET quantity=? WHERE id=?', (quantity, cart_id))
    conn.commit()
    conn.close()


def remove_cart_item(cart_id):
    conn = get_conn()
    conn.execute('DELETE FROM carts WHERE id=?', (cart_id,))
    conn.commit()
    conn.close()


def clear_cart(user_id):
    conn = get_conn()
    conn.execute('DELETE FROM carts WHERE user_id=?', (user_id,))
    conn.commit()
    conn.close()


# ================= 系统公告 =================

def add_notice(title, content, category='农旅活动', status='启用'):
    conn = get_conn()
    conn.execute('INSERT INTO notices (title, content, category, status) VALUES (?,?,?,?)',
                 (title, content, category, status))
    conn.commit()
    conn.close()


def list_notices(status=''):
    conn = get_conn()
    if status:
        rows = conn.execute('SELECT * FROM notices WHERE status=? ORDER BY id DESC', (status,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM notices ORDER BY id DESC').fetchall()
    conn.close()
    return rows


def delete_notice(nid):
    conn = get_conn()
    conn.execute('DELETE FROM notices WHERE id=?', (nid,))
    conn.commit()
    conn.close()


def toggle_notice(nid, status):
    conn = get_conn()
    conn.execute('UPDATE notices SET status=? WHERE id=?', (status, nid))
    conn.commit()
    conn.close()


# ================= 订单取消 / 退款 =================

def cancel_product_order(order_id):
    conn = get_conn()
    conn.execute("UPDATE product_orders SET status='已取消' WHERE id=? AND status='待发货'", (order_id,))
    conn.commit()
    conn.close()


def apply_refund_product_order(order_id, reason):
    conn = get_conn()
    conn.execute(
        "UPDATE product_orders SET status='退款申请', refund_reason=? WHERE id=? AND status IN ('已发货','已签收')",
        (reason, order_id))
    conn.commit()
    conn.close()


def process_refund_product_order(order_id, approve):
    conn = get_conn()
    import datetime
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    if approve:
        conn.execute("UPDATE product_orders SET status='已退款', refund_time=? WHERE id=?",
                     (now, order_id))
    else:
        row = conn.execute('SELECT status FROM product_orders WHERE id=?', (order_id,)).fetchone()
        # 驳回：按是否已发货恢复状态（简单恢复为已发货）
        conn.execute("UPDATE product_orders SET status='已发货', refund_reason='' WHERE id=?",
                     (order_id,))
    conn.commit()
    conn.close()


# ================= 预约取消 / 个人中心统计 / 溯源二维码 =================

def cancel_booking(booking_id, user_id):
    conn = get_conn()
    conn.execute("UPDATE bookings SET status='已取消' WHERE id=? AND user_id=?",
                 (booking_id, user_id))
    conn.commit()
    conn.close()


def count_user_data(user_id):
    conn = get_conn()
    bookings = conn.execute('SELECT COUNT(*) c FROM bookings WHERE user_id=?', (user_id,)).fetchone()['c']
    orders = conn.execute('SELECT COUNT(*) c FROM product_orders WHERE user_id=?', (user_id,)).fetchone()['c']
    favs = conn.execute('SELECT COUNT(*) c FROM favorites WHERE user_id=?', (user_id,)).fetchone()['c']
    revs = conn.execute('SELECT COUNT(*) c FROM reviews WHERE user_id=?', (user_id,)).fetchone()['c']
    conn.close()
    return {'bookings': bookings, 'orders': orders, 'favorites': favs, 'reviews': revs}


def gen_qr(data, path):
    """生成二维码图片（离线本地生成）"""
    import qrcode
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = qrcode.make(data)
    img.save(path)


# ================= 闲置资源对接意向 =================

def add_resource_intent(resource_id, user_id, message=''):
    conn = get_conn()
    conn.execute('INSERT INTO resource_intents (resource_id, user_id, message) VALUES (?,?,?)',
                 (resource_id, user_id, message))
    conn.commit()
    conn.close()


def list_user_intents(user_id):
    conn = get_conn()
    rows = conn.execute(
        'SELECT i.*, r.title, r.rtype, r.region, r.price FROM resource_intents i '
        'LEFT JOIN resources r ON i.resource_id=r.id '
        'WHERE i.user_id=? ORDER BY i.id DESC', (user_id,)).fetchall()
    conn.close()
    return rows


# ================= 农旅点浏览计数 =================

def inc_view(fid):
    conn = get_conn()
    conn.execute('UPDATE farmstays SET views=views+1 WHERE id=?', (fid,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print('数据库初始化完成：', DB_PATH)
