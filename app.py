# pip install streamlit pandas matplotlib seaborn
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fonte de Dados
# https://www.kaggle.com/datasets/whenamancodes/student-performance

# Especificando o título da página e o ícone
st.set_page_config(page_title="Dashboard - Student Dataset", page_icon=":books:")

# sidebar
st.sidebar.title("Configurações de Exibição")

gsheets_show_id = st.sidebar.radio("Selecione o Dataset", ("Matemática", "Português"))

st.sidebar.subheader("Selecione o que deseja exibir")
show_dataset = st.sidebar.checkbox("Dados do Dataset")
show_dataset_description = st.sidebar.checkbox("Descrição do Dataset")

graph1_type = st.sidebar.selectbox("Gráfico 1: Selecione o tipo de gráfico", ("Barra", "Pizza", "Dispersão", "Histograma", "Boxplot"))

# Carregando o dataset
gsheets_math_id = "1392993996"
gsheets_portuguese_id = "0"

show_id = gsheets_math_id if gsheets_show_id == "Matemática" else gsheets_portuguese_id

gsheets_url = 'https://docs.google.com/spreadsheets/d/1pfqNNPJrB1QFcqUm5evvDeijycnuPFDztInZvl3nOyU/edit#gid=' + show_id
@st.cache_data(ttl=120)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

data = load_data(gsheets_url)

# Adicionando um título
st.title("Análise de Dados do Dataset de Estudantes")

# Descritivo do dataset
if show_dataset_description:
    st.subheader("Descrição do Dataset")

    st.markdown("""
| Column    | Description                                                                                        |
|-----------|----------------------------------------------------------------------------------------------------|
| school    | Student's school (binary: 'GP' - Gabriel Pereira or 'MS' - Mousinho da Silveira)                   |
| sex       | Student's sex (binary: 'F' - female or 'M' - male)                                               |
| age       | Student's age (numeric: from 15 to 22)                                                            |
| address   | Student's home address type (binary: 'U' - urban or 'R' - rural)                                  |
| famsize   | Family size (binary: 'LE3' - less or equal to 3 or 'GT3' - greater than 3)                         |
| Pstatus   | Parent's cohabitation status (binary: 'T' - living together or 'A' - apart)                       |
| Medu      | Mother's education (numeric: 0 - none, 1 - primary education (4th grade), 2 - 5th to 9th grade, 3 - secondary education or 4 - higher education) |
| Fedu      | Father's education (numeric: 0 - none, 1 - primary education (4th grade), 2 - 5th to 9th grade, 3 - secondary education or 4 - higher education) |
| Mjob      | Mother's job (nominal: 'teacher', 'health' care related, civil 'services' (e.g. administrative or police), 'at_home' or 'other') |
| Fjob      | Father's job (nominal: 'teacher', 'health' care related, civil 'services' (e.g. administrative or police), 'at_home' or 'other') |
| reason    | Reason to choose this school (nominal: close to 'home', school 'reputation', 'course' preference or 'other') |
| guardian  | Student's guardian (nominal: 'mother', 'father' or 'other')                                        |
| traveltime| Home to school travel time (numeric: 1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour) |
| studytime | Weekly study time (numeric: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)   |
| failures  | Number of past class failures (numeric: n if 1<=n<3, else 4)                                       |
| schoolsup | Extra educational support (binary: yes or no)                                                      |
| famsup    | Family educational support (binary: yes or no)                                                     |
| paid      | Extra paid classes within the course subject (Math or Portuguese) (binary: yes or no)               |
| activities| Extra-curricular activities (binary: yes or no)                                                    |
| nursery   | Attended nursery school (binary: yes or no)                                                        |
| higher    | Wants to take higher education (binary: yes or no)                                                 |
| internet  | Internet access at home (binary: yes or no)                                                        |
| romantic  | With a romantic relationship (binary: yes or no)                                                   |
| famrel    | Quality of family relationships (numeric: from 1 - very bad to 5 - excellent)                       |
| freetime  | Free time after school (numeric: from 1 - very low to 5 - very high)                               |
| goout     | Going out with friends (numeric: from 1 - very low to 5 - very high)                               |
| Dalc      | Workday alcohol consumption (numeric: from 1 - very low to 5 - very high)                          |
| Walc      | Weekend alcohol consumption (numeric: from 1 - very low to 5 - very high)                          |
| health    | Current health status (numeric: from 1 - very bad to 5 - very good)                                |
| absences  | Number of school absences (numeric: from 0 to 93)                                                  |
""")            

if show_dataset:
    st.subheader("Conjunto de Dados")
    st.dataframe(data)


# Gráficos e tabelas

# Adicionando uma tabela para mostrar a média de idade dos estudantes por escola
st.subheader("Média de Idade dos Estudantes por Escola")
school_mean_age = data.groupby('school')['age'].mean()
fig, ax = plt.subplots()
sns.barplot(x=school_mean_age.index, y=school_mean_age.values)
ax.set_xlabel('Escola')
ax.set_ylabel('Media da idade dos Estudantes')
st.pyplot(fig)


