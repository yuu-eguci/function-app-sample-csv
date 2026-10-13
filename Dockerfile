# dev: lint とテスト (docker compose run --rm check)
FROM python:3.13-slim AS dev
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /uvx /bin/
RUN useradd --create-home app
USER app
ENV UV_PROJECT_ENVIRONMENT=/home/app/venv \
    UV_PYTHON_DOWNLOADS=never \
    PATH=/home/app/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    RUFF_NO_CACHE=true \
    PYTEST_ADDOPTS="-p no:cacheprovider"
WORKDIR /home/app/src
COPY --chown=app pyproject.toml uv.lock ./
RUN uv sync --locked --no-cache
COPY --chown=app . .
CMD ["sh", "-c", "ruff check . && ruff format --check . && pytest"]

# app: Functions ホスト (docker compose up app)。最後のステージなので素の docker build はこれになる
FROM mcr.microsoft.com/azure-functions/python:4-python3.13 AS app
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true
COPY requirements.txt /
RUN pip install --no-cache-dir --root-user-action=ignore -r /requirements.txt
COPY host.json /home/site/wwwroot/
COPY sample_csv_function /home/site/wwwroot/sample_csv_function
COPY shared_code /home/site/wwwroot/shared_code
