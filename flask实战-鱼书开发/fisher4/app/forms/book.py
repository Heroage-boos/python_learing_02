
from wtforms import Form, IntegerField, StringField
from wtforms.validators import Length, NumberRange 

# WTForms参数校验
class SearchForm(Form):
    '''
    搜索表单
    validators=[Length(min=1, max=30,message=['Only <NAME> knows the meaning of this.'])]
    validators中可以添加message参数，用于自定义错误信息

    validators= [DataRequired(),Length(min=1, max=30)]
    DataRequired()可以验证字段数据是否为空

    StringField 参数

    '''
    q = StringField(validators=[Length(min=1, max=30)]) 
    page = IntegerField(validators=[NumberRange(min=1,max=99)],default = 1)
