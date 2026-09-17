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
    for lock_file in ["bot_numbers.lock", "bot.lock"]:
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

ADMIN_ID = 8864430187

ADMIN_LINK = "https://t.me/Exec_me_shop"
CONTACT_URL = "https://t.me/dark_exec_me_shop"
ADMIN_USERNAME_TARGET = "exec_me_shop"
BTC_WALLET = "bc1qsxw3hsht6qkcc9y2jyj02pc0vwmn9fk7hrv2hj"
ETH_WALLET = "0x51ae3A2F9994541aFfe59c6633f10033683Bc821"
ETH_NETWORK = "Ethereum Mainnet (ERC-20)"

POLL_TIMEOUT = 60
REQUEST_TIMEOUT = 15
RECONNECT_DELAY = 1
MAX_RETRIES = 2

STAR_RATE = 1.69

# --- dark.web ---
DARKWEB_PRICE_USD = 3
DARKWEB_PRICE_STARS = 200
KRAKEN_PRICE_RUB = 100
KRAKEN_PRICE_STARS = 50
BTC_USD_RATE = 95000
ETH_USD_RATE = 3300
BTC_RUB_RATE = 7000000
ETH_RUB_RATE = 250000

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
DARKWEB_FILE = os.path.join(DATA_DIR, "darkweb_access.txt")
KRAKEN_FILE = os.path.join(DATA_DIR, "kraken_access.txt")

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
darkweb_users = set()
kraken_users = set()

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
# АККАУНТЫ
# ==================================================

ACCOUNTS_BASE_STOCK = {
    "acc_bd": 130, "acc_us": 375, "acc_mr": 24,
    "acc_mm": 231, "acc_co": 184, "acc_in": 223,
    "acc_ph": 91,  "acc_ng": 11,  "acc_id": 79,
    "acc_pk": 10,  "acc_cl": 114, "acc_ca": 59,
    "acc_ir": 62,  "acc_eg": 70,  "acc_mg": 47,
    "acc_np": 39,  "acc_pe": 39,  "acc_br": 91,
    "acc_vn": 58,  "acc_af": 40,  "acc_mx": 50,
    "acc_th": 47,  "acc_uz": 108, "acc_gb": 18,
    "acc_cu": 26,  "acc_ye": 20,  "acc_jm": 22,
    "acc_lk": 50,  "acc_my": 20,  "acc_ar": 45,
    "acc_ie": 18,  "acc_tr": 29,  "acc_it": 43,
    "acc_pl": 22,  "acc_sa": 21,  "acc_fj": 24,
    "acc_hk": 34,  "acc_jp": 22,  "acc_at": 28,
    "acc_pt": 39,  "acc_kw": 27,  "acc_am": 25,
    "acc_ee": 14,  "acc_sg": 10,
}

ACCOUNTS_CATALOG = {
    "acc_bd": {"name": "🔥🇧🇩 Бангладеш (+880)", "price": "123.38", "old_price": "154.23", "stars": "200", "discount": 20},
    "acc_us": {"name": "🔥🇺🇸 США (+1)",         "price": "123.38", "old_price": "154.23", "stars": "200", "discount": 20},
    "acc_mr": {"name": "🔥🇲🇷 Мавритания (+222)","price": "319.50", "old_price": "375.75", "stars": "650", "discount": 15},
    "acc_mm": {"name": "🇲🇲 Мьянма (+95)",             "price": "110.25", "stars": "200"},
    "acc_co": {"name": "🇨🇴 Колумбия (+57)",           "price": "117.00", "stars": "200"},
    "acc_in": {"name": "🇮🇳 Индия (+91)",              "price": "119.25", "stars": "200"},
    "acc_ph": {"name": "🇵🇭 Филиппины (+63)",          "price": "128.25", "stars": "200"},
    "acc_ng": {"name": "🇳🇬 Нигерия (+234)",           "price": "130.50", "stars": "200"},
    "acc_id": {"name": "🇮🇩 Индонезия (+62)",          "price": "141.75", "stars": "250"},
    "acc_pk": {"name": "🇵🇰 Пакистан (+92)",           "price": "144.00", "stars": "250"},
    "acc_cl": {"name": "🇨🇱 Чили (+56)",               "price": "177.75", "stars": "300"},
    "acc_ca": {"name": "🇨🇦 Канада (+1)",              "price": "193.50", "stars": "300"},
    "acc_ir": {"name": "🇮🇷 Иран (+98)",               "price": "218.25", "stars": "350"},
    "acc_eg": {"name": "🇪🇬 Египет (+20)",             "price": "222.75", "stars": "350"},
    "acc_mg": {"name": "🇲🇬 Мадагаскар (+261)",        "price": "245.25", "stars": "400"},
    "acc_np": {"name": "🇳🇵 Непал (+977)",             "price": "249.75", "stars": "400"},
    "acc_pe": {"name": "🇵🇪 Перу (+51)",               "price": "258.75", "stars": "450"},
    "acc_br": {"name": "🇧🇷 Бразилия (+55)",           "price": "261.00", "stars": "450"},
    "acc_vn": {"name": "🇻🇳 Вьетнам (+84)",            "price": "270.00", "stars": "450"},
    "acc_af": {"name": "🇦🇫 Афганистан (+93)",         "price": "279.00", "stars": "450"},
    "acc_mx": {"name": "🇲🇽 Мексика (+52)",            "price": "285.75", "stars": "500"},
    "acc_th": {"name": "🇹🇭 Таиланд (+66)",            "price": "297.00", "stars": "500"},
    "acc_uz": {"name": "🇺🇿 Узбекистан (+998)",        "price": "301.50", "stars": "500"},
    "acc_gb": {"name": "🇬🇧 Великобритания (+44)",     "price": "312.75", "stars": "500"},
    "acc_cu": {"name": "🇨🇺 Куба (+53)",               "price": "321.75", "stars": "550"},
    "acc_ye": {"name": "🇾🇪 Йемен (+967)",             "price": "324.00", "stars": "550"},
    "acc_jm": {"name": "🇯🇲 Ямайка (+1)",              "price": "330.75", "stars": "550"},
    "acc_lk": {"name": "🇱🇰 Шри-Ланка (+94)",          "price": "335.25", "stars": "550"},
    "acc_my": {"name": "🇲🇾 Малайзия (+60)",           "price": "348.75", "stars": "600"},
    "acc_ar": {"name": "🇦🇷 Аргентина (+54)",          "price": "357.75", "stars": "600"},
    "acc_ie": {"name": "🇮🇪 Ирландия (+353)",          "price": "384.75", "stars": "650"},
    "acc_tr": {"name": "🇹🇷 Турция (+90)",             "price": "420.75", "stars": "700"},
    "acc_it": {"name": "🇮🇹 Италия (+39)",             "price": "438.75", "stars": "750"},
    "acc_pl": {"name": "🇵🇱 Польша (+48)",             "price": "445.50", "stars": "750"},
    "acc_sa": {"name": "🇸🇦 Саудовская Аравия (+966)", "price": "445.50", "stars": "750"},
    "acc_fj": {"name": "🇫🇯 Фиджи (+679)",             "price": "447.75", "stars": "750"},
    "acc_hk": {"name": "🇭🇰 Гонконг (+852)",           "price": "477.00", "stars": "800"},
    "acc_jp": {"name": "🇯🇵 Япония (+81)",             "price": "479.25", "stars": "800"},
    "acc_at": {"name": "🇦🇹 Австрия (+43)",            "price": "488.25", "stars": "800"},
    "acc_pt": {"name": "🇵🇹 Португалия (+351)",        "price": "488.25", "stars": "800"},
    "acc_kw": {"name": "🇰🇼 Кувейт (+965)",            "price": "497.25", "stars": "850"},
    "acc_am": {"name": "🇦🇲 Армения (+374)",           "price": "542.25", "stars": "900"},
    "acc_ee": {"name": "🇪🇪 Эстония (+372)",           "price": "549.00", "stars": "900"},
    "acc_sg": {"name": "🇸🇬 Сингапур (+65)",           "price": "1930.50", "stars": "3250"},
}

