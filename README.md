# 每日 Bark 简报 🌅
一个基于 GitHub Actions 的每日晨间简报推送工具，每天定时向你的 Bark 应用推送天气、紫外线指数、日出日落时间、农历黄历以及生日倒计时。**无需自己购买服务器、无需部署网站，全部在 GitHub Actions 上免费运行。**
## 徽章 🏅
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
## 项目说明 📝
本项目通过 GitHub Actions 定时运行 Python 脚本，自动获取天气、农历等信息，聚合为一份个性化的每日简报，并通过 Bark 通知服务推送到你的手机。全程运行在 GitHub Actions 云端，**不需要你自己搭建服务器或部署网站**，Fork 仓库后配置几个环境变量即可使用。

聚合的信息包括：当前天气状况、紫外线指数及防晒建议、日出日落时间、降雨高概率时段提醒、风力等级、中国传统农历黄历（含宜忌、冲煞、彭祖百忌），以及距离下一个生日的倒计时。所有敏感配置均通过 GitHub Secrets 环境变量管理，公开仓库也不会泄露隐私。
## 目录 📜
- [功能特性](#功能特性-🌟)
- [技术栈](#技术栈-💻)
- [安装部署](#安装部署-🚀)
- [使用方法](#使用方法-💡)
- [项目结构](#项目结构-📁)
- [贡献指南](#贡献指南-🤝)
- [许可证](#许可证-⚖️)
- [页脚](#页脚-✨)
## 功能特性 🌟
- 🌦️ **每日天气更新：** 提供当前温度、风速等级和降雨高概率时段提醒。
- ☀ **紫外线指数提醒：** 告知当日紫外线峰值等级，并给出对应防晒建议。
- 🌅 **日出日落时间：** 显示每日日出和日落的具体时间。
- 🎂 **生日倒计时：** 自动计算距离下一个生日还剩多少天。
- 📜 **农历黄历集成：** 显示中国传统农历年月日，包括当日宜、忌事项，以及生肖冲煞和彭祖百忌（仅供娱乐参考）。
- 📱 **Bark 推送通知：** 以「时效性通知」级别将所有信息推送到你的 Bark 应用，支持锁屏显示。
- 🔒 **环境变量配置：** 所有敏感信息和设置均通过 GitHub Secrets 管理，避免硬编码。
- 🆓 **零成本运行：** 完全基于 GitHub Actions，无需购买服务器、无需部署网站，Fork 即用。
## 技术栈 💻
- **编程语言：** Python 🐍 3.12
- **天气数据：** [Open-Meteo](https://open-meteo.com/) 免费天气 API（无需注册、无需 API Key）
- **框架/库：**
  - `requests`：用于向 Open-Meteo 天气 API 和 Bark 推送接口发送 HTTP 请求。
  - `cnlunar`：用于计算和获取中国农历黄历信息。
  - `zoneinfo`：用于处理时区信息（固定使用 Asia/Shanghai）。
- **运行平台：** GitHub Actions（ubuntu-latest）
## 安装部署 🚀
本项目设计为以 GitHub Action 的方式运行，**不需要自己部署服务器或网站**。主要配置通过 GitHub Secrets 环境变量完成。

1.  **Fork 仓库：** 将本仓库 Fork 到你的 GitHub 账户。
2.  **配置环境变量：** 在你 Fork 的仓库中，进入 `Settings` > `Secrets and variables` > `Actions` > `New repository secret`，添加以下仓库密钥：
    *   `BARK_KEY`：你唯一的 Bark 推送密钥（必填）。
    *   `BARK_HOST`：（可选）你的 Bark 服务器地址，不填则使用默认 `https://api.day.app`。
    *   `WEATHER_LAT`：目标位置的纬度（例如北京为 `39.9042`）。
    *   `WEATHER_LON`：目标位置的经度（例如北京为 `116.4074`）。
    *   `BIRTH_MONTH`：你的出生月份（例如 7 月填 `7`）。
    *   `BIRTH_DAY`：你的出生日期（例如 `10`）。
3.  **启用工作流：** Fork 后 GitHub Actions 默认可能被禁用，进入仓库的 `Actions` 标签页，点击 `I understand my workflows, go ahead and enable them` 启用工作流。工作流文件 `.github/workflows/push.yml` 已预置好，无需额外创建。
## 使用方法 💡
配置好 Secrets 后，脚本将按照工作流中设定的时间自动运行，获取数据并向你的 Bark 应用发送通知。你也可以在 Actions 页面手动触发运行测试。

### 工作流配置说明
实际工作流文件为 `.github/workflows/push.yml`，核心配置如下：

```yaml
name: 每日简报推送
on:
  schedule:
    - cron: '0 23 * * *'  # UTC 时间 23:00 = 北京时间（UTC+8）次日 07:00
  workflow_dispatch:        # 支持手动触发

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - name: 检出代码
        uses: actions/checkout@v4

      - name: 设置Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install requests cnlunar

      - name: 运行每日简报脚本
        env:
          BARK_KEY: ${{ secrets.BARK_KEY }}
          BARK_HOST: ${{ secrets.BARK_HOST }}
          WEATHER_LAT: ${{ secrets.WEATHER_LAT }}
          WEATHER_LON: ${{ secrets.WEATHER_LON }}
          BIRTH_MONTH: ${{ secrets.BIRTH_MONTH }}
          BIRTH_DAY: ${{ secrets.BIRTH_DAY }}
        run: python main.py
```

**注意：** GitHub Actions 的 cron 表达式使用 UTC 时间。`'0 23 * * *'` 表示 UTC 每天 23:00 运行，换算为北京时间（UTC+8）是**每天早上 7:00**。如果你想调整推送时间，需要将目标北京时间减去 8 小时得到对应的 UTC 时间，再修改 cron 表达式。

### 如何使用
1.  **配置环境变量：** 确保所有必要的环境变量（`BARK_KEY`、`WEATHER_LAT`、`WEATHER_LON`、`BIRTH_MONTH`、`BIRTH_DAY`）都已在你的 GitHub 仓库 Secrets 中设置。
2.  **触发 Action：** 工作流将在每天北京时间早上 7:00 自动运行。你也可以在 GitHub 仓库的 `Actions` 标签页中选择「每日简报推送」工作流，点击 `Run workflow` 手动触发测试。
3.  **接收通知：** 检查你的 Bark 应用，即可收到每日简报推送。推送级别为「时效性通知」，会在锁屏上显示。
## 项目结构 📁
```
daily-bark-brief/
├── .github/
│   └── workflows/
│       └── push.yml          # GitHub Actions 工作流文件（定时推送）
├── assets/                   # 资源目录
├── main.py                   # 主脚本：获取天气/农历数据并通过 Bark 推送
├── .gitignore                # Git 忽略文件配置
├── LICENSE                   # 项目许可证文件（MIT）
└── README.md                 # 项目说明文件
```
## 贡献指南 🤝
欢迎贡献！请随意：
-   Fork 本仓库。
-   创建新分支（`git checkout -b feature/YourFeature`）。
-   进行修改。
-   提交修改（`git commit -am 'Add some feature'`）
-   推送到分支（`git push origin feature/YourFeature`）
-   发起 Pull Request。
请确保你的代码符合项目的代码风格，并在适用时包含测试。
## 许可证 ⚖️
本项目采用 MIT 许可证 — 详见 [LICENSE](LICENSE) 文件。
## 页脚 ✨
---
由 [62zxnxkcnmckcnkcjbnlschjxal](https://github.com/62zxnxkcnmckcnkcjbnlschjxal) 用 ❤️ 制作
[返回顶部](#每日-bark-简报-🌅)
[![在 GitHub 上点 Star](https://img.shields.io/github/stars/62zxnxkcnmckcnkcjbnlschjxal/daily-bark-brief?style=social)](https://github.com/62zxnxkcnmckcnkcjbnlschjxal/daily-bark-brief)
[![在 GitHub 上 Fork](https://img.shields.io/github/forks/62zxnxkcnmckcnkcjbnlschjxal/daily-bark-brief?style=social)](https://github.com/62zxnxkcnmckcnkcjbnlschjxal/daily-bark-brief)
---
**<p align="center">感谢豆包对开发的鼎力支持 <img src="https://aka.doubaocdn.com/s/UdCzsFo9lb" width="40" valign="middle" /></p>**
