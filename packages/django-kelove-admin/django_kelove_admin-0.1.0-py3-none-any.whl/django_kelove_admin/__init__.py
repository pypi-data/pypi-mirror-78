# ==================================================================
#       文 件 名: __init__.py
#       概    要: DJANGO 后台管理 增强
#       作    者: IT小强 
#       创建时间: 8/4/20 8:36 AM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

PACKAGE_VERSION = '0.1.0'

VERSION = tuple(PACKAGE_VERSION.split("."))

default_app_config = "django_kelove_admin.apps.DjangoKeloveAdminConfig"


class SettingsRegister:
    """
    配置注册
    """

    settings = []

    @classmethod
    def set(cls, settings_cls):
        if not isinstance(settings_cls, str):
            raise ValueError('settings_cls type must be a string')
        cls.settings.append(settings_cls)

    @classmethod
    def get(cls):
        return cls.settings
