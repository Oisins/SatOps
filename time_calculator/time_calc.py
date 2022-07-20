# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

with open("time_delta.txt") as file:
    start = file.readline().strip()
    start_datetime = datetime.strptime(start, "%d %b %Y %H:%M:%SZ")
    print(f"\nImage Capture at: {start_datetime.strftime('%d.%m.%Y %H:%M:%S')}\n")

    for i, line in enumerate(file.readlines()):
        name, dt = line.strip().split(" ")

        sign, dt = dt[:1], dt[1:]

        minutes, seconds = dt.split(":")

        minutes = int(minutes)
        seconds = int(seconds)

        delta = timedelta(minutes=minutes, seconds=seconds)

        new_datetime = start_datetime + delta if sign == "+" else start_datetime - delta

        print(f"{i:<3}{name:<20}{new_datetime.strftime('%d.%m.%Y %H:%M:%S')}")
