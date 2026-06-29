# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app

# Install opencoverage from GitHub when not on PyPI (override at build time if needed).
ARG OPENCOVERAGE_REF=main
RUN pip install --no-cache-dir \
    "opencoverage @ git+https://github.com/irvingvasquez/opencoverage.git@${OPENCOVERAGE_REF}"

COPY pyproject.toml README.md ./
COPY opencoverage_web/ opencoverage_web/
COPY app.py ./

RUN pip install --no-cache-dir .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