ACCOUNTS_STOCK = dict(ACCOUNTS_BASE_STOCK)

ANONYMOUS_EMAIL_PACKAGES = {
    "email_2_nodes": {
        "name": "📧 Почты в 2 узла",
        "price": "299.99",
        "stars": "300",
        "nodes": 2,
    },
    "email_3_nodes": {
        "name": "📧 Почты в 3 узла",
        "price": "599.99",
        "stars": "600",
        "nodes": 3,
    },
}

# ==================================================
# УТИЛИТЫ
# ==================================================

def format_gift_breakdown(stars):
    try:
        s = int(stars)
    except (TypeError, ValueError):
        return "—"
    if s <= 0:
        return "—"
    crystals = s // 100
    remainder = s % 100
    rockets = remainder // 50
    parts = []
    if crystals:
        parts.append(f"{crystals}× 💎")
    if rockets:
        parts.append(f"{rockets}× 🚀")
    return " + ".join(parts) if parts else "—"


def rub_to_btc(price):
    try:
        rub_value = float(str(price).replace(",", ".").replace("₽", "").strip())
        return f"{rub_value / BTC_RUB_RATE:.8f}"
    except (TypeError, ValueError, ZeroDivisionError):
        return "—"


def rub_to_eth(price):
    try:
        rub_value = float(str(price).replace(",", ".").replace("₽", "").strip())
        return f"{rub_value / ETH_RUB_RATE:.8f}"
    except (TypeError, ValueError, ZeroDivisionError):
        return "—"


def rub_to_stars(price):
    try:
        rub_value = float(str(price).replace(",", ".").replace("₽", "").strip())
        return str(max(1, round(rub_value / STAR_RATE)))
    except (TypeError, ValueError, ZeroDivisionError):
        return "—"


def usd_to_btc(usd):
    try:
        return f"{float(usd) / BTC_USD_RATE:.8f}"
    except (TypeError, ValueError, ZeroDivisionError):
        return "—"


def usd_to_eth(usd):
    try:
        return f"{float(usd) / ETH_USD_RATE:.8f}"
    except (TypeError, ValueError, ZeroDivisionError):
        return "—"


def load_darkweb_users():
    global darkweb_users
    darkweb_users = set()
    try:
        if os.path.exists(DARKWEB_FILE):
            with open(DARKWEB_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and line.lstrip("-").isdigit():
                        darkweb_users.add(int(line))
        print(f"\U0001f578\ufe0f dark.web \u0434\u043e\u0441\u0442\u0443\u043f\u043e\u0432: {len(darkweb_users)}")
    except Exception as e:
        print(f"\u26a0\ufe0f dark.web load: {e}")


def has_darkweb(chat_id):
    return chat_id in darkweb_users


def grant_darkweb(chat_id):
    if chat_id in darkweb_users:
        return False
    darkweb_users.add(chat_id)
    try:
        with open(DARKWEB_FILE, "a", encoding="utf-8") as f:
            f.write(f"{chat_id}\n")
    except Exception as e:
        print(f"\u26a0\ufe0f dark.web save: {e}")
    return True


def load_kraken_users():
    global kraken_users
    kraken_users = set()
    try:
        if os.path.exists(KRAKEN_FILE):
            with open(KRAKEN_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and line.lstrip("-").isdigit():
                        kraken_users.add(int(line))
        print(f"\U0001f419 kraken \u0434\u043e\u0441\u0442\u0443\u043f\u043e\u0432: {len(kraken_users)}")
    except Exception as e:
        print(f"\u26a0\ufe0f kraken load: {e}")


def has_kraken(chat_id):
    return chat_id in kraken_users


def grant_kraken(chat_id):
    if chat_id in kraken_users:
        return False
    kraken_users.add(chat_id)
    try:
        with open(KRAKEN_FILE, "a", encoding="utf-8") as f:
            f.write(f"{chat_id}\n")
    except Exception as e:
        print(f"\u26a0\ufe0f kraken save: {e}")
    return True


def order_amount_text(order):
    payment_method = order.get("payment_method")
    if payment_method == "btc":
        return f"₿ {order.get('btc', '—')} BTC"
    if payment_method == "eth":
        return f"Ξ {order.get('eth', '—')} ETH"
    if payment_method == "stars":
        return f"⭐ {order.get('stars', '—')}⭐"
    return f"₿ {rub_to_btc(order.get('price', '—'))} BTC"


def is_bad_message(text):
    if not text:
        return False
    lower = text.lower()
    return any(w in lower for w in BAD_WORDS)


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
    return bool(last and last.strip().lower() == text.strip().lower())


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
                        user_phones[uid] = parts[1]
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
    else:
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
                            "chat_id": parts[0], "code": parts[1], "item": parts[2],
                            "price": parts[3], "payment": parts[4], "username": parts[5],
                            "phone": parts[6], "name": parts[7], "date": parts[8],
                        })
                    else:
                        sales.append({
                            "chat_id": parts[0], "code": parts[1], "item": parts[2],
                            "price": parts[3], "payment": "RUB", "username": parts[4],
                            "phone": parts[5], "name": parts[6], "date": parts[7],
                        })
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
    return sales


def get_user_purchase_counters(chat_id):
    nb_count = 0
    st_count = 0
    for s in load_all_sales():
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
        for p in item_name.split():
            if p.isdigit():
                return p
        return ""
    except:
        return ""


def make_purchase_code(chat_id, is_stars, item_name):
    nb_count, st_count = get_user_purchase_counters(chat_id)
    if is_stars:
        return f"st{st_count + 1}+{extract_stars_count(item_name) or '?'}"
    return f"nb{nb_count + 1}{extract_phone_index(item_name) or ''}"


def save_sold_log(category, item, price, username, phone, chat_id, name,
                  is_stars=False, payment_method="btc", stars="?", btc="?", eth="?"):
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
            method_label = "TELEGRAM_STARS"
        elif payment_method == "btc":
            price_display = f"{btc} BTC"
            method_label = "BTC"
        elif payment_method == "eth":
            price_display = f"{eth} ETH"
            method_label = "ETH"
        else:
            price_display = f"{price_clean}₽"
            method_label = "LEGACY_RUB"

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
    user_sales = [s for s in load_all_sales() if str(s["chat_id"]) == str(chat_id)]
    if not user_sales:
        return ""
    return "\n".join(f"  <code>{s['code']}</code> {s['date']} — {s['item']} — {s['price']}" for s in user_sales)

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
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML"}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard, ensure_ascii=False)
    return api("editMessageText", data)


