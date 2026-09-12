import json
import time
import urllib.parse
import urllib.request
import urllib.error
import socket
import os
import sys

# ==================================================
# АВТОКИЛЛ СТАРЫХ ПРОЦЕССОВ
# ==================================================

def kill_old_bots():
    current_pid = os.getpid()
    killed = []
    print("🔍 Поиск старых экземпляров бота...")
    try:
        import subprocess
        if sys.platform == "win32":
            try:
                result = subprocess.run(
                    ['wmic', 'process', 'where', "name='python.exe'", 'get', 'ProcessId,CommandLine'],
                    capture_output=True, text=True, timeout=10
                )
                output = result.stdout
                for line in output.split('\n'):
                    line_lower = line.lower()
                    if ('z9' in line_lower or 'bot' in line_lower or 'numbers' in line_lower):
                        parts = line.strip().split()
                        if parts:
                            try:
                                pid = int(parts[-1])
                                if pid != current_pid:
                                    try:
                                        subprocess.run(['taskkill', '/F', '/PID', str(pid)],
                                                       capture_output=True, timeout=5)
                                        killed.append(str(pid))
                                        print(f"   ✅ Убит процесс PID: {pid}")
                                    except:
                                        pass
                            except ValueError:
                                continue
            except FileNotFoundError:
                print("   ℹ️ wmic не найден — пропуск")
        else:
            result = subprocess.run(['ps', '-A'], capture_output=True, text=True, timeout=10)
            for line in result.stdout.split('\n'):
                if 'python' in line.lower() and ('звезды' in line or 'stars' in line or '8675442691' in line or 'z9' in line.lower()):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            pid = int(parts[0]) if parts[0].isdigit() else int(parts[1])
                            if pid != current_pid:
                                try:
                                    os.kill(pid, 9)
                                    killed.append(str(pid))
                                    print(f"   ✅ Убит процесс PID: {pid}")
                                except:
                                    pass
                        except:
                            pass
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")

    if killed:
        print(f"✅ Убито процессов: {len(killed)}")
        time.sleep(1)
    else:
        print("✅ Старых процессов не найдено")
    return killed


def remove_lock_files():
    lock_files = ["bot_numbers.lock", "bot.lock"]
    for lock_file in lock_files:
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
                print(f"   🗑️ Удалён файл блокировки: {lock_file}")
        except:
            pass


print("\n" + "=" * 50)
print("     NUMBERS.EXE — PYDROID / WINDOWS")
print("=" * 50 + "\n")

kill_old_bots()
remove_lock_files()

# ==================================================
# КОНФИГУРАЦИЯ
# ==================================================

TOKEN = "8675442691:AAE7X7uOQMkpkH5fgOwleUlYHLAQhtaQfyY"

BANK_NAME = "OZON Банк"
CARD_NUMBER = "2204321255191702"
RECIPIENT = "Кирилл Ш."
ADMIN_ID = 8864430187

ADMIN_LINK = "https://t.me/Exec_me_shop"
ADMIN_USERNAME_TARGET = "exec_me_shop"

POLL_TIMEOUT = 60
REQUEST_TIMEOUT = 15
RECONNECT_DELAY = 1
MAX_RETRIES = 2

# ==================================================
# ПАПКА ДАННЫХ
# ==================================================

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()

if not SCRIPT_DIR:
    SCRIPT_DIR = os.getcwd()

DATA_DIR = os.path.join(SCRIPT_DIR, "data")

try:
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"📁 Папка данных: {DATA_DIR}")
except Exception as e:
    print(f"⚠️ Не удалось создать {DATA_DIR}: {e}")
    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.txt")
STOCK_FILE = os.path.join(DATA_DIR, "stock.txt")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.txt")
BANNED_FILE = os.path.join(DATA_DIR, "banned.txt")
ADMIN_FILE = os.path.join(DATA_DIR, "admin.txt")
SOLD_FILE = os.path.join(DATA_DIR, "sold.txt")

try:
    lock_path = os.path.join(SCRIPT_DIR, "bot_numbers.lock")
    lock_file = open(lock_path, "w")
    lock_file.write(str(os.getpid()))
    lock_file.flush()
    print("✅ Блокировка создана")
except Exception as e:
    print(f"⚠️ Не удалось создать блокировку: {e}")

print("🚀 Бот запускается...\n")

# ==================================================
# АДМИНЫ
# ==================================================

ADMIN_IDS = {ADMIN_ID}

# ==================================================
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ==================================================

user_phones = {}
user_verified = {}
user_first_names = {}
user_usernames = {}
banned_users = {}
orders = {}
pending_orders = {}
temp_data = {}
order_counter = 0

chat_mode = {}

SPAM_WINDOW = 10
SPAM_LIMIT = 5
user_msg_times = {}
user_last_msg = {}
user_warned_spam = {}
user_warned_bad = {}

BAD_WORDS = [
    "хуй", "хуя", "хую", "хуе", "хуё", "хуи", "хуйн",
    "пизд", "пизж",
    "ебал", "ебан", "ебат", "ебуч", "ебло", "ёб",
    "бляд", "блят", "блядь",
    "сука", "суки", "сучк",
    "мраз", "мразь",
    "гандон", "гондон",
    "долбоеб", "долбоёб", "долбаеб",
    "пидор", "пидар", "пидр",
    "шлюх", "шлюш",
    "ублюд",
    "дебил", "дебилы",
    "идиот", "идиоты",
    "кретин",
    "лох", "лохи",
    "тварь",
    "нахуй", "нахуя",
    "похуй", "похуи",
    "залуп",
    "мудак", "мудил",
    "хер", "херня",
    "срак", "срать", "сру",
    "жоп", "жопу",
    "говн", "говно",
    "мразот",
    "уёб", "уеб",
    "ахуе", "ахуй",
    "охуе", "охуй",
    "придур",
    "тупоу",
    "козел", "козёл",
    "баран",
    "свинья",
    "скотин",
    "шалав",
    "мандав",
    "педик",
]

# ==================================================
# АККАУНТЫ — ЦЕНЫ В ₽ И ⭐ (округление до 50)
# ==================================================

ACCOUNTS_BASE_STOCK = {
    "acc_mm": 231, "acc_co": 184, "acc_bd": 171, "acc_in": 166,
    "acc_us": 121, "acc_uz": 108, "acc_cl": 100, "acc_br": 91,
    "acc_pk": 80,  "acc_eg": 72,  "acc_ca": 71,  "acc_ir": 63,
    "acc_ng": 58,  "acc_vn": 58,  "acc_lk": 50,  "acc_mx": 50,
    "acc_mg": 47,  "acc_th": 47,  "acc_ar": 45,  "acc_it": 43,
    "acc_af": 40,  "acc_pe": 39,  "acc_pt": 39,  "acc_np": 39,
    "acc_ph": 34,  "acc_id": 34,  "acc_hk": 34,  "acc_tr": 29,
    "acc_at": 28,  "acc_kw": 27,  "acc_cu": 26,  "acc_am": 25,
    "acc_fj": 24,  "acc_pl": 22,  "acc_jp": 22,  "acc_mr": 22,
    "acc_jm": 22,  "acc_sa": 21,  "acc_my": 20,  "acc_ye": 20,
    "acc_gb": 18,  "acc_ie": 18,  "acc_ee": 14,  "acc_sg": 10,
}

ACCOUNTS_CATALOG = {
    "acc_mm": {"name": "🇲🇲 Мьянма (+95)",             "price": "110.25", "stars": "200"},
    "acc_co": {"name": "🇨🇴 Колумбия (+57)",           "price": "117.00", "stars": "200"},
    "acc_bd": {"name": "🇧🇩 Бангладеш (+880)",         "price": "119.25", "stars": "200"},
    "acc_in": {"name": "🇮🇳 Индия (+91)",              "price": "119.25", "stars": "200"},
    "acc_us": {"name": "🇺🇸 США (+1)",                 "price": "119.25", "stars": "200"},
    "acc_ph": {"name": "🇵🇭 Филиппины (+63)",          "price": "128.25", "stars": "250"},
    "acc_ng": {"name": "🇳🇬 Нигерия (+234)",           "price": "130.50", "stars": "250"},
    "acc_id": {"name": "🇮🇩 Индонезия (+62)",          "price": "141.75", "stars": "250"},
    "acc_pk": {"name": "🇵🇰 Пакистан (+92)",           "price": "144.00", "stars": "250"},
    "acc_cl": {"name": "🇨🇱 Чили (+56)",               "price": "177.75", "stars": "300"},
    "acc_ca": {"name": "🇨🇦 Канада (+1)",              "price": "193.50", "stars": "350"},
    "acc_ir": {"name": "🇮🇷 Иран (+98)",               "price": "218.25", "stars": "400"},
    "acc_eg": {"name": "🇪🇬 Египет (+20)",             "price": "222.75", "stars": "400"},
    "acc_mg": {"name": "🇲🇬 Мадагаскар (+261)",        "price": "245.25", "stars": "450"},
    "acc_np": {"name": "🇳🇵 Непал (+977)",             "price": "249.75", "stars": "450"},
    "acc_pe": {"name": "🇵🇪 Перу (+51)",               "price": "258.75", "stars": "450"},
    "acc_br": {"name": "🇧🇷 Бразилия (+55)",           "price": "261.00", "stars": "450"},
    "acc_vn": {"name": "🇻🇳 Вьетнам (+84)",            "price": "270.00", "stars": "500"},
    "acc_af": {"name": "🇦🇫 Афганистан (+93)",         "price": "279.00", "stars": "500"},
    "acc_mx": {"name": "🇲🇽 Мексика (+52)",            "price": "285.75", "stars": "500"},
    "acc_th": {"name": "🇹🇭 Таиланд (+66)",            "price": "297.00", "stars": "500"},
    "acc_uz": {"name": "🇺🇿 Узбекистан (+998)",        "price": "301.50", "stars": "550"},
    "acc_gb": {"name": "🇬🇧 Великобритания (+44)",     "price": "312.75", "stars": "550"},
    "acc_cu": {"name": "🇨🇺 Куба (+53)",               "price": "321.75", "stars": "550"},
    "acc_ye": {"name": "🇾🇪 Йемен (+967)",             "price": "324.00", "stars": "550"},
    "acc_jm": {"name": "🇯🇲 Ямайка (+1)",              "price": "330.75", "stars": "600"},
    "acc_lk": {"name": "🇱🇰 Шри-Ланка (+94)",          "price": "335.25", "stars": "600"},
    "acc_my": {"name": "🇲🇾 Малайзия (+60)",           "price": "348.75", "stars": "600"},
    "acc_ar": {"name": "🇦🇷 Аргентина (+54)",          "price": "357.75", "stars": "600"},
    "acc_mr": {"name": "🇲🇷 Мавритания (+222)",        "price": "375.75", "stars": "650"},
    "acc_ie": {"name": "🇮🇪 Ирландия (+353)",          "price": "384.75", "stars": "650"},
    "acc_tr": {"name": "🇹🇷 Турция (+90)",             "price": "420.75", "stars": "750"},
    "acc_it": {"name": "🇮🇹 Италия (+39)",             "price": "438.75", "stars": "750"},
    "acc_pl": {"name": "🇵🇱 Польша (+48)",             "price": "445.50", "stars": "750"},
    "acc_sa": {"name": "🇸🇦 Саудовская Аравия (+966)", "price": "445.50", "stars": "750"},
    "acc_fj": {"name": "🇫🇯 Фиджи (+679)",             "price": "447.75", "stars": "750"},
    "acc_hk": {"name": "🇭🇰 Гонконг (+852)",           "price": "477.00", "stars": "800"},
    "acc_jp": {"name": "🇯🇵 Япония (+81)",             "price": "479.25", "stars": "850"},
    "acc_at": {"name": "🇦🇹 Австрия (+43)",            "price": "488.25", "stars": "850"},
    "acc_pt": {"name": "🇵🇹 Португалия (+351)",        "price": "488.25", "stars": "850"},
    "acc_kw": {"name": "🇰🇼 Кувейт (+965)",            "price": "497.25", "stars": "850"},
    "acc_am": {"name": "🇦🇲 Армения (+374)",           "price": "542.25", "stars": "950"},
    "acc_ee": {"name": "🇪🇪 Эстония (+372)",           "price": "549.00", "stars": "950"},
    "acc_sg": {"name": "🇸🇬 Сингапур (+65)",           "price": "1930.50", "stars": "3250"},
}

