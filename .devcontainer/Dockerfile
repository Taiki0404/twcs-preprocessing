ARG VARIANT="3.12-bullseye"
FROM python:$VARIANT

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y \
    sudo git curl \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /workspaces

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc

ENV POETRY_VIRTUALENVS_IN_PROJECT=true