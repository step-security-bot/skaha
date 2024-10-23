FROM python:3.13-alpine AS BASE

FROM BASE AS BUILDER
COPY . /skaha
WORKDIR /skaha

# Install UV
RUN set -ex \
    && apk add --no-cache curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && source $HOME/.cargo/env \
    && uv build

FROM BASE AS production
COPY --from=BUILDER /skaha/dist /skaha/dist
RUN pip install --no-cache-dir /skaha/dist/*.whl