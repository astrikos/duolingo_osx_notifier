# Duolingo OSX Notifier
Practice makes perfect. Learning a language requires constantly repetition every day. This little tool will help you exactly with that. You can use it to get a MacOSX notification about a word and its meaning in any interval you would like.

This tool assumes you keep a file containing words and its definitions line by line. e.g.

![Alt](/file_format.jpg "File Format")

## HowTo
In order to run this tool you should clone this repo and run:
``````
./notifier.py --filename my_language_file --interval 3600
```
This example will read the my_language_file and give you a notification like the one below every one hour (3600 seconds).

![Alt](/notification.jpg "Notification")

## Notes
Make sure you have allowed python to send notifications through MacOSX Notification Center. You can check by going to System Preferences->Notifications. Preferable alert style for now is Banners.
