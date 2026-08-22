import os
import requests
from datetime import datetime, date
from zoneinfo import ZoneInfo
from cnlunar import Lunar

# ========== 全部配置读取自环境变量，公开仓库无硬编码隐私 ==========
# 环境变量说明：
# BARK_KEY       : Bark推送密钥
# BARK_HOST      : Bark接口域名，默认 https://api.day.app
# WEATHER_LAT    : 城市纬度，示例北京：39.9042
# WEATHER_LON    : 城市经度，示例北京：116.4074
# BIRTH_MONTH    : 生日月份，示例 7
# BIRTH_DAY      : 生日日期，示例 10

BARK_KEY = os.getenv("BARK_KEY", "")
BARK_HOST = os.getenv("BARK_HOST", "https://api.day.app")
LAT = float(os.getenv("WEATHER_LAT", "39.9042"))
LON = float(os.getenv("WEATHER_LON", "116.4074"))
BIRTH_MONTH = int(os.getenv("BIRTH_MONTH", "7"))
BIRTH_DAY = int(os.getenv("BIRTH_DAY", "10"))


# 文言词汇替换
replace_dict = {
    "剃头": "理发",
    "嫁娶": "办婚礼",
    "结婚姻": "订婚结婚",
    "纳采": "提亲订婚",
    "移徙": "搬家",
    "修造": "装修房屋",
    "冠带": "成人礼",
    "修置产室": "修缮房产",
    "开渠": "挖水沟",
    "开光": "神像仪式",
    "安香": "安放神位上香",
    "出火": "挪动神位香火",
    "求嗣": "求子女",
    "解除": "扫除化解不顺",
    "伐木": "砍树",
    "立券": "签合同",
    "纳财": "收账进财",
    "纳畜": "养宠物",
    "开市": "店铺开业",
    "入宅": "搬入新家",
    "栽种": "种花种树",
    "整手足甲": "修剪指甲",
    "畋猎": "打猎",
    "启攒": "捡骨迁葬",
    "订盟": "订立婚约"
}

explain_map = {
    "成人礼": "古代成年仪式",
    "修缮房产": "维修房子",
    "挖水沟": "开挖排水渠道",
    "神像仪式": "神像开光仪式",
    "安放神位上香": "安置神位烧香",
    "挪动神位香火": "移动家里供奉神像",
    "签合同": "签订契约合约",
    "捡骨迁葬": "迁坟捡骨",
    "订立婚约": "签订订婚约定"
}

keep_words = {
    "剃头","嫁娶","结婚姻","纳采","移徙","修造","冠带","修置产室",
    "开渠","求嗣","解除","伐木","立券","纳财","纳畜","开市","入宅",
    "栽种","整手足甲","畋猎","订盟","出行","宴会","理发"
}


def replace_old_word(word: str):
    if word in replace_dict:
        return replace_dict[word]
    return word


def get_birthday_countdown():
    today = date.today()
    this_year_birth = date(today.year, BIRTH_MONTH, BIRTH_DAY)
    if this_year_birth >= today:
        diff = (this_year_birth - today).days
    else:
        next_year_birth = date(today.year + 1, BIRTH_MONTH, BIRTH_DAY)
        diff = (next_year_birth - today).days
    return f"🎂距离生日还有 {diff} 天"


def get_wind_tip(speed):
    if speed < 5:
        return f"🍃微风 {speed}km/h"
    elif speed < 12:
        return f"💨和风 {speed}km/h"
    elif speed < 20:
        return f"🌬️有风 {speed}km/h 出行留意"
    else:
        return f"🌪️大风 {speed}km/h"


def get_uv_tip(uv):
    if uv < 3:
        return f"☀UV{uv:.1f}｜防晒需求低"
    elif uv <= 5:
        return f"☀UV{uv:.1f}｜建议涂防晒"
    else:
        return f"☀UV{uv:.1f}｜务必做好防晒"


def format_item(word):
    new_w = replace_old_word(word)
    if new_w in explain_map:
        return f"· {new_w}（{explain_map[new_w]}）"
    return f"· {new_w}"


