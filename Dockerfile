FROM python:3-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app


FROM python as poetry
# Needed for ARM images
ARG BUILDDEPS="build-essential cargo libffi-dev libssl-dev rustc"
RUN apt-get update && apt-get install -y ${BUILDDEPS} --no-install-recommends
RUN python3 -m pip install poetry
# ENV POETRY_HOME=/opt/poetry
# ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# ENV PATH="$POETRY_HOME/bin:$PATH"
# RUN python -c \
#     'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' \
#     | python -
COPY barcos/ ./
RUN poetry install --no-interaction --no-ansi -vvv



FROM python as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
CMD cd src && python run.py
