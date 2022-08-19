# SatOps Sose 2022
Repository für SatOps SoSe 2022 Projekt 5 "Kamera als Horizontsensor"

## Installation

1. `pip install -r requirements.txt`
2. Place images working directory
3. Add Metadata about image in `src/dictionary_satellites.py`
4. Set mission in `main.py`
5. Run `python main.py`

# Development Notes
## Finding position of moon
* https://heavens-above.com/Moon.aspx shows Ra and Dec. Altitude must be set to -6371000m to reference from earth's
  center
* The package "ephem" shows a difference of 10' for the Dec and 1' for Ra

## Images and Attitudes

| Description                  | File Name | Timestamp                | Quaternions                              | Euler |
|------------------------------|-----------|--------------------------|------------------------------------------|-------|
| Horizon with Moon            | 9-7.jpg   | 15 Feb 2022 12:36:43.000 | -0.490834, 0.395866, 0.775337, 0.0349882 |       |
| Moon in front of flight path |           | 3 Jul 2022 06:27:51.744  |                                          |       |
|                              |           |                          |                                          |       |
