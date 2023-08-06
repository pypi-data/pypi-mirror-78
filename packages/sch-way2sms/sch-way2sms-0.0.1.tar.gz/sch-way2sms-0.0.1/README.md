# Way2Sms

Send upto 2 free [SMS](https://www.way2sms.com/) instantly.

[Way2Sms](https://www.way2sms.com/) provides free SMS service upto 2 messages daily with message length upto **139**.

## Install

```
pip3 install waytosms
```

## Usage

```
import waytosms
# your login credentials
sms = waytosms.Sms("9XXXXXXXXX", "PASSWORD")
sms.send("9XXXXXXXXX", "Hi, this package is awesome! Lets me send free messages")
sms.logout()
```

Future Message added by [AbdHan](https://github.com/abdhan)
