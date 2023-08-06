import os
from copy import copy
from typing import Optional
from glasskit import ctx
from glasskit.errors import ConfigurationError
from .provider import BaseProvider


def get_conf(provider_name):

    oacfg = ctx.cfg.get("oauth")
    if not oacfg:
        raise ConfigurationError("oauth is not configured")

    gcfg = oacfg.get("_global")

    if provider_name not in oacfg:
        return None

    provider_cfg = {**gcfg, **copy(oacfg[provider_name])}
    if "client_id" not in provider_cfg:
        raise ConfigurationError(f"oauth provider {provider_name} id field missing")
    if "client_secret" not in provider_cfg:
        raise ConfigurationError(f"oauth provider {provider_name} secret field missing")
    if "provider_name" not in provider_cfg:
        provider_cfg["provider_name"] = provider_name
    if "redirect_uri" not in provider_cfg:
        raise ConfigurationError(
            f"oauth provider {provider_name} redirect_uri field missing and no"
            f" global redirect_uri found"
        )

    client_id = provider_cfg["client_id"]
    client_secret = provider_cfg["client_secret"]
    redirect_uri = provider_cfg["redirect_uri"]
    del provider_cfg["client_id"]
    del provider_cfg["client_secret"]
    del provider_cfg["redirect_uri"]

    return client_id, client_secret, redirect_uri, provider_cfg


def setup_providers(relative_path: Optional[str] = None) -> None:
    from . import FacebookProvider, YandexProvider, GithubProvider

    providers = [FacebookProvider, YandexProvider, GithubProvider]

    if relative_path:
        module_prefix = ".".join(relative_path.split("/")).strip(".")

        for filename in os.listdir(relative_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module_name = f"{module_prefix}.{module_name}"
                module = importlib.import_module(module_name)
                for obj_name in dir(module):
                    obj = getattr(module, obj_name)
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseProvider)
                        and obj != BaseProvider
                    ):
                        providers.append(obj)

    for provider in providers:
        if get_conf(provider.PROVIDER_NAME):
            provider().register()
        else:
            ctx.log.info(
                "Skipping OAuth2 provider %s, no configuration found",
                provider.PROVIDER_NAME,
            )