ACCOUNTS_STOCK = {}

STARS_PACKAGES = {
    "stars_50":    {"name": "🌟 50 Stars",    "price": "82.50"},
    "stars_100":   {"name": "🌟 100 Stars",   "price": "165"},
    "stars_250":   {"name": "🌟 250 Stars",   "price": "412.50"},
    "stars_500":   {"name": "🌟 500 Stars",   "price": "825"},
    "stars_1000":  {"name": "🌟 1000 Stars",  "price": "1650"},
    "stars_2500":  {"name": "🌟 2500 Stars",  "price": "4125"},
    "stars_5000":  {"name": "🌟 5000 Stars",  "price": "8250"},
    "stars_10000": {"name": "🌟 10000 Stars", "price": "16500"}
}

# ==================================================
# ПРОВЕРКИ
# ==================================================

def is_bad_message(text):
    if not text:
        return False
    lower = text.lower()
    for w in BAD_WORDS:
        if w in lower:
            return True
    return False


def is_spam(chat_id):
    now = time.time()
    if chat_id not in user_msg_times:
        user_msg_times[chat_id] = []
    user_msg_times[chat_id] = [t for t in user_msg_times[chat_id] if now - t < SPAM_WINDOW]
    user_msg_times[chat_id].append(now)
    return len(user_msg_times[chat_id]) > SPAM_LIMIT


def get_spam_count(chat_id):
    now = time.time()
    if chat_id not in user_msg_times:
        return 0
    return len([t for t in user_msg_times[chat_id] if now - t < SPAM_WINDOW])


def is_flood(chat_id, text):
    if not text:
        return False
    last = user_last_msg.get(chat_id)
    user_last_msg[chat_id] = text
    if last and last.strip().lower() == text.strip().lower():
        return True
    return False


def notify_admin_violation(user_chat_id, reason, extra_text, order_id=None):
    uname = user_usernames.get(user_chat_id, "") or "—"
    name = user_first_names.get(user_chat_id, "Пользователь")

    text = (
        f"⚠️ <b>ПОДОЗРЕНИЕ НА НАРУШЕНИЕ</b>\n\n"
        f"👤 <b>{name}</b>\n"
        f"🆔 ID: <code>{user_chat_id}</code>\n"
        f"🔗 @{uname if uname != '—' else 'нет'}\n"
    )
    if order_id:
        text += f"📦 Заказ #{order_id}\n"
    text += f"\n⚠️ Причина: <b>{reason}</b>\n\n"

    if extra_text:
        short = extra_text[:300] + ("…" if len(extra_text) > 300 else "")
        text += f"📝 Текст:\n<code>{short}</code>\n\n"

    text += "👇 Решение за вами:"

    keyboard = {
        "inline_keyboard": [
            [{"text": "🚫 Забанить", "callback_data": f"warn_ban:{user_chat_id}"}],
            [{"text": "❌ Игнорировать", "callback_data": f"warn_ignore:{user_chat_id}"}]
        ]
    }
    send_message(ADMIN_ID, text, keyboard)

# ==================================================
# ФАЙЛЫ
# ==================================================

def load_admins():
    if not os.path.exists(ADMIN_FILE):
        return
    try:
        with open(ADMIN_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    ADMIN_IDS.add(int(line))
                except ValueError:
                    continue
        print(f"👑 Загружено {len(ADMIN_IDS)} админов")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def save_admin(chat_id):
    if chat_id in ADMIN_IDS:
        return
    ADMIN_IDS.add(chat_id)
    try:
        with open(ADMIN_FILE, "a", encoding="utf-8") as f:
            f.write(f"{chat_id}\n")
        print(f"👑 Новый админ: {chat_id}")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def is_admin(chat_id):
    return chat_id in ADMIN_IDS


def load_banned_users():
    global banned_users
    banned_users = {}
    if not os.path.exists(BANNED_FILE):
        return
    try:
        with open(BANNED_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    banned_users[int(line)] = True
                except ValueError:
                    continue
        print(f"🚫 Загружено {len(banned_users)} забаненных")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def save_banned_users():
    try:
        with open(BANNED_FILE, "w", encoding="utf-8") as f:
            for uid in banned_users.keys():
                f.write(f"{uid}\n")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def ban_user(chat_id):
    banned_users[chat_id] = True
    save_banned_users()
    print(f"🚫 Забанен: {chat_id}")


def unban_user(chat_id):
    if chat_id in banned_users:
        del banned_users[chat_id]
        save_banned_users()
        print(f"✅ Разбанен: {chat_id}")


def load_verified_users():
    if not os.path.exists(USERS_FILE):
        return
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) >= 2:
                    try:
                        uid = int(parts[0])
                        phone = parts[1]
                        user_phones[uid] = phone
                        user_verified[uid] = True
                        if len(parts) >= 3:
                            user_usernames[uid] = parts[2] if parts[2] != "-" else ""
                        if len(parts) >= 4:
                            user_first_names[uid] = parts[3] if parts[3] != "-" else "Пользователь"
                    except ValueError:
                        continue
        print(f"✅ Загружено {len(user_verified)} пользователей")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def save_verified_user(chat_id, phone, username="", first_name="", last_name=""):
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(f"{chat_id}|"):
                        return
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        username_clean = username.replace("|", "_") if username else "-"
        fname_clean = f"{first_name} {last_name}".strip().replace("|", "_") or "-"
        with open(USERS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{chat_id}|{phone}|{username_clean}|{fname_clean}|{timestamp}\n")
        print(f"💾 Сохранён: {chat_id} ({phone})")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def get_all_users_data():
    result = []
    if not os.path.exists(USERS_FILE):
        return result
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) >= 4:
                    try:
                        uid = int(parts[0])
                        result.append({
                            "chat_id": uid,
                            "phone": parts[1],
                            "username": parts[2],
                            "name": parts[3],
                            "date": parts[4] if len(parts) >= 5 else "-",
                            "banned": uid in banned_users
                        })
                    except ValueError:
                        continue
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
    return result


def load_stock():
    global ACCOUNTS_STOCK
    ACCOUNTS_STOCK = dict(ACCOUNTS_BASE_STOCK)
    if not os.path.exists(STOCK_FILE):
        save_stock()
        return
    try:
        loaded = {}
        with open(STOCK_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) == 2:
                    try:
                        loaded[parts[0]] = int(parts[1])
                    except ValueError:
                        continue
        for key in ACCOUNTS_CATALOG.keys():
            if key in loaded:
                ACCOUNTS_STOCK[key] = loaded[key]
        print(f"✅ Загружены остатки для {len(ACCOUNTS_STOCK)} аккаунтов")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def save_stock():
    try:
        with open(STOCK_FILE, "w", encoding="utf-8") as f:
            for key, qty in ACCOUNTS_STOCK.items():
                f.write(f"{key}|{qty}\n")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def decrease_stock(item_id, by=1):
    if item_id not in ACCOUNTS_STOCK:
        return
    old = ACCOUNTS_STOCK[item_id]
    new = max(0, old - by)
    ACCOUNTS_STOCK[item_id] = new
    save_stock()
    print(f"📉 Остаток {item_id}: {old} → {new}")


def save_order_log(order_id, user_chat_id, username, item, price, status):
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        username_clean = (str(username) or "-").replace("|", "_")
        item_clean = (str(item) or "-").replace("|", "_")
        with open(ORDERS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{order_id}|{user_chat_id}|{username_clean}|{item_clean}|{price}|{status}|{timestamp}\n")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def load_all_sales():
    sales = []
    if not os.path.exists(SOLD_FILE):
        return sales
    try:
        with open(SOLD_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) >= 8:
                    if len(parts) >= 9:
                        sales.append({
                            "chat_id": parts[0],
                            "code": parts[1],
                            "item": parts[2],
                            "price": parts[3],
                            "payment": parts[4],
                            "username": parts[5],
                            "phone": parts[6],
                            "name": parts[7],
                            "date": parts[8],
                        })
                    else:
                        sales.append({
                            "chat_id": parts[0],
                            "code": parts[1],
                            "item": parts[2],
                            "price": parts[3],
                            "payment": "RUB",
                            "username": parts[4],
                            "phone": parts[5],
                            "name": parts[6],
                            "date": parts[7],
                        })
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
    return sales


def get_user_purchase_counters(chat_id):
    nb_count = 0
    st_count = 0
    sales = load_all_sales()
    for s in sales:
        if str(s["chat_id"]) == str(chat_id):
            code = s["code"]
            if code.startswith("nb"):
                nb_count += 1
            elif code.startswith("st"):
                st_count += 1
    return nb_count, st_count


def extract_phone_index(item_name):
    try:
        start = item_name.find("(+")
        if start == -1:
            return ""
        end = item_name.find(")", start)
        if end == -1:
            return ""
        return item_name[start + 1:end]
    except:
        return ""


def extract_stars_count(item_name):
    try:
        parts = item_name.split()
        for p in parts:
            if p.isdigit():
                return p
        return ""
    except:
        return ""


def make_purchase_code(chat_id, is_stars, item_name):
    nb_count, st_count = get_user_purchase_counters(chat_id)
    if is_stars:
        next_num = st_count + 1
        stars_count = extract_stars_count(item_name) or "?"
        return f"st{next_num}+{stars_count}"
    else:
        next_num = nb_count + 1
        index = extract_phone_index(item_name) or ""
        return f"nb{next_num}{index}"


def save_sold_log(category, item, price, username, phone, chat_id, name, is_stars=False, payment_method="rub", stars="?"):
    try:
        now = time.localtime()
        time_str = time.strftime("%H:%M", now)
        date_str = time.strftime("%d.%m", now)

        code = make_purchase_code(chat_id, is_stars, item)

        item_clean = (str(item) or "-").replace("|", "_").strip()
        price_clean = (str(price) or "-").replace("|", "_").replace("₽", "").strip()
        username_clean = (str(username) or "-").replace("|", "_").strip() or "-"
        phone_clean = (str(phone) or "-").replace("|", "_").strip() or "-"
        name_clean = (str(name) or "-").replace("|", "_").strip() or "-"

        if payment_method == "stars":
            price_display = f"{stars}⭐"
            method_label = "STARS"
        else:
            price_display = f"{price_clean}₽"
            method_label = "RUB"

        file_exists = os.path.exists(SOLD_FILE)
        with open(SOLD_FILE, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("# chat_id|code|item|price|payment|username|phone|name|date\n")
            f.write(
                f"{chat_id}|{code}|{item_clean}|{price_display}|{method_label}|"
                f"{username_clean}|{phone_clean}|{name_clean}|{date_str} {time_str}\n"
            )
        print(f"💰 Продажа: {code} — {item_clean} — {price_display} ({method_label})")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")


def get_user_purchases_display(chat_id):
    sales = load_all_sales()
    user_sales = [s for s in sales if str(s["chat_id"]) == str(chat_id)]
    if not user_sales:
        return ""
    lines = []
    for s in user_sales:
        lines.append(f"  <code>{s['code']}</code> {s['date']} — {s['item']} — {s['price']}")
    return "\n".join(lines)

# ==================================================
# API
# ==================================================

def api(method, data=None, retries=MAX_RETRIES):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    for attempt in range(retries):
        try:
            if data:
                encoded = urllib.parse.urlencode(data).encode("utf-8")
                req = urllib.request.Request(
                    url, data=encoded,
                    headers={"User-Agent": "NUMBERS-BOT/2.0", "Connection": "close"}
                )
            else:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "NUMBERS-BOT/2.0", "Connection": "close"}
                )
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 409:
                print("⚠️ Конфликт (409)")
                kill_old_bots()
                time.sleep(1)
                continue
            if attempt < retries - 1:
                time.sleep(0.5)
                continue
            return None
        except (socket.timeout, urllib.error.URLError):
            if attempt < retries - 1:
                time.sleep(0.5)
                continue
            return None
        except Exception:
            if attempt < retries - 1:
                time.sleep(0.5)
                continue
            return None
    return None


def send_message(chat_id, text, keyboard=None, disable_notification=False):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard, ensure_ascii=False)
    if disable_notification:
        data["disable_notification"] = True
    return api("sendMessage", data)


