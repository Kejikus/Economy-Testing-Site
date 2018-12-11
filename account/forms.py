from django import forms
from core.tools import input_choices_enum

GENDER = (
    ('male',   'Мужской'),
    ('female', 'Женский'),
)
GENDER_ENUM = input_choices_enum(GENDER)
EDUCATION = (
    ('basic-general',          'Основное общее образование (9 кл.)'),
    ('secondary-general',      'Среднее (полное) общее образование (10-11 кл.)'),
    ('secondary-professional', 'Среднее профессиональное образование'),
    ('incomplete-higher',      'Неполное высшее (неоконченное образование)'),
    ('higher',                 'Высшее образование'),
    ('scientific-degree',      'Наличие ученой степени'),
)
EDUCATION_ENUM = input_choices_enum(EDUCATION)
ACTIVITY_FIELD = (
    ('economic',          'Экономическая сфера'),
    ('industrial',        'Промышленная сфера'),
    ('financial',         'Финансовая сфера'),
    ('education-science', 'Сфера образования и науки'),
    ('trading',           'Сфера торговли'),
    ('services',          'Сфера услуг'),
    ('agriculture',       'Сельское хозяйство'),
    ('other',             'Другое'),
)
ACTIVITY_FIELD_ENUM = input_choices_enum(ACTIVITY_FIELD)
OCCUPATION = (
    ('schoolboy',               'Школьник'),
    # ('studying',                'Учащийся'),
    ('economic-university',     'Экономический ВУЗ'),
    ('technical-university',    'Технический ВУЗ'),
    ('humanitarian-university', 'Гуманитарный ВУЗ'),
    ('working',                 'Работающий'),
    ('pensioner',               'Пенсионер'),
    ('other',                   'Другое'),
)
OCCUPATION_ENUM = input_choices_enum(OCCUPATION)
ECONOMY_ATTITUDE = (
    ('interested',                'Интересующийся'),
    ('studying-economic-profile', 'Обучающийся по экономическому профилю'),
    ('specialist',                'Профессиональный специалист'),
    ('scientist',                 'Ученый'),
    ('teacher',                   'Преподаватель'),
    ('no-attitude',               'Не имею отношения'),
    ('other',                     'Другое'),
)
ECONOMY_ATTITUDE_ENUM = input_choices_enum(ECONOMY_ATTITUDE)


class RegisterForm(forms.Form):

    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER, label='Пол:', required=True)
    age = forms.IntegerField(min_value=5, max_value=100, label='Возраст:', help_text='Возраст', required=True)
    education = forms.ChoiceField(widget=forms.RadioSelect, choices=EDUCATION, label='Образование:', required=True)
    activity_field = forms.ChoiceField(widget=forms.RadioSelect, choices=ACTIVITY_FIELD, label='Сфера деятельности:',
                                       required=True)
    occupation = forms.ChoiceField(widget=forms.RadioSelect, choices=OCCUPATION, label='Род занятий:', required=True)
    economy_attitude = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=ECONOMY_ATTITUDE,
                                                 label='Отношение к экономике:', required=True)
