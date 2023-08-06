FROM python:latest

ARG CACHE_DIR=/poetry

WORKDIR /build

RUN python -m pip install \
    --no-cache-dir \
    --upgrade \
    pip setuptools wheel

RUN python -m pip install --no-cache-dir poetry \
    && python -m poetry config virtualenvs.create false

COPY pyproject.toml /build
COPY poetry.lock /build

RUN python -m poetry install --no-root

COPY . /build

RUN poetry install

ENTRYPOINT ["/bin/bash", "-c"]

CMD ["bash"]
