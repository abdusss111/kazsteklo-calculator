from data.glass_price import get_glass_price_legal, get_glass_price_physical, get_glass_price_economy
from data.furniture_price import get_furniture_price_legal, get_furniture_price_physical
def debug(msg):
    print(msg)


def calculate_price(args: dict) -> dict:
    # === ВХОДНЫЕ ПАРАМЕТРЫ ===
    shower_type = args.get("shower_type", "П-образная")
    customer_type = args.get("customer_type", "физлицо")  # физлицо или юрлицо
    glass_type = args.get("glass_type", "Стекло Ритм")
    frame_type = args.get("frame_type", "Квадратная труба")
    hardware_color = args.get("hardware_color", "Бронза")
    length = float(args.get("length", 2))
    height = float(args.get("height", 2))
    mount_type = args.get("mount_type", "На П-профиле")
    connector_type = args.get("connector_type", "Коннектор П-образный")
    handle_type = args.get("handle_type", "Скоба")
    bottom_element = args.get("bottom_element", "Порожек")
    binding_type = args.get("binding_type", "По периметру")
    door_count = args.get("door_count", "Две")
    door_position = args.get("door_position", "С боку")  # только для П-образной
    magnet_seal_type = args.get("magnet_seal_type", "Без магнитного уплотнителя")
    binding_position = args.get("binding_position", "Обвязка над стеклом")
    seal_type = args.get("seal_type", "Полусфера")
    rigid_element_type = args.get("rigid_element_type", "Труба круглая")  # Труба круглая / Штанга круглая / Штанга квадратная
    curtain_type = args.get("curtain_type", "Распашное")  # Распашное / Стационар / Гормошка
    city = args.get("city", "Алматы")

    # === DEBUG: вывод всех входных параметров ===
    debug("[DEBUG] Входные параметры:")
    debug(f"  shower_type: {shower_type}")
    debug(f"  customer_type: {customer_type}")
    debug(f"  glass_type: {glass_type}")
    debug(f"  frame_type: {frame_type}")
    debug(f"  hardware_color: {hardware_color}")
    debug(f"  length: {length}")
    debug(f"  height: {height}")
    debug(f"  mount_type: {mount_type}")
    debug(f"  connector_type: {connector_type}")
    debug(f"  handle_type: {handle_type}")
    debug(f"  bottom_element: {bottom_element}")
    debug(f"  binding_type: {binding_type}")
    debug(f"  door_count: {door_count}")
    debug(f"  door_position: {door_position}")
    debug(f"  magnet_seal_type: {magnet_seal_type}")
    debug(f"  binding_position: {binding_position}")
    debug(f"  seal_type: {seal_type}")
    debug(f"  rigid_element_type: {rigid_element_type}")
    debug(f"  curtain_type: {curtain_type}")
    debug(f"  city: {city}")

    # === ЦЕНЫ НА СТЕКЛО ===
    glass_prices_physical = get_glass_price_physical()

    glass_prices_economy = get_glass_price_economy()

    glass_prices_legal = get_glass_price_legal()


    if customer_type == "юрлицо":
        glass_price_m2 = glass_prices_legal.get(glass_type, 0)
    else:
        glass_price_m2 = glass_prices_physical.get(glass_type, 0)
    glass_total = glass_price_m2 * length * height

    glass_price_m2_economy = glass_prices_economy.get(glass_type, glass_price_m2)
    glass_total_economy = glass_price_m2_economy * length * height

    # === СУФФИКС ПО ЦВЕТУ ===
    color_suffix = {
    "Хром": "",
    "Черная": "b",
    "Бронза": "br",
    "Золото": "g"
    }
    suffix = color_suffix.get(hardware_color, "")


    # === ВСТАВЬ СЮДА КАТАЛОГ ЦЕН SKU ===
    price_catalog_physical = get_furniture_price_physical()


    price_catalog_legal = get_furniture_price_legal()

    # === ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ОКРУГЛЕНИЯ КАК В EXCEL ===
    def roundup_excel(value):
        val = float(value)
        return int(val) + (1 if val % 1 != 0 else 0)

    # === ОБЩИЙ РАСЧЁТ ДЛЯ ВСЕХ ТИПОВ ===

    # Кол-во профиля по общей формуле
    def count_profile_qty(length, height):
        return roundup_excel(length) + roundup_excel(height) * 2

    rounded_qty = count_profile_qty(length, height)

    # Excel-подобные формулы из таблиц (F8–F12)
    f8 = (length + height * 2) / 2.5 - 1
    f9 = (length + height * 2) / 2.5
    f10 = (length + height * 2) / 2.5
    f11 = (length + height) / 2.5
    f12 = (length + height * 2) / 2.5

    rounded_f8  = roundup_excel(f8)
    rounded_f9  = roundup_excel(f9)
    rounded_f10 = roundup_excel(f10)
    rounded_f11 = roundup_excel(f11)
    rounded_f12 = roundup_excel(f12)


    # === РАЗВЕТВЛЕНИЕ ПО ТИПУ КОНСТРУКЦИИ ===
    # === РАСЧЁТ "П-ОБРАЗНАЯ" ===
    if shower_type == "П-образная":
        sku_map = {
            "A8": f"P10088{suffix}",
            "A9": f"Q10078{suffix}",
            "A10": f"HS-6463{suffix}" if mount_type == "На П-профиле" else "-",
            "A11": (
                f"Q10068{suffix}" if connector_type == "Коннектор Г-образный" and mount_type == "На коннекторах" else
                f"Q10066{suffix}" if mount_type == "На коннекторах" else
                "-"
            ),
            "A12": f"L10073{suffix}" if frame_type == "Круглая труба" else f"L10084{suffix}",
            "A13": f"L10072{suffix}" if frame_type == "Круглая труба" else f"L10086{suffix}",
            "A14": f"L10074{suffix}" if frame_type == "Круглая труба" else f"L10081{suffix}",
            "A15": f"U10072{suffix}",
            "A16": f"U10025{suffix}",
            "A17": (
                f"J10255-19{suffix}" if handle_type == "Ручка полотенцесушитель" and frame_type == "Круглая труба" else
                f"J10265{suffix}" if handle_type == "Ручка полотенцесушитель" else
                f"J10275{suffix}" if handle_type == "Скоба" and frame_type == "Круглая труба" else
                f"J10270{suffix}" if handle_type == "Скоба" else
                f"J10333{suffix}" if frame_type == "Круглая труба" else
                f"J10347{suffix}"
            ),
            "A18": (
                f"HSK-1{suffix}" if bottom_element == "Порожек" else
                f"Покуп{('-' + suffix) if suffix else ''}" if bottom_element == "Крышка на П-профиль" else
                "-"
            )
        }
        debug(f"[Проверка A14] door_position: {door_position!r}")
        sku_qty = {
            "A8": 2,
            "A9": 2 if door_position == "С боку" else 4,
            "A10": (
                rounded_f12
                if mount_type == "На П-профиле" else 0
            ),
            "A11": (
                10 if mount_type == "На коннекторах" and door_position == "С боку" else
                12 if mount_type == "На коннекторах" and door_position == "По середине" else
                0
            ),
            "A12": (
                3 if door_position == "С боку" else
                4 if door_position == "По середине" else
                0
            ),
            "A13": 2,
            "A14": 2,
            "A15": 2 if mount_type == "На П-профиле" else 6,
            "A16": 1,
            "A17": 1,
            "A18": 1 if sku_map.get("A18", "-") != "-" else 0
        }

    elif shower_type == "Угловая распашная":
        # === ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ОКРУГЛЕНИЯ КАК В EXCEL ===

        hinge_base_code = "P10090" if door_count == "Одна от стекла 90" else "P10088"
        rounded_qty = roundup_excel((length + height * 2) / 2.5)

        sku_map = {
            "AA9": f"{hinge_base_code}{suffix}",
            "AA10": f"HS-6463{suffix}" if mount_type == "На П-профиле" else "-",
            "AA11": (
                f"Q10068{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор Г-образный"
                else f"Q10066{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор П-образный"
                else "-"
            ),
            "AA12": (
                f"L10073{suffix}" if frame_type == "Круглая труба" and binding_type == "По периметру"
                else f"L10084{suffix}" if frame_type == "Квадратная труба" and binding_type == "По периметру"
                else f"L10075{suffix}" if frame_type == "Круглая труба"
                else f"L10083{suffix}"
            ),
            "AA13": f"L10072{suffix}" if frame_type == "Круглая труба" else f"L10086{suffix}",
            "AA14": (
                f"L10074{suffix}" if frame_type == "Круглая труба" and binding_type == "По периметру"
                else f"L10081{suffix}" if frame_type == "Квадратная труба" and binding_type == "По периметру"
                else f"L10058{suffix}" if frame_type == "Круглая труба"
                else f"L10079{suffix}"
            ),
            "AA15": f"U10072{suffix}",
            "AA16": f"U10025{suffix}",
            "AA17": (
                f"J10255-19{suffix}" if handle_type == "Ручка полотенцесушитель" and frame_type == "Круглая труба"
                else f"J10265{suffix}" if handle_type == "Ручка полотенцесушитель" and frame_type == "Квадратная труба"
                else f"J10275{suffix}" if handle_type == "Скоба" and frame_type == "Круглая труба"
                else f"J10270{suffix}" if handle_type == "Скоба" and frame_type == "Квадратная труба"
                else f"J10333{suffix}" if frame_type == "Круглая труба"
                else f"J10347{suffix}"
            ),
            "AA18": (
                f"HSK-1{suffix}" if bottom_element == "Порожек"
                else f"Покуп{('-' + suffix) if suffix else ''}" if bottom_element == "Крышка на П-профиль"
                else "-"
            )
        }

        sku_qty = {
            "AA9" : (
                4 if door_count == "Две" and binding_type == "По периметру" else
                0 if door_count == "Две" and binding_type == "С одной стороны" else
                2
            ),
            "AA10": rounded_f10 if mount_type == "На П-профиле" else 0,
            "AA11": (
                6 if mount_type == "На коннекторах" and door_count == "Одна от стены" else
                0 if mount_type == "На П-профиле" else
                8
            ),
            "AA12": 2 if binding_type == "По периметру" else 1,
            "AA13": 2 if binding_type == "По периметру" else 1,
            "AA14": 1,
            "AA15": (
                5 if door_count == "Две" and binding_type == "По периметру" and mount_type == "На коннекторах" else
                3 if door_count == "Две" and binding_type == "По периметру" and mount_type == "На П-профиле" else
                2 if door_count in ["Одна от стекла 180", "Одна от стекла 90"] and mount_type == "На П-профиле" else
                4 if door_count in ["Одна от стекла 180", "Одна от стекла 90"] and mount_type == "На коннекторах" else
                3 if door_count == "Одна от стены" and mount_type == "На коннекторах" else
                2 if door_count == "Одна от стены" and mount_type == "На П-профиле" else
                0
            ),
            "AA16": 1,
            "AA17": 1 if door_count in ["Одна от стены", "Одна от стекла 180", "Одна от стекла 90"] else 2,
            "AA18": 1 if sku_map["AA18"] != "-" else 0
        }

    elif shower_type == "Угловая раздвижная":
        is_g_profile = frame_type == "G-профиль"
        is_square = frame_type == "Квадратная труба"
        has_magnet_seal = magnet_seal_type == "С магнитным уплотнителем"

        # Округление количества П-профиля (AAA10) по Excel
        f11 = (length + height * 2) / 2.5
        rounded_qty = roundup_excel(f11)

        sku_AAA14 = f"U10025{suffix}" if (is_g_profile or (is_square and has_magnet_seal)) else "-"

        sku_map = {
            "AAA9": f"HF-1{suffix}" if is_g_profile else f"WXD-101{suffix}" if is_square else "-",
            "AAA10": f"HS-6463{suffix}" if mount_type == "На П-профиле" else "-",
            "AAA11": (
                f"Q10068{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор Г-образный" else
                f"Q10066{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор П-образный" else "-"
            ),
            "AAA12": f"U10072{suffix}" if frame_type in ["G-профиль", "Квадратная труба"] else "-",
            "AAA13": f"U10075{suffix}" if frame_type in ["G-профиль", "Квадратная труба"] else "-",
            "AAA14": sku_AAA14,
            "AAA15": f"L10081{suffix}" if is_square else "-",
            "AAA16": (
                f"HSK-1{suffix}" if bottom_element == "Порожек" else
                f"Покуп{('-' + suffix) if suffix else ''}" if bottom_element == "Крышка на П-профиль" else "-"
            ),
            "AAA17": (
                f"J10255-19{suffix}" if handle_type == "Ручка полотенцесушитель" and is_g_profile else
                f"J10275{suffix}" if handle_type == "Скоба" and is_g_profile else
                f"J10333{suffix}" if handle_type == "Кноб" and is_g_profile else "-"
            ),
            "AAA18": f"HF-2{suffix}" if is_g_profile else "-",
            "AAA19": f"HF-3{suffix}" if is_g_profile else "-"
        }

        sku_qty = {
            "AAA9" : 2 if door_count == "Две" and frame_type == "Квадратная труба" else 1,
            "AAA10": rounded_f11 if mount_type == "На П-профиле" else 0,
            "AAA11": 8 if mount_type == "На коннекторах" else 0,
            "AAA12": 1 if door_count in ["Одна", "Две"] and mount_type == "На П-профиле" else 4,
            "AAA13": 2 if door_count == "Одна" else 4,
            "AAA14": 1 if sku_map["AAA14"] != "-" else 0,
            "AAA15": 1 if frame_type == "Квадратная труба" and magnet_seal_type == "С магнитным уплотнителем" else 0,
            "AAA16": 1,
            "AAA17": (
                1 if door_count == "Одна" and frame_type == "G-профиль" else
                2 if door_count == "Две" and frame_type == "G-профиль" else 0
            ),
            "AAA18": (
                2 if door_count == "Две" and frame_type == "G-профиль" else
                1 if door_count == "Одна" and frame_type == "G-профиль" else 0
            ),
            "AAA19": 1 if frame_type == "G-профиль" else 0
        }
        
    elif shower_type == "Прямая распашная":
        # === ДОП. ПОДСЧЁТ ===
        f10 = (length + height * 2) / 2.5

        # === Excel-совместимое округление количества для HS-6463 ===
        if mount_type == "На П-профиле" and door_position == "От стекла к стеклу":
            qty_hs6463 = roundup_excel(f10)
        else:
            qty_hs6463 = roundup_excel(f10 - 1)

        # === ОСНОВНЫЕ УСЛОВИЯ ===
        hinge_code = "P10086" if door_position == "От стены" else "P10088"
        b10_value = "П-образный профиль" if mount_type == "На П-профиле" else "-"
        b16_value = (
            "Уплотнитель магнитный 90/180"
            if not (door_position == "От стекла к стене" and seal_type == "Полусфера")
            else "-"
        )

        sku_map = {
            "AAAA9": f"{hinge_code}{suffix}",
            "AAAA10": f"HS-6463{suffix}" if mount_type == "На П-профиле" else "-",
            "AAAA11": (
                f"Q10068{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор Г-образный" else
                f"Q10066{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор П-образный" else "-"
            ),
            "AAAA12": (
                f"L10073{suffix}" if frame_type == "Круглая труба" and binding_position == "Обвязка над стеклом" else
                f"L10084{suffix}" if frame_type == "Квадратная труба" and binding_position == "Обвязка над стеклом" else
                f"L10075{suffix}" if frame_type == "Круглая труба" else
                f"L10083{suffix}"
            ),
            "AAAA13": f"L10072{suffix}" if frame_type == "Круглая труба" else f"L10086{suffix}",
            "AAAA14": (
                f"U10084{suffix}" if door_position == "От стекла к стене" and seal_type == "Полусфера" else
                f"HSK-2{suffix}" if door_position == "От стекла к стене" and seal_type == "Притворная планка" and hardware_color != "Бронза" else "-"
            ),
            "AAAA15": f"U10072{suffix}",
            "AAAA16": f"U10025{suffix}" if b16_value == "Уплотнитель магнитный 90/180" else "-",
            "AAAA17": (
                f"J10255-19{suffix}" if handle_type == "Ручка полотенцесушитель" and frame_type == "Круглая труба" else
                f"J10265{suffix}" if handle_type == "Ручка полотенцесушитель" and frame_type == "Квадратная труба" else
                f"J10275{suffix}" if handle_type == "Скоба" and frame_type == "Круглая труба" else
                f"J10270{suffix}" if handle_type == "Скоба" and frame_type == "Квадратная труба" else
                f"J10333{suffix}" if frame_type == "Круглая труба" else
                f"J10347{suffix}"
            ),
            "AAAA18": (
                f"HSK-1{suffix}" if bottom_element == "Порожек" else
                f"Покуп{('-' + suffix) if suffix else ''}" if bottom_element == "Крышка на П-профиль" else "-"
            )
        }

        sku_qty = {
            "AAAA9" : 2,
            "AAAA10": (
                rounded_f10 if mount_type == "На П-профиле" and door_position == "От стекла к стеклу" else
                max(rounded_f10 - 1, 0) if mount_type == "На П-профиле" else 0
            ),
            "AAAA11": 4 if mount_type == "На коннекторах" else 0,
            "AAAA12": 2 if door_position == "От стекла к стеклу" else 1,
            "AAAA13": 2,
            "AAAA14": 1 if sku_map["AAAA14"] != "-" else 0,
            "AAAA15": (
                3 if door_position == "От стены" and mount_type == "На коннекторах" else
                2 if mount_type == "На П-профиле" else
                4 if door_position == "От стекла к стеклу" and mount_type == "На коннекторах" else 0
            ),
            "AAAA16": 1 if b16_value == "Уплотнитель магнитный 90/180" else 0,
            "AAAA17": 1,
            "AAAA18": 1,
            "CCCC20": 1 if length > 1.7 else 0
        }

    elif shower_type == "Прямая раздвижная":
        f10 = length / 3
        f11 = (length + height * 2) / 2.5

        is_g_profile = frame_type == "G-профиль"
        is_square = frame_type == "Квадратная труба"
        is_double = door_count == "Две"
        is_single = door_count == "Одна"
        is_from_wall = door_position == "От стены"
        is_center = door_position == "По середине"

        b16_value = (
            "-" if is_from_wall and seal_type == "Полусфера" else
            "-" if is_center and is_single else
            "Уплотнитель магнитный 90/180"
        )

        sku_map = {
            "AAAAA10": f"HF-1{suffix}" if is_g_profile else f"WXD-101{suffix}" if is_square else "-",
            "AAAAA11": f"HS-6463{suffix}" if mount_type == "На П-профиле" else "-",
            "AAAAA12": (
                f"Q10068{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор Г-образный" else
                f"Q10066{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор П-образный" else "-"
            ),
            "AAAAA13": f"U10072{suffix}",
            "AAAAA14": f"U10075{suffix}",
            "AAAAA15": (
                "U10084" if is_from_wall and seal_type == "Полусфера" else
                f"HSK-2{suffix}" if is_from_wall and seal_type == "Притворная планка" and hardware_color != "Бронза" else "-"
            ),
            "AAAAA16": f"U10028{suffix}" if b16_value == "Уплотнитель магнитный 90/180" else "-",
            "AAAAA17": (
                f"J10255-19{suffix}" if handle_type == "Ручка полотенцесушитель" and is_g_profile else
                f"J10275{suffix}" if handle_type == "Скоба" and is_g_profile else
                f"J10333{suffix}" if handle_type == "Кноб" and is_g_profile else "-"
            ),
            "AAAAA18": (
                f"HSK-1{suffix}" if bottom_element == "Порожек" else
                f"Покуп{('-' + suffix) if suffix else ''}" if bottom_element == "Крышка на П-профиль" else "-"
            ),
            "AAAAA19": f"HF-2{suffix}" if is_g_profile else "-"
        }

        sku_qty = {
            "AAAAA10": (
                roundup_excel(length / 3) if frame_type == "G-профиль" else
                2 if frame_type == "Квадратная труба" and door_count == "Две" else
                1 if frame_type == "Квадратная труба" and door_count == "Одна" else 0
            ),
            "AAAAA11": (
                roundup_excel(f11)                 if mount_type == "На П-профиле" and door_position == "По середине" and door_count == "Две" else
                max(roundup_excel(f11 - 1), 0)     if mount_type == "На П-профиле" and door_position == "От стены"     and door_count == "Одна" else
                "Ошибка"                           if mount_type == "На П-профиле" and door_position == "От стены"     and door_count == "Две" else
                roundup_excel(f11)                 if mount_type == "На П-профиле" and door_position == "По середине" and door_count == "Одна" else
                0
            ),
            "AAAAA12": (
                8 if mount_type == "На коннекторах" and door_position == "По середине" and door_count == "Две" else
                4 if mount_type == "На коннекторах" and door_position == "От стены" and door_count == "Одна" else
                8 if mount_type == "На коннекторах" and door_position == "По середине" and door_count == "Одна" else 0
            ),
            "AAAAA13": (
                3 if mount_type == "На коннекторах" and door_position == "По середине" and door_count == "Две" else
                2 if mount_type == "На коннекторах" and door_position == "От стены" and door_count == "Одна" else
                3 if mount_type == "На коннекторах" and door_position == "По середине" and door_count == "Одна" else
                1 if mount_type == "На П-профиле" and door_position == "По середине" and door_count == "Две" else
                1 if mount_type == "На П-профиле" and door_position == "От стены" and door_count == "Одна" else
                1 if mount_type == "На П-профиле" and door_position == "По середине" and door_count == "Одна" else 0
            ),
            "AAAAA14": (
                4 if door_position == "По середине" and door_count == "Две" else
                2 if door_position == "От стены" and door_count == "Одна" else 4
            ),
            "AAAAA15": 1 if sku_map["AAAAA15"] != "-" else 0,
            "AAAAA16": 1 if sku_map["AAAAA16"] != "-" else 0,
            "AAAAA17": (
                1 if door_count == "Одна" and frame_type == "G-профиль" else
                2 if door_count == "Две" and frame_type == "G-профиль" else 0
            ),
            "AAAAA18": 1,
            "AAAAA19": (
                2 if door_count == "Две" and frame_type == "G-профиль" else
                1 if door_count == "Одна" and frame_type == "G-профиль" else 0
            ),
            "CCCCC21": 1 if frame_type == "Квадратная труба" and length > 1.7 else 0
        }

    elif shower_type == "Трапециевидная":
        # === ОСНОВНЫЕ УСЛОВИЯ ===
        b9_value  = "П-образный профиль хром" if mount_type == "На П-профиле" else "-"
        b18_value = "Коннектор стекло-стекло 135º" if door_position == "С боку" else "-"
        b19_value = "Коннектор П-образный" if door_position == "С боку" else "-"

        # === КАРТА АРТИКУЛОВ ===
        sku_map = {
            "AAAAAA8" : f"P10089{suffix}" if door_position == "По середине" else f"P10086{suffix}",
            "AAAAAA9" : f"HS-6463{suffix}" if mount_type == "На П-профиле" else "-",
            "AAAAAA10": (
                f"Q10068{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор Г-образный" else
                f"Q10066{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор П-образный" else "-"
            ),
            "AAAAAA11": f"L10073{suffix}" if frame_type == "Круглая труба" else f"L10084{suffix}",
            "AAAAAA12": f"L10072{suffix}" if frame_type == "Круглая труба" else f"L10086{suffix}",
            "AAAAAA13": f"L10074{suffix}" if frame_type == "Круглая труба" else f"L10091{suffix}",
            "AAAAAA14": f"U10072{suffix}",
            "AAAAAA15": f"U10032{suffix}",
            "AAAAAA16": (
                f"J10255-19{suffix}" if handle_type == "Ручка полотенцесушитель" and frame_type == "Круглая труба" else
                f"J10265{suffix}"     if handle_type == "Ручка полотенцесушитель" and frame_type == "Квадратная труба" else
                f"J10275{suffix}"     if handle_type == "Скоба" and frame_type == "Круглая труба" else
                f"J10270{suffix}"     if handle_type == "Скоба" and frame_type == "Квадратная труба" else
                f"J10333{suffix}"     if frame_type == "Круглая труба" else
                f"J10347{suffix}"
            ),
            "AAAAAA17": (
                f"HSK-1{suffix}" if bottom_element == "Порожек" else
                f"Покуп{('-' + suffix) if suffix else ''}" if bottom_element == "Крышка на П-профиль" else "-"
            ),
            "AAAAAA18": f"Q10070{suffix}" if door_position == "С боку" else "-",
            "AAAAAA19": f"Q10066{suffix}" if door_position == "С боку" else "-"
        }

        # === КОЛИЧЕСТВА ===
        sku_qty = {
            "AAAAAA8" : 2,
            "AAAAAA9" : (
                rounded_f9 if door_position == "По середине" and mount_type == "На П-профиле" else
                rounded_f8 if door_position == "С боку" and mount_type == "На П-профиле" else 0
            ),
            "AAAAAA10": (
                8 if door_position == "По середине" and mount_type == "На коннекторах" else
                6 if door_position == "С боку" and mount_type == "На коннекторах" else 0
            ),
            "AAAAAA11": 2,
            "AAAAAA12": 2,
            "AAAAAA13": 2,
            "AAAAAA14": (
                4 if door_position == "По середине" and mount_type == "На коннекторах" else
                3 if door_position == "С боку" and mount_type == "На коннекторах" else 2
            ),
            "AAAAAA15": 1,
            "AAAAAA16": 1,
            "AAAAAA17": 1,
            "AAAAAA18": 2 if sku_map["AAAAAA18"].startswith("Q10070") else 0,
            "AAAAAA19": 2 if sku_map["AAAAAA19"].startswith("Q10066") else 0
        }

    elif shower_type == "Стационар":
        sku_map = {
            "AAAAAAA8" : f"HS-6463{suffix}" if mount_type == "На П-профиле" else "-",
            "AAAAAAA9" : (
                f"Q10068{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор Г-образный" else
                f"Q10066{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор П-образный" else "-"
            ),
            "AAAAAAA10": (
                f"L10073{suffix}" if frame_type == "Круглая труба" and binding_position == "Обвязка над стеклом" else
                f"L10084{suffix}" if frame_type == "Квадратная труба" and binding_position == "Обвязка над стеклом" else
                f"L10075{suffix}" if frame_type == "Круглая труба" else
                f"L10083{suffix}"
            ),
            "AAAAAAA11": f"L10072{suffix}" if frame_type == "Круглая труба" else f"L10086{suffix}",
            "AAAAAAA12": f"U10072{suffix}"
        }

        sku_qty = {
            "AAAAAAA8" : rounded_f12 if mount_type == "На П-профиле" else 0,
            "AAAAAAA9" : 4 if mount_type == "На коннекторах" else 0,
            "AAAAAAA10": 1,
            "AAAAAAA11": 2,
            "AAAAAAA12": 2
        }

    elif shower_type == "Шторка":
        sku_map = {
            "AAAAAAAA9" : (
                f"P10088{suffix}" if curtain_type == "Распашное" else
                f"P10049{suffix}" if curtain_type == "Гормошка" else "-"
            ),
            "AAAAAAAA10": f"P10050{suffix}" if curtain_type == "Гормошка" else "-",
            "AAAAAAAA11": f"HS-6463{suffix}" if mount_type == "На П-профиле" else "-",
            "AAAAAAAA12": (
                f"Q10068{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор Г-образный" else "-"
            ),
            "AAAAAAAA13": (
                f"Q10066{suffix}" if mount_type == "На коннекторах" and connector_type == "Коннектор П-образный" else "-"
            ),
            "AAAAAAAA14": f"U10072{suffix}",
            "AAAAAAAA15": (
                f"J10255-19{suffix}" if handle_type == "Ручка полотенцесушитель" and frame_type == "Круглая труба" else
                f"J10265{suffix}"     if handle_type == "Ручка полотенцесушитель" and frame_type == "Квадратная труба" else
                f"J10275{suffix}"     if handle_type == "Скоба" and frame_type == "Круглая труба" else
                f"J10270{suffix}"     if handle_type == "Скоба" and frame_type == "Квадратная труба" else
                f"J10333{suffix}"     if handle_type == "Кноб" and frame_type == "Круглая труба" else
                f"J10347{suffix}"     if handle_type == "Кноб" and frame_type == "Квадратная труба" else "-"
            ),
            "AAAAAAAA16": (
                f"002{suffix}"     if rigid_element_type == "Труба круглая" else
                f"S10001{suffix}"  if rigid_element_type == "Штанга круглая" else
                f"S10012{suffix}"  if rigid_element_type == "Штанга квадратная" else "-"
            ),
            "AAAAAAAA17": f"L10058{suffix}" if rigid_element_type == "Труба круглая" else "-",
            "AAAAAAAA18": f"L10078{suffix}" if rigid_element_type == "Труба круглая" else "-"
        }

        # === УЛУЧШЕННЫЕ КОЛИЧЕСТВА С ПРАВИЛЬНОЙ ЛОГИКОЙ ШТАНГА ===
        
        # Вспомогательные расчеты для штанги
        def calculate_shtanga_qty(element_type, length):
            """Рассчитывает количество штанги в зависимости от типа и длины"""
            if element_type == "Штанга квадратная":
                # Квадратная штанга: 1 шт при длине > 0.9м, иначе 0
                return 1 if length > 0.9 else 0
            elif element_type == "Штанга круглая":
                # Круглая штанга: 1 шт при длине > 0.6м, иначе 0
                return 1 if length > 0.6 else 0
            elif element_type == "Труба круглая":
                # Круглая труба: всегда 1 шт
                return 1
            else:
                return 0

        shtanga_qty = calculate_shtanga_qty(rigid_element_type, length)
        
        # Дополнительная логика: если штанга нужна, то возможно нужны дополнительные крепления
        additional_fittings_needed = shtanga_qty > 0 and length > 1.5
        
        sku_qty = {
            "AAAAAAAA9" : 2,
            "AAAAAAAA10": 2 if curtain_type == "Гормошка" else 0,
            "AAAAAAAA11": rounded_f11 if mount_type == "На П-профиле" else 0,
            "AAAAAAAA12": 2 if sku_map["AAAAAAAA12"] != "-" else 0,
            "AAAAAAAA13": 2 if sku_map["AAAAAAAA13"] != "-" else 0,
            "AAAAAAAA14": 2,
            "AAAAAAAA15": 1 if sku_map["AAAAAAAA15"] != "-" else 0,
            "AAAAAAAA16": shtanga_qty,  # Используем улучшенный расчет
            "AAAAAAAA17": 1 if sku_map["AAAAAAAA17"] != "-" else 0,
            "AAAAAAAA18": 1 if sku_map["AAAAAAAA18"] != "-" else 0,
            # Дополнительные позиции для штанги (если нужны)
            "AAAAAAAA19": (
                2 if rigid_element_type in ["Штанга круглая", "Штанга квадратная"] and additional_fittings_needed else 0
            )
        }
        
        # === ДОПОЛНИТЕЛЬНЫЕ АРТИКУЛЫ ДЛЯ ШТАНГИ (если требуются) ===
        if shtanga_qty > 0:
            # Добавляем артикулы креплений для штанги
            additional_sku_map = {
                "AAAAAAAA19": (
                    f"L10060{suffix}" if rigid_element_type == "Штанга круглая" and additional_fittings_needed else
                    f"L10061{suffix}" if rigid_element_type == "Штанга квадратная" and additional_fittings_needed else "-"
                )
            }
            sku_map.update(additional_sku_map)
        
        # === DEBUG: вывод расчетов штанги ===
        if shtanga_qty > 0:
            debug(f"[ШТАНГА] Тип: {rigid_element_type}")
            debug(f"[ШТАНГА] Длина: {length}")
            debug(f"[ШТАНГА] Количество штанги: {shtanga_qty}")
            debug(f"[ШТАНГА] Доп. крепления нужны: {additional_fittings_needed}")
            debug(f"[ШТАНГА] Артикул штанги: {sku_map.get('AAAAAAAA16', '-')}")
            if additional_fittings_needed:
                debug(f"[ШТАНГА] Артикул доп. креплений: {sku_map.get('AAAAAAAA19', '-')}")

    elif shower_type == "Дверь":
        seal_type_effective = (
            "Уплотнитель магнитный 90/180"
            if seal_type != "Полусфера"
            else seal_type
        )

        sku_map = {
            "AAAAAAAAA5": (
                f"P10086{suffix}"
                if hardware_color in ["Хром", "Черная", "Бронза", "Золото"]
                else "-"
            ),
            "AAAAAAAAA6": (
                f"U10084{suffix}"   if seal_type == "Полусфера" and hardware_color == "Хром" else
                f"U10084b{suffix}"  if seal_type == "Полусфера" and hardware_color == "Черная" else
                f"U10084br{suffix}" if seal_type == "Полусфера" and hardware_color == "Бронза" else
                f"U10084g{suffix}"  if seal_type == "Полусфера" and hardware_color == "Золото" else
                f"HSK-2{suffix}"    if seal_type == "Притворная планка" and hardware_color == "Хром" else
                f"HSK-2b{suffix}"   if seal_type == "Притворная планка" and hardware_color == "Черная" else
                f"HSK-2g{suffix}"   if seal_type == "Притворная планка" and hardware_color == "Золото" else "-"
            ),
            "AAAAAAAAA7": (
                f"U10072{suffix}"   if hardware_color == "Хром" else
                f"U10072b{suffix}"  if hardware_color == "Черная" else
                f"U10072br{suffix}" if hardware_color == "Бронза" else
                f"U10072g{suffix}"  if hardware_color == "Золото" else "-"
            ),
            "AAAAAAAAA8": (
                f"U10025{suffix}"   if seal_type_effective == "Уплотнитель магнитный 90/180" and hardware_color == "Хром" else
                f"U10025b{suffix}"  if seal_type_effective == "Уплотнитель магнитный 90/180" and hardware_color == "Черная" else
                f"U10025br{suffix}" if seal_type_effective == "Уплотнитель магнитный 90/180" and hardware_color == "Бронза" else
                f"U10025g{suffix}"  if seal_type_effective == "Уплотнитель магнитный 90/180" and hardware_color == "Золото" else "-"
            ),
            "AAAAAAAAA9": (
                f"J10255-19{suffix}"  if handle_type == "Ручка полотенцесушитель" and hardware_color == "Хром" else
                f"J10255-19b{suffix}" if handle_type == "Ручка полотенцесушитель" and hardware_color == "Черная" else
                f"J10255-19br{suffix}"if handle_type == "Ручка полотенцесушитель" and hardware_color == "Бронза" else
                f"J10255-19g{suffix}" if handle_type == "Ручка полотенцесушитель" and hardware_color == "Золото" else
                f"J10275{suffix}"     if handle_type == "Скоба" and hardware_color == "Хром" else
                f"J10275b{suffix}"    if handle_type == "Скоба" and hardware_color == "Черная" else
                f"J10275br{suffix}"   if handle_type == "Скоба" and hardware_color == "Бронза" else
                f"J10275g{suffix}"    if handle_type == "Скоба" and hardware_color == "Золото" else
                f"J10333{suffix}"     if handle_type == "Кноб" and hardware_color == "Хром" else
                f"J10333b{suffix}"    if handle_type == "Кноб" and hardware_color == "Черная" else
                f"J10333br{suffix}"   if handle_type == "Кноб" and hardware_color == "Бронза" else
                f"J10333g{suffix}"    if handle_type == "Кноб" and hardware_color == "Золото" else
                f"J10265{suffix}"     if handle_type == "Ручка полотенцесушитель" and hardware_color == "Хром" else
                f"J10265b{suffix}"    if handle_type == "Ручка полотенцесушитель" and hardware_color == "Черная" else
                f"J10265br{suffix}"   if handle_type == "Ручка полотенцесушитель" and hardware_color == "Бронза" else
                f"J10265g{suffix}"    if handle_type == "Ручка полотенцесушитель" and hardware_color == "Золото" else
                f"J10270{suffix}"     if handle_type == "Скоба" and hardware_color == "Хром" else
                f"J10270b{suffix}"    if handle_type == "Скоба" and hardware_color == "Черная" else
                f"J10270br{suffix}"   if handle_type == "Скоба" and hardware_color == "Бронза" else
                f"J10270g{suffix}"    if handle_type == "Скоба" and hardware_color == "Золото" else
                f"J10347{suffix}"     if handle_type == "Кноб" and hardware_color == "Хром" else
                f"J10347b{suffix}"    if handle_type == "Кноб" and hardware_color == "Черная" else
                f"J10347br{suffix}"   if handle_type == "Кноб" and hardware_color == "Бронза" else
                f"J10347g{suffix}"    if handle_type == "Кноб" and hardware_color == "Золото" else "-"
            ),
            "AAAAAAAAA10": (
                f"HSK-1{suffix}"     if bottom_element == "Порожек" and hardware_color == "Хром" else
                f"HSK-1b{suffix}"    if bottom_element == "Порожек" and hardware_color == "Черная" else
                f"HSK-1br{suffix}"   if bottom_element == "Порожек" and hardware_color == "Бронза" else
                f"HSK-1g{suffix}"    if bottom_element == "Порожек" and hardware_color == "Золото" else
                f"Покуп{suffix}"     if bottom_element == "Крышка на П-профиль" and hardware_color == "Хром" else
                f"Покуп-b{suffix}"   if bottom_element == "Крышка на П-профиль" and hardware_color == "Черная" else
                f"Покуп-br{suffix}"  if bottom_element == "Крышка на П-профиль" and hardware_color == "Бронза" else
                f"Покуп-g{suffix}"   if bottom_element == "Крышка на П-профиль" and hardware_color == "Золото" else "-"
            ),
        }

        sku_qty = {
            "AAAAAAAAA5": 2,
            "AAAAAAAAA6": 1,
            "AAAAAAAAA7": 2,
            "AAAAAAAAA8": 1 if seal_type_effective == "Уплотнитель магнитный 90/180" else 0,
            "AAAAAAAAA9": 1,
            "AAAAAAAAA10": 1,
        }

    # === РАСЧЁТ ФУРНИТУРЫ ===
    furniture_total = 0
    furniture_items = []

    for key in sku_map:
        sku = sku_map[key]
        qty = sku_qty.get(key, 0)
        if customer_type == "юрлицо":
            info = price_catalog_legal.get(sku, {"price": 0, "name": "Не найдено"})
        else:
            info = price_catalog_physical.get(sku, {"price": 0, "name": "Не найдено"})
        price = info["price"]
        name = info["name"]
        total = price * qty
        furniture_total += total
        furniture_items.append({
            "sku": sku,
            "name": name,
            "price": price,
            "qty": qty,
            "total": total
        })

    # === РАСЧЁТ ОБВЯЗКИ ===
    binding_prices = {
        "Круглая труба": {
            "Хром": 2000,
            "Черная": 4000,
            "Бронза": 4500,
            "Золото": 4500
        },
        "Квадратная труба": {
            "Хром": 4500,
            "Черная": 5000,
            "Бронза": 5000,
            "Золото": 5000
        },
        "G-профиль": {
            "Хром": 0,
            "Черная": 0,
            "Бронза": 0,
            "Золото": 0
        }
    }

    # Цена за погонный метр
    binding_price_per_meter = binding_prices.get(frame_type, {}).get(hardware_color, 0)

    # Кол-во погонных метров с округлением вверх
    binding_meter_qty = int(length) + (1 if length % 1 > 0 else 0)

    # Итоговая стоимость
    binding_total = binding_meter_qty * binding_price_per_meter


    # === ДОСТАВКА ===
    area = length * height

    pickup_without_pack = glass_total + furniture_total + binding_total
    pickup_with_pack = pickup_without_pack + (area * 2000) # упаковка + сбор

    if city == "Алматы":
        delivery_city = pickup_with_pack
    elif city in ["Актау", "Актобе", "Астана", "Атырау", "Караганда", "Павлодар", "Семей", "Тараз", "Уральск"]:
        delivery_city = pickup_with_pack + (8000 if area < 2 else area * 3000)
    elif city == "Костанай":
        delivery_city = pickup_with_pack + (10000 if area < 2 else area * 4000)
    elif city == "Кызылорда":
        delivery_city = pickup_with_pack + (8000 if area < 2 else area * 2500)
    elif city == "Петропавловск":
        delivery_city = pickup_with_pack + (8000 if area < 2 else area * 2500)
    elif city == "Талдыкорган":
        delivery_city = pickup_with_pack + 15000
    elif city == "Усть-Каменогорск":
        delivery_city = pickup_with_pack + (10000 if area < 2 else area * 4000)
    else:
        delivery_city = pickup_with_pack
        

    # === ПАКЕТЫ С УЧЁТОМ СКИДКИ НА ОБЩУЮ СУММУ ===
    base_total = glass_total + furniture_total + binding_total
    delivery_cost = 8000  # фиксированная доставка


    # === ПАКЕТЫ ДЛЯ ОСНОВНЫХ ТИПОВ КОНСТРУКЦИЙ ===
    def calculate_packages_default(pickup_without_pack: int, tsvet: str = "Хром") -> dict:
        pickup_econom = pickup_without_pack - glass_total + glass_total_economy
        return {
            "Эконом": {
                "стоимость_пакета_без_скидки": pickup_econom + 70000,
                "итого_с_монтажом_и_скидкой": int((pickup_econom + 70000) * 0.85),
                "выгода_по_скидке": int((pickup_econom + 70000) * 0.15)
            },
            "Стандарт": {
                "стоимость_пакета_без_скидки": pickup_without_pack + 130000,
                "итого_со_скидкой": int((pickup_without_pack + 130000) * 0.75),
                "выгода_по_скидке": int((pickup_without_pack + 130000) * 0.25)
            },
            "Премиум": {
                "стоимость_пакета_без_скидки": pickup_without_pack + 200000,
                "итого_со_скидкой": int((pickup_without_pack + 200000) * 0.75),
                "выгода_по_скидке": int((pickup_without_pack + 200000) * 0.25)
            }
        }

    # === ПАКЕТЫ ДЛЯ СТАЦИОНАР / ШТОРКА / ПРЯМАЯ РАСПАШНАЯ ===
    def calculate_packages_v2(pickup_without_pack: int, tsvet: str, shower_type: str) -> dict:
        pickup_econom = pickup_without_pack - glass_total + glass_total_economy
        if shower_type in ["Стационар", "Шторка"]:
            return {
                "Эконом": {
                    "стоимость_пакета_без_скидки": pickup_econom + 60000,
                    "итого_с_монтажом_и_скидкой": int((pickup_econom + 60000) * 0.85),
                    "выгода_по_скидке": int((pickup_econom + 60000) * 0.15)
                },
                "Стандарт": {
                    "стоимость_пакета_без_скидки": pickup_without_pack + 110000,
                    "итого_со_скидкой": int((pickup_without_pack + 110000) * 0.75),
                    "выгода_по_скидке": int((pickup_without_pack + 110000) * 0.25)
                },
                "Премиум": {
                    "стоимость_пакета_без_скидки": pickup_without_pack + 160000,
                    "итого_со_скидкой": int((pickup_without_pack + 160000) * 0.75),
                    "выгода_по_скидке": int((pickup_without_pack + 160000) * 0.25)
                }
            }
        else:
            return calculate_packages_default(pickup_without_pack, tsvet)

    pickup_without_pack = glass_total + furniture_total + binding_total

    # пакеты со скидками
    packages = calculate_packages_v2(pickup_without_pack, hardware_color, shower_type)

    # === ПРОВЕРКА НА ОБЯЗАТЕЛЬНЫЕ ПАРАМЕТРЫ ===
    missing_inputs = []

    if not glass_total:
        missing_inputs.append("glass_total")
    if not furniture_total:
        missing_inputs.append("furniture_total")

    if missing_inputs:
        result = {
        "error": "Недостаточно данных для расчёта. Отсутствуют или равны нулю:",
        "missing": missing_inputs
    }
    else:
        result = {
            "glass_total":      glass_total,
            "furniture_total":  furniture_total,
            "sku_details": [
                {
                    "sku": item["sku"],
                    "name": item["name"],  # ← ДОБАВЛЕНО НАИМЕНОВАНИЕ
                    "qty": item["qty"],
                    "price_per_unit": item["price"],
                    "total_price": item["total"]
                }
                for item in furniture_items if item["sku"] != "-"
            ],
            "binding_total":    binding_total,
            "pickup_without_pack": pickup_without_pack,
            "delivery_city":      delivery_city,
        }

    if customer_type == "физлицо":
        result["packages"] = packages

    debug(f"Result сформирован: {result}")
    return result