def get_lunar_calendar():
    try:
        now = datetime.now(tz=ZoneInfo("Asia/Shanghai")).replace(tzinfo=None)
        lu = Lunar(now)
        lunar_str = f"{lu.lunarYearCn}{lu.lunarMonthCn}{lu.lunarDayCn}"

        raw_yi = lu.goodThing if hasattr(lu, "goodThing") and lu.goodThing else []
        raw_ji = lu.badThing if hasattr(lu, "badThing") and lu.badThing else []

        yi_list = [x for x in raw_yi if x in keep_words]
        ji_list = [x for x in raw_ji if x in keep_words]

        yi_lines = [format_item(i) for i in yi_list]
        ji_lines = [format_item(i) for i in ji_list]

        yi_out = "\n".join(yi_lines) if yi_lines else "· 无适宜事项"
        ji_out = "\n".join(ji_lines) if ji_lines else "· 无禁忌事项"

        out = f"📜 {lunar_str}\n"
        out += "——————————————————\n"
        out += "✅ 今日宜：\n"
        out += f"{yi_out}\n"
        out += "——————————————————\n"
        out += "❌ 今日忌：\n"
        out += f"{ji_out}\n"

        chong_raw = getattr(lu, "chineseZodiacClash", "")
        if chong_raw:
            out += f"\n⚔ {chong_raw}（民俗：该属相多留意）"

        peng_raw = getattr(lu, "pengZuJi", "")
        if peng_raw:
            out += f"\n⚠ {peng_raw}（仅供娱乐）"
        return out
    except Exception as e:
        print("黄历异常详情：", repr(e))
        return "📜黄历读取异常"


def fetch_weather():
    url = (
        f"https://api.open‑meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}&timezone=Asia/Shanghai&"
        f"hourly=temperature_2m,precipitation_probability,wind_speed_10m,uv_index&"
        f"daily=sunrise,sunset&forecast_days=1"
    )
    try:
        resp = requests.get(url, timeout=12)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def main():
    birthday_text = get_birthday_countdown()
    lunar_text = get_lunar_calendar()
    weather_data = fetch_weather()

    uv_text = "☀天气获取失败"
    sunrise = "--:--"
    sunset = "--:--"
    wind_text = ""
    rain_tip = "🌤降雨信息获取失败"

    if weather_data is not None:
        hourly = weather_data.get("hourly", {})
        daily = weather_data.get("daily", {})
        uv_arr = hourly.get("uv_index", [])
        wind_arr = hourly.get("wind_speed_10m", [])
        time_arr = hourly.get("time", [])

        if len(uv_arr) > 0:
            uv_max = max(uv_arr)
            uv_text = get_uv_tip(uv_max)

        sun_rise_list = daily.get("sunrise", [])
        sun_set_list = daily.get("sunset", [])
        if len(sun_rise_list) > 0:
            sunrise = sun_rise_list[0][11:16]
        if len(sun_set_list) > 0:
            sunset = sun_set_list[0][11:16]

        if len(wind_arr) >7:
            wind_text = get_wind_tip(wind_arr[7])

        rain_text_list = []
        max_h = min(24, len(time_arr))
        for i in range(max_h):
            prob = hourly.get("precipitation_probability",[0])[i]
            if prob >=70:
                hh = time_arr[i][11:13]
                rain_text_list.append(f"🌧{hh}点 {prob}%")
        if rain_text_list:
            rain_tip = "🌧降雨提醒：" + " ".join(rain_text_list)
        else:
            rain_tip = "🌤今日无高概率降雨"

    content = f"""📅每日简报
{birthday_text}

{uv_text}
🌅{sunrise}  🌇{sunset}
{wind_text}

{rain_tip}

{lunar_text}
"""

    if not BARK_KEY:
        print("警告：未配置BARK_KEY，仅打印内容，不推送")
        print(content)
        return

    push_url = f"{BARK_HOST}/{BARK_KEY}"
    params = {
        "title": "每日简报",
        "body": content,
        "level": "timeSensitive"
    }
    try:
        res = requests.get(push_url, params=params, timeout=15)
        print(f"Bark_status={res.status_code}")
        print(f"Bark_resp={res.text}")
    except Exception as e:
        print(f"Bark_error={str(e)}")


if __name__ == "__main__":
    main()
