# ==================================================================
#       文 件 名: models.py
#       概    要: 数据模型
#       作    者: IT小强 
#       创建时间: 8/6/20 5:26 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from json import dumps

from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel as BaseMPTTModel

from .conf import settings


class Model(models.Model):
    """
    数据模型基类
    """

    class Meta:
        abstract = True


class CreatedUserModel(Model):
    """
    添加创建用户外键
    """

    # 创建用户
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('创建用户'),
        related_name="%(app_label)s_%(class)s_created_user_set",
        on_delete=getattr(settings, 'DATABASE_FOREIGN_DELETE_TYPE', models.PROTECT),
        db_constraint=getattr(settings, 'DATABASE_CONSTRAINT_USER', False),
        null=True,
        blank=True,
        editable=getattr(settings, 'DATABASE_USER_EDITABLE', False),
        default=None
    )

    class Meta:
        abstract = True


class UpdatedUserModel(Model):
    """
    添加更新用户外键
    """

    # 更新用户
    updated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('更新用户'),
        related_name="%(app_label)s_%(class)s_updated_user_set",
        on_delete=getattr(settings, 'DATABASE_FOREIGN_DELETE_TYPE', models.PROTECT),
        db_constraint=getattr(settings, 'DATABASE_CONSTRAINT_USER', False),
        null=True,
        blank=True,
        editable=getattr(settings, 'DATABASE_USER_EDITABLE', False),
        default=None
    )

    class Meta:
        abstract = True


class CreatedTimeModel(Model):
    """
    添加创建时间
    """

    # 创建时间
    created_time = models.DateTimeField(verbose_name=_('创建时间'), auto_now_add=True, editable=True)

    class Meta:
        abstract = True


class UpdatedTimeModel(Model):
    """
    添加更新时间
    """

    # 更新时间
    updated_time = models.DateTimeField(verbose_name=_('更新时间'), auto_now=True)

    class Meta:
        abstract = True


class StatusModel(Model):
    """
    添加状态字段
    """

    STATUS_CHOICES = settings.DATABASE_STATUS_CHOICES

    # 状态
    status = models.IntegerField(
        verbose_name=_('状态'),
        null=False,
        default=1,
        choices=STATUS_CHOICES,
        help_text=_('状态') + dumps(dict(STATUS_CHOICES), ensure_ascii=False)
    )

    class Meta:
        abstract = True


class EnabledModel(Model):
    """
    添加是否启用字段
    """

    # 是否启用
    enabled = models.BooleanField(
        verbose_name=_('是否启用'),
        default=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class SortModel(Model):
    """
    添加排序字段
    """

    # 排序
    sort = models.IntegerField(
        verbose_name=_('排序'),
        null=False,
        default=0,
    )

    class Meta:
        abstract = True


class NoUserModel(CreatedTimeModel, UpdatedTimeModel, SortModel, StatusModel, EnabledModel):
    """
    数据模型基类（不包括创建用户、更新用户字段）
    """

    class Meta:
        abstract = True


class NoTimeModel(CreatedUserModel, UpdatedUserModel, SortModel, StatusModel, EnabledModel):
    """
    数据模型基类（不包括创建时间、更新时间字段）
    """

    class Meta:
        abstract = True


class OnlyTimeModel(CreatedTimeModel, UpdatedTimeModel):
    """
    数据模型基类（仅包含时间字段）
    """

    class Meta:
        abstract = True


class OnlyUserModel(CreatedUserModel, UpdatedUserModel):
    """
    数据模型基类（仅包含创建、更新用户字段）
    """

    class Meta:
        abstract = True


class AllModel(OnlyUserModel, OnlyTimeModel, StatusModel, EnabledModel, SortModel):
    """
    数据模型基类(添加全部公用字段)
    """

    class Meta:
        abstract = True


class MPTTModel(BaseMPTTModel):
    """
    树形数据模型基类
    """

    # 级别
    level = models.PositiveIntegerField(verbose_name=_('级别'), editable=False)

    class Meta:
        abstract = True


# class UserOTP(OnlyTimeModel):
#     """
#     用户OTP信息存储
#     """
#
#     user = models.OneToOneField(
#         to=settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#
#     otp_device = models.CharField(
#         verbose_name=_('一次性密码设备'),
#         max_length=191,
#         default='',
#         blank=True,
#         null=False,
#         editable=False,
#     )


class Settings(OnlyTimeModel, OnlyUserModel):
    """
    配置表
    """

    settings_key = models.CharField(
        verbose_name=_('配置标识'),
        unique=True,
        db_index=True,
        max_length=191,
        blank=False,
        null=False
    )

    settings_title = models.CharField(
        verbose_name=_('配置名称'),
        max_length=191,
        default='',
        blank=True,
        null=False
    )

    settings_val = models.JSONField(
        verbose_name=_('配置内容'),
        default=dict,
        null=False,
        blank=True
    )

    def __str__(self):
        return '%s | %s' % (self.settings_title, self.settings_key)

    class Meta:
        verbose_name = _('配置')
        verbose_name_plural = _('配置管理')
        permissions = (
            ('ck_finder_folder_view', _('ck_finder_folder_view')),
            ('ck_finder_folder_create', _('ck_finder_folder_create')),
            ('ck_finder_folder_rename', _('ck_finder_folder_rename')),
            ('ck_finder_folder_delete', _('ck_finder_folder_delete')),
            ('ck_finder_file_view', _('ck_finder_file_view')),
            ('ck_finder_file_create', _('ck_finder_file_create')),
            ('ck_finder_file_rename', _('ck_finder_file_rename')),
            ('ck_finder_file_delete', _('ck_finder_file_delete')),
            ('ck_finder_image_resize', _('ck_finder_image_resize')),
            ('ck_finder_image_resize_custom', _('ck_finder_image_resize_custom')),
        )
