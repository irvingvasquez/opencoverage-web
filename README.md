# OpenCoverage Web

Browser UI for [OpenCoverage](https://github.com/irvingvasquez/opencoverage) UAV coverage path planning.

Upload a survey polygon (KML or Mission Planner `.poly`) and an INI configuration file, plan a mission, preview the flight path on a map, and download QGroundControl waypoint files.

This project is **independent** from the OpenCoverage library: it depends on `opencoverage` as a Python package and can be deployed on its own.

## Features

- Upload KML / `.poly` survey areas
- Upload INI planner configuration (UAV, camera, overlaps, pattern)
- Optional mission splitting by flight time
- Interactive map preview (field boundary + waypoint path)
- Download QGC `.waypoints` files

## Local development

### 1. Install the library

From a checkout of OpenCoverage (sibling repo or any path):

```bash
cd ../opencoverage
pip install -e ".[dev]"
```

### 2. Install and run the web app

```bash
cd ../opencoverage-web
python -m venv .venv
source .venv/bin/activate
pip install -e .
streamlit run app.py
```

Open http://localhost:8501

Example inputs live in the OpenCoverage repo:

- `../opencoverage/examples/sample_field.kml`
- `../opencoverage/config/quad_tetracam.ini`

## Deploy

### Streamlit Community Cloud (easiest)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. Set **Main file path** to `app.py`.
4. Add a `requirements.txt` or configure packages (see below).

Because `opencoverage` may not be on PyPI yet, add a **`requirements.txt`** at the repo root for Streamlit Cloud:

```text
opencoverage @ git+https://github.com/irvingvasquez/opencoverage.git@main
streamlit>=1.30
folium>=0.15
streamlit-folium>=0.18
```

Once OpenCoverage is published to PyPI, you can simplify to `opencoverage>=0.2.0`.

### Docker (Render, Railway, Fly.io, VPS)

```bash
docker build -t opencoverage-web .
docker run -p 8501:8501 opencoverage-web
```

Pin a library version at build time:

```bash
docker build --build-arg OPENCOVERAGE_REF=v0.2.0 -t opencoverage-web .
```

## Project layout

```
opencoverage-web/
├── app.py                  # Streamlit entry point
├── opencoverage_web/
│   ├── map_view.py         # Folium map rendering
│   └── planning.py         # Upload → plan() wrapper
├── Dockerfile
├── pyproject.toml
└── .streamlit/config.toml
```

## License

MIT License. Copyright (c) J. Irving Vasquez-Gomez.
