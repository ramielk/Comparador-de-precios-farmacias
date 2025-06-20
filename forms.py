from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import re

# Validación personalizada para fortaleza de contraseña
def strong_password(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Debe contener al menos una letra mayúscula')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Debe contener al menos una letra minúscula')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Debe contener al menos un número')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Debe contener al menos un carácter especial')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(), 
        Length(min=4, max=20, message='El usuario debe tener entre 4 y 20 caracteres')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Ingresa un email válido')
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        strong_password  # Validación personalizada de fortaleza
    ])
    
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Por favor confirma tu contraseña'),
        EqualTo('password', message='Las contraseñas no coinciden')
    ])
    
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Ingresa un email válido')
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria')
    ])
    
    submit = SubmitField('Iniciar Sesión')