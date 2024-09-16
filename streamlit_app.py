import streamlit as st
import pandas as pd

# Streamlit app
st.title('Demo: Configurar ND')

# Function to load data
@st.cache_data
def load_data_nf():
    return pd.read_csv('data/nf_cod_servico.csv')

@st.cache_data
def load_data_config():
    return pd.read_csv('data/nf_config.csv')

# Load the data
df = load_data_nf()
df_config = load_data_config()

# Sidebar for user input
st.sidebar.header('Filtros')

# CNAE selection
cnae_options = sorted(df['cnae_nota'].unique().tolist())
selected_cnae = st.sidebar.selectbox('Selecione o CNAE:', cnae_options)

# Filter dataframe based on selected CNAE
df_filtered_cnae = df[df['cnae_nota'] == selected_cnae]

# City selection (dependent on CNAE)
city_options = sorted(df_filtered_cnae['id_cidade_empresa'].unique().tolist())
selected_city = st.sidebar.selectbox('Selecione a Cidade:', city_options)

# Filter dataframe based on selected City
df_filtered_city = df_filtered_cnae[df_filtered_cnae['id_cidade_empresa'] == selected_city]

# Tax regime selection (dependent on CNAE and City)
regime_options = sorted(df_filtered_city['regime_tributacao_empresa'].unique().tolist())
selected_regime = st.sidebar.selectbox('Selecione o Regime Tributário:', regime_options)

# Final filtered dataframe
filtered_df = df_filtered_city[df_filtered_city['regime_tributacao_empresa'] == selected_regime]


# Display results
st.header('Filtros selecionados')
st.write(f"Mostrando resultados para: **CNAE**: {selected_cnae}, **Cidade**: {selected_city}, **Regime Tributário**: {selected_regime}")

# Display top 10 services
st.subheader('Top 10 Códigos de Serviços')
st.table(filtered_df[['id_servico_prestado_nota', 'quantidade_empresas','total_empresas_grupo','quantidade_notas','total_notas_grupo']].sort_values(by=['quantidade_empresas', 'quantidade_notas'], ascending=False).head(10))

# Display results
st.header('Configuração')
st.write('Selecione Código e município para ver a configuração')

service_options = sorted(filtered_df['id_servico_prestado_nota'].dropna().unique().tolist())
selected_service = st.selectbox('Selecione o Código de serviço:', service_options)

filtered_config = df_config[(df_config['cnae_nota'] == selected_cnae) &
                            (df_config['id_cidade_empresa'] == selected_city) &
                            (df_config['regime_tributacao_empresa'] == selected_regime) & 
                            (df_config['id_servico_prestado_nota'] == selected_service)]


city_service_options = sorted(filtered_config['id_local_de_prestacao_nota'].unique().tolist())
selected_city_service = st.selectbox('Selecione a cidade de prestação de serviço:', city_service_options)

final_filtered_config = filtered_config[filtered_config['id_local_de_prestacao_nota'] == selected_city_service]

# Display top 10 Configurações
st.subheader('Top 10 Configurações')
st.table(final_filtered_config[['id_natureza_operacao_do_servico',
                                'aliquota_iss_nota',
                                'iss_retido_nota',
                                'aliquota_inss_nota',
                                'quantidade_empresas',
                                'total_empresas_grupo',
                                'quantidade_notas',
                                'total_notas_grupo']].sort_values(by=['quantidade_empresas', 'quantidade_notas'], ascending=False).head(10))
