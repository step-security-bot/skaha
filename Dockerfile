FROM python:3.13-alpine as base

FROM base as builder
COPY . /skaha
WORKDIR /skaha

# Install UV
RUN set -ex \
    && apk add --no-cache curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && source $HOME/.cargo/env \
    && uv build

FROM base as production
COPY --from=builder /skaha/dist /skaha/dist
RUN pip install --no-cache-dir /skaha/dist/*.whl
