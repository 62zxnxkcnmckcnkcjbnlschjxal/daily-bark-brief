# 每日 Bark 简报 🌅
一个 GitHub Actions 工作流，每天向你的 Bark 应用发送晨间简报，内容包括天气、紫外线指数、日出日落时间、农历信息以及生日倒计时。
## 徽章 🏅
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
## 项目说明 📝
本项目通过 Bark 通知服务，自动将个性化的每日简报直接推送到你的移动设备。它聚合了各类实用的日常信息，包括当前天气状况、紫外线指数、日出日落时间、中国传统农历详情（含宜忌事项），以及距离你下一个生日的倒计时。所有配置均通过环境变量管理，确保隐私安全且易于使用，尤其适合在公开仓库中部署。
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
- 🌦️ **每日天气更新：** 提供当前天气信息，包括温度、风速和降水概率。
- ☀ **紫外线指数提醒：** 告知你当日紫外线指数等级，并给出防晒建议。
- 🌅 **日出日落时间：** 让你了解每日日出和日落的具体时间。
- 🎂 **生日倒计时：** 追踪距离你下一个生日还剩多少天。
- 📜 **农历集成：** 显示中国传统农历，包括当日的宜（`宜`）和忌（`忌`）事项。
- 📱 **Bark 推送通知：** 将所有信息无缝推送到你的 Bark 应用。
- 🔒 **环境变量配置：** 所有敏感信息和设置均通过环境变量管理，避免硬编码。
## 技术栈 💻
- **编程语言：** Python 🐍
- **框架/库：**
  - `requests`：用于向天气 API 和 Bark 发送 HTTP 请求。
  - `cnlunar`：用于计算和获取中国农历信息。
  - `zoneinfo`：用于处理时区信息。
## 安装部署 🚀
本项目设计为以 GitHub Action 的方式运行，主要配置通过环境变量完成。
1.  **Fork 仓库：** 将本仓库 Fork 到你的 GitHub 账户。
2.  **配置环境变量：** 在你 Fork 的仓库中，进入 `Settings` > `Secrets and variables` > `Actions`，添加以下仓库密钥：
    *   `BARK_KEY`：你唯一的 Bark 推送密钥。
    *   `BARK_HOST`：（可选）如果你不使用默认的 `https://api.day.app`，可填写你的 Bark 服务器地址。
    *   `WEATHER_LAT`：目标位置的纬度（例如北京为 `39.9042`）。
    *   `WEATHER_LON`：目标位置的经度（例如北京为 `116.4074`）。
    *   `BIRTH_MONTH`：你的出生月份（例如 7 月填 `7`）。
    *   `BIRTH_DAY`：你的出生日期（例如 `10`）。
3.  **配置 GitHub Actions：** 工作流已在 `.github/workflows/main.yml` 中设置好（假设工作流文件已存在或即将创建）。你可能需要根据自己的偏好调整 `schedule` 定时时间。
## 使用方法 💡
本脚本旨在通过 GitHub Actions 按每日计划自动运行。配置好环境变量后，它将自动获取数据并向你的 Bark 应用发送通知。
### 工作流触发示例（GitHub Actions）
要在每天中国标准时间（CST）早上 8:00 运行脚本，你可以添加一个工作流文件（例如 `.github/workflows/daily_brief.yml`），内容如下：
```yaml
name: 每日简报
on:
  schedule:
    - cron: '0 0 * * *' # 在 UTC 时间 00:00 运行，根据你的时区调整
  workflow_dispatch: # 允许手动触发
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 设置 Python 环境
        uses: actions/setup-python@v3
        with:
          python-version: '3.x'
      - name: 安装依赖
        run: pip install requests cnlunar
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
**注意：** `cron` 表达式 `'0 0 * * *'` 表示在 UTC 时间午夜运行。请根据你所在的时区进行调整。例如，要在 CST（UTC+8）早上 8 点运行，你可以使用 `'24 * * * *'`（从 UTC 角度看这是第二天的 UTC+8 早上 8 点，或根据你的具体需求调整）。如果运行器的时区被视为 CST，更直接的方式是使用 `'0 0 * * *'`，或者根据 UTC 偏移量相应调整。
### 如何使用
1.  **配置环境变量：** 确保所有必要的环境变量（`BARK_KEY`、`WEATHER_LAT`、`WEATHER_LON`、`BIRTH_MONTH`、`BIRTH_DAY`）都已在你的 GitHub 仓库密钥中设置。
2.  **触发 Action：** 工作流将根据你 `.yml` 文件中定义的计划自动运行。你也可以在 GitHub 仓库的 Actions 标签页中手动触发。
3.  **接收通知：** 在你的 Bark 应用中查看每日简报。
## 项目结构 📁
```
daily-bark-brief/
├── .github/
│   └── workflows/
│       └── daily_brief.yml  # 示例 GitHub Actions 工作流文件
├── assets/
│   └── 12                      # 可能用于存放资源，内容未分析
├── main.py                     # 获取数据并发送通知的主脚本
├── LICENSE                     # 项目许可证文件
└── README.md                   # 项目说明文件
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
