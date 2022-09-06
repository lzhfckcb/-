from blog import models
from django import forms
from django.core.exceptions import ValidationError
from blog.utils.encrypt import md5


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="确认密码"
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "telephone"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        exists = models.UserInfo.objects.filter(name=name).exists()
        if not exists:
            return name
        else:
            raise ValidationError("名称已经被注册！")

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        exists = models.UserInfo.objects.filter(telephone=telephone).exists()
        if not exists:
            return telephone
        else:
            raise ValidationError("手机号已经被注册！")

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致，请重新输入！")
        else:
            return confirm


class Login(forms.ModelForm):
    code = forms.CharField(
        label="验证码",
        required=True,
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password"]

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        return md5_pwd


class FindUserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="确认密码"
    )

    class Meta:
        model = models.UserInfo
        fields = ["password"]

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        exists = models.UserInfo.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与过去的密码一致！！！")
        else:
            return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        print(pwd, confirm)
        if pwd != confirm:
            if pwd:
                raise ValidationError("密码不一致，请重新输入！")
            else:
                return confirm
        else:
            return confirm


class FindTelephone(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["telephone"]

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        exists = models.UserInfo.objects.filter(telephone=telephone).exists()
        if exists:
            return telephone
        else:
            raise ValidationError("手机号未注册！")
