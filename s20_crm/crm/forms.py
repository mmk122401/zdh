from crm import models
from django import forms
from django.core.exceptions import ValidationError
import hashlib


class RegForm(forms.ModelForm):
    # 重写密码
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'placeholder': '您的密码'}))
    re_password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'placeholder': '请再次输入您的密码'}))

    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ['is_active']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '您的用户名', 'oncontextmenu': 'return false'}),
            'password': forms.PasswordInput(attrs={'placeholder': '您的密码'}),
            'name': forms.TextInput(attrs={'placeholder': '您的真实姓名'}),
            'mobile': forms.TextInput(attrs={'placeholder': '您的手机号'}),
            'department': forms.TextInput(attrs={'placeholder': '您的Department'}),
        }
        error_messages = {  # 重写错误信息
            'username': {'invalid': '请输入正确的网址'}
        }

    def clean(self):
        # 获取两次密码
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password', '')
        if password == re_password:
            md5 = hashlib.md5()
            md5.update(password.encode('utf8'))
            password = md5.hexdigest()
            self.cleaned_data['password'] = password
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')


class BootStrapModelform(forms.ModelForm):
    def __init__(self, *args, **kwargs):  # 把所有的框添加class样式
        super().__init__(*args, **kwargs)
        for field in self.fields.values():  # 从有序字典中取值
            if isinstance(field, (forms.MultipleChoiceField, forms.BooleanField)):
                continue
            field.widget.attrs['class'] = 'form-control'


class CustomerForm(BootStrapModelform):
    class Meta:
        model = models.Customer
        fields = '__all__'


class ConsultForm(BootStrapModelform):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].choices = [('', '-------------------')] + [(i.pk, str(i)) for i in
                                                                           self.instance.consultant.customers.all()]
        self.fields['consultant'].choices = [(self.instance.consultant.pk, self.instance.consultant)]


class EnrollmentForm(BootStrapModelform):
    class Meta:
        model = models.Enrollment
        fields = '__all__'
        # exclude = ['contract_approved']

    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        self.fields['customer'].choices = [(self.instance.customer_id, self.instance.customer)]


class ClassListForm(BootStrapModelform):
    class Meta:
        model = models.ClassList
        fields = '__all__'


class CourseRecordForm(BootStrapModelform):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseRecordForm, self).__init__(*args, **kwargs)
        # 限制当前的班级
        self.fields['re_class'].choices = [(self.instance.re_class_id, self.instance.re_class)]
        # 限制记录者
        self.fields['recorder'].choices = [(self.instance.recorder_id, self.instance.recorder)]
        # 限制讲师为当前编辑的老师
        self.fields['teacher'].choices = [(teacher.pk, str(teacher)) for teacher in
                                          self.instance.re_class.teachers.all()]


class StudyRecordForm(BootStrapModelform):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'
