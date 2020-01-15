from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "이메일 주소 입력(필수)"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 입력(필수)"})
    )
    # clean으로 기본적인 유효성 체크
    # clean_xxx 이렇게 특정 필드로 clean하는 것이 아니면, 에러를 직접 필드마다 추가해줘야한다.
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(email=email)

            if user.check_password(password):
                # clean된 데이터를 통으로 넘겨줌
                return self.cleaned_data
            else:
                # clean을 특정 필드로 한 것이 아니기 때문에, 에러가 어디서 왔는지를 알려줘야한다.
                self.add_error("password", forms.ValidationError("비밀번호를 다시 입력해주세요."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("존재하지 않는 이메일 주소입니다."))


# Form과 ModelForm의 차이는 Meta를 통해 필드를 간편하게 정의하는지 마는지이다.
class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "(필수)이메일 주소 입력"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "(필수)비밀번호 입력"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "(필수)비밀번호 재확인"})
    )
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "(필수)닉네임 입력"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("이미 가입된 이메일 주소입니다.")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("재확인 비밀번호를 다시 입력해주세요.")
        else:
            return password

    def save(self, *args, **kwargs):
        # commit=False : object를 생성하지만, db에 저장하지는 않음
        user = super().save(commit=False)

        return user