# Moda do endereço dos alunos na escola MS 
st.subheader("Moda do endereço dos alunos na escola MS")
school_moda_address = data[data.school == 'MS']['address'].mode()
match school_moda_address.values[0]:
    case 'U':
        st.write("Urbano")
    case 'R':
        st.write("Rural")
    case _:
        st.write("Não informado")

################################

# Mediana do tempo de viagem dos alunos que estudam na escola GP 
st.subheader("Mediana do Tempo de Viagem dos Alunos das Escolas")
gp_students = data[data['school'] == 'GP']
ms_students = data[data['school'] == 'MS']

median_travel_time_gp = gp_students['traveltime'].median()
median_travel_time_ms = ms_students['traveltime'].median()

fig, ax = plt.subplots()
sns.barplot(x=['GP', 'MS'], y=[median_travel_time_gp, median_travel_time_ms])
ax.set_ylabel('Tempo de Viagem (Mediana)')
st.pyplot(fig)


# Desvio padrão da idade dos alunos que têm apoio educacional extra na escola MS
st.subheader("Desvio padrão da idade dos alunos que têm apoio educacional extra na escola")
gp_students_extra_support = data[(data['school'] == 'GP') & (data['schoolsup'] == 'yes')]
ms_students_extra_support = data[(data['school'] == 'MS') & (data['schoolsup'] == 'yes')]

std_dev_age_ms = ms_students_extra_support['age'].std()
std_dev_age_gp = gp_students_extra_support['age'].std()

fig, ax = plt.subplots()
sns.barplot(x=['GP','MS'], y=[std_dev_age_gp, std_dev_age_ms])
ax.set_ylabel('Desvio Padrão da Idade')
st.pyplot(fig)


#Média do Tempo Semanal de Estudo dos Alunos com Pais Separados na Escola GP
st.subheader("Média do Tempo Semanal de Estudo dos Alunos com Pais Separados na Escola")
gp_students_parents_apart = data[(data['school'] == 'GP') & (data['Pstatus'] == 'A')]
ms_students_parents_apart = data[(data['school'] == 'MS') & (data['Pstatus'] == 'A')]

mean_study_time_gp = gp_students_parents_apart['studytime'].mean()
mean_study_time_ms = ms_students_parents_apart['studytime'].mean()

fig, ax = plt.subplots()
sns.barplot(x=['GP', 'MS'], y=[mean_study_time_gp, mean_study_time_ms])
ax.set_ylabel('Tempo Semanal de Estudo (Média)')
st.pyplot(fig)

##########################
#Moda do motivo pelo qual os alunos escolheram a escola MS
st.subheader("Moda do motivo pelo qual os alunos escolheram a escola MS")
# Filtrando os dados dos alunos da escola MS
ms_students = data[data['school'] == 'MS']

# Calculando a moda do motivo de escolha para a escola MS
mode_reason_ms = ms_students['reason'].mode()

# Criando uma tabela para mostrar a moda do motivo de escolha
mode_reason_table_ms = pd.DataFrame({'Escola': ['MS'], 'Moda do Motivo de Escolha': [mode_reason_ms]})
mode_reason_table_ms
###########################

#Mediana do número de faltas dos alunos que frequentam a escola GP
st.subheader("Mediana do número de faltas dos alunos que frequentam a escola")
gp_students = data[data['school'] == 'GP']
ms_students = data[data['school'] == 'MS']

median_absences_gp = gp_students['absences'].median()
median_absences_ms = ms_students['absences'].median()

fig, ax = plt.subplots()
sns.barplot(x=['GP', 'MS'], y=[median_absences_gp, median_absences_ms])
ax.set_ylabel('Mediana do Número de Faltas')
st.pyplot(fig)


#Desvio padrão do nível de saúde dos alunos que frequentam atividades extracurriculares na escola MS
st.subheader("Desvio padrão do nível de saúde dos alunos que frequentam atividades extracurriculares na escola MS")
gp_activities_students = data[(data['school'] == 'GP') & (data['activities'] == 'yes')]
ms_activities_students = data[(data['school'] == 'MS') & (data['activities'] == 'yes')]

std_health_gp = gp_activities_students['health'].std()
std_health_ms = ms_activities_students['health'].std()

fig, ax = plt.subplots()
sns.barplot(x=['GP', 'MS'], y=[std_health_gp, std_health_ms])
ax.set_ylabel('Desvio Padrão do Nível de Saúde')
st.pyplot(fig)


#Alunos já cumpriram as horas extracurriculares

#Moda do consumo de álcool dos alunos da escola MS durante a semana de trabalho
st.subheader('Moda do Consumo de Álcool (MS - Semana de Trabalho)')
ms_students = data[data['school'] == 'MS']
workday_alcohol_mode = ms_students['Dalc'].mode()
table = pd.DataFrame({'Moda do Consumo de Álcool (MS - Semana de Trabalho)': workday_alcohol_mode})
st.dataframe(table)
