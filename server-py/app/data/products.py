"""家电产品 Mock 数据：效果图 + 细节图 + 卖点 + 参数"""

_U = "https://images.unsplash.com/"

PRODUCTS = [
    {
        "id": "fridge-508",
        "name": "卡萨帝 508L 法式对开门冰箱",
        "category": "冰箱",
        "price": 6999,
        "badge": "热销",
        "main_image": _U + "photo-1584568694244-14fbdf83bd30?w=900&q=80",
        "detail_images": [
            _U + "photo-1571175443880-49e1d25b2bc5?w=600&q=80",
            _U + "photo-1593359677879-a4bb92f829d1?w=600&q=80",
        ],
        "slogan": "细胞级养鲜，果蔬 7 天新鲜如初",
        "features": ["细胞级养鲜", "全空间恒温", "智能除菌", "508L 大容量"],
        "params": {
            "总容积": "508L",
            "能效等级": "新一级能效",
            "制冷方式": "风冷无霜",
            "噪音": "35dB",
            "尺寸": "833×665×1800mm",
        },
        "description": "法式对开门设计，搭载细胞级养鲜科技，果蔬保鲜周期提升 30%；全空间恒温与智能除菌净化，守护全家饮食健康。",
    },
    {
        "id": "washer-10kg",
        "name": "海尔 10kg 洗烘一体滚筒洗衣机",
        "category": "洗衣机",
        "price": 4599,
        "badge": "新品",
        "main_image": _U + "photo-1626806787461-102c1bfaaea1?w=900&q=80",
        "detail_images": [
            _U + "photo-1604335399105-a0c585fd81a1?w=600&q=80",
            _U + "photo-1626806787461-102c1bfaaea1?w=600&q=80",
        ],
        "slogan": "洗烘 15 分钟，即洗即穿",
        "features": ["洗烘一体", "AI 智慧洗", "紫外线除菌", "1:1 正反转"],
        "params": {
            "洗涤容量": "10kg",
            "烘干容量": "7kg",
            "能效等级": "一级",
            "电机": "BLDC 变频",
            "尺寸": "595×530×850mm",
        },
        "description": "10kg 洗烘一体，微蒸汽空气洗快速除味；AI 智慧洗自动匹配洗涤方案，变频静音更节能。",
    },
    {
        "id": "ac-15p",
        "name": "海尔 1.5 匹新一级变频空调",
        "category": "空调",
        "price": 3299,
        "badge": "节能",
        "main_image": _U + "photo-1584622650111-993a426fbf0a?w=900&q=80",
        "detail_images": [
            _U + "photo-1584622650111-993a426fbf0a?w=600&q=80",
        ],
        "slogan": "30 秒速冷，一晚低至 1 度电",
        "features": ["新一级能效", "30 秒速冷", "自清洁", "智能除湿"],
        "params": {
            "匹数": "1.5 匹",
            "能效等级": "新一级",
            "循环风量": "650m³/h",
            "噪音": "18dB",
            "适用面积": "16-22㎡",
        },
        "description": "新一级能效变频，30 秒速冷 60 秒速热；内外机自清洁，第五代智能除湿，舒适静音。",
    },
    {
        "id": "tv-65",
        "name": "海尔 65 英寸 4K 全面屏智能电视",
        "category": "电视",
        "price": 4999,
        "badge": "影音旗舰",
        "main_image": _U + "photo-1549490349-8643362247b5?w=900&q=80",
        "detail_images": [
            _U + "photo-1549490349-8643362247b5?w=600&q=80",
        ],
        "slogan": "8K 解码，影院级视听",
        "features": ["4K HDR", "120Hz 高刷", "杜比全景声", "AI 语音"],
        "params": {
            "屏幕尺寸": "65 英寸",
            "分辨率": "3840×2160 (4K)",
            "刷新率": "120Hz",
            "亮度": "500nits",
            "系统": "Android 11",
        },
        "description": "65 英寸 4K 全面屏，120Hz 高刷新率，MEMC 运动补偿；杜比全景声，AI 语音控制，海量内容随心看。",
    },
    {
        "id": "range-hood",
        "name": "海尔智能烟灶套装",
        "category": "厨房电器",
        "price": 2999,
        "badge": "套装优惠",
        "main_image": _U + "photo-1556911220-bff31c812dba?w=900&q=80",
        "detail_images": [
            _U + "photo-1556911220-bff31c812dba?w=600&q=80",
        ],
        "slogan": "22m³ 大吸力，挥手即控",
        "features": ["22m³ 大吸力", "挥手感应", "5.0kW 猛火", "一级能效"],
        "params": {
            "风量": "22m³/min",
            "风压": "420Pa",
            "灶具火力": "5.0kW",
            "能效等级": "一级",
            "噪音": "52dB",
        },
        "description": "22m³ 大吸力油烟机，挥手感应开关；5.0kW 大火力燃气灶，烟灶联动，厨房清新无油烟。",
    },
    {
        "id": "freezer-200",
        "name": "海尔 200L 风冷无霜冷柜",
        "category": "冷柜",
        "price": 3899,
        "badge": "囤货必备",
        "main_image": _U + "photo-1593359677879-a4bb92f829d1?w=900&q=80",
        "detail_images": [
            _U + "photo-1571175443880-49e1d25b2bc5?w=600&q=80",
        ],
        "slogan": "大容量囤鲜，-40℃ 深冷速冻",
        "features": ["风冷无霜", "-40℃ 深冷", "200L 大容量", "一键速冻"],
        "params": {
            "总容积": "200L",
            "制冷方式": "风冷无霜",
            "最低温度": "-40℃",
            "能效等级": "一级",
            "尺寸": "940×560×860mm",
        },
        "description": "200L 大容量风冷冷柜，-40℃ 深冷速冻锁住营养；一键速冻、断电保温，年节囤货无忧。",
    },
]


def get_product(product_id: str):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None
