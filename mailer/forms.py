from django import forms

class FileMailForm(forms.Form):
    addressees = forms.CharField(label='收件地址', help_text='Fill in the recipient address, multiple recipient addresses should be separated by commas ","', label_suffix='：',
                                 widget=forms.TextInput(attrs={'style': 'width:440px', 'maxlength': '100'}))
    # 定义收件地址字段，因为支持群发，所以未使用“EmailField”。
    subject = forms.CharField(label='邮件标题', help_text='Fill in your subject', label_suffix='：',
                              widget=forms.TextInput(attrs={'style': 'width:440px', 'maxlength': '100'}))
    # 定义邮件标题字段，指定文本框宽度并限定字符数量。
    message = forms.CharField(label='邮件内容', help_text='Fill in your email content',label_suffix='：', widget=forms.Textarea(attrs={'cols': '60', 'rows': '10'}))
    # 定义邮件内容字段，指定使用文本域（多行文本框）标签，并设置标签的属性。
    file = forms.FileField(label='添加附件', help_text='Add appendix', label_suffix='：')
    # 定义邮件附件的字段。
    cc_myself = forms.BooleanField(label='抄送自己', help_text='Tick to copy email to yourself',label_suffix='：', required=False)
    # 定义抄送给发件人字段，指定为布尔类型（真假值）的字段。

class TextEmailForm(FileMailForm):
    file = None