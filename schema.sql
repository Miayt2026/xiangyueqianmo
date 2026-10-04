-- ============================================
-- 乡约阡陌 · AI赋能全国乡村农旅体验与助农服务平台
-- 数据库脚本（SQLite3 兼容，演示数据版）
-- 生成时间：2026-10-03 23:32
-- 与 data.db 完整一致：23账号 / 31点位 / 71项目 / 22房型 / 30特产 / 150溯源 / 15评价
-- ============================================
PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE users (
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
        );

-- Records of users (23 rows)
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (25, '游客小美', '123456', 0, '正常', '13800001001', '河北省-张家口市-崇礼区', 'user.jpg', '', '', '', '', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (26, '游客小凯', '123456', 0, '正常', '13800001002', '河北省-保定市-涞源县', 'user.jpg', '', '', '', '', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (27, '青山农家乐', '123456', 1, '正常', '13800001003', '河北省-张家口市-崇礼区', 'user.jpg', '青山农家乐', '正规农家乐', '张家口崇礼区西湾子镇', '农家饭菜、果蔬采摘、山景民宿，崇礼夏季避暑首选。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (28, '赵大姐果园', '123456', 1, '正常', '13800001004', '河北省-保定市-涞源县', 'user.jpg', '赵大姐果园', '农户体验点', '涞源县白石山镇', '苹果、桃子采摘体验，自家果园，现摘现吃。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (30, '平台管理员', '123456', 3, '正常', '13800001006', '北京市', 'user.jpg', '', '', '', '', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (31, '陕北红果合作社', '123456', 1, '正常', '13800001007', '陕西省-延安市-洛川县', 'user.jpg', '陕北红果合作社', '农业合作社', '洛川县凤栖街道', '黄土高原苹果之乡，主营洛川苹果采摘与关中民俗农家宴。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (32, '晋韵非遗工坊', '123456', 1, '正常', '13800001008', '山西省-晋中市-平遥县', 'user.jpg', '晋韵非遗工坊', '非遗工坊', '平遥古城东大街', '平遥剪纸非遗体验，古城里的匠心手艺。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (33, '江南乡居文旅', '123456', 1, '正常', '13800001009', '浙江省-湖州市-德清县', 'user.jpg', '江南乡居文旅', '文旅合作社', '德清县莫干山镇', '莫干山竹海民宿、仙居杨梅采摘、龙泉青瓷体验一体化运营。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (34, '云岭农旅联盟', '123456', 1, '正常', '13800001010', '云南省-大理州-大理市', 'user.jpg', '云岭农旅联盟', '农旅合作社', '大理市才村码头', '苍山洱海间的白族小院与特色美食体验。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (35, '徽州人家', '123456', 1, '正常', '13800001011', '安徽省-黄山市-黟县', 'user.jpg', '徽州人家', '特色民宿', '宏村镇宏村景区', '粉墙黛瓦马头墙，住在水墨画里的徽派民宿。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (36, '客家土楼文旅', '123456', 1, '正常', '13800001012', '福建省-龙岩市-永定区', 'user.jpg', '客家土楼文旅', '特色民宿', '湖坑镇洪坑村', '世界遗产土楼改造民宿，体验客家人围屋生活。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (37, '八桂山水农旅', '123456', 1, '正常', '13800001013', '广西省-桂林市-阳朔县', 'user.jpg', '八桂山水农旅', '农旅合作社', '阳朔县遇龙河畔', '喀斯特山水间的田园民宿与骑行漫游。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (38, '巴蜀田园合作社', '123456', 1, '正常', '13800001014', '四川省-乐山市-市中区', 'user.jpg', '巴蜀田园合作社', '农家餐饮', '苏稽古镇', '百年跷脚牛肉老汤，川西坝子的烟火味道。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (39, '湘西苗乡人家', '123456', 1, '正常', '13800001015', '湖南省-湘西州-凤凰县', 'user.jpg', '湘西苗乡人家', '农家餐饮', '凤凰古城沱江镇', '苗家柴火腊肉、酸汤土鸡，古城边的家常味。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (40, '岭南乡味工坊', '123456', 1, '正常', '13800001016', '广东省-佛山市-顺德区', 'user.jpg', '岭南乡味工坊', '农家餐饮', '顺德区大良街道', '顺德桑拿鸡、鱼生，食在广州厨出凤城。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (41, '齐鲁果乡合作社', '123456', 1, '正常', '13800001017', '山东省-烟台市-福山区', 'user.jpg', '齐鲁果乡合作社', '农业合作社', '福山区门楼镇', '烟台大樱桃采摘，北纬37度的甜蜜。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (42, '黑土粮仓研学基地', '123456', 1, '正常', '13800001018', '黑龙江省-佳木斯市-富锦市', 'user.jpg', '黑土粮仓研学基地', '研学基地', '建三江农高区', '北大荒智慧农机与三江平原稻田研学。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (43, '中原农耕研学社', '123456', 1, '正常', '13800001019', '河南省-开封市-兰考县', 'user.jpg', '中原农耕研学社', '研学基地', '兰考县堌阳镇', '焦桐精神与黄河农耕文化研学。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (44, '陇原治沙农场', '123456', 1, '正常', '13800001020', '甘肃省-武威市民勤县', 'user.jpg', '陇原治沙农场', '研学基地', '民勤县薛百镇', '腾格里沙漠边缘的治沙研学与生态农场。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (45, '热带农业研学园', '123456', 1, '正常', '13800001021', '海南省-儋州市', 'user.jpg', '热带农业研学园', '研学基地', '儋州市那大镇', '热带水果科普与采摘研学。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (46, '天山果香合作社', '123456', 1, '正常', '13800001022', '新疆省-阿克苏地区', 'user.jpg', '天山果香合作社', '农业合作社', '阿克苏市红旗坡农场', '冰糖心苹果之乡，日照16小时的甜蜜。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (47, '黔东南非遗工坊', '123456', 1, '正常', '13800001023', '贵州省-黔东南州-丹寨县', 'user.jpg', '黔东南非遗工坊', '非遗工坊', '丹寨万达小镇', '苗族蜡染非遗体验，蓝白之间的匠心。', '2026-09-27 22:57:22');
INSERT INTO `users` (id, username, password, role, status, phone, region, avatar, shop_name, shop_type, shop_address, shop_desc, created_at) VALUES (48, '洛阳唐三彩工坊', '123456', 1, '正常', '13800001024', '河南省-洛阳市-孟津区', 'user.jpg', '洛阳唐三彩工坊', '非遗工坊', '孟津区三彩小镇', '三彩烧制技艺体验，丝路驼铃的千年记忆。', '2026-09-27 22:57:22');

-- ----------------------------
-- Table structure for farmstays
-- ----------------------------
DROP TABLE IF EXISTS `farmstays`;
CREATE TABLE farmstays (
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
        );

-- Records of farmstays (31 rows)
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (28, 28, '赵大姐果园', '河北省-保定市-涞源县', '涞源县白石山镇下碾盘村', '采摘体验', 39.0, 5.0, '果园,现摘,亲子,助农', '自家30亩果园，种植苹果、油桃、杏，全部农家肥种植，入园现摘现吃，助力山区农户增收。', 'farm_pick.jpg', 114.69, 39.36, '上架', 4836, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (29, 31, '洛川苹果园', '陕西省-延安市-洛川县', '洛川县旧县镇', '采摘体验', 45.0, 5.0, '苹果,高原,采摘,助农', '黄土高原上的苹果之乡，海拔千米、昼夜温差大，冰糖心苹果脆甜多汁，秋季采摘正当时，还可以认养一棵苹果树。', 'luochuan.jpg', 109.43, 35.76, '上架', 4973, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (30, 33, '仙居杨梅园', '浙江省-台州市-仙居县', '仙居县步路乡', '采摘体验', 60.0, 5.0, '杨梅,山野,亲子,采摘', '仙居栽培杨梅已有千年历史，山地红黄壤孕育的东魁杨梅个大核小、汁多味甜，六月杨梅季入园现摘，畅吃管饱。', 'yangmei.jpg', 120.73, 28.85, '上架', 5110, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (31, 34, '石林血桃园', '云南省-昆明市-石林县', '石林县板桥街道叠水村', '采摘体验', 38.0, 5.0, '血桃,喀斯特,采摘,亲子', '石林喀斯特地貌里的千亩血桃，脆硬红甜，六七月正是采摘期，摘完桃子还可以逛石林地质公园。', 'shilin.jpg', 103.27, 24.75, '上架', 5247, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (32, 46, '阿克苏冰糖心苹果园', '新疆省-阿克苏地区-红旗坡', '阿克苏市红旗坡农场', '采摘体验', 42.0, 5.0, '苹果,冰糖心,戈壁,助农', '塔里木盆地北缘、日照16小时，昼夜温差造就冰糖心苹果，霜降后采摘，切开就是琥珀色的糖心。', 'akesu.jpg', 80.26, 41.17, '上架', 5384, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (33, 41, '烟台樱桃采摘园', '山东省-烟台市-福山区', '福山区门楼镇', '采摘体验', 50.0, 5.0, '樱桃,海滨,采摘,亲子', '北纬37度黄金纬度带上的烟台大樱桃，美早、红灯等品种轮番成熟，五六月采摘季一颗颗红玛瑙挂满枝头。', 'yantai.jpg', 121.27, 37.49, '上架', 5521, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (34, 27, '青山农家乐', '河北省-张家口市-崇礼区', '崇礼区西湾子镇青山村', '农家住宿', 168.0, 5.0, '山景,亲子,避暑,采摘', '坐落于崇礼青山脚下，推窗见山，提供农家餐饮、果蔬采摘、山景民宿，夏季均温22℃，是京津冀周边避暑度假的好去处。', 'farm_default.jpg', 115.28, 40.97, '上架', 5659, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (35, 33, '莫干山竹海民宿', '浙江省-湖州市-德清县', '莫干山镇劳岭村', '农家住宿', 388.0, 5.0, '竹海,度假,溪流,星空', '竹林深处的白墙小院，门前溪水潺潺，夜晚枕着虫鸣入睡，白天可以徒步莫干山、骑行乡间绿道。', 'mogan.jpg', 119.96, 30.59, '上架', 5795, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (36, 34, '洱海白族小院', '云南省-大理州-大理市', '大理市才村码头', '农家住宿', 298.0, 5.0, '洱海,白族,海景,慢生活', '白族传统木结构小院改造的民宿，青石板小径、木质梁柱，推门就是洱海日出，体验本地人的生活节奏。', 'dali.jpg', 100.2, 25.7, '上架', 5932, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (37, 35, '宏村徽派人家', '安徽省-黄山市-黟县', '宏村镇宏村景区', '农家住宿', 258.0, 5.0, '徽派,古村,写生,水墨', '粉墙黛瓦马头墙，住在月沼边的百年老宅里，清晨推开木窗就是水墨画般的南湖晨雾。', 'hongcun.jpg', 117.99, 29.97, '上架', 6069, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (38, 36, '永定土楼民宿', '福建省-龙岩市-永定区', '湖坑镇洪坑村', '农家住宿', 228.0, 5.0, '土楼,世遗,客家,围屋', '世界文化遗产永定土楼改造的民宿，住在几百年历史的围屋里，听客家人讲土楼的故事，尝客家酿豆腐。', 'tulou.jpg', 116.95, 24.63, '上架', 6206, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (39, 37, '遇龙河山水民宿', '广西省-桂林市-阳朔县', '阳朔县遇龙河畔', '农家住宿', 268.0, 5.0, '喀斯特,遇龙河,田园,骑行', '喀斯特峰林环抱的田园民宿，门前稻田、远山如黛，清晨沿着遇龙河骑行，傍晚看落日把群山染成金色。', 'yangshuo.jpg', 110.44, 24.78, '上架', 6344, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (40, 31, '袁家村关中农家宴', '陕西省-咸阳市-礼泉县', '袁家村关中印象体验地', '农家餐饮', 68.0, 5.0, '关中,民俗,长桌宴,小吃', '关中民俗第一村，biangbiang面、油泼辣子、锅盔馍，几十种关中农家小吃一桌摆开，还原老陕的味道。', 'yuanjiacun.jpg', 108.51, 34.48, '上架', 6480, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (41, 34, '蒙自过桥米线农家', '云南省-红河州-蒙自市', '蒙自市南湖边', '农家餐饮', 45.0, 5.0, '过桥米线,百年,非遗,老字号', '过桥米线发源地蒙自，滚烫鸡汤配十几种鲜料，一碗下肚鲜掉眉毛，体验百年非遗美食。', 'mixian.jpg', 103.38, 23.36, '上架', 6617, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (42, 38, '苏稽跷脚牛肉馆', '四川省-乐山市-市中区', '苏稽古镇', '农家餐饮', 55.0, 5.0, '跷脚牛肉,川菜,百年老店,药膳', '乐山苏稽百年老汤，牛骨与三十余味香料熬煮，薄切牛肉滚汤即捞，配秘制辣椒蘸碟，暖胃又养生。', 'qiaojiao.jpg', 103.72, 29.58, '上架', 6754, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (43, 39, '凤凰苗家土菜馆', '湖南省-湘西州-凤凰县', '凤凰古城沱江镇', '农家餐饮', 65.0, 5.0, '苗家,腊肉,酸汤,古城', '柏树枝柴火烟熏的苗家腊肉，配酸汤鱼、血粑鸭，在沱江边的吊脚楼里吃一顿地道的苗家饭。', 'miao.jpg', 109.6, 27.95, '上架', 6891, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (44, 40, '顺德桑拿鸡农家', '广东省-佛山市-顺德区', '顺德区大良街道', '农家餐饮', 80.0, 5.0, '桑拿鸡,粤菜,蒸鲜,顺德', '顺德人对鲜的极致追求——桑拿鸡：一锅鸡汤两盘鸡，荷叶垫底3分钟蒸熟，鸡肉脆爽、鸡汤鲜甜，鲜掉眉毛。', 'shunde.jpg', 113.25, 22.84, '上架', 7028, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (45, 27, '青山农事研学基地', '河北省-张家口市-崇礼区', '崇礼区四台嘴乡', '农耕研学', 98.0, 5.0, '研学,农耕,非遗,夏令营', '面向亲子与学校团体的农耕研学基地，含播种体验、豆腐制作、非遗剪纸课堂，让孩子在田野里成长。', 'farm_study.jpg', 115.28, 40.97, '上架', 7165, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (46, 42, '建三江智慧农场研学', '黑龙江省-佳木斯市-富锦市', '建三江国家农高区', '农耕研学', 128.0, 5.0, '北大荒,智慧农业,稻田,研学', '走进北大荒建三江，看无人农机在金色稻田里作业，听三代垦荒人的故事，感受中国饭碗的力量。', 'jiansanjiang.jpg', 132.05, 47.25, '上架', 7302, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (47, 43, '兰考焦桐研学农园', '河南省-开封市-兰考县', '兰考县堌阳镇', '农耕研学', 88.0, 5.0, '焦桐,黄河,农耕,研学', '在焦桐树下听焦裕禄治沙的故事，认识泡桐、花生、大枣兰考三宝，体验黄河滩区农事劳作。', 'lankao.jpg', 114.82, 34.82, '上架', 7439, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (48, 44, '民勤治沙研学农场', '甘肃省-武威市民勤县', '民勤县薛百镇', '农耕研学', 108.0, 5.0, '治沙,草方格,梭梭,生态', '腾格里沙漠边缘的治沙课堂，亲手扎一个草方格、种一株梭梭，在沙漠里上一堂最生动的生态课。', 'minqin.jpg', 103.09, 38.62, '上架', 7576, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (49, 45, '儋州热带农业研学园', '海南省-儋州市', '儋州市那大镇', '农耕研学', 95.0, 5.0, '热带,水果,科普,研学', '认识香蕉、菠萝蜜、椰子等几十种热带作物，体验割胶、采果，探索热带农业的奥秘。', 'danzhou.jpg', 109.58, 19.52, '上架', 7713, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (50, 27, '崇礼剪纸工坊', '河北省-张家口市-崇礼区', '崇礼区西湾子镇', '非遗体验', 68.0, 5.0, '剪纸,非遗,手作,亲子', '蔚县剪纸国家级非遗，在老师傅指导下剪一张属于自己的窗花，把北方的年味带回家。', 'chongli_jianzhi.jpg', 115.28, 40.97, '上架', 7850, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (51, 32, '平遥剪纸坊', '山西省-晋中市-平遥县', '平遥古城东大街', '非遗体验', 58.0, 5.0, '剪纸,古城,非遗,手作', '平遥民间剪纸鼎盛于清代，窗花、顶棚花、灯笼花各有讲究，古城老宅里体验指尖上的非遗。', 'pingyao_jianzhi.jpg', 112.18, 37.19, '上架', 7988, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (52, 33, '龙泉青瓷坊', '浙江省-丽水市-龙泉市', '龙泉市上垟镇', '非遗体验', 88.0, 5.0, '青瓷,非遗,拉坯,烧制', '青如玉、明如镜、声如磬——在千年瓷都亲手拉坯、刻花，体验龙泉青瓷烧制技艺，烧一件自己的作品。', 'qingci.jpg', 118.94, 28.07, '上架', 8124, '2026-09-27 22:57:22');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (53, 47, '丹寨蜡染坊', '贵州省-黔东南州-丹寨县', '丹寨万达小镇', '非遗体验', 76.0, 5.0, '蜡染,苗绣,非遗,手作', '苗族蜡染以蜂蜡作画、蓝靛染色，在白布上画下心里的图腾，做一条独一无二的蓝染围巾。', 'larran.jpg', 107.79, 26.2, '上架', 8261, '2026-09-27 22:57:23');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (54, 48, '洛阳唐三彩工坊', '河南省-洛阳市-孟津区', '孟津区三彩小镇', '非遗体验', 82.0, 5.0, '唐三彩,烧制,丝路,非遗', '在三彩小镇亲手给陶马点彩上釉，了解唐三彩烧制技艺，感受丝路驼铃里的盛唐气象。', 'sancai.jpg', 112.44, 34.83, '上架', 8399, '2026-09-27 22:57:23');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (55, 28, '密云山水采摘园', '北京市-密云区-古北口镇', '古北口镇司马台村', '采摘体验', 52.0, 5.0, '古北水镇,采摘,亲子,山果', '密云古北水镇旁的山水果园，桃李、苹果、葡萄按季成熟，长城脚下摘果、逛水镇，京津冀近郊游首选。', 'beijing_miyun.jpg', 117.14, 40.64, '上架', 8535, '2026-09-29 14:37:24');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (56, 27, '雁栖湖山水民宿', '北京市-怀柔区-雁栖镇', '雁栖镇莲花池村', '农家住宿', 268.0, 5.0, '雁栖湖,长城,民宿,山景', '慕田峪长城脚下的山景民宿，推窗见长城、出门逛雁栖湖，提供农家宴与长城徒步向导。', 'beijing_huairou.jpg', 116.52, 40.41, '上架', 8674, '2026-09-29 14:37:24');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (57, 33, '延庆四季花海研学园', '北京市-延庆区-四海镇', '四海镇大吉祥村', '农耕研学', 108.0, 5.0, '四季花海,研学,花田,亲子', '千亩四季花海中的自然课堂，认识马鞭草、油葵、百日菊等花卉，体验花田研学与园艺手作。', 'beijing_yanqing.jpg', 116.28, 40.54, '上架', 8851, '2026-09-29 14:37:24');
INSERT INTO `farmstays` (id, merchant_id, name, region, address, category, price_min, score, tags, description, image, lng, lat, status, views, created_at) VALUES (58, 40, '延庆柳沟豆腐宴农家院', '北京市-延庆区-井庄镇', '井庄镇柳沟村', '农家餐饮', 78.0, 5.0, '豆腐宴,京郊,农家菜,非遗', '柳沟豆腐宴是京郊非遗名片，火盆锅豆腐宴一桌十几道豆腐做法，配柴鸡、野菜贴饼子，国庆来北京必打卡的农家味道。', 'liugou_doufu.jpg', 115.97, 40.46, '上架', 8965, '2026-09-29 14:59:02');

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS `projects`;
CREATE TABLE projects (
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
        );

-- Records of projects (71 rows)
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (60, 34, '山景标准间', 168.0, '间/晚', '全天', '上架', '', '', 'room_huokang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (61, 34, '农家土炕房', 128.0, '间/晚', '全天', '上架', '', '', 'room_mufang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (62, 34, '时令果蔬采摘', 39.0, '人/次', '08:00-18:00', '上架', '', '', 'grape.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (63, 34, '柴火灶农家宴', 58.0, '人/餐', '11:00-13:00,17:00-19:00', '上架', '', '', 'shunde.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (64, 28, '苹果采摘', 39.0, '人/次', '08:00-18:00', '上架', '', '', 'apple.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (65, 28, '油桃采摘', 35.0, '人/次', '08:00-18:00', '上架', '', '', 'grape.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (66, 28, '果园农家饭', 45.0, '人/餐', '11:00-14:00', '上架', '', '', 'yantai.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (67, 29, '苹果采摘', 45.0, '人/次', '09:00-17:00', '上架', '', '', 'apple.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (68, 29, '果树认养', 299.0, '棵/年', '全年', '上架', '', '', 'grape.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (69, 29, '苹果脆片DIY', 30.0, '人/次', '10:00-16:00', '上架', '', '', 'yantai.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (70, 30, '杨梅畅吃采摘', 60.0, '人/次', '08:00-17:00', '上架', '', '', 'apple.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (71, 30, '杨梅酒制作', 88.0, '人/次', '14:00-16:00', '上架', '', '', 'grape.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (72, 31, '血桃采摘', 38.0, '人/次', '08:00-18:00', '上架', '', '', 'apple.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (73, 31, '石林地质徒步', 20.0, '人/次', '09:00-15:00', '上架', '', '', 'dali.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (74, 32, '苹果采摘', 42.0, '人/次', '10:00-18:00', '上架', '', '', 'apple.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (75, 32, '戈壁果园晚餐', 60.0, '人/餐', '18:30-20:30', '上架', '', '', 'grape.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (76, 33, '大樱桃采摘', 50.0, '人/次', '08:00-18:00', '上架', '', '', 'apple.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (77, 33, '樱桃果酱DIY', 48.0, '人/次', '14:00-16:00', '上架', '', '', 'grape.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (78, 35, '竹海徒步导览', 30.0, '人/次', '09:00-11:00', '上架', '', '', 'mogan.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (79, 35, '乡间骑行', 50.0, '辆/天', '全天', '上架', '', '', 'room_yaodong.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (80, 36, '洱海日出骑行', 68.0, '人/次', '06:00-08:00', '上架', '', '', 'mogan.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (81, 36, '白族三道茶体验', 45.0, '人/次', '15:00-17:00', '上架', '', '', 'yuanjiacun.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (82, 37, '宏村古村导览', 30.0, '人/次', '09:00-17:00', '上架', '', '', 'mogan.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (83, 37, '徽派写生', 40.0, '人/次', '全天', '上架', '', '', 'sancai.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (84, 38, '土楼文化讲解', 25.0, '人/次', '10:00-16:00', '上架', '', '', 'mogan.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (85, 38, '客家美食制作', 68.0, '人/次', '15:00-17:00', '上架', '', '', 'yuanjiacun.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (86, 39, '遇龙河骑行', 60.0, '辆/天', '全天', '上架', '', '', 'mogan.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (87, 39, '漓江竹筏漂流', 120.0, '人/次', '09:00-16:00', '上架', '', '', 'hongcun.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (88, 40, '关中农家小吃宴', 68.0, '人/餐', '11:00-14:00,17:00-20:00', '上架', '', '', 'mixian.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (89, 40, '民俗表演', 30.0, '人/场', '19:30-20:30', '上架', '', '', 'dali.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (90, 41, '过桥米线套餐', 45.0, '人/份', '08:00-21:00', '上架', '', '', 'room_huokang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (91, 41, '米线制作体验', 68.0, '人/次', '10:00-12:00', '上架', '', '', 'yuanjiacun.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (92, 42, '跷脚牛肉套餐', 55.0, '人/餐', '10:00-21:00', '上架', '', '', 'room_huokang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (93, 42, '老汤熬制参观', 20.0, '人/次', '09:00-10:00', '上架', '', '', 'yuanjiacun.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (94, 43, '苗家土菜套餐', 65.0, '人/餐', '11:00-21:00', '上架', '', '', 'room_huokang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (95, 43, '苗绣体验', 58.0, '人/次', '14:00-16:00', '上架', '', '', 'sancai.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (96, 44, '桑拿鸡套餐', 80.0, '人/餐', '11:00-14:00,17:00-21:00', '上架', '', '', 'room_huokang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (97, 44, '顺德美食导览', 40.0, '人/次', '16:00-18:00', '上架', '', '', 'yuanjiacun.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (98, 45, '农耕体验课', 98.0, '人/次', '09:00-16:00', '上架', '', '', 'farm_study.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (99, 45, '非遗剪纸课堂', 68.0, '人/次', '14:00-16:00', '上架', '', '', 'jiansanjiang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (100, 45, '豆腐制作体验', 88.0, '人/次', '10:00-12:00', '上架', '', '', 'qiaojiao.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (101, 46, '智慧农机参观', 128.0, '人/次', '09:00-16:00', '上架', '', '', 'farm_study.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (102, 46, '稻田插秧体验', 88.0, '人/次', '10:00-15:00', '上架', '', '', 'jiansanjiang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (103, 47, '焦桐研学课堂', 88.0, '人/次', '09:00-16:00', '上架', '', '', 'farm_study.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (104, 47, '泡桐种植体验', 48.0, '人/次', '10:00-12:00', '上架', '', '', 'jiansanjiang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (105, 48, '扎草方格体验', 108.0, '人/次', '09:00-16:00', '上架', '', '', 'farm_study.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (106, 48, '梭梭种植', 60.0, '人/次', '10:00-14:00', '上架', '', '', 'jiansanjiang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (107, 49, '热带水果科普', 95.0, '人/次', '09:00-16:00', '上架', '', '', 'apple.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (108, 49, '割胶体验', 58.0, '人/次', '06:30-08:00', '上架', '', '', 'millet.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (109, 50, '蔚县剪纸体验', 68.0, '人/次', '09:00-17:00', '上架', '', '', 'larran.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (110, 50, '窗花装裱', 30.0, '人/次', '全天', '上架', '', '', 'qingci.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (111, 51, '平遥剪纸体验', 58.0, '人/次', '09:00-18:00', '上架', '', '', 'larran.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (112, 51, '古城寻宝导览', 35.0, '人/次', '10:00-12:00', '上架', '', '', 'dali.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (113, 52, '青瓷拉坯体验', 88.0, '人/次', '09:00-17:00', '上架', '', '', 'larran.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (114, 52, '青瓷刻花课', 128.0, '人/次', '14:00-16:00', '上架', '', '', 'qingci.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (115, 53, '蜡染手作体验', 76.0, '人/次', '09:00-17:00', '上架', '', '', 'larran.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (116, 53, '苗绣体验', 88.0, '人/次', '14:00-16:00', '上架', '', '', 'qingci.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (117, 54, '唐三彩点彩体验', 82.0, '人/次', '09:00-17:00', '上架', '', '', 'larran.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (118, 54, '陶马制作课', 128.0, '人/次', '14:00-16:00', '上架', '', '', 'qingci.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (119, 55, '应季果蔬采摘', 88.0, '人/次', '08:30-17:30', '上架', '采摘体验', '进园自由采摘应季果蔬，带走按斤另计，提供篮子与草帽。', 'apple.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (120, 55, '古北水镇半日游', 128.0, '人/次', '09:00-16:00', '上架', '农家餐饮', '司马台长城脚下古镇漫游，江南水乡风韵与北方古村的碰撞。', 'dali.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (121, 55, '亲子农事体验课', 68.0, '人/次', '09:30-12:00', '上架', '农耕研学', '识五谷、喂小动物、磨豆浆，配亲子手册。', 'jiansanjiang.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (122, 56, '雁栖湖环湖骑行', 58.0, '人/次', '07:00-18:00', '上架', '采摘体验', '湖边绿道骑行，湖光山色尽收眼底，提供山地车与头盔。', 'mogan.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (123, 56, '长城脚下徒步', 98.0, '人/次', '08:00-15:00', '上架', '农耕研学', '慕田峪方向野径徒步，含向导与补给。', 'hongcun.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (124, 56, '湖畔农家宴', 108.0, '人/次', '11:00-14:00', '上架', '农家餐饮', '怀柔水库鱼、虹鳟鱼两吃，配农家时蔬。', 'qiaojiao.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (125, 57, '花田研学课', 108.0, '人/次', '09:00-16:00', '上架', '农耕研学', '认识马鞭草、油葵、百日菊，学花卉种植与压花手作。', 'farm_study.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (126, 57, '花海骑行', 58.0, '人/次', '08:00-17:00', '上架', '采摘体验', '四季花海绿道骑行，延庆花海打卡黄金季。', 'dali.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (127, 57, '园艺手作工坊', 68.0, '人/次', '10:00-15:00', '上架', '非遗体验', '多肉盆栽、干花相框DIY，成品可带走。', 'qingci.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (128, 58, '豆腐宴（八菜一汤）', 128.0, '人/次', '11:00-14:00', '上架', '农家餐饮', '柳沟传统火盆锅豆腐宴，配时蔬小菜，食材本村自种。', 'mixian.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (129, 58, '石磨豆腐体验', 48.0, '人/次', '09:00-12:00', '上架', '农耕研学', '亲手推石磨、点卤水，做一锅属于自己的豆腐。', 'qiaojiao.jpg');
INSERT INTO `projects` (id, farmstay_id, name, price, unit, open_time, status, category, desc, image) VALUES (130, 58, '豆腐工坊参观', 30.0, '人/次', '08:30-17:00', '上架', '非遗体验', '看老手艺豆腐的完整制作流程，尝鲜豆浆。', 'farm_default.jpg');

-- ----------------------------
-- Table structure for rooms
-- ----------------------------
DROP TABLE IF EXISTS `rooms`;
CREATE TABLE rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmstay_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            beds INTEGER DEFAULT 1,
            price REAL DEFAULT 0,
            stock INTEGER DEFAULT 1,
            status TEXT DEFAULT '上架',
            image TEXT DEFAULT ''
        );

-- Records of rooms (22 rows)
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (15, 34, '山景大床房', 2, 268.0, 5, '上架', 'room_xiandai.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (16, 34, '家庭亲子房', 4, 368.0, 3, '上架', 'room_huokang.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (17, 34, '标准双人间', 2, 198.0, 6, '上架', 'room_yaodong.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (18, 45, '研学宿舍(8人间)', 8, 68.0, 10, '上架', 'room_mufang.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (19, 35, '竹景大床房', 2, 488.0, 4, '上架', 'mogan.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (20, 35, '溪景家庭房', 3, 588.0, 3, '上架', 'dali.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (21, 36, '洱海观景房', 2, 398.0, 5, '上架', 'hongcun.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (22, 36, '白族木屋房', 2, 298.0, 4, '上架', 'tulou.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (23, 37, '徽派古宅房', 2, 328.0, 4, '上架', 'yangshuo.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (24, 37, '临湖景观房', 2, 388.0, 2, '上架', 'miao.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (25, 38, '土楼围屋房', 2, 268.0, 6, '上架', 'yuanjiacun.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (26, 38, '土楼家庭房', 3, 328.0, 3, '上架', 'larran.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (27, 39, '山水景观房', 2, 348.0, 5, '上架', 'qingci.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (28, 39, '田园大床房', 2, 268.0, 4, '上架', 'sancai.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (29, 55, '山景小院', 2, 168.0, 4, '上架', 'pingyao_jianzhi.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (30, 55, '家庭套间', 3, 268.0, 2, '上架', 'chongli_jianzhi.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (31, 56, '湖景标准间', 2, 268.0, 3, '上架', 'mixian.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (32, 56, '湖景大床房', 2, 328.0, 2, '上架', 'qiaojiao.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (33, 57, '田园标准间', 2, 168.0, 5, '上架', 'shunde.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (34, 57, '亲子主题房', 3, 228.0, 3, '上架', 'liugou_doufu.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (35, 58, '火炕间', 2, 128.0, 4, '上架', 'farm_default.jpg');
INSERT INTO `rooms` (id, farmstay_id, name, beds, price, stock, status, image) VALUES (36, 58, '家庭火炕房', 4, 228.0, 2, '上架', 'beijing_huairou.jpg');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE products (
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
        );

-- Records of products (30 rows)
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (23, 34, '崇礼土豆', 3.5, '斤', 500, '高山土豆，沙瓤绵甜', '河北张家口崇礼', 'potato.jpg', 'XYQM1001', '上架', '2026-09-27 22:57:24');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (24, 34, '坝上莜面', 12.0, '斤', 200, '手工莜面，非遗制作', '河北张家口崇礼', 'oats.jpg', 'XYQM1002', '上架', '2026-09-27 22:57:24');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (25, 34, '山野蘑菇干', 68.0, '斤', 80, '秋季采晒，山珍美味', '河北张家口崇礼', 'mushroom.jpg', 'XYQM1003', '上架', '2026-09-27 22:57:24');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (26, 34, '高山娃娃菜', 5.0, '斤', 300, '高山冷凉蔬菜，清甜脆嫩', '河北张家口崇礼', 'vegetable.jpg', 'XYQM1004', '上架', '2026-09-27 22:57:24');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (27, 34, '崇礼小米', 9.0, '斤', 260, '坝上小米，金黄绵稠', '河北张家口崇礼', 'millet.jpg', 'XYQM1005', '上架', '2026-09-27 22:57:24');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (28, 34, '高山土蜂蜜', 58.0, '瓶', 120, '百花蜜，自然成熟', '河北张家口崇礼', 'honey.jpg', 'XYQM1006', '上架', '2026-09-27 22:57:24');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (29, 34, '坝上红薯', 4.0, '斤', 400, '沙地红薯，蜜心软糯', '河北张家口崇礼', 'sweetpotato.jpg', 'XYQM1007', '上架', '2026-09-27 22:57:24');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (30, 34, '崇礼甜玉米', 3.5, '斤', 350, '高山甜玉米，现掰现发', '河北张家口崇礼', 'corn.jpg', 'XYQM1008', '上架', '2026-09-27 22:57:24');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (31, 28, '涞源红富士苹果', 6.5, '斤', 800, '高山果园，冰糖心，脆甜多汁', '河北保定涞源', 'apple.jpg', 'XYQM1009', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (32, 28, '涞源油桃', 8.0, '斤', 600, '农家肥种植，香甜多汁', '河北保定涞源', 'peach.jpg', 'XYQM1010', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (33, 28, '涞源鸭梨', 5.5, '斤', 500, '皮薄多汁，清脆爽口', '河北保定涞源', 'pear.jpg', 'XYQM1011', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (34, 28, '涞源葡萄', 9.0, '斤', 400, '玫瑰香葡萄，粒大香甜', '河北保定涞源', 'grape.jpg', 'XYQM1012', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (35, 28, '山区土鸡蛋', 1.8, '枚', 900, '散养土鸡，天然谷物喂养', '河北保定涞源', 'egg.jpg', 'XYQM1013', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (36, 28, '涞源山核桃', 22.0, '斤', 200, '野生山核桃，皮薄仁香', '河北保定涞源', 'walnut.jpg', 'XYQM1014', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (37, 29, '洛川红富士苹果', 8.0, '斤', 900, '高原冰糖心，脆甜多汁', '陕西延安洛川', 'luochuan.jpg', 'XYQM1015', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (38, 30, '仙居杨梅', 25.0, '盒', 300, '东魁杨梅，个大汁多', '浙江台州仙居', 'yangmei.jpg', 'XYQM1016', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (39, 31, '石林血桃', 10.0, '斤', 400, '喀斯特脆桃，红润香甜', '云南昆明石林', 'shilin.jpg', 'XYQM1017', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (40, 32, '阿克苏冰糖心苹果', 9.9, '斤', 800, '冰糖心，脆甜多汁', '新疆阿克苏', 'akesu.jpg', 'XYQM1018', '上架', '2026-09-27 22:57:25');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (41, 33, '烟台大樱桃', 39.9, '盒', 400, '美早大果，北纬37度甜蜜', '山东烟台', 'yantai.jpg', 'XYQM1019', '上架', '2026-09-27 22:57:26');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (42, 46, '建三江大米', 12.8, '袋', 600, '北大荒黑土，米香绵软', '黑龙江佳木斯', 'jiansanjiang.jpg', 'XYQM1020', '上架', '2026-09-27 22:57:26');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (43, 49, '儋州香蕉', 5.5, '斤', 500, '热带香蕉，自然熟', '海南儋州', 'danzhou.jpg', 'XYQM1021', '上架', '2026-09-27 22:57:26');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (44, 52, '龙泉青瓷茶杯', 128.0, '只', 100, '手工青瓷，粉青釉色', '浙江丽水龙泉', 'qingci.jpg', 'XYQM1022', '上架', '2026-09-27 22:57:26');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (45, 55, '密云板栗', 9.8, '斤', 200, '燕山板栗，皮薄肉厚，糖炒、炖肉皆宜。', '北京密云', 'product_banli.jpg', 'XYQM1023', '上架', '2026-09-29 16:18:47');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (46, 55, '古北口山楂', 6.5, '斤', 150, '酸甜开胃，农家自制山楂条原料。', '北京密云', 'product_shanzha.jpg', 'XYQM1024', '上架', '2026-09-29 16:18:47');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (47, 56, '怀柔虹鳟鱼', 28.0, '斤', 80, '鲜活冷水鱼，肉质细嫩，适合烧烤与清蒸。', '北京怀柔', 'product_hongzun.jpg', 'XYQM1025', '上架', '2026-09-29 16:18:47');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (48, 56, '板栗仁', 15.0, '袋', 120, '去皮熟板栗仁，开袋即食。', '北京怀柔', 'product_banliren.jpg', 'XYQM1026', '上架', '2026-09-29 16:18:47');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (49, 57, '延庆国光苹果', 8.5, '斤', 300, '果肉紧实酸甜，京郊老品种，秋收时令果。', '北京延庆', 'product_guoguang.jpg', 'XYQM1027', '上架', '2026-09-29 16:18:47');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (50, 57, '四季花海干花束', 25.0, '束', 60, '当季鲜花烘干制成，留住花海的颜色。', '北京延庆', 'product_ganhua.jpg', 'XYQM1028', '上架', '2026-09-29 16:18:47');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (51, 58, '柳沟卤水豆腐', 5.0, '块', 200, '卤水点制，豆香浓郁，可真空打包带走。', '北京延庆', 'product_laoshui.jpg', 'XYQM1029', '上架', '2026-09-29 16:18:47');
INSERT INTO `products` (id, farmstay_id, name, price, unit, stock, description, origin, image, trace_code, status, created_at) VALUES (52, 58, '自制豆干', 18.0, '斤', 100, '五香豆干，真空包装，下酒小菜。', '北京延庆', 'product_dougan.jpg', 'XYQM1030', '上架', '2026-09-29 16:18:47');

-- ----------------------------
-- Table structure for trace_records
-- ----------------------------
DROP TABLE IF EXISTS `trace_records`;
CREATE TABLE trace_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            stage TEXT DEFAULT '',
            location TEXT DEFAULT '',
            detail TEXT DEFAULT '',
            recorder TEXT DEFAULT '',
            record_time TEXT DEFAULT (datetime('now', 'localtime'))
        );

-- Records of trace_records (150 rows)
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (111, 23, '种植', '河北张家口崇礼', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (112, 23, '管理', '河北张家口崇礼', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (113, 23, '采摘', '河北张家口崇礼', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (114, 23, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (115, 23, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (116, 24, '种植', '河北张家口崇礼', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (117, 24, '管理', '河北张家口崇礼', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (118, 24, '采摘', '河北张家口崇礼', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (119, 24, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (120, 24, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (121, 25, '种植', '河北张家口崇礼', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (122, 25, '管理', '河北张家口崇礼', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (123, 25, '采摘', '河北张家口崇礼', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (124, 25, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (125, 25, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (126, 26, '种植', '河北张家口崇礼', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (127, 26, '管理', '河北张家口崇礼', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (128, 26, '采摘', '河北张家口崇礼', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (129, 26, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (130, 26, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (131, 27, '种植', '河北张家口崇礼', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (132, 27, '管理', '河北张家口崇礼', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (133, 27, '采摘', '河北张家口崇礼', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (134, 27, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (135, 27, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (136, 28, '种植', '河北张家口崇礼', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (137, 28, '管理', '河北张家口崇礼', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (138, 28, '采摘', '河北张家口崇礼', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (139, 28, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (140, 28, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (141, 29, '种植', '河北张家口崇礼', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (142, 29, '管理', '河北张家口崇礼', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (143, 29, '采摘', '河北张家口崇礼', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (144, 29, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (145, 29, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (146, 30, '种植', '河北张家口崇礼', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (147, 30, '管理', '河北张家口崇礼', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (148, 30, '采摘', '河北张家口崇礼', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (149, 30, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:24');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (150, 30, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (151, 31, '种植', '河北保定涞源', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (152, 31, '管理', '河北保定涞源', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (153, 31, '采摘', '河北保定涞源', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (154, 31, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (155, 31, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (156, 32, '种植', '河北保定涞源', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (157, 32, '管理', '河北保定涞源', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (158, 32, '采摘', '河北保定涞源', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (159, 32, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (160, 32, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (161, 33, '种植', '河北保定涞源', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (162, 33, '管理', '河北保定涞源', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (163, 33, '采摘', '河北保定涞源', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (164, 33, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (165, 33, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (166, 34, '种植', '河北保定涞源', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (167, 34, '管理', '河北保定涞源', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (168, 34, '采摘', '河北保定涞源', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (169, 34, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (170, 34, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (171, 35, '种植', '河北保定涞源', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (172, 35, '管理', '河北保定涞源', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (173, 35, '采摘', '河北保定涞源', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (174, 35, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (175, 35, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (176, 36, '种植', '河北保定涞源', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (177, 36, '管理', '河北保定涞源', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (178, 36, '采摘', '河北保定涞源', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (179, 36, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (180, 36, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (181, 37, '种植', '陕西延安洛川', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (182, 37, '管理', '陕西延安洛川', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (183, 37, '采摘', '陕西延安洛川', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (184, 37, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (185, 37, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (186, 38, '种植', '浙江台州仙居', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (187, 38, '管理', '浙江台州仙居', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (188, 38, '采摘', '浙江台州仙居', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (189, 38, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (190, 38, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (191, 39, '种植', '云南昆明石林', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (192, 39, '管理', '云南昆明石林', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (193, 39, '采摘', '云南昆明石林', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (194, 39, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (195, 39, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (196, 40, '种植', '新疆阿克苏', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (197, 40, '管理', '新疆阿克苏', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (198, 40, '采摘', '新疆阿克苏', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (199, 40, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (200, 40, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:25');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (201, 41, '种植', '山东烟台', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (202, 41, '管理', '山东烟台', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (203, 41, '采摘', '山东烟台', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (204, 41, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (205, 41, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (206, 42, '种植', '黑龙江佳木斯', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (207, 42, '管理', '黑龙江佳木斯', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (208, 42, '采摘', '黑龙江佳木斯', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (209, 42, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (210, 42, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (211, 43, '种植', '海南儋州', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (212, 43, '管理', '海南儋州', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (213, 43, '采摘', '海南儋州', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (214, 43, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (215, 43, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (216, 44, '种植', '浙江丽水龙泉', '选用当地优良品种，农家肥种植，不使用化学农药。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (217, 44, '管理', '浙江丽水龙泉', '人工除草、物理防虫，全程生态管理。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (218, 44, '采摘', '浙江丽水龙泉', '成熟期人工分批采摘，精选优质果。', '农户', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (219, 44, '检测', '县级农产品质检站', '农残检测合格，可放心食用。', '质检站', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (220, 44, '上架', '乡约阡陌平台', '产地直供，溯源档案完整。', '平台', '2026-09-27 22:57:26');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (221, 45, '种植', '北京密云', '密云区板栗基地，山区坡地老树板栗，自然落果采收。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (222, 45, '管理', '北京密云', '人工除虫、疏枝管理，板栗品质稳定。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (223, 45, '采摘', '北京密云', '白露前后分批捡拾，剔除虫果。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (224, 45, '检测', '县级农产品质检站', '板栗水分与农残检测合格。', '质检站', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (225, 45, '上架', '乡约阡陌平台', '密云板栗直供，溯源档案完整。', '平台', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (226, 46, '种植', '北京密云', '古北口镇浅山丘陵山楂园，老品种大山楂。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (227, 46, '管理', '北京密云', '修剪控旺、生物防虫，全程生态管理。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (228, 46, '采摘', '北京密云', '霜降前人工采摘，果色红亮。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (229, 46, '检测', '县级农产品质检站', '山楂农残检测合格，果肉紧实。', '质检站', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (230, 46, '上架', '乡约阡陌平台', '古北口山楂直供，溯源档案完整。', '平台', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (231, 47, '种植', '北京怀柔', '怀柔区冷水鱼养殖基地，山泉水活水养殖。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (232, 47, '管理', '北京怀柔', '定期换水、科学投喂，水质全程监测。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (233, 47, '采摘', '北京怀柔', '分塘捕捞，活鱼冷链直送。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (234, 47, '检测', '县级农产品质检站', '鱼体检疫与兽药残留检测合格。', '质检站', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (235, 47, '上架', '乡约阡陌平台', '怀柔虹鳟鱼直供，溯源档案完整。', '平台', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (236, 48, '种植', '北京怀柔', '怀柔板栗加工车间，选用当年新板栗。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (237, 48, '管理', '北京怀柔', '脱壳分选、低温烘焙，无添加剂。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (238, 48, '采摘', '北京怀柔', '成熟板栗人工脱壳，剔除坏果。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (239, 48, '检测', '县级农产品质检站', '成品水分与微生物检测合格。', '质检站', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (240, 48, '上架', '乡约阡陌平台', '板栗仁加工直供，溯源档案完整。', '平台', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (241, 49, '种植', '北京延庆', '延庆区旧县镇国光苹果园，昼夜温差大。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (242, 49, '管理', '北京延庆', '农家肥种植、套袋防虫，老树结果。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (243, 49, '采摘', '北京延庆', '十月成熟期人工分批采摘。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (244, 49, '检测', '县级农产品质检站', '苹果糖度与农残检测合格。', '质检站', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (245, 49, '上架', '乡约阡陌平台', '延庆国光苹果直供，溯源档案完整。', '平台', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (246, 50, '种植', '北京延庆', '延庆四季花海种植区，百日草、格桑花等。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (247, 50, '管理', '北京延庆', '露地种植、物理防虫，花期轮作。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (248, 50, '采摘', '北京延庆', '盛花期人工剪取，自然晾干。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (249, 50, '检测', '县级农产品质检站', '干花含水率与霉变检测合格。', '质检站', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (250, 50, '上架', '乡约阡陌平台', '四季花海干花直供，溯源档案完整。', '平台', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (251, 51, '种植', '北京延庆', '延庆柳沟村豆腐坊，非遗手工卤水点浆。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (252, 51, '管理', '北京延庆', '选本地黄豆，泡豆磨浆，卤水点制。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (253, 51, '采摘', '北京延庆', '每日凌晨现做，晾凉装盒。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (254, 51, '检测', '县级农产品质检站', '豆腐菌落与重金属检测合格。', '质检站', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (255, 51, '上架', '乡约阡陌平台', '柳沟卤水豆腐直供，溯源档案完整。', '平台', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (256, 52, '种植', '北京延庆', '延庆柳沟村豆腐坊，手工卤制豆干。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (257, 52, '管理', '北京延庆', '卤水豆腐压制成型，老汤卤煮入味。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (258, 52, '采摘', '北京延庆', '卤煮后自然风干，真空包装。', '农户', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (259, 52, '检测', '县级农产品质检站', '豆干微生物与防腐剂检测合格。', '质检站', '2026-09-29 21:04:18');
INSERT INTO `trace_records` (id, product_id, stage, location, detail, recorder, record_time) VALUES (260, 52, '上架', '乡约阡陌平台', '自制豆干直供，溯源档案完整。', '平台', '2026-09-29 21:04:18');

-- ----------------------------
-- Table structure for bookings
-- ----------------------------
DROP TABLE IF EXISTS `bookings`;
CREATE TABLE bookings (
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
        );

-- Records of bookings (3 rows)
INSERT INTO `bookings` (id, booking_no, user_id, farmstay_id, project_id, visit_date, people, phone, remark, add_product, status, created_at) VALUES (1, 'XYQM61757709', 25, 57, 0, '2026-10-05', 2, '13800001111', '', 1, '已取消', '2026-09-29 14:56:06');
INSERT INTO `bookings` (id, booking_no, user_id, farmstay_id, project_id, visit_date, people, phone, remark, add_product, status, created_at) VALUES (2, 'XYQM31818033', 25, 39, 0, '2026-10-03', 2, '43573535', '', 1, '待审核', '2026-10-03 22:11:09');
INSERT INTO `bookings` (id, booking_no, user_id, farmstay_id, project_id, visit_date, people, phone, remark, add_product, status, created_at) VALUES (3, 'XYQM00511732', 25, 58, 0, '2026-10-19', 2, 'g ji l 115151', '', 0, '待审核', '2026-10-03 22:14:11');

-- ----------------------------
-- Table structure for product_orders
-- ----------------------------
DROP TABLE IF EXISTS `product_orders`;
CREATE TABLE product_orders (
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
        );

-- Records of product_orders (8 rows)
INSERT INTO `product_orders` (id, order_no, user_id, product_id, quantity, status, recv_name, recv_phone, recv_address, company_name, tracking_number, expected_arrival, refund_reason, refund_time, created_at) VALUES (1, 'PO23026516', 25, 23, 2, '已退款', '张小明', '13800001111', '北京市海淀区学院路1号院3号楼', '顺丰快递', 'SF88888888', '2026-10-01', '产品包装破损，申请退货退款', '2026-09-29 11:54', '2026-09-28 16:43:46');
INSERT INTO `product_orders` (id, order_no, user_id, product_id, quantity, status, recv_name, recv_phone, recv_address, company_name, tracking_number, expected_arrival, refund_reason, refund_time, created_at) VALUES (2, 'PO24026524', 26, 24, 1, '待发货', '李小红', '13800002222', '上海市浦东新区张江路88号', '', '', '', '', '', '2026-09-28 16:43:46');
INSERT INTO `product_orders` (id, order_no, user_id, product_id, quantity, status, recv_name, recv_phone, recv_address, company_name, tracking_number, expected_arrival, refund_reason, refund_time, created_at) VALUES (3, 'PO25026531', 25, 25, 3, '已发货', '张小明', '13800001111', '北京市海淀区学院路1号院3号楼', '顺丰快递', 'SF026.516336', '2026-09-29', '', '', '2026-09-28 16:43:46');
INSERT INTO `product_orders` (id, order_no, user_id, product_id, quantity, status, recv_name, recv_phone, recv_address, company_name, tracking_number, expected_arrival, refund_reason, refund_time, created_at) VALUES (4, 'PO26026539', 26, 26, 1, '已发货', '李小红', '13800002222', '上海市浦东新区张江路88号', '中通快递', 'ZT026.516336', '2026-09-30', '', '', '2026-09-28 16:43:46');
INSERT INTO `product_orders` (id, order_no, user_id, product_id, quantity, status, recv_name, recv_phone, recv_address, company_name, tracking_number, expected_arrival, refund_reason, refund_time, created_at) VALUES (5, 'PO27026545', 25, 27, 2, '已签收', '张小明', '13800001111', '北京市海淀区学院路1号院3号楼', '圆通快递', 'YT026.516336', '2026-09-22 16:43', '', '', '2026-09-28 16:43:46');
INSERT INTO `product_orders` (id, order_no, user_id, product_id, quantity, status, recv_name, recv_phone, recv_address, company_name, tracking_number, expected_arrival, refund_reason, refund_time, created_at) VALUES (6, 'PO24533549', 25, 44, 1, '待发货', '测试收货人', '13800009999', '河北省保定市竞秀区测试路1号', '', '', '', '', '', '2026-09-28 16:48:52');
INSERT INTO `product_orders` (id, order_no, user_id, product_id, quantity, status, recv_name, recv_phone, recv_address, company_name, tracking_number, expected_arrival, refund_reason, refund_time, created_at) VALUES (7, 'PO32219294', 25, 44, 1, '已取消', '张小明', '13800001111', '北京市海淀区学院路1号', '', '', '', '', '', '2026-09-29 11:45:46');
INSERT INTO `product_orders` (id, order_no, user_id, product_id, quantity, status, recv_name, recv_phone, recv_address, company_name, tracking_number, expected_arrival, refund_reason, refund_time, created_at) VALUES (8, 'PO89598244', 25, 44, 1, '待发货', '张小明', '13800001111', '北京市海淀区学院路1号', '', '', '', '', '', '2026-09-29 14:53:50');

-- ----------------------------
-- Table structure for carts
-- ----------------------------
DROP TABLE IF EXISTS `carts`;
CREATE TABLE carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            UNIQUE(user_id, product_id)
        );

-- Records of carts (0 rows)

-- ----------------------------
-- Table structure for notices
-- ----------------------------
DROP TABLE IF EXISTS `notices`;
CREATE TABLE notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT DEFAULT '',
            category TEXT DEFAULT '农旅活动',     -- 农旅活动/政策公告/平台通知
            status TEXT DEFAULT '启用',            -- 启用/停用
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

-- Records of notices (4 rows)
INSERT INTO `notices` (id, title, content, category, status, created_at) VALUES (1, '乡约阡陌平台上线公告', '平台已接入全国31个农旅目的地与30款助农特产，支持在线下单、物流配送、溯源查询，欢迎体验！', '平台通知', '启用', '2026-09-29 11:33:47');
INSERT INTO `notices` (id, title, content, category, status, created_at) VALUES (2, '国庆假期服务提示', '国庆期间部分农家乐预约火爆，建议提前1-2天预约；特产订单物流可能延迟1-2天，感谢理解。', '政策公告', '启用', '2026-09-29 11:33:47');
INSERT INTO `notices` (id, title, content, category, status, created_at) VALUES (3, '2026全国乡村丰收节预约通道开启', '2026全国乡村丰收节预约通道开启。详见平台公告栏。', '农旅活动', '启用', '2026-09-29 14:37:24');
INSERT INTO `notices` (id, title, content, category, status, created_at) VALUES (4, '婺源晒秋摄影大赛报名中', '婺源晒秋摄影大赛报名中。详见平台公告栏。', '农旅活动', '启用', '2026-09-29 14:37:24');

-- ----------------------------
-- Table structure for logistics_tracks
-- ----------------------------
DROP TABLE IF EXISTS `logistics_tracks`;
CREATE TABLE logistics_tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            node TEXT DEFAULT '',                  -- 节点说明
            location TEXT DEFAULT '',              -- 地点
            track_time TEXT DEFAULT '',            -- 时间
            sort INTEGER DEFAULT 0
        );

-- Records of logistics_tracks (12 rows)
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (1, 3, '商家已发货，包裹已交给顺丰快递', '河北保定涞源县发货仓', '2026-09-24 16:43', 1);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (2, 3, '包裹已到达北京顺丰分拨中心', '北京市顺义区', '2026-09-26 16:43', 2);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (3, 3, '运输中，即将送达目的地', '运输途中', '2026-09-27 16:43', 3);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (4, 4, '商家已发货，包裹已交给中通快递', '浙江台州仙居县发货仓', '2026-09-26 16:43', 1);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (5, 4, '包裹已到达上海中通分拨中心', '上海市青浦区', '2026-09-27 16:43', 2);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (6, 5, '商家已发货，包裹已交给圆通快递', '云南昆明石林发货仓', '2026-09-22 16:43', 1);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (7, 5, '包裹已到达昆明圆通分拨中心', '云南省昆明市', '2026-09-24 16:43', 2);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (8, 5, '包裹已到达北京朝阳区派送点，快递员派送中', '北京市朝阳区', '2026-09-26 16:43', 3);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (9, 5, '包裹已签收，感谢您在乡约阡陌选购', '北京市海淀区', '2026-09-27 16:43', 4);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (10, 1, '商家已发货，包裹已交给顺丰快递', '发货地', '2026-09-28 16:50', 1);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (11, 1, '包裹已到达顺丰快递分拨中心', '中转中心', '2026-09-28 16:50', 2);
INSERT INTO `logistics_tracks` (id, order_id, node, location, track_time, sort) VALUES (12, 1, '运输中，即将送达目的地', '运输途中', '2026-09-28 16:50', 3);

-- ----------------------------
-- Table structure for resources
-- ----------------------------
DROP TABLE IF EXISTS `resources`;
CREATE TABLE resources (
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
        );

-- Records of resources (6 rows)
INSERT INTO `resources` (id, user_id, rtype, title, region, description, price, contact, image, status, created_at) VALUES (7, 28, '闲置农具', '闲置播种机一台', '河北省-保定市-涞源县', '八成新小型播种机，可出租可转让。', 200.0, '赵大姐 13800001004', 'farm_pick.jpg', '发布中', '2026-09-27 22:57:26');
INSERT INTO `resources` (id, user_id, rtype, title, region, description, price, contact, image, status, created_at) VALUES (8, 27, '闲置农房', '青山村农家院东厢房', '河北省-张家口市-崇礼区', '独立小院东厢房两间，可做仓库或民宿改造。', 500.0, '王叔 13800001003', 'yuanjiacun.jpg', '发布中', '2026-09-27 22:57:26');
INSERT INTO `resources` (id, user_id, rtype, title, region, description, price, contact, image, status, created_at) VALUES (9, 28, '临时用工', '苹果采摘季招工', '河北省-保定市-涞源县', '10月中旬苹果采摘季，招10名临时工，管吃住。', 150.0, '赵大姐 13800001004', 'apple.jpg', '发布中', '2026-09-27 22:57:26');
INSERT INTO `resources` (id, user_id, rtype, title, region, description, price, contact, image, status, created_at) VALUES (10, 26, '土地流转', '涞源白石山脚下2亩地', '河北省-保定市-涞源县', '2亩菜地，水源方便，适合有机种植。', 800.0, '游客小凯 13800001002', 'vegetable.jpg', '发布中', '2026-09-27 22:57:26');
INSERT INTO `resources` (id, user_id, rtype, title, region, description, price, contact, image, status, created_at) VALUES (11, 33, '闲置农房', '莫干山民宿旁老屋一间', '浙江省-湖州市-德清县', '竹海边的老屋，适合改造工作室或茶室。', 1200.0, '江南乡居 13800001009', 'mogan.jpg', '发布中', '2026-09-27 22:57:26');
INSERT INTO `resources` (id, user_id, rtype, title, region, description, price, contact, image, status, created_at) VALUES (12, 34, '临时用工', '杨梅季采摘招工', '浙江省-台州市-仙居县', '六月杨梅季，招20名采摘工，日结。', 200.0, '云岭农旅 13800001010', 'yangmei.jpg', '发布中', '2026-09-27 22:57:26');

-- ----------------------------
-- Table structure for resource_intents
-- ----------------------------
DROP TABLE IF EXISTS `resource_intents`;
CREATE TABLE resource_intents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT DEFAULT '',
            status TEXT DEFAULT '待对接',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

-- Records of resource_intents (1 rows)
INSERT INTO `resource_intents` (id, resource_id, user_id, message, status, created_at) VALUES (1, 12, 25, '想招3名采摘工，能否推荐？', '待对接', '2026-09-29 14:57:48');

-- ----------------------------
-- Table structure for reviews
-- ----------------------------
DROP TABLE IF EXISTS `reviews`;
CREATE TABLE reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            farmstay_id INTEGER NOT NULL,
            rating INTEGER DEFAULT 5,
            content TEXT DEFAULT '',
            reply TEXT DEFAULT '',
            status TEXT DEFAULT '正常',
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        );

-- Records of reviews (15 rows)
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (8, 25, 34, 5, '环境特别好，推窗就是山，农家饭特别香，孩子玩得不想走！', '', '正常', '2026-09-27 22:57:26');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (9, 26, 34, 4, '住宿干净，早餐的土豆丝绝了，就是周末人多一点。', '', '正常', '2026-09-27 22:57:26');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (10, 25, 28, 5, '赵大姐特别热情，苹果又甜又脆，孩子第一次摘苹果超开心。', '', '正常', '2026-09-27 22:57:26');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (11, 25, 35, 5, '莫干山的竹海太治愈了，民宿干净有设计感，早餐很精致。', '', '正常', '2026-09-27 22:57:26');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (12, 26, 36, 5, '洱海边的白族小院，老板人很好，三道茶体验很地道。', '', '正常', '2026-09-27 22:57:26');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (13, 25, 41, 5, '过桥米线发源地果然不一样，汤鲜料足，一碗下肚太满足了。', '', '正常', '2026-09-27 22:57:26');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (14, 26, 48, 5, '带孩子扎草方格种梭梭，治沙故事很震撼，很棒的研学体验。', '', '正常', '2026-09-27 22:57:26');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (15, 2, 55, 5, '采摘园很大，果子又大又甜，孩子玩得不想走！', '', '正常', '2026-09-29 16:18:47');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (16, 3, 55, 5, '小院干净，晚上看星星特别清楚，老板热情。', '', '正常', '2026-09-29 16:18:47');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (17, 2, 56, 5, '湖景房太美了，早上推窗就是湖面晨雾。', '', '正常', '2026-09-29 16:18:47');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (18, 3, 56, 4, '鱼做得地道，就是周末人多要早点订。', '', '正常', '2026-09-29 16:18:47');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (19, 2, 57, 5, '研学课老师很专业，孩子学会了认识十几种花。', '', '正常', '2026-09-29 16:18:47');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (20, 3, 57, 5, '九月的花海真的绝，随手一拍都是壁纸。', '', '正常', '2026-09-29 16:18:47');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (21, 2, 58, 5, '豆腐宴名不虚传，火盆锅咕嘟咕嘟特别有年味。', '', '正常', '2026-09-29 16:18:47');
INSERT INTO `reviews` (id, user_id, farmstay_id, rating, content, reply, status, created_at) VALUES (22, 3, 58, 5, '带孩子体验了磨豆腐，回来一直念叨还要去。', '', '正常', '2026-09-29 16:18:47');

-- ----------------------------
-- Table structure for favorites
-- ----------------------------
DROP TABLE IF EXISTS `favorites`;
CREATE TABLE favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target_type TEXT DEFAULT 'farmstay',  -- farmstay/product
            target_id INTEGER NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            UNIQUE(user_id, target_type, target_id)
        );

-- Records of favorites (0 rows)

-- ----------------------------
-- Table structure for banners
-- ----------------------------
DROP TABLE IF EXISTS `banners`;
CREATE TABLE banners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT DEFAULT '',
            image TEXT DEFAULT 'banner1.jpg',
            link TEXT DEFAULT '/',
            sort INTEGER DEFAULT 0
        );

-- Records of banners (3 rows)
INSERT INTO `banners` (id, title, image, link, sort) VALUES (4, '全国农旅地图 · 31个乡村目的地任你挑', 'banner1.jpg', '/farmstays', 0);
INSERT INTO `banners` (id, title, image, link, sort) VALUES (5, '助农专区 · 全国各地土特产直达', 'banner2.jpg', '/products', 0);
INSERT INTO `banners` (id, title, image, link, sort) VALUES (6, 'AI出行规划 · 一键定制全国乡村游', 'banner3.jpg', '/ai_travel', 0);
