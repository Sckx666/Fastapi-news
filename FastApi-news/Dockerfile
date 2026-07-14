FROM python:3.13-slim

WORKDIR /app

RUN pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

COPY pyproject.toml uv.lock ./

ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

RUN uv sync --frozen --no-install-project --no-dev --no-cache --verbose

COPY . .

EXPOSE 8000

CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
