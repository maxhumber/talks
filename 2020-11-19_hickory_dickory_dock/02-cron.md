### cron Instructions

Open up the cron file at the command:

```sh
crontab -e
```

Add scripts to the schedule:

```sh
* * * * * /Users/max/Repos/HDD/02-cron_me.py
```

To write:

```
:w <enter>
:q <enter>
```

And use [this website](https://crontab.guru/) to figure out the \*
