# author:klx
# time:2022/5/5 -{TIME}
# function:样式公共组件，
#
from django import forms
class bootstrapModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有插件，添加class
        for name,field in self.fields.items():
            if field.widget.attrs :
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs = {
                    "class": "form-control"
                }