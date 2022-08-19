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