def answer_callback(callback_id):
    return api("answerCallbackQuery", {"callback_query_id": callback_id})


def answer_callback_text(callback_id, text, show_alert=False):
    return api("answerCallbackQuery", {
        "callback_query_id": callback_id, "text": text, "show_alert": show_alert
    })


def remove_reply_keyboard(chat_id, text="⬇️ Клавиатура обновлена"):
    return send_message(chat_id, text, {"remove_keyboard": True})

# ==================================================
# КЛАВИАТУРЫ
# ==================================================

def main_keyboard(chat_id=None):
    keyboard = [
        [{"text": "🕶️ Anon Socials 🕶️", "callback_data": "cat:anon_socials"}],
    ]
    if chat_id and has_darkweb(chat_id):
        keyboard.append([{"text": "⚠️ dark.web ⚠️", "callback_data": "darkweb:open"}])
    else:
        keyboard.append([{"text": "⚠️ dark.web ⚠️", "callback_data": "buy_darkweb"}])
    keyboard.append([{"text": "💬 Администрация", "url": ADMIN_LINK}])
    if chat_id and is_admin(chat_id):
        keyboard.append([{"text": "👥 Все пользователи", "callback_data": "admin:users"}])
        keyboard.append([{"text": "🚫 Забаненные", "callback_data": "admin:banned_list"}])
    return {"inline_keyboard": keyboard}


def anon_socials_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "⛓️‍💥 АККАУНТЫ TELEGRAM ⛓️‍💥", "callback_data": "sub:accounts:by_country"}],
            [{"text": "📧 Анонимные почты", "callback_data": "cat:anonymous_emails"}],
            [{"text": "⬅️ В главное меню", "callback_data": "back:main"}]
        ]
    }


def anonymous_emails_keyboard():
    keyboard = []
    for email_id, item in ANONYMOUS_EMAIL_PACKAGES.items():
        btc = rub_to_btc(item["price"])
        eth = rub_to_eth(item["price"])
        stars = item.get("stars", rub_to_stars(item["price"]))
        keyboard.append([{
            "text": f"{item['name']} — {btc} BTC | {eth} ETH | {stars}⭐",
            "callback_data": f"buy_email:{email_id}"
        }])
    keyboard.append([{"text": "💬 Администрация", "url": ADMIN_LINK}])
    keyboard.append([{"text": "⬅️ Назад", "callback_data": "cat:anon_socials"}])
    return {"inline_keyboard": keyboard}


def accounts_by_country_keyboard():
    keyboard = []
    for acc_id, item in ACCOUNTS_CATALOG.items():
        qty = ACCOUNTS_STOCK.get(acc_id, 0)
        price = item.get("price", "?")
        btc = rub_to_btc(price)
        eth = rub_to_eth(price)
        stars = item.get("stars", rub_to_stars(price))
        discount = item.get("discount")

        if discount:
            price_part = f"BTC | ETH | {stars}⭐ 🎁-{discount}%"
        else:
            price_part = f"BTC | ETH | {stars}⭐"

        keyboard.append([{
            "text": f"{item['name']} {price_part} ({qty}шт)",
            "callback_data": f"buy_acc:{acc_id}"
        }])
    keyboard.append([{"text": "💬 Администрация", "url": ADMIN_LINK}])
    keyboard.append([{"text": "⬅️ Назад", "callback_data": "cat:anon_socials"}])
    return {"inline_keyboard": keyboard}


def payment_method_keyboard(order_id, btc, eth, stars, back_callback="back:main"):
    return {
        "inline_keyboard": [
            [{"text": f"₿ Оплатить Bitcoin — {btc} BTC", "callback_data": f"pay_btc:{order_id}"}],
            [{"text": f"Ξ Оплатить Ethereum — {eth} ETH", "callback_data": f"pay_eth:{order_id}"}],
            [{"text": f"⭐ Оплатить звёздами — {stars}⭐", "callback_data": f"pay_stars:{order_id}"}],
            [{"text": "⬅️ Назад", "callback_data": back_callback}]
        ]
    }


def payment_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "✅ Я оплатил", "callback_data": "payment_done"}],
            [{"text": "💬 Связаться с админом", "url": ADMIN_LINK}],
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


def user_profile_keyboard(order_id=None):
    safe_order_id = order_id if order_id else 0
    return {
        "inline_keyboard": [
            [{"text": "⭐ Оставить отзыв", "callback_data": f"feedback:{safe_order_id}"}],
            [{"text": "🛒 Перейти в магазин", "callback_data": "back:main"}],
            [{"text": "💬 Администрация", "url": ADMIN_LINK}]
        ]
    }


def admin_user_actions_keyboard(target_chat_id, is_banned):
    if is_banned:
        return {
            "inline_keyboard": [
                [{"text": "✅ Разблокировать", "callback_data": f"admin:unban:{target_chat_id}"}],
                [{"text": "⬅️ К списку", "callback_data": "admin:users"}]
            ]
        }
    return {
        "inline_keyboard": [
            [{"text": "🚫 Забанить", "callback_data": f"admin:ban:{target_chat_id}"}],
            [{"text": "⬅️ К списку", "callback_data": "admin:users"}]
        ]
    }

# ==================================================
# ТЕКСТЫ
# ==================================================

def darkweb_payment_keyboard(order_id, btc, eth, stars=DARKWEB_PRICE_STARS):
    return {
        "inline_keyboard": [
            [{"text": f"₿ Оплатить Bitcoin — {btc} BTC", "callback_data": f"pay_btc:{order_id}"}],
            [{"text": f"Ξ Оплатить Ethereum — {eth} ETH", "callback_data": f"pay_eth:{order_id}"}],
            [{"text": f"⭐ Оплатить звёздами — {stars}⭐", "callback_data": f"pay_stars:{order_id}"}],
            [{"text": "⬅️ Назад", "callback_data": "back:main"}]
        ]
    }


def darkweb_access_keyboard(chat_id=None):
    keyboard = []
    keyboard.append([{"text": "🐙 Выход в Kraken", "url": CONTACT_URL}])
    keyboard.append([{"text": "🚚 Анон аккаунты для курьера", "url": CONTACT_URL}])
    keyboard.append([{"text": "⬅️ В главное меню", "callback_data": "back:main"}])
    return {"inline_keyboard": keyboard}


def kraken_payment_keyboard(order_id, btc, eth, stars=KRAKEN_PRICE_STARS):
    return {
        "inline_keyboard": [
            [{"text": f"₿ Оплатить Bitcoin — {btc} BTC", "callback_data": f"pay_btc:{order_id}"}],
            [{"text": f"Ξ Оплатить Ethereum — {eth} ETH", "callback_data": f"pay_eth:{order_id}"}],
            [{"text": f"⭐ Оплатить звёздами — {stars}⭐", "callback_data": f"pay_stars:{order_id}"}],
            [{"text": "⬅️ Назад", "callback_data": "darkweb:open"}]
        ]
    }


def kraken_offer_text(btc, eth):
    return (
        "🐙 <b>ВЫХОД В KRAKEN</b>\n\n"
        f"₿ Bitcoin: <b>{btc} BTC</b>\n"
        f"Ξ Ethereum: <b>{eth} ETH</b>\n"
        f"⭐ Звёзды: <b>{KRAKEN_PRICE_STARS}⭐</b>\n\n"
        "🔓 После подтверждения оплаты доступ откроется навсегда.\n\n"
        "👇 Выберите способ оплаты:"
    )


