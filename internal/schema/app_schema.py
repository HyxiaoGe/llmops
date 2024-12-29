from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionRequestForm(FlaskForm):
    query = StringField('query', validators=[DataRequired(message="输入内容不能为空"),
                                             Length(max=2000, message="输入内容的最大长度不能超过2000")])