def edit_message(chat_id, message_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard, ensure_ascii=False)
    return api("editMessageText", data)


def answer_callback(callback_id):
    return api("answerCallbackQuery", {"callback_query_id": callback_id})


def answer_callback_text(callback_id, text, show_alert=False):
    return api("answerCallbackQuery", {
        "callback_query_id": callback_id,
        "text": text,
        "show_alert": show_alert
    })


def send_contact_request(chat_id):
    keyboard = {
        "keyboard": [
            [{"text": "📱 Поделиться номером", "request_contact": True}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    return send_message(
        chat_id,
        "📱 <b>Поделитесь номером телефона</b>\n\n"
        "🛡️ Для доступа к товарам нужно подтвердить, что вы реальный пользователь.\n\n"
        "🔒 Ваш номер:\n"
        "• Не передаётся третьим лицам\n"
        "• Используется только для идентификации\n\n"
        "👇 Нажмите кнопку ниже:",
        keyboard
    )


def remove_reply_keyboard(chat_id, text="⬇️ Клавиатура обновлена"):
    return send_message(chat_id, text, {"remove_keyboard": True})

# ==================================================
# КЛАВИАТУРЫ
# ==================================================

def main_keyboard(chat_id=None):
    keyboard = [
        [{"text": "🎯🔥 АККАУНТЫ 🔥🎯", "callback_data": "sub:accounts:by_country"}],
        [{"text": "⭐ Звёзды Telegram", "callback_data": "cat:stars"}],
        [{"text": "👤 Администрация", "url": ADMIN_LINK}]
    ]
    if chat_id and is_admin(chat_id):
        keyboard.append([{"text": "👥 Все пользователи", "callback_data": "admin:users"}])
        keyboard.append([{"text": "🚫 Забаненные", "callback_data": "admin:banned_list"}])
    return {"inline_keyboard": keyboard}


def stars_keyboard():
    keyboard = []
    for stars_id, stars in STARS_PACKAGES.items():
        count = stars['name'].split()[1]
        keyboard.append([
            {"text": f"⭐ {count} Stars — {stars['price']} ₽", "callback_data": f"buy_stars:{stars_id}"}
        ])
    keyboard.append([{"text": "👤 Администрация", "url": ADMIN_LINK}])
    keyboard.append([{"text": "⬅️ В главное меню", "callback_data": "back:main"}])
    return {"inline_keyboard": keyboard}


def accounts_by_country_keyboard():
    keyboard = []
    for acc_id, item in ACCOUNTS_CATALOG.items():
        qty = ACCOUNTS_STOCK.get(acc_id, 0)
        stars = item.get("stars", "?")
        keyboard.append([{
            "text": f"{item['name']} — {item['price']}₽ ({stars}⭐) ({qty}шт)",
            "callback_data": f"buy_acc:{acc_id}"
        }])
    keyboard.append([{"text": "👤 Администрация", "url": ADMIN_LINK}])
    keyboard.append([{"text": "⬅️ Назад", "callback_data": "back:main"}])
    return {"inline_keyboard": keyboard}


def payment_method_keyboard(order_id, item_name, price, stars):
    return {
        "inline_keyboard": [
            [{"text": f"💳 Оплатить рублями — {price}₽", "callback_data": f"pay_rub:{order_id}"}],
            [{"text": f"⭐ Оплатить звёздами — {stars}⭐", "callback_data": f"pay_stars:{order_id}"}],
            [{"text": "⬅️ Назад", "callback_data": "sub:accounts:by_country"}]
        ]
    }


def payment_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "✅ Я оплатил", "callback_data": "payment_done"}],
            [{"text": "👤 Связаться с админом", "url": ADMIN_LINK}],
            [{"text": "⬅️ В главное меню", "callback_data": "back:main"}]
        ]
    }


def admin_confirm_keyboard(order_id):
    return {
        "inline_keyboard": [
            [{"text": "✅ Подтвердить", "callback_data": f"confirm:{order_id}"},
             {"text": "❌ Отклонить", "callback_data": f"reject:{order_id}"}]
        ]
    }


def admin_order_keyboard(order_id):
    return {
        "inline_keyboard": [
            [{"text": "💬 Открыть чат с покупателем", "callback_data": f"open_chat:{order_id}"}],
            [{"text": "✅ Завершить покупку", "callback_data": f"finish_send:{order_id}"}],
            [{"text": "🚫 Забанить покупателя", "callback_data": f"ban_ask:{order_id}"}]
        ]
    }


def admin_chat_keyboard(order_id):
    return {
        "inline_keyboard": [
            [{"text": "✅ Завершить покупку", "callback_data": f"finish_send:{order_id}"}],
            [{"text": "🚫 Забанить покупателя", "callback_data": f"ban_ask:{order_id}"}]
        ]
    }


def ban_confirm_keyboard(target_chat_id, order_id):
    return {
        "inline_keyboard": [
            [{"text": "✅ Да, забанить", "callback_data": f"ban_confirm:{target_chat_id}:{order_id}"}],
            [{"text": "❌ Отмена", "callback_data": f"ban_cancel:{target_chat_id}:{order_id}"}]
        ]
    }


def user_confirm_keyboard(order_id):
    return {
        "inline_keyboard": [
            [{"text": "✅ Подтвердить получение", "callback_data": f"user_confirm:{order_id}"}]
        ]
    }


def user_feedback_keyboard(order_id):
    return {
        "inline_keyboard": [
            [{"text": "⭐ Оставить отзыв", "callback_data": f"feedback:{order_id}"}],
            [{"text": "⬅️ В главное меню", "callback_data": "back:main"}]
        ]
    }


