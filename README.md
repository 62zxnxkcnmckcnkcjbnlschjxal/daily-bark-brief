# Daily Bark Brief 🌅

A GitHub Actions workflow that sends a daily morning briefing to your Bark app, including weather, UV index, sunrise/sunset times, lunar calendar information, and birthday countdowns.

## Badges 🏅

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Description 📝

This project automates the delivery of a personalized daily briefing directly to your mobile device via the Bark notification service. It aggregates useful daily information such as current weather conditions, UV index, sunrise and sunset times, traditional Chinese lunar calendar details (including auspicious and inauspicious activities), and a countdown to your birthday. All configuration is managed through environment variables, ensuring privacy and ease of use, especially in public repositories.

## Table of Contents 📜

- [Features](#features-🌟)
- [Tech Stack](#tech-stack-💻)
- [Installation](#installation-🚀)
- [Usage](#usage-💡)
- [Project Structure](#project-structure-📁)
- [Contributing](#contributing-🤝)
- [License](#license-⚖️)
- [Footer](#footer-✨)

## Features 🌟

- 🌦️ **Daily Weather Updates:** Provides current weather information including temperature, wind speed, and precipitation probability.
- ☀ **UV Index Alerts:** Notifies you about the UV index level and provides recommendations for sun protection.
- 🌅 **Sunrise & Sunset Times:** Keeps you informed about the daily sunrise and sunset times.
- 🎂 **Birthday Countdown:** Tracks the number of days remaining until your next birthday.
- 📜 **Lunar Calendar Integration:** Displays the traditional Chinese lunar calendar, including auspicious (`宜`) and inauspicious (`忌`) activities for the day.
- 📱 **Bark Push Notifications:** Delivers all information seamlessly to your Bark app.
- 🔒 **Environment Variable Configuration:** All sensitive information and settings are managed via environment variables, preventing hardcoding.

## Tech Stack 💻

- **Language:** Python 🐍
- **Frameworks/Libraries:**
  - `requests`: For making HTTP requests to weather APIs and Bark.
  - `cnlunar`: For calculating and retrieving Chinese lunar calendar information.
  - `zoneinfo`: For handling timezone information.

## Installation 🚀

This project is designed to be run as a GitHub Action. The primary configuration is done through environment variables.

1.  **Fork the Repository:** Fork this repository to your GitHub account.
2.  **Set Up Environment Variables:** In your forked repository, navigate to `Settings` > `Secrets and variables` > `Actions` and add the following repository secrets:
    *   `BARK_KEY`: Your unique Bark push key.
    *   `BARK_HOST`: (Optional) Your Bark server address if not using the default `https://api.day.app`.
    *   `WEATHER_LAT`: The latitude of your desired location (e.g., `39.9042` for Beijing).
    *   `WEATHER_LON`: The longitude of your desired location (e.g., `116.4074` for Beijing).
    *   `BIRTH_MONTH`: Your birth month (e.g., `7` for July).
    *   `BIRTH_DAY`: Your birth day (e.g., `10`).

3.  **Configure GitHub Actions:** The workflow is already set up in `.github/workflows/main.yml` (assuming a workflow file exists or will be created). You might need to adjust the `schedule` to your preferred timing.

## Usage 💡

This script is intended to be run automatically via GitHub Actions on a daily schedule. Once configured with your environment variables, it will fetch the data and send a notification to your Bark app.

### Example Workflow Trigger (GitHub Actions)

To run the script daily at 8:00 AM China Standard Time (CST), you can add a workflow file (e.g., `.github/workflows/daily_brief.yml`) with the following content:

```yaml
name: Daily Briefing

on:
  schedule:
    - cron: '0 0 * * *' # Runs at 00:00 UTC, adjust to your timezone
  workflow_dispatch: # Allows manual triggering

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install requests cnlunar
      - name: Run Daily Brief Script
        env:
          BARK_KEY: ${{ secrets.BARK_KEY }}
          BARK_HOST: ${{ secrets.BARK_HOST }}
          WEATHER_LAT: ${{ secrets.WEATHER_LAT }}
          WEATHER_LON: ${{ secrets.WEATHER_LON }}
          BIRTH_MONTH: ${{ secrets.BIRTH_MONTH }}
          BIRTH_DAY: ${{ secrets.BIRTH_DAY }}
        run: python main.py
```

**Note:** The `cron` expression `'0 0 * * *'` runs at midnight UTC. Adjust this to your local time. For example, to run at 8 AM CST (UTC+8), you would use `'24 * * * *'` (which is 8 AM UTC+8 on the *next* day from UTC perspective, or adjust based on your specific needs). A more direct way for 8 AM CST would be `'0 0 * * *'` if your runner's timezone is considered CST or adjust the UTC offset accordingly.

### How to use

1.  **Configure Environment Variables:** Ensure all necessary environment variables (`BARK_KEY`, `WEATHER_LAT`, `WEATHER_LON`, `BIRTH_MONTH`, `BIRTH_DAY`) are set in your GitHub repository secrets.
2.  **Trigger the Action:** The workflow will run automatically based on the schedule defined in your `.yml` file. You can also manually trigger it from the Actions tab in your GitHub repository.
3.  **Receive Notifications:** Check your Bark app for the daily briefing.

## Project Structure 📁

```
daily-bark-brief/
├── .github/
│   └── workflows/
│       └── daily_brief.yml  # Example GitHub Actions workflow file
├── assets/
│   └── 12                      # Potentially used for assets, content not analyzed
├── main.py                     # Main script for fetching data and sending notifications
├── LICENSE                     # Project license file
└── README.md                   # Project README file
```

## Contributing 🤝

Contributions are welcome! Please feel free to:

-   Fork the repository.
-   Create a new branch (`git checkout -b feature/YourFeature`).
-   Make your changes.
-   Commit your changes (`git commit -am 'Add some feature'`)
-   Push to the branch (`git push origin feature/YourFeature`)
-   Open a Pull Request.

Please ensure your code adheres to the project's style and includes tests if applicable.

## License ⚖️

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Footer ✨

---

Made with ❤️ by [62zxnxkcnmckcnkcjbnlschjxal](https://github.com/62zxnxkcnmckcnkcjbnlschjxal)

[Back to Top](#daily-bark-brief-🌅)

[![Star us on GitHub](https://img.shields.io/github/stars/62zxnxkcnmckcnkcjbnlschjxal/daily-bark-brief?style=social)](https://github.com/62zxnxkcnmckcnkcjbnlschjxal/daily-bark-brief)
[![Fork us on GitHub](https://img.shields.io/github/forks/62zxnxkcnmckcnkcjbnlschjxal/daily-bark-brief?style=social)](https://github.com/62zxnxkcnmckcnkcjbnlschjxal/daily-bark-brief)



---
**<p align="center">Generated by [ReadmeCodeGen](https://www.readmecodegen.com/)</p>**
