<div align="center">

# daily‑bark‑brief
> 🕖 GitHub Actions 全自动晨间简报推送 | Bark 手机消息通知

**天气 · 紫外线指数 · 日出日落 · 风力降雨预报 · 传统黄历宜忌 · 生日倒计时**

<p>
  <img src="https://img.shields.io/badge/GitHub‑Actions‑enabled‑2ea44f" alt="GitHub‑Actions">
  <img src="https://img.shields.io/badge/Python‑3.12‑3776AB" alt="Python">
  <img src="https://img.shields.io/badge/license‑MIT‑blue" alt="MIT">
  <img src="https://img.shields.io/badge/Open‑Meteo‑Weather‑009688" alt="Open‑Meteo">
</p>

</div>

## 📖 项目介绍
完全基于 GitHub Actions 免费运行，**无需服务器、无需本地开机**。
每日北京时间早上 07:00 自动执行，将整合好的晨间简报推送到你的手机 Bark APP。

### 🧠 环境变量读取逻辑
> 脚本读取顺序：**优先读取 GitHub‑Actions Secrets 注入的环境变量 → 如果不存在，使用代码内示例兜底默认值（仅演示）**
>
> 👉 `os.getenv("变量名", "兜底示例值")`
> - 在 GitHub Actions 运行：yml 文件会把仓库 Secrets 注入为运行时环境变量，脚本优先使用这一组真实配置。
> - 本地手动运行脚本：没有环境变量时，会自动 fallback 使用代码内写死的示例样例数据（北京坐标、示例生日）。

> ⚠️ **【公开仓库强制禁令】请勿在公开仓库的代码文件填写任何真实配置！**
> 如果把真实 `BARK_KEY`、真实经纬度写进 `main.py`，所有互联网访问仓库的人都可以拿到密钥，疯狂向你的手机推送垃圾骚扰消息！
> 所有真实隐私配置，**只允许填写在仓库 Secrets 里面，绝对不能直接修改 main.py 内的兜底默认值为自己真实数据**。

## 📱 推送效果示例（Bark手机弹窗预览）
【标题】每日简报
【内容】
📅每日简报
🎂距离生日还有 128 天

☀UV4.3｜建议涂防晒
🌅05:12  🌇19:08
🍃微风 4km/h

🌤今日无高概率降雨

📜丙午年七月初十
——————————————————
✅ 今日宜：
· 出行
· 宴会
· 理发
——————————————————
❌ 今日忌：
· 开市（店铺开业）
· 入宅（搬入新家）

⚔ 冲鼠（民俗：该属相多留意）
⚠ 彭祖百忌：子不问卜自惹祸殃（仅供娱乐）
## 📂 项目目录结构
daily‑bark‑brief/
├── main.py                          # 主业务脚本，核心逻辑
├── README.md                        # 项目文档（本文件）
└── .github/
└── workflows/
└── push.yml                 # GitHub‑Actions 定时工作流配置
| 文件 | 作用 | 是否需要修改 |
|---|---|---|
| `main.py` | 推送逻辑、天气接口、黄历计算、消息拼接 | **一般无需修改**，高级自定义才改动；公开仓库禁止修改兜底默认值为自己真实信息 |
| `.github/workflows/push.yml` | 定时时间、**Secrets注入环境变量配置**、运行配置 | **无需修改**，Fork直接使用 |
| `README.md` | 使用说明文档 | Fork后可按需修改介绍文字 |

## ⚙️ 部署完整步骤
### 1. Fork本仓库
点击右上角 `Fork`，复制一份仓库到自己账号下。

### 2. 在仓库配置 Secrets（存放你的真实隐私配置）
> Secrets 是 GitHub 的加密存储，网页上看不到明文，只在 Actions 执行的时候注入为运行环境变量给到 Python 脚本读取。

进入仓库页面 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

依次添加下面 6 条密钥变量，**全部填入自己真实信息**

| Secret变量名称 | 说明 | 参考示例 |
|---|---|---|
| `BARK_KEY` | Bark APP内获取的推送密钥 | `xxxxxxx` |
| `BARK_HOST` | Bark服务域名，自建服务可修改 | `https://api.day.app` |
| `WEATHER_LAT` | 目标城市纬度 | `39.9042`（北京） |
| `WEATHER_LON` | 目标城市经度 | `116.4074`（北京） |
| `BIRTH_MONTH` | 生日‑月份数字 | `7` |
| `BIRTH_DAY` | 生日‑日期数字 | `10` |

> 💡 获取城市经纬度：搜索引擎搜索「城市名 经纬度」即可。