def kraken_access_text():
    return (
        "🐙 <b>KRAKEN — ДОСТУП АКТИВЕН</b>\n\n"
        "✅ Выход в Kraken куплен и закреплён за вами.\n"
        "🛡️ Ссылки и инструкции выдаёт администрация.\n\n"
        "👤 <b>Мой второй аккаунт (для купивших):</b> @dark_exec_me_shop"
    )


def kraken_access_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "📬 Получить доступ у админа", "url": ADMIN_LINK}],
            [{"text": "⬅️ Назад", "callback_data": "darkweb:open"}]
        ]
    }


def courier_accounts_text():
    return (
        "🚶 <b>АНОН АККАУНТЫ ДЛЯ РАБОТЫ КУРЬЕРОМ</b>\n\n"
        "✅ Аккаунты без привязки к вашим данным\n"
        "🔒 Чистые, готовые к работе\n"
        "⚡ Выдача сразу после оплаты\n\n"
        "📬 По наличию и оформлению — пишите администрации."
    )


def courier_accounts_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "💬 Администрация", "url": ADMIN_LINK}],
            [{"text": "⬅️ В главное меню", "callback_data": "back:main"}]
        ]
    }


def darkweb_offer_text(btc, eth):
    return (
        "🕸️ <b>DARK.WEB ДОСТУП</b>\n\n"
        f"₿ Bitcoin: <b>{btc} BTC</b>\n"
        f"Ξ Ethereum: <b>{eth} ETH</b>\n"
        f"⭐ Звёзды: <b>{DARKWEB_PRICE_STARS}⭐</b>\n\n"
        "🔓 После подтверждения оплаты кнопка <b>dark.web</b> навсегда появится в вашем меню.\n\n"
        "👇 Выберите способ оплаты:"
    )


def darkweb_access_text():
    return (
        "🕸️ <b>DARK.WEB — ДОСТУП АКТИВЕН</b>\n\n"
        "\u2800"
    )


def start_text():
    return (
        "👁️‍🗨️ <b>N U M B E R S . E X E</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "\n"
        "you ▸ numbers.exe ▸ tor ▸ .dark.net\n"
        "\n"
        "🔒 <b>оплата:</b> крипта · звёзды"
    )


def anon_socials_text():
    return (
        "🕶️ <b>ANON SOCIALS</b>\n\n"
        "🔒 Анонимные аккаунты и почты для приватного присутствия в сети.\n\n"
        "👇 Выберите категорию:"
    )


def accounts_by_country_text():
    total = sum(ACCOUNTS_STOCK.get(k, 0) for k in ACCOUNTS_CATALOG)
    return (
        "╔══════════════════════════╗\n"
        "║  🌍 <b>АККАУНТЫ TELEGRAM</b>  ║\n"
        "╚══════════════════════════╝\n\n"
        f"📦 В наличии: {total} шт\n"
        f"🌏 Стран: {len(ACCOUNTS_CATALOG)}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🕶️ Качество проверено.\n"
        "✅ Без следов. Без имён.\n"
        "🔥 Зашёл, взял, вышел — и ты чистый.\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 Выбери страну:"
    )


def anonymous_emails_text():
    return (
        "📧 <b>АНОНИМНЫЕ ПОЧТЫ</b>\n\n"
        "🔒 Почтовые ящики созданы для приватной регистрации "
        "на ресурсах и перехода по гиперссылкам, где важна конфиденциальность.\n\n"
        "🛡️ Без публикации ваших личных данных\n"
        "⚡ Быстрая выдача после подтверждения оплаты\n"
        "🌐 Подходят для регистрации на приватных ресурсах, "
        "включая ссылки в сети .onion\n\n"
        "👇 Выберите нужный вариант:"
    )


def anonymous_email_payment_text(item_name, price, nodes, stars=None):
    btc = rub_to_btc(price)
    eth = rub_to_eth(price)
    stars = stars or rub_to_stars(price)
    return (
        "📧 <b>ОФОРМЛЕНИЕ АНОНИМНОЙ ПОЧТЫ</b>\n\n"
        f"📦 Товар: <b>{item_name}</b>\n"
        f"₿ Bitcoin: <b>{btc} BTC</b>\n"
        f"Ξ Ethereum: <b>{eth} ETH</b>\n"
        f"⭐ Telegram Stars: <b>{stars}⭐</b>\n"
        f"🔗 Количество узлов: <b>{nodes}</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "🔒 <b>О КОНФИДЕНЦИАЛЬНОСТИ</b>\n\n"
        "Почта предназначена для приватной регистрации и использования "
        "гиперссылок без указания ваших основных личных данных.\n"
        "Не используйте её для незаконных действий и не передавайте "
        "доступ третьим лицам.\n\n"
        "━━━━━━━━━━━━━━\n"
        "👇 Выберите способ оплаты:"
    )


def payment_choice_text(item_name, price, stars=None):
    btc = rub_to_btc(price)
    eth = rub_to_eth(price)
    calculated_stars = stars or rub_to_stars(price)
    return (
        "💳 <b>ВЫБОР СПОСОБА ОПЛАТЫ</b>\n\n"
        f"📦 Товар: <b>{item_name}</b>\n"
        f"₿ Bitcoin: <b>{btc} BTC</b>\n"
        f"Ξ Ethereum: <b>{eth} ETH</b>\n"
        f"⭐ Telegram Stars: <b>{calculated_stars}⭐</b>\n\n"
        "🔒 Выберите удобный способ оплаты ниже:"
    )


def bitcoin_payment_text(item_name, btc, stars=None):
    stars_line = f"⭐ Альтернатива: <b>{stars}⭐</b>\n" if stars else ""
    return (
        "₿ <b>ОПЛАТА BITCOIN</b>\n\n"
        f"📦 Товар: <b>{item_name}</b>\n"
        f"₿ Сумма: <b>{btc} BTC</b>\n"
        f"{stars_line}\n"
        "━━━━━━━━━━━━━━\n"
        "📍 <b>Bitcoin-кошелёк для оплаты:</b>\n"
        f"<code>{BTC_WALLET}</code>\n\n"
        "━━━━━━━━━━━━━━\n"
        "📌 <b>ИНСТРУКЦИЯ:</b>\n"
        "1️⃣ Отправьте точную сумму BTC на указанный кошелёк\n"
        "2️⃣ Нажмите «✅ Я оплатил» ниже\n"
        "3️⃣ Дождитесь подтверждения — откроется чат с админом\n"
        "4️⃣ Получите <b>товар</b> в течение 5-15 минут\n\n"
        "💬 По всем вопросам — к администрации!"
    )


