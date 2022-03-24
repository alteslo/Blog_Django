from dataclasses import dataclass

from environs import Env


@dataclass
class EmailConfig:
    host: str
    use_tls: bool
    port: int
    host_user: str
    host_password: str

@dataclass
class DjangoConfig:
    sekret_key: str


@dataclass
class Config:
    email: EmailConfig
    django: DjangoConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        email=EmailConfig(
            host=env.str('EMAIL_HOST'),
            use_tls=env.bool('EMAIL_USE_TLS'),
            port=env.int('EMAIL_PORT'),
            host_user=env.str('EMAIL_HOST_USER'),
            host_password=env.str('EMAIL_HOST_PASSWORD')
        ),
        django=DjangoConfig(
            sekret_key=env.str('SECRET_KEY')
        )
    )
