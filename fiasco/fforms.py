from wtforms import Form, TextAreaField, TextField, SelectField, validators

class NewPlayset(Form):
	name = TextField('Playset Name', [validators.Length(min=4, max=100), validators.Required()])
	description = TextAreaField('Description', [validators.Length(min=4), validators.Required()])

class NewGame(Form):
	name = TextField('Game Name', [validators.Length(min=4, max=50), validators.Required()])
	playset = SelectField('Choose a Playset', coerce=int)

class EditPlayset(Form):
	name = TextField('Playset Name', [validators.Length(min=4, max=100), validators.Required()])
	description = TextAreaField('Description', [validators.Length(min=4), validators.Required()])