def ethereum_payment_text(item_name, eth, stars=None, btc=None):
    alternatives = []
    if btc:
        alternatives.append(f"₿ Bitcoin: <b>{btc} BTC</b>")
    if stars:
        alternatives.append(f"⭐ Telegram Stars: <b>{stars}⭐</b>")
    alternatives_text = "\n".join(alternatives)
    return (
        "Ξ <b>ОПЛАТА ETHEREUM</b>\n\n"
        f"📦 Товар: <b>{item_name}</b>\n"
        f"Ξ Сумма: <b>{eth} ETH</b>\n"
        f"{alternatives_text}\n\n"
        "━━━━━━━━━━━━━━\n"
        f"🌐 <b>Сеть:</b> {ETH_NETWORK}\n"
        "📍 <b>Ethereum-кошелёк для оплаты:</b>\n"
        f"<code>{ETH_WALLET}</code>\n\n"
        "━━━━━━━━━━━━━━\n"
        "📌 <b>ИНСТРУКЦИЯ:</b>\n"
        f"1️⃣ Отправьте точную сумму ETH в сети {ETH_NETWORK}\n"
        "2️⃣ Нажмите «✅ Я оплатил» ниже\n"
        "3️⃣ Дождитесь подтверждения администратора\n"
        "4️⃣ Получите <b>товар</b> в течение 5-15 минут\n\n"
        "⚠️ Не отправляйте ETH через другую сеть.\n\n"
        "💬 По всем вопросам — к администрации!"
    )