def user_profile_keyboard(order_id=None):
    keyboard = []
    safe_order_id = order_id if order_id else 0
    keyboard.append([{"text": "⭐ Оставить отзыв", "callback_data": f"feedback:{safe_order_id}"}])
    keyboard.append([{"text": "🛒 Перейти в магазин", "callback_data": "back:main"}])
    keyboard.append([{"text": "👤 Администрация", "url": ADMIN_LINK}])
    return {"inline_keyboard": keyboard}


def admin_user_actions_keyboard(target_chat_id, is_banned):
    if is_banned:
        return {
            "inline_keyboard": [
                [{"text": "✅ Разблокировать", "callback_data": f"admin:unban:{target_chat_id}"}],
                [{"text": "⬅️ К списку", "callback_data": "admin:users"}]
            ]
        }
    else:
        return {
            "inline_keyboard": [
                [{"text": "🚫 Забанить", "callback_data": f"admin:ban:{target_chat_id}"}],
                [{"text": "⬅️ К списку", "callback_data": "admin:users"}]
            ]
        }

# ==================================================
# ТЕКСТЫ
# ==================================================

def start_text():
    return (
        "👁️‍🗨️ <b>NUMBERS.EXE</b>\n\n"
        "🛒 <b>Добро пожаловать в магазин!</b>\n\n"
        "👇 Выберите категорию:"
    )


def accounts_by_country_text():
    return "🌍 <b>Аккаунты по странам</b>\n\n👇 Выберите страну:"


def stars_text():
    return (
        "⭐ <b>Звёзды Telegram (Stars)</b>\n\n"
        "🌟 Пополните свой баланс звёзд в Telegram!\n\n"
        "💎 <b>Курс: 1 Star = 1.65 ₽</b>\n\n"
        "💡 <b>Что такое Telegram Stars?</b>\n"
        "• Внутренняя валюта Telegram\n"
        "• Можно тратить на стикеры, каналы и ботов\n"
        "• Поддерживает разработчиков\n\n"
        "📦 <b>Доступные пакеты:</b>\n\n"
        "👇 Выберите нужный пакет:"
    )


def payment_text(item_name, price, stars=None):
    return (
        "💳 <b>ОФОРМЛЕНИЕ ЗАКАЗА</b>\n\n"
        f"📦 Товар: <b>{item_name}</b>\n"
        f"💰 Сумма: <b>{price} ₽</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "💳 <b>РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ</b>\n\n"
        f"🏦 Банк: {BANK_NAME}\n"
        f"💳 Карта: {CARD_NUMBER}\n"
        f"👤 Получатель: {RECIPIENT}\n\n"
        "━━━━━━━━━━━━━━\n"
        "🔴 <b>ВАЖНОЕ ПРАВИЛО ОПЛАТЫ!</b> 🔴\n\n"
        "⚠️ <b>Переводите ТОЧНУЮ сумму, указанную выше!</b>\n\n"
        "Администратор идентифицирует ваш заказ ТОЛЬКО по сумме платежа.\n\n"
        "❌ Если вы переведёте БОЛЬШЕ или МЕНЬШЕ —\n"
        "администратор НЕ СМОЖЕТ определить, какой аккаунт вы выбрали,\n"
        "и может предоставить НЕ ТОТ, который вы заказывали!\n\n"
        "✅ Переведите РОВНО столько, сколько указано в чеке.\n\n"
        "━━━━━━━━━━━━━━\n"
        "📌 <b>ИНСТРУКЦИЯ:</b>\n"
        "1️⃣ Переведите ТОЧНУЮ сумму на карту\n"
        "2️⃣ Отправьте скриншот чека @Exec_me_shop\n"
        "3️⃣ В сообщении укажите категорию товара\n"
        "4️⃣ Получите товар через 5-15 минут\n\n"
        "💬 По всем вопросам обращайтесь к администрации!"
    )


def payment_stars_only_text(item_name, stars):
    return (
        "⭐ <b>ОПЛАТА ЗВЁЗДАМИ TELEGRAM</b>\n\n"
        f"📦 Товар: <b>{item_name}</b>\n"
        f"⭐ Сумма: <b>{stars}⭐</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "🔴 <b>ВАЖНАЯ ИНСТРУКЦИЯ!</b> 🔴\n\n"
        "📸 <b>ШАГ 1.</b> Сделайте <b>скриншот этого чека</b>\n"
        "📩 <b>ШАГ 2.</b> Отправьте скриншот администратору:\n"
        f"👤 {ADMIN_LINK}\n"
        "⭐ <b>ШАГ 3.</b> Отправьте звёзды администратору\n"
        f"👤 {ADMIN_LINK}\n\n"
        "━━━━━━━━━━━━━━\n"
        f"⭐ <b>Сумма:</b> <b>{stars}⭐</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "⏳ <b>ОБРАБОТКА ЗАКАЗА:</b>\n"
        "Ответ администратора может занять\n"
        "некоторое время (до 24 часов).\n"
        "Пожалуйста, ожидайте — ваш заказ принят! ✅\n\n"
        "━━━━━━━━━━━━━━\n"
        "📌 <b>КАК ОТПРАВИТЬ ЗВЁЗДЫ:</b>\n"
        "1️⃣ Откройте чат с администратором\n"
        "2️⃣ Нажмите на скрепку 📎 → «Подарок» / «Gift»\n"
        "3️⃣ Выберите «Отправить звёзды»\n"
        f"4️⃣ Введите <b>{stars}⭐</b> и отправьте\n\n"
        "⚠️ <b>ВАЖНО:</b>\n"
        "❌ НЕ отправляйте больше или меньше указанной суммы!\n"
        "✅ Отправляйте РОВНО столько, сколько указано.\n\n"
        "💬 По всем вопросам — к администрации!"
    )


def payment_stars_text(item_name, price):
    return (
        "💳 <b>ОФОРМЛЕНИЕ ЗАКАЗА</b>\n\n"
        f"📦 Товар: <b>{item_name}</b>\n"
        f"💰 Сумма: <b>{price} ₽</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "💳 <b>РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ</b>\n\n"
        f"🏦 Банк: {BANK_NAME}\n"
        f"💳 Карта: {CARD_NUMBER}\n"
        f"👤 Получатель: {RECIPIENT}\n\n"
        "━━━━━━━━━━━━━━\n"
        "📌 <b>ИНСТРУКЦИЯ:</b>\n"
        "1️⃣ Переведите сумму указанную в чеке\n"
        "2️⃣ Отправьте скриншот чека @Exec_me_shop\n"
        "3️⃣ В сообщении укажите <b>Звёзды Telegram</b> и выбранный пакет\n"
        "4️⃣ Получите звёзды на свой аккаунт через 5-15 минут\n\n"
        "💬 По всем вопросам обращайтесь к администрации!"
    )

# ==================================================
# ОБРАБОТЧИК СООБЩЕНИЙ ОТ АДМИНА
# ==================================================

def handle_admin_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()
    if not text:
        return False

    for order_id, order_data in list(temp_data.items()):
        if order_data.get("awaiting_feedback") and order_data.get("feedback_order_id") == order_id:
            if chat_id == order_data["chat_id"]:
                send_message(
                    ADMIN_ID,
                    f"⭐ <b>НОВЫЙ ОТЗЫВ!</b>\n\n"
                    f"Заказ #{order_id}\n"
                    f"👤 {order_data.get('username', '-')}\n"
                    f"📦 {order_data.get('item', '-')}\n\n"
                    f"📝 Текст:\n{text}",
                    None
                )
                send_message(
                    chat_id,
                    "❤️ <b>СПАСИБО ЗА ОТЗЫВ!</b>\n\n"
                    "Приходите ещё! 🛒\n\n"
                    "👇 Вернитесь в главное меню:",
                    {
                        "inline_keyboard": [
                            [{"text": "⬅️ В главное меню", "callback_data": "back:main"}]
                        ]
                    }
                )
                order_data["awaiting_feedback"] = False
                if chat_id in orders:
                    del orders[chat_id]
                return True

    if chat_id in chat_mode:
        order_id = chat_mode[chat_id]

        if text == "/stop":
            del chat_mode[chat_id]
            send_message(
                chat_id,
                f"✅ <b>Режим чата выключен</b>\n\n"
                f"📦 Заказ #{order_id}\n\n"
                f"👇 Что дальше?",
                admin_order_keyboard(order_id)
            )
            if order_id in temp_data:
                user_chat_id = temp_data[order_id]["chat_id"]
                send_message(
                    user_chat_id,
                    f"📴 <b>ЧАТ С АДМИНОМ ЗАКРЫТ</b>\n\n"
                    f"📦 Заказ #{order_id}\n\n"
                    f"Если появятся вопросы — {ADMIN_LINK}",
                    None
                )
            return True

        if order_id in temp_data:
            user_chat_id = temp_data[order_id]["chat_id"]
            send_message(
                user_chat_id,
                f"💬 <b>СООБЩЕНИЕ ОТ АДМИНИСТРАТОРА</b>\n\n"
                f"📦 Заказ #{order_id}\n\n"
                f"{text}",
                None
            )
            send_message(
                chat_id,
                f"✅ Отправлено покупателю заказа #{order_id}\n\n"
                f"<i>Чтобы выйти — /stop</i>",
                None
            )
        else:
            del chat_mode[chat_id]
            send_message(chat_id, "❌ Заказ не найден. Режим чата выключен.", main_keyboard(chat_id))
        return True

    return False

# ==================================================
# ОБРАБОТЧИК ОБНОВЛЕНИЙ
# ==================================================

