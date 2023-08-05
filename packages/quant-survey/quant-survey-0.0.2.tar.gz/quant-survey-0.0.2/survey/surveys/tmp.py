from survey.surveys.survey_creators import SurveyMonkeyCreator

data_fn = r'C:\Users\vahnd\Desktop\work\ps\gy\survey\condensed.xlsx'
metadata_fn = r'C:\Users\vahnd\Desktop\work\ps\gy\survey\survey-metadata.xlsx'
#
data = read_excel(fn, header=[0, 1])
level_0 = data.columns.get_level_values(0).to_series()
level_1 = data.columns.get_level_values(1).to_series()
level_1 = level_1.map(lambda x: '' if x.startswith('Unnamed: ') else x)
data.columns = MultiIndex.from_tuples(
    tuples=[(l0, l1) for l0, l1 in zip(
        level_0.to_list(), level_1.to_list()
    )]
)

creator = SurveyMonkeyCreator(
    survey_name='Tire Survey',
    survey_data_fn=data_fn,
    metadata_fn=metadata_fn
)
survey = creator.run()