> ✅ `push.yml` 内部已经写好注入逻辑，无需改动yml文件：
> ```yaml
> env:
>   BARK_KEY: ${{ secrets.BARK_KEY }}
>   BARK_HOST: ${{ secrets.BARK_HOST }}
>   WEATHER_LAT: ${{ secrets.WEATHER_LAT }}
>   WEATHER_LON: ${{ secrets.WEATHER_LON }}
>   BIRTH_MONTH: ${{ secrets.BIRTH_MONTH }}
>   BIRTH_DAY: ${{ secrets.BIRTH_DAY }}
> ```
> Actions运行时，会自动把上面 Secrets 的内容变成 Python 脚本可以读取的环境变量。

### 3. 运行测试
1. 顶部菜单打开 `Actions`
2. 选择「每日简报推送」工作流
3. 点击右侧 `Run workflow` → 直接执行一次
4. 查看运行日志，手机 Bark 接收消息，确认功能正常。

### 4. 定时时间说明
> ⚠️ GitHub Actions cron 使用 **UTC零时区时间**，不是北京时间
- 配置：`cron: '0 23 * * *'`
- UTC‑23:00 = **北京时间早上 07:00**
> 允许 0‑15分钟浮动延迟，属于GitHub免费服务正常现象，无法做到分秒不差。

> 🕐 修改推送时间：改动 `.github/workflows/push.yml` 文件内 `cron: '0 23 * * *'`。
> cron格式：`分 时 日 月 星期`

## 🧩 依赖库
> Actions环境会自动安装，本地调试执行：
```bash
pip install requests cnlunar
⚠️ 重要注意事项

1. 仓库休眠限制
GitHub Actions定时任务：仓库连续60天无任何提交改动，定时会自动休眠停止执行。
解决：随便修改README增加空格/注释，提交一次即可重新激活定时调度。

2. 漏执行问题
免费GitHub‑Actions定时调度不保证100%稳定，极小概率会漏跑一次任务，属于平台限制，无法彻底避免。

3. 🔒隐私安全红线（非常重要）

• 严禁将 Bark‑Key、个人坐标等隐私信息直接写进代码提交公开仓库！全部必须放在 Secrets 环境变量。

• main.py内的默认值仅作为示例演示，不要修改为自己真实信息并提交公开仓库，一旦泄露密钥，任何人都可以给你的手机发送骚扰推送消息。

4. 接口说明

• 天气来源：Open‑Meteo 免费公共API，无申请Key，有访问频率限制；短时间大量调用会被限流。

• 黄历计算库：cnlunar 本地算法计算，黄历内容仅供民俗娱乐参考，不作为生活决策依据。

5. Bark服务

• 默认使用官方公共Bark服务；自建Bark服务器，修改BARK_HOST变量填入自建域名。

✨ 高级自定义修改指引

修改推送消息文案内容

编辑 main.py 文件底部 content = f""" ... """ 代码块，修改输出文字格式。

增删黄历宜/忌词条

编辑 main.py 文件中 keep_words = {...} 集合，增加/删减词条关键字。

修改文言释义翻译对照表

编辑 replace_dict、explain_map 字典，自定义翻译文字。

更换天气接口

修改函数 fetch_weather()，替换接口URL与解析JSON逻辑。

📄 License

MIT License，可自由复制、修改、二次分发，保留开源协议声明。
## main.py 头部安全注释片段（完整main沿用之前版本，只强化头部注释）
```python
import os
import requests
from datetime import datetime, date
from zoneinfo import ZoneInfo
from cnlunar import Lunar

# ==============================================================
# ⚠️ 【安全警告 · 公开仓库用户必读】
# 脚本读取优先级：优先读取 GitHub‑Actions Secrets注入的环境变量
# 下面仅为【演示兜底示例值】，仅用于本地调试演示！
#
# ❌ 禁止！禁止！禁止！在公开仓库把下面默认值改成你的真实信息提交！
# 如果填入真实BARK_KEY并上传公开仓库，密钥全网可见，会遭受大量骚扰推送。
# 所有真实配置全部填写在仓库 Settings → Secrets and variables → Actions
# ==============================================================
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
# ……后面代码不变
push.yml文件内容保持不变，yml里面已经写好 secrets.xxx 注入逻辑，脚本运行的时候yml会把Secrets变成环境变量给到Python的os.getenv()读取。
执行顺序：GitHub Secrets → yml注入环境变量 → Python脚本os.getenv()读取，没有则使用示例兜底。

# 🤝 特别致谢
## 感谢豆包对本项目开发的大力支持 🤖
<img height="48" src="https://lf3-static.bytednsdoc.com/obj/eden-cn/zh-cn/ljhwZthlaukjlkulzlp/doubao_logo.png" alt="豆包">
