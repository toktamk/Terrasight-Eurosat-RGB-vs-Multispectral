FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1         PIP_NO_CACHE_DIR=1         MPLBACKEND=Agg         KMP_DUPLICATE_LIB_OK=TRUE

WORKDIR /app
COPY . /app
EXPOSE 8501
RUN apt-get update         && apt-get install -y --no-install-recommends            build-essential            git            libgl1            libglib2.0-0         && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt* README.md ./
COPY src ./src
COPY configs ./configs
COPY tests ./tests
COPY docs ./docs
COPY scripts ./scripts

RUN python -m pip install --upgrade pip         && if [ -f requirements.txt ]; then pip install -r requirements.txt; fi         && pip install -e .

CMD ["python", "-c", "import terrasight; print('Installation successful')"]