def handle_update(update):
    global order_counter

    message = update.get("message")
    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if chat_id not in ADMIN_IDS and text and not text.startswith("/start"):
            if chat_id in banned_users:
                return

            awaiting_fb = False
            for oid, o in temp_data.items():
                if o.get("chat_id") == chat_id and o.get("awaiting_feedback"):
                    awaiting_fb = True
                    break
            if awaiting_fb:
                return

            active_order_id = None
            for oid, o in temp_data.items():
                if o.get("chat_id") == chat_id and not o.get("finished"):
                    active_order_id = oid
                    break

            if is_bad_message(text):
                if not user_warned_bad.get(chat_id, False):
                    user_warned_bad[chat_id] = True
                    notify_admin_violation(chat_id, "МАТ / ОСКОРБЛЕНИЯ", text, active_order_id)

            if is_spam(chat_id):
                if not user_warned_spam.get(chat_id, False):
                    user_warned_spam[chat_id] = True
                    cnt = get_spam_count(chat_id)
                    extra = f"За {SPAM_WINDOW} сек: {cnt} сообщений (лимит {SPAM_LIMIT})"
                    notify_admin_violation(chat_id, "СПАМ", extra, active_order_id)

            if is_flood(chat_id, text):
                if not user_warned_spam.get(chat_id, False):
                    user_warned_spam[chat_id] = True
                    notify_admin_violation(chat_id, "ФЛУД / ПОВТОРЫ", text, active_order_id)

        if chat_id not in ADMIN_IDS and text and not text.startswith("/start"):
            for oid, o in list(temp_data.items()):
                if o.get("chat_id") == chat_id:
                    if o.get("finished"):
                        continue
                    send_message(
                        ADMIN_ID,
                        f"💬 <b>СООБЩЕНИЕ ОТ ПОКУПАТЕЛЯ</b>\n\n"
                        f"📦 Заказ #{oid}\n"
                        f"👤 {o.get('username', '-')}\n\n"
                        f"{text}",
                        None
                    )
                    send_message(
                        chat_id,
                        "✅ <b>Сообщение доставлено администратору</b>\n\n"
                        "⏳ Ожидайте ответа...",
                        None
                    )
                    return

        if text.strip() == "/start":
            print(f"📩 /start от {chat_id}")
            remove_reply_keyboard(chat_id, "🔄 Обновление меню...")

            if chat_id in banned_users:
                send_message(
                    chat_id,
                    "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\nДоступ к боту закрыт.\n\nЕсли считаете это ошибкой — свяжитесь с администрацией.",
                    None
                )
                return

            user_obj = message.get("from", {})
            user_username = user_obj.get("username", "").lower()
            if user_username == ADMIN_USERNAME_TARGET:
                if chat_id not in ADMIN_IDS:
                    save_admin(chat_id)
                    send_message(chat_id, "👑 <b>Вы добавлены как администратор!</b>", None)

            if user_verified.get(chat_id, False):
                send_message(chat_id, start_text(), main_keyboard(chat_id))
                return

            send_contact_request(chat_id)
            return

        if "contact" in message:
            contact = message["contact"]
            phone_number = contact.get("phone_number")
            first_name = contact.get("first_name", "")
            last_name = contact.get("last_name", "")
            user_obj = message.get("from", {})
            username = user_obj.get("username", "")

            user_phones[chat_id] = phone_number
            user_verified[chat_id] = True
            user_first_names[chat_id] = f"{first_name} {last_name}".strip() or "Пользователь"
            user_usernames[chat_id] = username
            user_info = user_first_names[chat_id]

            save_verified_user(chat_id, phone_number, username, first_name, last_name)

            remove_reply_keyboard(chat_id, "📱 Номер получен")

            load_msg = send_message(
                chat_id,
                "🔄 <b>Проверяем номер...</b>\n\n⏳ [1/5] Установка соединения...\n░ ░ ░ ░ ░",
                None
            )
            load_msg_id = None
            if load_msg and load_msg.get("ok"):
                load_msg_id = load_msg["result"]["message_id"]

            time.sleep(1.0)
            if load_msg_id:
                edit_message(chat_id, load_msg_id,
                    "🔄 <b>Проверяем номер...</b>\n\n✅ [1/5] Соединение установлено\n⏳ [2/5] Проверка номера...\n█ ░ ░ ░ ░", None)

            time.sleep(1.0)
            if load_msg_id:
                edit_message(chat_id, load_msg_id,
                    "🔄 <b>Проверяем номер...</b>\n\n✅ [1/5] Соединение установлено\n✅ [2/5] Номер валидный\n⏳ [3/5] Проверка безопасности...\n█ █ ░ ░ ░", None)

            time.sleep(1.0)
            if load_msg_id:
                edit_message(chat_id, load_msg_id,
                    "🔄 <b>Проверяем номер...</b>\n\n✅ [1/5] Соединение установлено\n✅ [2/5] Номер валидный\n✅ [3/5] Проверка пройдена\n⏳ [4/5] Создание аккаунта...\n█ █ █ ░ ░", None)

            time.sleep(1.0)
            if load_msg_id:
                edit_message(chat_id, load_msg_id,
                    "🔄 <b>Проверяем номер...</b>\n\n✅ [1/5] Соединение установлено\n✅ [2/5] Номер валидный\n✅ [3/5] Проверка пройдена\n✅ [4/5] Аккаунт создан\n⏳ [5/5] Загрузка меню...\n█ █ █ █ ░", None)

            time.sleep(1.0)
            if load_msg_id:
                edit_message(chat_id, load_msg_id,
                    "✅ <b>ПРОВЕРКА ПРОЙДЕНА!</b>\n\n✅ [1/5] Соединение установлено\n✅ [2/5] Номер валидный\n✅ [3/5] Проверка пройдена\n✅ [4/5] Аккаунт создан\n✅ [5/5] Меню загружено\n█ █ █ █ █", None)

            time.sleep(0.5)

            send_message(
                chat_id,
                f"📱 <b>Ваш номер:</b> <code>{phone_number}</code>\n\n" + start_text(),
                main_keyboard(chat_id)
            )

            username_display = f"@{username}" if username else "нет"
            send_message(
                ADMIN_ID,
                f"🛡️ <b>НОВЫЙ ВЕРИФИЦИРОВАННЫЙ</b>\n\n👤 {user_info}\n🆔 ID: <code>{chat_id}</code>\n🔗 {username_display}\n📱 <code>{phone_number}</code>",
                None
            )
            return

        return

    callback = update.get("callback_query")
    if not callback:
        return

    callback_id = callback["id"]
    data = callback.get("data", "")
    message = callback.get("message")

    if not message:
        answer_callback(callback_id)
        return

    chat_id = message["chat"]["id"]
    message_id = message["message_id"]

    print(f"🔘 Кнопка: {data}")

    if chat_id in banned_users and not is_admin(chat_id):
        answer_callback_text(callback_id, "🚫 Вы забанены. Доступ закрыт.", show_alert=True)
        try:
            edit_message(
                chat_id, message_id,
                "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\nДоступ к боту закрыт.",
                None
            )
        except:
            pass
        return

    if data == "back:main":
        answer_callback(callback_id)
        edit_message(chat_id, message_id, start_text(), main_keyboard(chat_id))
        return

    if data == "chat_active_info":
        answer_callback_text(
            callback_id,
            "💬 Чат активен!\n\n"
            "📡 Если сообщение не доставляется сразу — отправьте его ещё раз через 10-15 сек.\n\n"
            "⚠️ Спам / оскорбления / флуд = БАН\n\n"
            "Пишите по делу — админ ответит.",
            show_alert=True
        )
        return

    if data.startswith("cat:"):
        cat_id = data.split(":", 1)[1]
        if cat_id == "stars":
            answer_callback(callback_id)
            edit_message(chat_id, message_id, stars_text(), stars_keyboard())
            return
        return

    if data.startswith("sub:"):
        parts = data.split(":")
        if len(parts) < 3:
            answer_callback(callback_id)
            return
        cat_id = parts[1]
        sub_id = parts[2]
        if cat_id == "accounts" and sub_id == "by_country":
            answer_callback(callback_id)
            edit_message(chat_id, message_id, accounts_by_country_text(), accounts_by_country_keyboard())
            return
        return

    if data.startswith("buy_stars:"):
        stars_id = data.split(":", 1)[1]
        stars = STARS_PACKAGES.get(stars_id)
        if stars:
            answer_callback(callback_id)
            order_counter += 1
            orders[chat_id] = {
                "order_id": order_counter,
                "item_id": stars_id,
                "item": stars["name"],
                "price": stars["price"],
                "status": "waiting_payment"
            }
            edit_message(chat_id, message_id, payment_stars_text(stars["name"], stars["price"]), payment_keyboard())
        return

    if data.startswith("buy_acc:"):
        acc_id = data.split(":", 1)[1]
        item = ACCOUNTS_CATALOG.get(acc_id)
        if not item:
            answer_callback(callback_id)
            return
        qty = ACCOUNTS_STOCK.get(acc_id, 0)
        if qty <= 0:
            answer_callback_text(callback_id, "❌ Нет в наличии", show_alert=True)
            return
        answer_callback(callback_id)
        order_counter += 1
        orders[chat_id] = {
            "order_id": order_counter,
            "item_id": acc_id,
            "item": item["name"],
            "price": item["price"],
            "stars": item.get("stars", "?"),
            "status": "waiting_payment"
        }
        edit_message(
            chat_id, message_id,
            f"💳 <b>ВЫБЕРИТЕ СПОСОБ ОПЛАТЫ</b>\n\n"
            f"📦 Товар: <b>{item['name']}</b>\n"
            f"💰 Цена: <b>{item['price']} ₽</b>\n"
            f"⭐ Или: <b>{item.get('stars', '?')} ⭐</b>\n\n"
            f"👇 Как хотите оплатить?",
            payment_method_keyboard(order_counter, item["name"], item["price"], item.get("stars", "?"))
        )
        return

    if data.startswith("pay_rub:"):
        order_id = int(data.split(":")[1])
        answer_callback(callback_id)
        if chat_id not in orders or orders[chat_id].get("order_id") != order_id:
            edit_message(chat_id, message_id, "❌ <b>Заказ не найден.</b>", main_keyboard(chat_id))
            return
        order = orders[chat_id]
        order["payment_method"] = "rub"
        edit_message(
            chat_id, message_id,
            payment_text(order["item"], order["price"], order.get("stars")),
            payment_keyboard()
        )
        return

    if data.startswith("pay_stars:"):
        order_id = int(data.split(":")[1])
        answer_callback(callback_id)
        if chat_id not in orders or orders[chat_id].get("order_id") != order_id:
            edit_message(chat_id, message_id, "❌ <b>Заказ не найден.</b>", main_keyboard(chat_id))
            return
        order = orders[chat_id]
        order["payment_method"] = "stars"
        edit_message(
            chat_id, message_id,
            payment_stars_only_text(order["item"], order.get("stars", "?")),
            payment_keyboard()
        )
        return

    if data == "payment_done":
        answer_callback(callback_id)
        if chat_id not in orders:
            edit_message(chat_id, message_id, "❌ <b>Заказ не найден.</b>", main_keyboard(chat_id))
            return
        order = orders[chat_id]
        order_id = order["order_id"]
        user_obj = callback.get("from", {})
        username = user_obj.get("username", "")
        first_name = user_obj.get("first_name", "")
        user_info = f"@{username}" if username else f"{first_name} (ID: {chat_id})"

        pending_orders[order_id] = {
            "chat_id": chat_id,
            "item_id": order.get("item_id"),
            "item": order["item"],
            "price": order["price"],
            "stars": order.get("stars", "?"),
            "username": user_info,
            "phone": user_phones.get(chat_id, "Не указан"),
            "payment_method": order.get("payment_method", "rub")
        }
        save_order_log(order_id, chat_id, user_info, order["item"], order["price"], "waiting_admin")

        method = order.get("payment_method", "rub")
        if method == "stars":
            method_block = f"⭐ <b>Оплата:</b> {order.get('stars', '?')}⭐ (Звёзды)"
        else:
            method_block = f"💳 <b>Оплата:</b> {order['price']} ₽ (Рубли)"

        send_message(
            ADMIN_ID,
            f"🆕 <b>НОВЫЙ ЗАКАЗ #{order_id}</b>\n\n"
            f"👤 {user_info}\n"
            f"🆔 ID: <code>{chat_id}</code>\n"
            f"📱 <code>{user_phones.get(chat_id, 'Не указан')}</code>\n"
            f"📦 {order['item']}\n"
            f"{method_block}\n\n"
            f"👇 Подтвердите оплату:",
            admin_confirm_keyboard(order_id)
        )

        if method == "stars":
            sum_block = f"⭐ <b>Сумма:</b> {order.get('stars', '?')}⭐"
            method_text = "⭐ Звёзды"
        else:
            sum_block = f"💰 <b>Сумма:</b> {order['price']} ₽"
            method_text = "💳 Рубли"

        edit_message(
            chat_id, message_id,
            f"╔══════════════════════════╗\n"
            f"║  📩 <b>ЗАЯВКА ОТПРАВЛЕНА</b>  ║\n"
            f"╚══════════════════════════╝\n\n"
            f"🆔 <b>Заказ:</b> #{order_id}\n"
            f"📦 <b>Товар:</b> {order['item']}\n"
            f"{sum_block}\n"
            f"💳 <b>Способ:</b> {method_text}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏳ <b>ОЖИДАЙТЕ ПОДТВЕРЖДЕНИЯ</b>\n\n"
            f"Администратор проверит оплату.\n"
            f"Это может занять <b>5-15 минут</b>.\n\n"
            f"✅ После подтверждения товар\n"
            f"будет отправлен вам в чат.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💬 По вопросам — @Exec_me_shop",
            None
        )
        return

    if data.startswith("confirm:"):
        order_id = int(data.split(":")[1])
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        if order_id not in pending_orders:
            answer_callback_text(callback_id, "❌ Заказ не найден", show_alert=True)
            return
        order = pending_orders[order_id]
        user_chat_id = order["chat_id"]
        temp_data[order_id] = dict(order)
        save_order_log(order_id, user_chat_id, order.get("username", "-"), order["item"], order["price"], "confirmed")
        answer_callback(callback_id)
        send_message(
            user_chat_id,
            f"✅ <b>ЗАКАЗ #{order_id} ПОДТВЕРЖДЁН!</b>\n\n📦 {order['item']}\n💰 {order['price']} ₽\n\n⏳ Администратор скоро отправит данные...",
            None
        )

        method = order.get("payment_method", "rub")
        if method == "stars":
            method_block = f"⭐ <b>Оплата:</b> {order.get('stars', '?')}⭐ (Звёзды)"
        else:
            method_block = f"💳 <b>Оплата:</b> {order['price']} ₽ (Рубли)"

        edit_message(
            chat_id, message_id,
            f"╔══════════════════════════╗\n"
            f"║   ✅ <b>ЗАКАЗ ПОДТВЕРЖДЁН</b>   ║\n"
            f"╚══════════════════════════╝\n\n"
            f"🆔 <b>Заказ:</b> #{order_id}\n"
            f"👤 <b>Покупатель:</b> {order.get('username', '-')}\n"
            f"📱 <b>Номер:</b> <code>{order.get('phone', '-')}</code>\n"
            f"📦 <b>Товар:</b> {order['item']}\n"
            f"{method_block}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👇 <b>ВЫБЕРИТЕ ДЕЙСТВИЕ:</b>",
            admin_order_keyboard(order_id)
        )
        del pending_orders[order_id]
        return

    if data.startswith("reject:"):
        order_id = int(data.split(":")[1])
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        if order_id not in pending_orders:
            answer_callback_text(callback_id, "❌ Заказ не найден", show_alert=True)
            return
        order = pending_orders[order_id]
        user_chat_id = order["chat_id"]
        save_order_log(order_id, user_chat_id, order.get("username", "-"), order["item"], order["price"], "rejected")
        answer_callback(callback_id)
        send_message(user_chat_id, f"❌ <b>ЗАКАЗ #{order_id} ОТКЛОНЁН</b>\n\nСвяжитесь: @Exec_me_shop", None)
        edit_message(chat_id, message_id, f"❌ <b>ЗАКАЗ #{order_id} ОТКЛОНЁН</b>", None)
        if user_chat_id in orders:
            del orders[user_chat_id]
        del pending_orders[order_id]
        return

    if data.startswith("open_chat:"):
        order_id = int(data.split(":")[1])

        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        if order_id not in temp_data:
            answer_callback_text(callback_id, "❌ Заказ не найден", show_alert=True)
            return

        chat_mode[chat_id] = order_id
        order = temp_data[order_id]
        user_chat_id = order["chat_id"]

        answer_callback(callback_id)

        edit_message(
            chat_id, message_id,
            f"╔══════════════════════════╗\n"
            f"║    💬 <b>ЧАТ С ПОКУПАТЕЛЕМ</b>    ║\n"
            f"╚══════════════════════════╝\n\n"
            f"🆔 <b>Заказ:</b> #{order_id}\n"
            f"👤 <b>Покупатель:</b> {order.get('username', '-')}\n"
            f"📦 <b>Товар:</b> {order['item']}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📤 Пишите сюда — сообщения уходят покупателю\n"
            f"📥 Ответы покупателя приходят вам сюда же\n\n"
            f"⚠️ <b>Чтобы выйти</b> — /stop\n"
            f"━━━━━━━━━━━━━━━━━━━━━━",
            admin_chat_keyboard(order_id)
        )

        send_message(
            user_chat_id,
            f"💬 <b>АДМИНИСТРАТОР ОТКРЫЛ ЧАТ</b>\n\n"
            f"📦 Заказ #{order_id} — {order['item']}\n\n"
            f"👀 Администратор видит все ваши сообщения.\n"
            f"📝 Можете задать вопросы или уточнить данные.\n\n"
            f"⚠️ <b>ВАЖНО:</b>\n"
            f"📡 Сообщения могут доставляться не сразу.\n"
            f"📩 Если через 10-15 секунд <b>нет ответа</b> — \n"
            f"отправьте сообщение <b>повторно</b>.\n"
            f"✅ Когда сообщение дойдёт — появится подтверждение.\n\n"
            f"⚠️ <b>ПРАВИЛА ОБЩЕНИЯ:</b>\n"
            f"🚫 <b>Спам</b> — бан\n"
            f"🚫 <b>Оскорбления</b> — бан\n"
            f"🚫 <b>Флуд / повторы</b> — бан\n\n"
            f"🛡️ Автомодерация работает 24/7.\n"
            f"🔒 При нарушении — блокировка и аннулирование заказа.\n\n"
            f"💬 Пишите по делу — админ ответит.",
            {
                "inline_keyboard": [
                    [{"text": "💬 Чат активен", "callback_data": "chat_active_info"}]
                ]
            }
        )
        return

    if data.startswith("finish_send:"):
        order_id = int(data.split(":")[1])

        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        if order_id not in temp_data:
            answer_callback_text(callback_id, "❌ Заказ не найден", show_alert=True)
            return

        order = temp_data[order_id]
        user_chat_id = order["chat_id"]
        item_id = order.get("item_id") or ""

        if item_id.startswith("acc_"):
            real_item = ACCOUNTS_CATALOG.get(item_id, {}).get("name", order.get("item", "—"))
        elif item_id.startswith("stars_"):
            real_item = STARS_PACKAGES.get(item_id, {}).get("name", order.get("item", "—"))
        else:
            real_item = order.get("item", "—")
        order["item"] = real_item

        if item_id.startswith("acc_") and item_id in ACCOUNTS_STOCK:
            decrease_stock(item_id, 1)

        if item_id.startswith("acc_"):
            category = "Аккаунт"
        elif item_id.startswith("stars_"):
            category = "Звёзды"
        else:
            category = "Другое"

        save_order_log(order_id, user_chat_id, order.get("username", "-"),
                       real_item, order["price"], "sent")

        buyer_username = user_usernames.get(user_chat_id, "") or "-"
        buyer_phone = user_phones.get(user_chat_id, "-")
        buyer_name = user_first_names.get(user_chat_id, "-")

        is_stars = item_id.startswith("stars_")

        save_sold_log(
            category=category,
            item=real_item,
            price=order["price"],
            username=buyer_username,
            phone=buyer_phone,
            chat_id=user_chat_id,
            name=buyer_name,
            is_stars=is_stars,
            payment_method=order.get("payment_method", "rub"),
            stars=order.get("stars", "?")
        )

        temp_data[order_id]["finished"] = True

        for admin_id in list(chat_mode.keys()):
            if chat_mode[admin_id] == order_id:
                del chat_mode[admin_id]
                try:
                    send_message(
                        admin_id,
                        f"╔══════════════════════════╗\n"
                        f"║  📴 <b>ЧАТ АВТОМАТИЧЕСКИ ЗАКРЫТ</b> ║\n"
                        f"╚══════════════════════════╝\n\n"
                        f"🆔 <b>Заказ:</b> #{order_id}\n"
                        f"✅ Покупка завершена\n"
                        f"🔒 Режим чата отключён\n\n"
                        f"<i>Можете продолжить работу с другими заказами.</i>",
                        None
                    )
                except:
                    pass

        user_warned_spam.pop(user_chat_id, None)
        user_warned_bad.pop(user_chat_id, None)

        answer_callback(callback_id)

        send_message(
            user_chat_id,
            f"🎉 <b>ЗАКАЗ #{order_id} ЗАВЕРШЁН</b>\n\n"
            f"📦 {real_item}\n\n"
            f"✅ <b>Подтвердите получение:</b>",
            user_confirm_keyboard(order_id)
        )

        qty_now = ACCOUNTS_STOCK.get(item_id, "-") if item_id.startswith("acc_") else "-"

        method = order.get("payment_method", "rub")
        if method == "stars":
            sum_block = f"⭐ <b>Сумма:</b> {order.get('stars', '?')}⭐"
            method_text = "⭐ Звёзды"
        else:
            sum_block = f"💰 <b>Сумма:</b> {order['price']} ₽"
            method_text = "💳 Рубли"

        edit_message(
            chat_id, message_id,
            f"╔══════════════════════════╗\n"
            f"║   ✅ <b>ЗАКАЗ ЗАВЕРШЁН</b>   ║\n"
            f"╚══════════════════════════╝\n\n"
            f"🆔 <b>Номер заказа:</b> #{order_id}\n"
            f"📦 <b>Товар:</b> {real_item}\n"
            f"{sum_block}\n"
            f"💳 <b>Оплата:</b> {method_text}\n"
            f"📉 <b>Остаток:</b> {qty_now}шт\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💾 Сохранено в <code>sold.txt</code>\n"
            f"📊 Категория: {category}",
            None
        )
        return

    if data.startswith("ban_ask:"):
        order_id = int(data.split(":")[1])

        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        if order_id not in temp_data:
            answer_callback_text(callback_id, "❌ Заказ не найден", show_alert=True)
            return

        order = temp_data[order_id]
        user_chat_id = order["chat_id"]
        uname = user_usernames.get(user_chat_id, "") or "—"
        name = user_first_names.get(user_chat_id, "Пользователь")

        answer_callback(callback_id)
        edit_message(
            chat_id, message_id,
            f"⚠️ <b>ПОДТВЕРДИТЕ БАН</b>\n\n"
            f"👤 <b>{name}</b>\n"
            f"🆔 ID: <code>{user_chat_id}</code>\n"
            f"🔗 @{uname if uname != '—' else 'нет'}\n"
            f"📦 Заказ #{order_id} — {order['item']}\n\n"
            f"🔴 <b>Что произойдёт:</b>\n"
            f"• Пользователь будет ЗАБАНЕН в боте\n"
            f"• Заказ #{order_id} будет АННУЛИРОВАН\n"
            f"• Пользователь больше не сможет пользоваться ботом\n\n"
            f"⚠️ <b>Действие необратимо!</b>",
            ban_confirm_keyboard(user_chat_id, order_id)
        )
        return

    if data.startswith("ban_confirm:"):
        parts = data.split(":")
        if len(parts) < 3:
            answer_callback(callback_id)
            return
        target_id = int(parts[1])
        order_id = int(parts[2])

        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return

        ban_user(target_id)

        if order_id in temp_data:
            order_item = temp_data[order_id].get("item", "-")
            order_price = temp_data[order_id].get("price", "-")
            del temp_data[order_id]
            save_order_log(order_id, target_id, "-", order_item, order_price, "banned")

        if target_id in orders:
            del orders[target_id]

        if order_id in pending_orders:
            del pending_orders[order_id]

        for admin_id in list(chat_mode.keys()):
            if chat_mode[admin_id] == order_id:
                del chat_mode[admin_id]

        user_warned_spam.pop(target_id, None)
        user_warned_bad.pop(target_id, None)

        send_message(
            target_id,
            "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\n"
            "Доступ к боту закрыт администратором.\n\n"
            "Ваш заказ был аннулирован.\n\n"
            "Если считаете это ошибкой — обратитесь в поддержку.",
            None
        )

        answer_callback_text(callback_id, "✅ Пользователь забанен", show_alert=True)

        edit_message(
            chat_id, message_id,
            f"✅ <b>ПОЛЬЗОВАТЕЛЬ ЗАБАНЕН</b>\n\n"
            f"🆔 ID: <code>{target_id}</code>\n"
            f"📦 Заказ #{order_id} — АННУЛИРОВАН\n"
            f"💾 Записано в <code>banned.txt</code>",
            None
        )
        return

    if data.startswith("ban_cancel:"):
        parts = data.split(":")
        if len(parts) < 3:
            answer_callback(callback_id)
            return
        order_id = int(parts[2])

        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return

        answer_callback_text(callback_id, "❌ Бан отменён", show_alert=True)

        edit_message(
            chat_id, message_id,
            f"❌ <b>Бан отменён</b>\n\n"
            f"📦 Заказ #{order_id}\n\n"
            f"👇 Что дальше?",
            admin_order_keyboard(order_id)
        )
        return

    if data.startswith("warn_ban:"):
        target_id = int(data.split(":")[1])

        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return

        ban_user(target_id)

        for oid, o in list(temp_data.items()):
            if o.get("chat_id") == target_id:
                save_order_log(oid, target_id, "-", o.get("item", "-"), o.get("price", "-"), "banned")
                del temp_data[oid]
                if target_id in chat_mode:
                    del chat_mode[target_id]

        if target_id in orders:
            del orders[target_id]

        for oid in list(pending_orders.keys()):
            if pending_orders[oid].get("chat_id") == target_id:
                del pending_orders[oid]

        user_warned_spam.pop(target_id, None)
        user_warned_bad.pop(target_id, None)

        send_message(
            target_id,
            "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\n"
            "Доступ к боту закрыт администратором.\n"
            "Ваши заказы аннулированы.",
            None
        )

        answer_callback_text(callback_id, "🚫 Пользователь забанен", show_alert=True)

        edit_message(
            chat_id, message_id,
            f"✅ <b>ПОЛЬЗОВАТЕЛЬ ЗАБАНЕН</b>\n\n"
            f"🆔 ID: <code>{target_id}</code>\n"
            f"💾 Записано в <code>banned.txt</code>",
            None
        )
        return

    if data.startswith("warn_ignore:"):
        target_id = int(data.split(":")[1])

        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return

        user_warned_spam.pop(target_id, None)
        user_warned_bad.pop(target_id, None)
        user_msg_times[target_id] = []

        answer_callback_text(callback_id, "❌ Игнорировано", show_alert=True)
        edit_message(
            chat_id, message_id,
            f"❌ <b>Нарушение проигнорировано</b>\n\n"
            f"🆔 ID: <code>{target_id}</code>\n"
            f"<i>Бот предупредит снова, если повторится</i>",
            None
        )
        return

    if data.startswith("user_confirm:"):
        order_id = int(data.split(":")[1])
        answer_callback(callback_id)

        if order_id not in temp_data:
            temp_data[order_id] = {
                "chat_id": chat_id,
                "item": "—",
                "price": "—",
                "username": user_usernames.get(chat_id, "-"),
                "finished": True
            }

        order = temp_data[order_id]

        if chat_id != order["chat_id"]:
            send_message(chat_id, "❌ Это не ваш заказ!", None)
            return

        nb_count, st_count = get_user_purchase_counters(chat_id)
        total_purchases = nb_count + st_count

        if total_purchases >= 5:
            status_line = "💎 <b>VIP-КЛИЕНТ</b>"
        elif total_purchases >= 2:
            status_line = "⭐ <b>ПОСТОЯННЫЙ КЛИЕНТ</b>"
        else:
            status_line = "🆕 <b>НОВЫЙ КЛИЕНТ</b>"

        history = get_user_purchases_display(chat_id)

        send_message(
            ADMIN_ID,
            f"✅ <b>ПОКУПАТЕЛЬ ПОДТВЕРДИЛ ПОЛУЧЕНИЕ</b>\n\n"
            f"Заказ #{order_id}\n"
            f"👤 {order.get('username', '-')}\n"
            f"📦 {order['item']}\n"
            f"💰 {order['price']} ₽",
            None
        )

        profile_text = (
            f"╔══════════════════════════╗\n"
            f"║  ✅ <b>ПОКУПКА ЗАВЕРШЕНА!</b> ║\n"
            f"╚══════════════════════════╝\n\n"
            f"🎉 <b>Спасибо за покупку!</b>\n"
            f"Будем рады видеть вас снова ❤️\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>ВАШ ПРОФИЛЬ</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📛 Имя: <b>{user_first_names.get(chat_id, 'Пользователь')}</b>\n"
            f"🆔 ID: <code>{chat_id}</code>\n"
            f"📱 Номер: <code>{user_phones.get(chat_id, '-')}</code>\n"
            f"🔗 Юзернейм: @{user_usernames.get(chat_id, 'нет') if user_usernames.get(chat_id) else 'нет'}\n\n"
            f"👑 Статус: {status_line}\n"
            f"📦 Покупок всего: <b>{total_purchases}</b>\n"
            f"   • Номера: <b>{nb_count}</b>\n"
            f"   • Звёзды: <b>{st_count}</b>\n"
        )

        if history:
            profile_text += f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
            profile_text += f"📜 <b>ИСТОРИЯ ПОКУПОК</b>\n"
            profile_text += f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            profile_text += history + "\n"

        profile_text += (
            f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💫 <b>ЧТО ДАЛЬШЕ?</b>\n\n"
            f"⭐ Понравилось? Оставьте отзыв!\n"
            f"🛒 Загляните в магазин ещё — есть новинки!\n"
            f"👤 Остались вопросы? Свяжитесь с админом.\n\n"
            f"👇 Выберите действие:"
        )

        if len(profile_text) > 4000:
            profile_text = profile_text[:3900] + "\n\n<i>… обрезано</i>"

        edit_message(chat_id, message_id, profile_text, user_profile_keyboard(order_id))
        return

    if data.startswith("feedback:"):
        order_id = int(data.split(":")[1])
        answer_callback(callback_id)

        if order_id == 0 or order_id not in temp_data:
            found_id = None
            for oid, o in temp_data.items():
                if o.get("chat_id") == chat_id:
                    found_id = oid
                    break
            if found_id:
                order_id = found_id
            else:
                order_id = 999999
                temp_data[order_id] = {
                    "chat_id": chat_id,
                    "item": "—",
                    "price": "—",
                    "username": user_usernames.get(chat_id, "-"),
                    "finished": True
                }

        if order_id not in temp_data:
            temp_data[order_id] = {
                "chat_id": chat_id,
                "item": "—",
                "price": "—",
                "username": user_usernames.get(chat_id, "-"),
                "finished": True
            }

        temp_data[order_id]["awaiting_feedback"] = True
        temp_data[order_id]["feedback_order_id"] = order_id
        temp_data[order_id]["chat_id"] = chat_id

        for admin_id in list(chat_mode.keys()):
            if chat_mode[admin_id] == order_id:
                del chat_mode[admin_id]

        edit_message(
            chat_id, message_id,
            "✍️ <b>НАПИШИТЕ ВАШ ОТЗЫВ</b>\n\n"
            "📝 Просто напишите сообщение — оно уйдёт администратору.\n\n"
            "💬 Отзыв можно отправить один раз.",
            None
        )
        return

    if data == "admin:users":
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        answer_callback(callback_id)
        users = get_all_users_data()
        if not users:
            edit_message(chat_id, message_id, "👥 <b>Все пользователи</b>\n\n📭 Список пуст.",
                         {"inline_keyboard": [[{"text": "⬅️ В главное меню", "callback_data": "back:main"}]]})
            return

        text = f"👥 <b>ВСЕ ПОЛЬЗОВАТЕЛИ ({len(users)})</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        keyboard = []
        for idx, u in enumerate(users, 1):
            ban_mark = "🚫" if u["banned"] else "✅"
            nb_count, st_count = get_user_purchase_counters(u["chat_id"])
            total = nb_count + st_count
            buyer_mark = f"⭐ ПОСТОЯННЫЙ ({total})" if total > 0 else "🆕 НОВЫЙ"
            uname = f"@{u['username']}" if u["username"] and u["username"] != "-" else "—"

            text += f"┌─ 👤 <b>#{idx} {u['name']}</b>\n"
            text += f"│ 🆔 <code>{u['chat_id']}</code>\n"
            text += f"│ 📱 <code>{u['phone']}</code>\n"
            text += f"│ 🔗 {uname}\n"
            text += f"│ 👤 {buyer_mark}\n"
            text += f"│ {ban_mark} {'ЗАБАНЕН' if u['banned'] else 'АКТИВЕН'}\n"
            text += f"└──────────────────────\n\n"

            btn_text = f"{ban_mark} #{idx} {u['name'][:18]}"
            keyboard.append([{"text": btn_text, "callback_data": f"admin:view:{u['chat_id']}"}])

        keyboard.append([{"text": "⬅️ В главное меню", "callback_data": "back:main"}])

        if len(text) > 4000:
            text = text[:3900] + "\n\n<i>… Список обрезан.</i>"

        edit_message(chat_id, message_id, text, {"inline_keyboard": keyboard})
        return

    if data == "admin:banned_list":
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        answer_callback(callback_id)
        users = get_all_users_data()
        banned = [u for u in users if u["banned"]]
        if not banned:
            edit_message(chat_id, message_id, "🚫 <b>Забаненные</b>\n\n📭 Список пуст.",
                         {"inline_keyboard": [[{"text": "⬅️ В главное меню", "callback_data": "back:main"}]]})
            return
        text = f"🚫 <b>ЗАБАНЕННЫЕ ({len(banned)})</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        keyboard = []
        for idx, u in enumerate(banned, 1):
            uname = f"@{u['username']}" if u["username"] and u["username"] != "-" else "—"
            text += f"┌─ 🚫 <b>#{idx} {u['name']}</b>\n"
            text += f"│ 🆔 <code>{u['chat_id']}</code>\n"
            text += f"│ 📱 <code>{u['phone']}</code>\n"
            text += f"│ 🔗 {uname}\n"
            text += f"└──────────────────────\n\n"
            keyboard.append([{"text": f"🚫 #{idx} {u['name'][:20]}", "callback_data": f"admin:view:{u['chat_id']}"}])
        keyboard.append([{"text": "⬅️ В главное меню", "callback_data": "back:main"}])
        edit_message(chat_id, message_id, text, {"inline_keyboard": keyboard})
        return

    if data.startswith("admin:view:"):
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        target_id = int(data.split(":")[2])
        answer_callback(callback_id)
        users = get_all_users_data()
        target = next((u for u in users if u["chat_id"] == target_id), None)
        if not target:
            edit_message(chat_id, message_id, "❌ Пользователь не найден",
                         {"inline_keyboard": [[{"text": "⬅️ К списку", "callback_data": "admin:users"}]]})
            return
        uname = f"@{target['username']}" if target["username"] and target["username"] != "-" else "—"
        ban_status = "🚫 <b>ЗАБАНЕН</b>" if target["banned"] else "✅ <b>Активен</b>"

        nb_count, st_count = get_user_purchase_counters(target_id)
        total = nb_count + st_count
        buyer_status = f"⭐ <b>ПОСТОЯННЫЙ</b> ({total} покупок)" if total > 0 else "🆕 <b>НОВЫЙ</b>"

        history = get_user_purchases_display(target_id)
        history_block = f"\n📦 <b>ИСТОРИЯ ПОКУПОК:</b>\n{history}\n" if history else "\n📦 Покупок пока нет\n"

        text = (
            f"👤 <b>КАРТОЧКА ПОЛЬЗОВАТЕЛЯ</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📛 Имя: <b>{target['name']}</b>\n"
            f"🆔 ID: <code>{target['chat_id']}</code>\n"
            f"📱 Номер: <code>{target['phone']}</code>\n"
            f"🔗 Юзернейм: {uname}\n"
            f"📅 Регистрация: {target['date']}\n"
            f"👤 Статус: {buyer_status}\n"
            f"{history_block}\n"
            f"🔐 Бан: {ban_status}\n\n"
            f"👇 Действия:"
        )

        if len(text) > 4000:
            text = text[:3900] + "\n\n<i>… обрезано</i>"

        edit_message(chat_id, message_id, text, admin_user_actions_keyboard(target_id, target["banned"]))
        return

    if data.startswith("admin:ban:"):
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        target_id = int(data.split(":")[2])
        ban_user(target_id)
        answer_callback_text(callback_id, "🚫 Пользователь забанен", show_alert=True)
        send_message(target_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\nДоступ к боту закрыт администратором.", None)
        return

    if data.startswith("admin:unban:"):
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        target_id = int(data.split(":")[2])
        unban_user(target_id)
        answer_callback_text(callback_id, "✅ Пользователь разблокирован", show_alert=True)
        send_message(target_id, "✅ <b>ВЫ РАЗБЛОКИРОВАНЫ</b>\n\nДоступ восстановлен.\n\nНапишите /start", None)
        return

    answer_callback(callback_id)

# ==================================================
# ОСНОВНОЙ ЦИКЛ
# ==================================================

def main():
    print("\n" + "=" * 50)
    print("        NUMBERS.EXE — PYDROID / WINDOWS")
    print("=" * 50 + "\n")

    load_admins()
    load_verified_users()
    load_stock()
    load_banned_users()

    print("🔄 Очистка webhook...", end=" ", flush=True)
    api("deleteWebhook", {"drop_pending_updates": True})
    print("✅")

    print("🔄 Проверка Telegram...", end=" ", flush=True)
    result = api("getMe")

    if result and result.get("ok"):
        username = result["result"].get("username", "unknown")
        print(f"✅ @{username}")
    else:
        print("❌ Ошибка")
        print("⏳ Повтор через 3 сек...")
        time.sleep(3)
        main()
        return

    print("✅ Webhook отключён\n")
    print("🟢 БОТ ЗАПУЩЕН")
    print("💓 Статус: ONLINE")
    print(f"📁 Пользователи: {USERS_FILE}")
    print(f"📁 Остатки:     {STOCK_FILE}")
    print(f"📁 Заказы:      {ORDERS_FILE}")
    print(f"📁 Баны:        {BANNED_FILE}")
    print(f"📁 Админы:      {ADMIN_FILE}")
    print(f"📁 Продажи:     {SOLD_FILE}")
    print(f"👥 Пользователей: {len(user_verified)}")
    print(f"👑 Админов: {len(ADMIN_IDS)}")
    print(f"🚫 Забаненных: {len(banned_users)}")
    print("⏳ Ожидание сообщений...\n")

    offset = 0
    last_status = time.time()

    while True:
        try:
            if time.time() - last_status >= 30:
                print(f"💓 Жив | {time.strftime('%H:%M:%S')} | 👥 {len(user_verified)} | 🚫 {len(banned_users)} | 📦 {len(pending_orders)}")
                last_status = time.time()

            result = api("getUpdates", {
                "offset": offset,
                "timeout": POLL_TIMEOUT,
                "limit": 100,
                "allowed_updates": json.dumps(["message", "callback_query"])
            })

            if not result:
                time.sleep(RECONNECT_DELAY)
                continue

            if not result.get("ok"):
                time.sleep(RECONNECT_DELAY)
                continue

            updates = result.get("result", [])
            for update in updates:
                update_id = update.get("update_id")
                if update_id is not None:
                    offset = update_id + 1
                try:
                    msg = update.get("message")
                    if msg and "text" in msg:
                        if handle_admin_message(msg):
                            continue
                    handle_update(update)
                except Exception as e:
                    print(f"❌ Ошибка: {e}")

        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен.")
            try:
                if os.path.exists("bot_numbers.lock"):
                    os.remove("bot_numbers.lock")
            except:
                pass
            break
        except Exception as e:
            print(f"🔴 Ошибка: {e}")
            time.sleep(RECONNECT_DELAY)


if __name__ == "__main__":
    main()
