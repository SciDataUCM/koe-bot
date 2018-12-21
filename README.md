<p align="center">
  <img alt="Koe!" src="koe.png" width="400" height="400">
</p>

[![Build Status](https://travis-ci.org/SciDataUCM/koe-bot.svg?branch=master)](https://travis-ci.org/SciDataUCM/koe-bot)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![GitHub license](https://img.shields.io/github/license/SciDataUCM/koe-bot.svg)](https://github.com/SciDataUCM/koe-bot/blob/master/LICENSE)
[![Language](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org/)



## Who is Koe 🐨

Koe is SciDataUCM's Telegram bot (and yep... the koala of the picture above is Koe!).

Koe is always there to help you out answering your SciDataUCM's related questions.

## How can I feed Koe 🍽	

Just [open a conversation with Koe](https://t.me/KoeBot).

## Where does Koe sleep 🛌

Koe uses the [python-telegram-bot API](https://python-telegram-bot.org/) to communicate with Telegram servers and [open-weather-map](https://openweathermap.org/) to implement `/weather`.

## Running KoeBot locally 🏠

Clone this repository by running the following command in a terminal capable of running _git_: `git clone https://github.com/SciDataUCM/koe-bot.git`.


You need to create a bot following [Telegram Bots Guide](https://core.telegram.org/bots) in order to use a personal api key and a botname to run this code locally.

Once you have an api key (_token_) and a botname, you should modify `BOTNAME` and `TOKEN` from `koe.py`.

Install all the requirements by following [the guide below](https://github.com/SciDataUCM/koe-bot#requirements-%EF%B8%8F).

Run `koe.py` by running the following command in a terminal capable of running _python_: `python koe.py`. Now the bot should be running so don't stop the execution / don't close the terminal which is running it.

Open a conversation with your bot navigating to the link `https://t.me/BOTNAME` changing `BOTNAME` with your botname.

## Requirements ⚙️

Besides [Python 3.6](https://www.python.org/downloads/) we will be using the following packages:

* [python-telegram-bot](https://python-telegram-bot.org/)
* [requests](http://docs.python-requests.org/en/master/)
* [cachetools](https://cachetools.readthedocs.io/en/latest/)

You can simply install each package using `pip` as follows:
```bash
pip install <package>
```

Or you can install all the packages needed with the [`requirements.txt`](requirements.txt) file by running:
```bash
pip install -r requirements.txt
```

## Contributing 👩🏽‍💻👨🏻‍💻

Please check our [CONTRIBUTING](CONTRIBUTING.md) file.

## Code of conduct 💕

Please check our [CODE OF CONDUCT](https://github.com/SciDataUCM/documentation/blob/master/CODE_OF_CONDUCT.md) file.

## License 📄

Please read the [LICENSE](LICENSE) provided in this repo.