def payment_stars_only_text(item_name, stars):
    try:
        stars_int = int(stars)
    except (TypeError, ValueError):
        stars_int = 0

    breakdown = format_gift_breakdown(stars_int)

    nft_block = ""
    strict_warning = ""
    if stars_int >= 500:
        nft_block = (
            "🎁 <b>ИЛИ оплата NFT-подарком (Resale/Upgraded)</b>\n\n"
            "⚠️ <b>NFT-подарки принимаются только для сумм от 500⭐</b>\n\n"
        )
    else:
        strict_warning = (
            "⚠️ <b>Админ принимает ТОЛЬКО эти подарки!</b>\n"
            "❌ Если вы отправите другой подарок — номер <b>НЕ будет выдан</b>.\n"
            "🔒 Отправляйте ровно 🚀 Ракету или 💎 Кристалл.\n\n"
        )

    return (
        "⭐ <b>ОПЛАТА ЗВЁЗДАМИ TELEGRAM</b>\n\n"
        f"📦 Товар: <b>{item_name}</b>\n"
        f"⭐ Сумма: <b>{stars}⭐</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "📌 <b>СПОСОБЫ ОПЛАТЫ:</b>\n\n"
        "🚀 <b>Ракета</b> — 50⭐\n"
        "💎 <b>Кристалл</b> — 100⭐\n\n"
        f"{nft_block}"
        f"{strict_warning}"
        "━━━━━━━━━━━━━━\n"
        f"🎁 <b>Для этой суммы нужно отправить:</b>\n"
        f"   <b>{breakdown}</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "📌 <b>ИНСТРУКЦИЯ:</b>\n"
        "1️⃣ Откройте чат с администратором:\n"
        f"   👤 {ADMIN_LINK}\n"
        "2️⃣ Нажмите 📎 → «Подарок» (Gift)\n"
        "3️⃣ Выберите 🚀 Ракету или 💎 Кристалл\n"
        f"4️⃣ Отправьте нужное количество, чтобы вышло <b>{stars}⭐</b>\n"
        "5️⃣ Нажмите «✅ Я оплатил» под сообщением\n"
        "6️⃣ Дождитесь подтверждения — откроется чат с админом\n"
        "7️⃣ Получите <b>товар</b> в течение 5-15 минут\n\n"
        "━━━━━━━━━━━━━━\n"
        f"⭐ <b>Сумма:</b> <b>{stars}⭐</b>\n"
        f"🎁 <b>Раскладка:</b> {breakdown}\n"
        f"👤 <b>Получатель:</b> {ADMIN_LINK}\n\n"
        "⏳ <b>ОБРАБОТКА ЗАКАЗА:</b>\n"
        "Ответ администратора может занять до 24 часов.\n\n"
        "💬 По всем вопросам — к администрации!"
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
                    "❤️ <b>СПАСИБО ЗА ОТЗЫВ!</b>\n\nПриходите ещё! 🛒",
                    {"inline_keyboard": [[{"text": "⬅️ В главное меню", "callback_data": "back:main"}]]}
                )
                order_data["awaiting_feedback"] = False
                if chat_id in orders:
                    del orders[chat_id]
                return True

    if chat_id in chat_mode:
        order_id = chat_mode[chat_id]
        if text == "/stop":
            del chat_mode[chat_id]
            send_message(chat_id, f"✅ <b>Режим чата выключен</b>\n\n📦 Заказ #{order_id}",
                         admin_order_keyboard(order_id))
            if order_id in temp_data:
                user_chat_id = temp_data[order_id]["chat_id"]
                send_message(user_chat_id, f"📴 <b>ЧАТ С АДМИНОМ ЗАКРЫТ</b>\n\n📦 Заказ #{order_id}", None)
            return True

        if order_id in temp_data:
            user_chat_id = temp_data[order_id]["chat_id"]
            send_message(user_chat_id,
                         f"💬 <b>СООБЩЕНИЕ ОТ АДМИНИСТРАТОРА</b>\n\n📦 Заказ #{order_id}\n\n{text}", None)
            send_message(chat_id,
                         f"✅ Отправлено покупателю заказа #{order_id}\n\n<i>Чтобы выйти — /stop</i>", None)
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

        if "video" in message:
            print(f"🎬 VIDEO FILE_ID: {message['video'].get('file_id')}")
            print(f"🎬 VIDEO UNIQUE: {message['video'].get('file_unique_id')}")
            return

        if chat_id not in ADMIN_IDS and text and not text.startswith("/start"):
            if chat_id in banned_users:
                return

            awaiting_fb = any(
                o.get("chat_id") == chat_id and o.get("awaiting_feedback")
                for o in temp_data.values()
            )
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
                    extra = f"За {SPAM_WINDOW} сек: {get_spam_count(chat_id)} сообщений (лимит {SPAM_LIMIT})"
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
                        f"💬 <b>СООБЩЕНИЕ ОТ ПОКУПАТЕЛЯ</b>\n\n📦 Заказ #{oid}\n👤 {o.get('username', '-')}\n\n{text}",
                        None
                    )
                    send_message(chat_id,
                                 "✅ <b>Сообщение доставлено администратору</b>\n\n⏳ Ожидайте ответа...", None)
                    return

        if text.strip() == "/start":
            print(f"📩 /start от {chat_id}")

            if chat_id in banned_users:
                send_message(chat_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\nДоступ к боту закрыт.", None)
                return

            user_obj = message.get("from", {})
            user_username = user_obj.get("username", "").lower()
            if user_username == ADMIN_USERNAME_TARGET and chat_id not in ADMIN_IDS:
                save_admin(chat_id)
                send_message(chat_id, "👑 <b>Вы добавлены как администратор!</b>", None)

            if chat_id not in user_verified:
                user_verified[chat_id] = True
                first_name = user_obj.get("first_name", "")
                last_name = user_obj.get("last_name", "")
                user_first_names[chat_id] = f"{first_name} {last_name}".strip() or "Пользователь"
                user_usernames[chat_id] = user_obj.get("username", "")
                user_phones[chat_id] = "-"
                save_verified_user(
                    chat_id, "-",
                    user_obj.get("username", ""),
                    first_name, last_name
                )

            send_message(chat_id, start_text(), main_keyboard(chat_id))
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
        answer_callback_text(callback_id, "🚫 Вы забанены.", show_alert=True)
        return

    if data == "back:main":
        answer_callback(callback_id)
        edit_message(chat_id, message_id, start_text(), main_keyboard(chat_id))
        return

    if data.startswith("cat:"):
        cat_id = data.split(":", 1)[1]
        if cat_id == "anon_socials":
            answer_callback(callback_id)
            edit_message(
                chat_id,
                message_id,
                anon_socials_text(),
                anon_socials_keyboard()
            )
        elif cat_id == "anonymous_emails":
            answer_callback(callback_id)
            edit_message(
                chat_id,
                message_id,
                anonymous_emails_text(),
                anonymous_emails_keyboard()
            )
        return

    if data.startswith("sub:"):
        parts = data.split(":")
        if len(parts) >= 3 and parts[1] == "accounts" and parts[2] == "by_country":
            answer_callback(callback_id)
            edit_message(chat_id, message_id, accounts_by_country_text(), accounts_by_country_keyboard())
        return

    if data == "darkweb:open":
        if not has_darkweb(chat_id):
            answer_callback_text(callback_id, "🔒 Доступ не куплен", show_alert=True)
            return
        answer_callback(callback_id)
        edit_message(chat_id, message_id, darkweb_access_text(), darkweb_access_keyboard(chat_id))
        return

    if data == "cat:courier":
        answer_callback(callback_id)
        edit_message(chat_id, message_id, courier_accounts_text(), courier_accounts_keyboard())
        return

    if data == "kraken:open":
        if not has_kraken(chat_id):
            answer_callback_text(callback_id, "🔒 Доступ не куплен", show_alert=True)
            return
        answer_callback(callback_id)
        edit_message(chat_id, message_id, kraken_access_text(), kraken_access_keyboard())
        return

    if data == "buy_kraken":
        if not has_darkweb(chat_id):
            answer_callback_text(callback_id, "🔒 Сначала dark.web", show_alert=True)
            return
        if has_kraken(chat_id):
            answer_callback(callback_id)
            edit_message(chat_id, message_id, kraken_access_text(), kraken_access_keyboard())
            return
        answer_callback(callback_id)
        order_counter += 1
        btc = rub_to_btc(KRAKEN_PRICE_RUB)
        eth = rub_to_eth(KRAKEN_PRICE_RUB)
        orders[chat_id] = {
            "order_id": order_counter,
            "item_id": "kraken",
            "item": "🐙 Выход в Kraken",
            "price": str(KRAKEN_PRICE_RUB),
            "btc": btc,
            "eth": eth,
            "stars": str(KRAKEN_PRICE_STARS),
            "status": "waiting_payment",
        }
        edit_message(
            chat_id, message_id,
            kraken_offer_text(btc, eth),
            kraken_payment_keyboard(order_counter, btc, eth)
        )
        return

    if data == "buy_darkweb":
        if has_darkweb(chat_id):
            answer_callback(callback_id)
            edit_message(chat_id, message_id, darkweb_access_text(), darkweb_access_keyboard(chat_id))
            return
        answer_callback(callback_id)
        order_counter += 1
        btc = usd_to_btc(DARKWEB_PRICE_USD)
        eth = usd_to_eth(DARKWEB_PRICE_USD)
        orders[chat_id] = {
            "order_id": order_counter,
            "item_id": "darkweb",
            "item": "🕸️ dark.web доступ",
            "price": str(DARKWEB_PRICE_USD),
            "btc": btc,
            "eth": eth,
            "stars": str(DARKWEB_PRICE_STARS),
            "status": "waiting_payment",
        }
        edit_message(
            chat_id, message_id,
            darkweb_offer_text(btc, eth),
            darkweb_payment_keyboard(order_counter, btc, eth)
        )
        return

    if data.startswith("buy_email:"):
        email_id = data.split(":", 1)[1]
        item = ANONYMOUS_EMAIL_PACKAGES.get(email_id)
        if not item:
            answer_callback_text(callback_id, "❌ Товар не найден", show_alert=True)
            return

        answer_callback(callback_id)
        order_counter += 1
        orders[chat_id] = {
            "order_id": order_counter,
            "item_id": email_id,
            "item": item["name"],
            "price": item["price"],
            "nodes": item["nodes"],
            "stars": item.get("stars", rub_to_stars(item["price"])),
            "status": "waiting_payment",
        }
        edit_message(
            chat_id,
            message_id,
            anonymous_email_payment_text(
                item["name"], item["price"], item["nodes"], item.get("stars")
            ),
            payment_method_keyboard(
                order_counter,
                rub_to_btc(item["price"]),
                rub_to_eth(item["price"]),
                item.get("stars", rub_to_stars(item["price"])),
                "cat:anonymous_emails"
            )
        )
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
        calculated_stars = item.get("stars", rub_to_stars(item["price"]))
        orders[chat_id] = {
            "order_id": order_counter, "item_id": acc_id, "item": item["name"],
            "price": item["price"], "stars": calculated_stars, "status": "waiting_payment"
        }

        edit_message(
            chat_id, message_id,
            payment_choice_text(item["name"], item["price"], calculated_stars),
            payment_method_keyboard(
                order_counter,
                rub_to_btc(item["price"]),
                rub_to_eth(item["price"]),
                calculated_stars,
                "sub:accounts:by_country"
            )
        )
        return

    if data.startswith("pay_btc:"):
        order_id = int(data.split(":")[1])
        answer_callback(callback_id)
        if chat_id not in orders or orders[chat_id].get("order_id") != order_id:
            edit_message(chat_id, message_id, "❌ <b>Заказ не найден.</b>", main_keyboard(chat_id))
            return
        order = orders[chat_id]
        order["payment_method"] = "btc"
        order["btc"] = order.get("btc") or rub_to_btc(order["price"])
        edit_message(
            chat_id,
            message_id,
            bitcoin_payment_text(order["item"], order["btc"], order.get("stars")),
            payment_keyboard()
        )
        return

    if data.startswith("pay_eth:"):
        order_id = int(data.split(":")[1])
        answer_callback(callback_id)
        if chat_id not in orders or orders[chat_id].get("order_id") != order_id:
            edit_message(chat_id, message_id, "❌ <b>Заказ не найден.</b>", main_keyboard(chat_id))
            return
        order = orders[chat_id]
        order["payment_method"] = "eth"
        order["eth"] = order.get("eth") or rub_to_eth(order["price"])
        edit_message(
            chat_id,
            message_id,
            ethereum_payment_text(
                order["item"],
                order["eth"],
                order.get("stars"),
                order.get("btc", rub_to_btc(order["price"]))
            ),
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
            chat_id,
            message_id,
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
            "chat_id": chat_id, "item_id": order.get("item_id"), "item": order["item"],
            "price": order["price"], "btc": order.get("btc", rub_to_btc(order["price"])),
            "eth": order.get("eth", rub_to_eth(order["price"])),
            "stars": order.get("stars", rub_to_stars(order["price"])), "username": user_info,
            "phone": user_phones.get(chat_id, "Не указан"),
            "payment_method": order.get("payment_method", "btc")
        }
        save_order_log(order_id, chat_id, user_info, order["item"], order["price"], "waiting_admin")

        method_block = f"💳 <b>Оплата:</b> {order_amount_text(order)}"

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

        edit_message(
            chat_id, message_id,
            f"📩 <b>ЗАЯВКА ОТПРАВЛЕНА</b>\n\n"
            f"🆔 <b>Заказ:</b> #{order_id}\n"
            f"📦 <b>Товар:</b> {order['item']}\n"
            f"💰 <b>Сумма:</b> {order_amount_text(order)}\n\n"
            f"⏳ Ожидайте подтверждения администратора (5-15 минут).",
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
        send_message(user_chat_id,
                     f"✅ <b>ЗАКАЗ #{order_id} ПОДТВЕРЖДЁН!</b>\n\n"
                     f"📦 {order['item']}\n💰 {order_amount_text(order)}", None)
        edit_message(
            chat_id, message_id,
            f"✅ <b>ЗАКАЗ #{order_id} ПОДТВЕРЖДЁН</b>\n\n"
            f"👤 {order.get('username', '-')}\n"
            f"📱 <code>{order.get('phone', '-')}</code>\n"
            f"📦 {order['item']}\n\n"
            f"👇 Выберите действие:",
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
            f"💬 <b>ЧАТ С ПОКУПАТЕЛЕМ</b>\n\n"
            f"🆔 Заказ #{order_id}\n"
            f"👤 {order.get('username', '-')}\n"
            f"📦 {order['item']}\n\n"
            f"⚠️ Чтобы выйти — /stop",
            admin_chat_keyboard(order_id)
        )
        send_message(user_chat_id,
                     f"💬 <b>АДМИНИСТРАТОР ОТКРЫЛ ЧАТ</b>\n\n📦 Заказ #{order_id} — {order['item']}\n\nПишите сообщение — админ ответит.",
                     None)
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
            real_item = order.get("item", "—")
        elif item_id.startswith("email_"):
            real_item = ANONYMOUS_EMAIL_PACKAGES.get(item_id, {}).get("name", order.get("item", "—"))
        elif item_id == "darkweb":
            real_item = "🕸️ dark.web доступ"
        elif item_id == "kraken":
            real_item = "🐙 Выход в Kraken"
        else:
            real_item = order.get("item", "—")
        order["item"] = real_item

        if item_id.startswith("acc_") and item_id in ACCOUNTS_STOCK:
            decrease_stock(item_id, 1)

        save_order_log(order_id, user_chat_id, order.get("username", "-"), real_item, order["price"], "sent")

        buyer_username = user_usernames.get(user_chat_id, "") or "-"
        buyer_phone = user_phones.get(user_chat_id, "-")
        buyer_name = user_first_names.get(user_chat_id, "-")
        is_stars = item_id.startswith("stars_")

        save_sold_log(
            category=(
                "Аккаунт" if item_id.startswith("acc_")
                else ("Звёзды" if is_stars
                      else ("Анонимная почта" if item_id.startswith("email_")
                            else ("dark.web" if item_id == "darkweb" else ("Kraken" if item_id == "kraken" else "Другое"))))
            ),
            item=real_item, price=order["price"], username=buyer_username,
            phone=buyer_phone, chat_id=user_chat_id, name=buyer_name,
            is_stars=is_stars, payment_method=order.get("payment_method", "btc"),
            stars=order.get("stars", "?"),
            btc=order.get("btc", rub_to_btc(order["price"])),
            eth=order.get("eth", rub_to_eth(order["price"]))
        )

        if item_id == "kraken":
            grant_kraken(user_chat_id)
            send_message(
                user_chat_id,
                "🐙 <b>Выход в Kraken открыт!</b>\n\n"
                "Кнопка <b>Выход в Kraken</b> теперь доступна в разделе dark.web.",
                darkweb_access_keyboard(user_chat_id)
            )

        if item_id == "darkweb":
            grant_darkweb(user_chat_id)
            send_message(
                user_chat_id,
                "🕸️ <b>Доступ dark.web открыт!</b>\n\n"
                "Кнопка <b>dark.web</b> теперь в вашем меню.",
                main_keyboard(user_chat_id)
            )

        temp_data[order_id]["finished"] = True

        for admin_id in list(chat_mode.keys()):
            if chat_mode[admin_id] == order_id:
                del chat_mode[admin_id]

        answer_callback(callback_id)
        send_message(user_chat_id,
                     f"🎉 <b>ЗАКАЗ #{order_id} ЗАВЕРШЁН</b>\n\n📦 {real_item}\n\n✅ Подтвердите получение:",
                     user_confirm_keyboard(order_id))
        edit_message(chat_id, message_id,
                     f"✅ <b>ЗАКАЗ #{order_id} ЗАВЕРШЁН</b>\n\n"
                     f"📦 {real_item}\n💰 {order_amount_text(order)}", None)
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
        answer_callback(callback_id)
        edit_message(
            chat_id, message_id,
            f"⚠️ <b>ПОДТВЕРДИТЕ БАН</b>\n\n"
            f"🆔 ID: <code>{user_chat_id}</code>\n"
            f"📦 Заказ #{order_id}\n\n"
            f"⚠️ Действие необратимо!",
            ban_confirm_keyboard(user_chat_id, order_id)
        )
        return

    if data.startswith("ban_confirm:"):
        parts = data.split(":")
        target_id = int(parts[1])
        order_id = int(parts[2])
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        ban_user(target_id)
        if order_id in temp_data:
            del temp_data[order_id]
        if target_id in orders:
            del orders[target_id]
        if order_id in pending_orders:
            del pending_orders[order_id]
        for admin_id in list(chat_mode.keys()):
            if chat_mode[admin_id] == order_id:
                del chat_mode[admin_id]
        send_message(target_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>\n\nДоступ закрыт, заказ аннулирован.", None)
        answer_callback_text(callback_id, "✅ Пользователь забанен", show_alert=True)
        edit_message(chat_id, message_id, f"✅ <b>ПОЛЬЗОВАТЕЛЬ ЗАБАНЕН</b>\n\n🆔 <code>{target_id}</code>", None)
        return

    if data.startswith("ban_cancel:"):
        parts = data.split(":")
        order_id = int(parts[2])
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        answer_callback_text(callback_id, "❌ Бан отменён", show_alert=True)
        edit_message(chat_id, message_id, f"❌ <b>Бан отменён</b>\n\n📦 Заказ #{order_id}",
                     admin_order_keyboard(order_id))
        return

    if data.startswith("warn_ban:"):
        target_id = int(data.split(":")[1])
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        ban_user(target_id)
        for oid, o in list(temp_data.items()):
            if o.get("chat_id") == target_id:
                del temp_data[oid]
        if target_id in orders:
            del orders[target_id]
        for oid in list(pending_orders.keys()):
            if pending_orders[oid].get("chat_id") == target_id:
                del pending_orders[oid]
        send_message(target_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>", None)
        answer_callback_text(callback_id, "🚫 Пользователь забанен", show_alert=True)
        edit_message(chat_id, message_id, f"✅ <b>ПОЛЬЗОВАТЕЛЬ ЗАБАНЕН</b>\n\n🆔 <code>{target_id}</code>", None)
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
        edit_message(chat_id, message_id, f"❌ <b>Нарушение проигнорировано</b>\n\n🆔 <code>{target_id}</code>", None)
        return

    if data.startswith("user_confirm:"):
        order_id = int(data.split(":")[1])
        answer_callback(callback_id)
        if order_id not in temp_data:
            temp_data[order_id] = {
                "chat_id": chat_id, "item": "—", "price": "—",
                "username": user_usernames.get(chat_id, "-"), "finished": True
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
        send_message(ADMIN_ID, f"✅ <b>ПОКУПАТЕЛЬ ПОДТВЕРДИЛ ПОЛУЧЕНИЕ</b>\n\nЗаказ #{order_id}\n📦 {order['item']}", None)

        profile_text = (
            f"✅ <b>ПОКУПКА ЗАВЕРШЕНА!</b>\n\n"
            f"🎉 Спасибо за покупку! ❤️\n\n"
            f"👤 <b>ВАШ ПРОФИЛЬ</b>\n\n"
            f"📛 {user_first_names.get(chat_id, 'Пользователь')}\n"
            f"🆔 <code>{chat_id}</code>\n"
            f"📱 <code>{user_phones.get(chat_id, '-')}</code>\n\n"
            f"👑 Статус: {status_line}\n"
            f"📦 Покупок: <b>{total_purchases}</b> (номера: {nb_count}, звёзды: {st_count})\n"
        )
        if history:
            profile_text += f"\n📜 <b>ИСТОРИЯ:</b>\n{history}\n"
        profile_text += "\n👇 Выберите действие:"

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
                    "chat_id": chat_id, "item": "—", "price": "—",
                    "username": user_usernames.get(chat_id, "-"), "finished": True
                }
        temp_data[order_id]["awaiting_feedback"] = True
        temp_data[order_id]["feedback_order_id"] = order_id
        temp_data[order_id]["chat_id"] = chat_id
        edit_message(chat_id, message_id,
                     "✍️ <b>НАПИШИТЕ ВАШ ОТЗЫВ</b>\n\nПросто напишите сообщение — оно уйдёт администратору.", None)
        return

    if data == "admin:users":
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        answer_callback(callback_id)
        users = get_all_users_data()
        if not users:
            edit_message(chat_id, message_id, "👥 Список пуст.",
                         {"inline_keyboard": [[{"text": "⬅️ Назад", "callback_data": "back:main"}]]})
            return
        text = f"👥 <b>ПОЛЬЗОВАТЕЛИ ({len(users)})</b>\n\n"
        keyboard = []
        for idx, u in enumerate(users, 1):
            ban_mark = "🚫" if u["banned"] else "✅"
            text += f"{ban_mark} <b>#{idx} {u['name']}</b>\n🆔 <code>{u['chat_id']}</code>\n📱 <code>{u['phone']}</code>\n\n"
            keyboard.append([{"text": f"{ban_mark} #{idx} {u['name'][:18]}",
                              "callback_data": f"admin:view:{u['chat_id']}"}])
        keyboard.append([{"text": "⬅️ Назад", "callback_data": "back:main"}])
        if len(text) > 4000:
            text = text[:3900] + "\n\n<i>… обрезано</i>"
        edit_message(chat_id, message_id, text, {"inline_keyboard": keyboard})
        return

    if data == "admin:banned_list":
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        answer_callback(callback_id)
        banned = [u for u in get_all_users_data() if u["banned"]]
        if not banned:
            edit_message(chat_id, message_id, "🚫 Список пуст.",
                         {"inline_keyboard": [[{"text": "⬅️ Назад", "callback_data": "back:main"}]]})
            return
        text = f"🚫 <b>ЗАБАНЕННЫЕ ({len(banned)})</b>\n\n"
        keyboard = []
        for idx, u in enumerate(banned, 1):
            text += f"🚫 <b>#{idx} {u['name']}</b>\n🆔 <code>{u['chat_id']}</code>\n\n"
            keyboard.append([{"text": f"🚫 #{idx} {u['name'][:20]}",
                              "callback_data": f"admin:view:{u['chat_id']}"}])
        keyboard.append([{"text": "⬅️ Назад", "callback_data": "back:main"}])
        edit_message(chat_id, message_id, text, {"inline_keyboard": keyboard})
        return

    if data.startswith("admin:view:"):
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        target_id = int(data.split(":")[2])
        answer_callback(callback_id)
        target = next((u for u in get_all_users_data() if u["chat_id"] == target_id), None)
        if not target:
            edit_message(chat_id, message_id, "❌ Не найден",
                         {"inline_keyboard": [[{"text": "⬅️ К списку", "callback_data": "admin:users"}]]})
            return
        uname = f"@{target['username']}" if target["username"] and target["username"] != "-" else "—"
        ban_status = "🚫 <b>ЗАБАНЕН</b>" if target["banned"] else "✅ <b>Активен</b>"
        nb_count, st_count = get_user_purchase_counters(target_id)
        text = (
            f"👤 <b>КАРТОЧКА</b>\n\n"
            f"📛 {target['name']}\n"
            f"🆔 <code>{target['chat_id']}</code>\n"
            f"📱 <code>{target['phone']}</code>\n"
            f"🔗 {uname}\n"
            f"📅 {target['date']}\n"
            f"📦 Покупок: {nb_count + st_count}\n"
            f"🔐 Бан: {ban_status}"
        )
        edit_message(chat_id, message_id, text, admin_user_actions_keyboard(target_id, target["banned"]))
        return

    if data.startswith("admin:ban:"):
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        target_id = int(data.split(":")[2])
        ban_user(target_id)
        answer_callback_text(callback_id, "🚫 Забанен", show_alert=True)
        send_message(target_id, "🚫 <b>ВЫ ЗАБАНЕНЫ</b>", None)
        return

    if data.startswith("admin:unban:"):
        if not is_admin(chat_id):
            answer_callback_text(callback_id, "❌ Только для админа", show_alert=True)
            return
        target_id = int(data.split(":")[2])
        unban_user(target_id)
        answer_callback_text(callback_id, "✅ Разблокирован", show_alert=True)
        send_message(target_id, "✅ <b>ВЫ РАЗБЛОКИРОВАНЫ</b>\n\nНапишите /start", None)
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
    load_darkweb_users()
    load_kraken_users()
    load_stock()
    load_banned_users()

    print("🔄 Очистка webhook...", end=" ", flush=True)
    api("deleteWebhook", {"drop_pending_updates": True})
    print("✅")

    print("🔄 Проверка Telegram...", end=" ", flush=True)
    result = api("getMe")
    if result and result.get("ok"):
        print(f"✅ @{result['result'].get('username', 'unknown')}")
    else:
        print("❌ Ошибка")
        time.sleep(3)
        main()
        return

    print("🟢 БОТ ЗАПУЩЕН")
    print("⏳ Ожидание сообщений...\n")

    offset = 0
    last_status = time.time()

    while True:
        try:
            if time.time() - last_status >= 30:
                print(f"💓 {time.strftime('%H:%M:%S')} | 👥 {len(user_verified)} | 🚫 {len(banned_users)} | 📦 {len(pending_orders)}")
                last_status = time.time()

            result = api("getUpdates", {
                "offset": offset,
                "timeout": POLL_TIMEOUT,
                "limit": 100,
                "allowed_updates": json.dumps(["message", "callback_query"])
            })

            if not result or not result.get("ok"):
                time.sleep(RECONNECT_DELAY)
                continue

            for update in result.get("result", []):
                update_id = update.get("update_id")
                if update_id is not None:
                    offset = update_id + 1
                try:
                    msg = update.get("message")
                    if msg and "text" in msg and handle_admin_message(msg):
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
