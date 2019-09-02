FROM python:3

ENV PROJECT_PATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEFAULT_USER=django_user

WORKDIR ${PROJECT_PATH}

COPY requirements.txt ${PROJECT_PATH}/

RUN pip install -r requirements.txt

COPY ./ ${PROJECT_PATH}/

RUN useradd -ms /bin/bash ${DEFAULT_USER}

USER ${DEFAULT_USER}

RUN echo 'alias ls="ls -la --color=auto"' > /home/${DEFAULT_USER}/.bashrc
