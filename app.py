import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import sys
import streamlit.components.v1 as components

def create_responsive_layout_config():
    """
    Retorna configuração de layout responsivo para todos os gráficos Plotly.
    Adapta-se automaticamente ao tamanho da tela.
    """
    return dict(
        autosize=True,
        margin=dict(l=80, r=40, t=60, b=100, pad=10),  
        plot_bgcolor='rgba(248, 242, 230, 0.3)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, family='Arial'),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial',
            bordercolor='rgba(196, 166, 114, 0.4)'
        )
    )

def calculate_responsive_height(num_items, min_height=400, item_height=35, max_height=900):
    """
    Calcula altura responsiva baseada no número de itens.
    
    Args:
        num_items: Número de itens no gráfico
        min_height: Altura mínima em pixels
        item_height: Altura por item em pixels
        max_height: Altura máxima em pixels
    
    Returns:
        Altura calculada em pixels
    """
    calculated = num_items * item_height + 150
    return max(min_height, min(calculated, max_height))

st.set_page_config(
    page_title="Análise de Riscos Psicossociais - NR-01",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f1e8 0%, #e8dcc8 100%) !important;
    }
    
    .block-container {
        background: transparent !important;
        padding-top: 2rem !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f1e8 0%, #e8dcc8 100%) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1e293b;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    h2 {
        color: #334155;
        font-weight: 600;
    }
    .narrative-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .insight-card {
        background: white;
        padding: 18px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .warning-banner {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        text-align: center;
        font-weight: 600;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

def carregar_dados():
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).parent
    
    archives_dir = base_dir / 'archives'
    panorama_data = pd.read_csv(archives_dir / 'panorama_semaforo.csv')
    ranking_data = pd.read_csv(archives_dir / 'ranking_subescalas_criticas.csv')
    cargo_data = pd.read_csv(archives_dir / 'subescala_por_cargo.csv')
    setor_data = pd.read_csv(archives_dir / 'subescala_por_setor.csv')
    matriz_data = pd.read_csv(archives_dir / 'matriz_risco.csv')
    detalhamento_data = pd.read_csv(archives_dir / 'detalhamento_geral.csv')
    
    return panorama_data, ranking_data, cargo_data, setor_data, matriz_data, detalhamento_data

def get_risk_color(value, tipo='score'):
    if tipo == 'perc':
        if value >= 0.7:
            return '#dc2626'
        elif value >= 0.5:
            return '#ea580c'
        elif value >= 0.3:
            return '#f59e0b'
        else:
            return '#10b981'
    else:
        if value >= 4:
            return '#dc2626'
        elif value >= 3:
            return '#ea580c'
        elif value >= 2:
            return '#f59e0b'
        else:
            return '#10b981'

def get_risk_color_classe(classe):
    cores = {
        'alto': '#dc2626',
        'medio': '#f59e0b',
        'baixo': '#10b981'
    }
    return cores.get(classe, '#6b7280')

import base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

## dados geral
panorama_data, ranking_data, cargo_data, setor_data, matriz_data, detalhamento_data = carregar_dados()

## CSS sidebar

logo_base64 = get_base64_image("archives/logo.png")
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Carregar a logo
logo_base64 = get_base64_image("archives/logo.png")  # Ajuste o nome do arquivo se necessário

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            #c9baa9 0%, 
            #d4c4a8 20%, 
            #e8dcc8 40%, 
            #f0e6d2 50%, 
            #e8dcc8 60%, 
            #d4c4a8 80%, 
            #c9baa9 100%) !important;
        border-radius: 0 30px 30px 0 !important;
        box-shadow: 8px 0 40px rgba(0, 0, 0, 0.15), 
                    inset -2px 0 20px rgba(255, 255, 255, 0.5),
                    inset 2px 0 30px rgba(184, 148, 102, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 245, 220, 0.4) 0%, transparent 70%);
        animation: pulse 12s ease-in-out infinite;
    }
    
    [data-testid="stSidebar"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 3px,
                rgba(212, 180, 130, 0.03) 3px,
                rgba(212, 180, 130, 0.03) 6px
            );
        pointer-events: none;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.5; }
        50% { transform: scale(1.1) rotate(180deg); opacity: 0.8; }
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
        padding: 2rem 1.25rem;
        position: relative;
        z-index: 1;
    }
    
    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        padding: 1.1rem 1.4rem !important;
        margin: 0.45rem 0 !important;
        border: none !important;
        border-radius: 16px !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.7) 0%, rgba(248, 242, 230, 0.6) 100%) !important;
        color: #6b5847 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(184, 148, 102, 0.25) !important;
        box-shadow: 0 2px 8px rgba(107, 88, 71, 0.12), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="stSidebar"] .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212, 180, 130, 0.3), transparent);
        transition: left 0.6s;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, rgba(212, 180, 130, 0.35) 0%, rgba(196, 166, 114, 0.35) 100%) !important;
        transform: translateX(10px) scale(1.02) !important;
        border-color: rgba(184, 148, 102, 0.5) !important;
        box-shadow: 0 8px 24px rgba(184, 148, 102, 0.25), 
                    0 0 30px rgba(212, 180, 130, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
        color: #5a4a3a !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover::before {
        left: 100%;
    }
    
    [data-testid="stSidebar"] .stButton button:active {
        transform: translateX(8px) scale(0.99) !important;
        box-shadow: 0 4px 12px rgba(184, 148, 102, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stButton button[kind="primary"],
    [data-testid="stSidebar"] .stButton button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, #c4a672 0%, #b89656 35%, #a88846 70%, #987a36 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-color: rgba(152, 122, 54, 0.5) !important;
        box-shadow: 0 8px 32px rgba(168, 136, 70, 0.45), 
                    0 0 40px rgba(196, 166, 114, 0.3),
                    inset 0 2px 4px rgba(255, 255, 255, 0.3),
                    inset 0 -2px 4px rgba(0, 0, 0, 0.15) !important;
        position: relative !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stButton button[kind="primary"]::after {
        content: '';
        position: absolute;
        right: 1.2rem;
        top: 50%;
        transform: translateY(-50%);
        width: 8px;
        height: 8px;
        background: #ffffff;
        border-radius: 50%;
        box-shadow: 0 0 12px rgba(255, 255, 255, 0.9), 
                    0 0 20px rgba(255, 255, 255, 0.6);
        animation: blink 2.5s ease-in-out infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; transform: translateY(-50%) scale(1); }
        50% { opacity: 0.5; transform: translateY(-50%) scale(1.3); }
    }
    
    [data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #d0b080 0%, #c4a672 35%, #b89656 70%, #a88846 100%) !important;
        transform: translateX(10px) scale(1.02) !important;
        box-shadow: 0 10px 40px rgba(168, 136, 70, 0.55), 
                    0 0 50px rgba(196, 166, 114, 0.4),
                    inset 0 2px 4px rgba(255, 255, 255, 0.35) !important;
    }
    
    [data-testid="stSidebar"] .stButton button:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(184, 148, 102, 0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

## SIDEBAR
with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center; padding: 2.5rem 1rem 2rem 1rem; background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 242, 230, 0.7) 100%); border-radius: 24px; backdrop-filter: blur(15px); margin-bottom: 2.5rem; border: 2px solid rgba(196, 166, 114, 0.3); box-shadow: 0 8px 32px rgba(107, 88, 71, 0.15), inset 0 2px 4px rgba(255, 255, 255, 0.9), 0 0 60px rgba(212, 180, 130, 0.2); position: relative; overflow: hidden;'>
            <div style='position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(212, 180, 130, 0.15) 0%, transparent 70%); animation: rotate 15s linear infinite;'></div>
            <div style='position: relative; z-index: 1;'>
                <img src="data:image/png;base64,{logo_base64}" alt="Logo" style='width: clamp(100px, 25vw, 150px); height: auto; margin-bottom: 1rem; filter: drop-shadow(0 4px 12px rgba(168, 136, 70, 0.3)); border-radius: 12px;'/>
                <p style='margin: 0 0 1.5rem 0; font-size: clamp(0.9rem, 2.2vw, 1.1rem); color: #6b5847; font-weight: 600; letter-spacing: 1px; text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);'>Luana Portella</p>
                <div style='height: 2px; width: clamp(50px, 15vw, 70px); margin: 1.2rem auto; background: linear-gradient(90deg, transparent, #c4a672, transparent); box-shadow: 0 0 8px rgba(196, 166, 114, 0.5);'></div>
                <p style='margin: 0; font-size: clamp(0.65rem, 1.8vw, 0.8rem); color: #6b5847; font-weight: 700; letter-spacing: clamp(1.5px, 0.5vw, 2.5px); text-transform: uppercase; text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);'>Gestão dos Fatores de Riscos Psicossociais</p>
            </div>
        </div>
        <style>
        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style='margin-bottom: 1.25rem; padding-left: 0.5rem;'>
            <div style='display: inline-block; padding: 0.5rem 1.2rem;
                        background: linear-gradient(135deg, rgba(196, 166, 114, 0.25) 0%, rgba(184, 148, 102, 0.2) 100%);
                        border-radius: 20px;
                        border: 1px solid rgba(184, 148, 102, 0.35);
                        box-shadow: 0 3px 10px rgba(107, 88, 71, 0.15), 
                                    inset 0 1px 0 rgba(255, 255, 255, 0.7);'>
                <p style='margin: 0; color: #6b5847; font-size: 0.68rem; 
                          text-transform: uppercase; letter-spacing: 2.5px; 
                          font-weight: 800;
                          text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);'>
                    Navegação
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if 'pagina_selecionada' not in st.session_state:
        st.session_state.pagina_selecionada = "Panorama Geral"
    
    paginas = [
        "Panorama Geral",
        "Priorização de Riscos",
        "Análise por Cargo",
        "Análise por Setor",
        "Matriz de Risco",
        "Detalhamento & Ações"
    ]
    
    for pagina_item in paginas:
        if st.button(
            pagina_item,
            key=f"nav_{pagina_item}",
            use_container_width=True,
            type="primary" if st.session_state.pagina_selecionada == pagina_item else "secondary"
        ):
            st.session_state.pagina_selecionada = pagina_item
            st.rerun()
    
    pagina = st.session_state.pagina_selecionada
    
    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.75) 0%, rgba(248, 242, 230, 0.65) 100%); 
                    padding: 1.5rem; 
                    border-radius: 20px; 
                    margin-bottom: 2rem;
                    border: 2px solid rgba(196, 166, 114, 0.3);
                    backdrop-filter: blur(10px);
                    box-shadow: 0 6px 24px rgba(107, 88, 71, 0.12), 
                                inset 0 2px 4px rgba(255, 255, 255, 0.8);
                    position: relative;'>
            <div style='display: flex; align-items: center; margin-bottom: 1.25rem; gap: 0.75rem;'>
                <div style='width: 42px; height: 42px; 
                            background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);
                            border-radius: 12px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(168, 136, 70, 0.35), 
                                        inset 0 1px 0 rgba(255, 255, 255, 0.4);'>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5">
                        <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                    </svg>
                </div>
                <p style='margin: 0; color: #6b5847; font-weight: 800; font-size: 0.8rem; 
                          text-transform: uppercase; letter-spacing: 1.8px;
                          text-shadow: 0 1px 2px rgba(255, 255, 255, 0.7);'>
                    Conforme NR-01
                </p>
            </div>
            <div style='background: rgba(255, 255, 255, 0.5); 
                        padding: 1.3rem; 
                        border-radius: 14px;
                        border-left: 3px solid #b89656;
                        box-shadow: inset 0 1px 3px rgba(107, 88, 71, 0.1);'>
                <p style='margin: 0 0 1rem 0; font-weight: 700; color: #5a4a3a; font-size: 0.85rem;
                          text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);'>
                    Narrativa estruturada:
                </p>
                <div style='color: #6b5847; font-size: 0.85rem; line-height: 2;'>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <div style='width: 7px; height: 7px; background: #b89656; border-radius: 50%; margin-right: 0.85rem;
                                    box-shadow: 0 0 6px rgba(184, 150, 86, 0.6);'></div>
                        <span>Identificação do cenário</span>
                    </div>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <div style='width: 7px; height: 7px; background: #b89656; border-radius: 50%; margin-right: 0.85rem;
                                    box-shadow: 0 0 6px rgba(184, 150, 86, 0.6);'></div>
                        <span>Caracterização dos riscos</span>
                    </div>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <div style='width: 7px; height: 7px; background: #b89656; border-radius: 50%; margin-right: 0.85rem;
                                    box-shadow: 0 0 6px rgba(184, 150, 86, 0.6);'></div>
                        <span>Hierarquização</span>
                    </div>
                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                        <div style='width: 7px; height: 7px; background: #b89656; border-radius: 50%; margin-right: 0.85rem;
                                    box-shadow: 0 0 6px rgba(184, 150, 86, 0.6);'></div>
                        <span>Contextualização</span>
                    </div>
                    <div style='display: flex; align-items: center;'>
                        <div style='width: 7px; height: 7px; background: #b89656; border-radius: 50%; margin-right: 0.85rem;
                                    box-shadow: 0 0 6px rgba(184, 150, 86, 0.6);'></div>
                        <span>Fundamentação de ações</span>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Divider suave
    st.markdown("""
        <div style='position: relative; height: 1px; margin: 2.5rem 0;'>
            <div style='position: absolute; width: 100%; height: 1px;
                        background: linear-gradient(90deg, transparent, rgba(184, 148, 102, 0.4), transparent);
                        box-shadow: 0 0 8px rgba(184, 148, 102, 0.3);'></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; padding: 1.3rem;
                    background: linear-gradient(135deg, rgba(255, 255, 255, 0.7) 0%, rgba(248, 242, 230, 0.6) 100%);
                    border-radius: 18px;
                    border: 2px solid rgba(196, 166, 114, 0.25);
                    backdrop-filter: blur(10px);
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.12), 
                                inset 0 2px 4px rgba(255, 255, 255, 0.8);'>
            <div style='display: inline-block; padding: 0.5rem 1.2rem;
                        background: linear-gradient(135deg, rgba(196, 166, 114, 0.3) 0%, rgba(184, 148, 102, 0.25) 100%);
                        border-radius: 20px;
                        margin-bottom: 0.75rem;
                        border: 1px solid rgba(184, 148, 102, 0.3);
                        box-shadow: 0 2px 6px rgba(107, 88, 71, 0.1), 
                                    inset 0 1px 0 rgba(255, 255, 255, 0.6);'>
                <p style='margin: 0; color: #6b5847; font-size: 0.75rem; font-weight: 800;
                          letter-spacing: 1.2px;
                          text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);'>
                    Dashboard v1.0
                </p>
            </div>
            <p style='margin: 0.5rem 0; color: #8b7663; font-size: 0.7rem; font-weight: 500;'>
                Janeiro 2026
            </p>
            <div style='height: 1px; width: 50%; margin: 1rem auto;
                        background: linear-gradient(90deg, transparent, rgba(184, 148, 102, 0.35), transparent);'></div>
            <p style='margin: 0; color: #6b5847; font-size: 0.7rem; font-weight: 700;
                      letter-spacing: 2px;
                      text-shadow: 0 1px 2px rgba(255, 255, 255, 0.6);'>
                LUANA PORTELLA
            </p>
        </div>
    """, unsafe_allow_html=True)


####### PANORAMA GERAL ########
if pagina == "Panorama Geral":
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 100%;
            padding: clamp(0.5rem, 2vw, 2rem);
        }
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem;
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        
        [data-testid="stExpander"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 242, 230, 0.6) 100%);
            border: 1px solid rgba(196, 166, 114, 0.3);
            border-radius: 10px;
        }
        
        [data-testid="stExpander"] summary {
            color: #5a4a3a !important;
            font-weight: 600;
        }
        
        .stMultiSelect [data-baseweb="select"] {
            min-height: 38px;
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stMultiSelect [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #c4a672 !important;
            color: white !important;
            border-radius: 6px;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stSlider [data-baseweb="slider"] [role="slider"] {
            background-color: #c4a672 !important;
        }
        
        .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
            background: linear-gradient(90deg, #c4a672 0%, #b89656 100%);
        }
        
        .stCheckbox label {
            color: #5a4a3a;
            font-weight: 500;
        }
        
        .stCheckbox [data-testid="stCheckbox"] {
            accent-color: #c4a672;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.12) 0%, rgba(232, 220, 200, 0.08) 100%);
                    padding: clamp(1rem, 3vw, 1.5rem) clamp(1.5rem, 4vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    margin-bottom: 2rem;
                    border-left: 4px solid #c4a672;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;'>
                <div style='flex: 1; min-width: 200px;'>
                    <h1 style='margin: 0; color: #5a4a3a; font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: 800; letter-spacing: -0.5px;'>
                        Panorama Geral
                    </h1>
                    <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.85rem, 2vw, 1rem);'>
                        Identificação e caracterização dos riscos psicossociais
                    </p>
                </div>
                <div style='background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);
                            padding: 0.7rem 1.3rem;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 12px rgba(168, 136, 70, 0.3);'>
                    <div style='color: rgba(255, 255, 255, 0.85); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;'>
                        CONFORME
                    </div>
                    <div style='color: white; font-size: 1.3rem; font-weight: 800; letter-spacing: 1.5px;'>
                        NR-01
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Filtros e Configurações", expanded=False):
        filter_cols = st.columns([1, 1, 1, 1])
        
        with filter_cols[0]:
            unique_subescalas = sorted(panorama_data['subescala'].unique().tolist())
            selected_subescalas = st.multiselect(
                "Fatores Psicossociais",
                options=unique_subescalas,
                default=unique_subescalas,
                help="Selecione os fatores que deseja analisar"
            )
        
        with filter_cols[1]:
            risk_options = ['baixo', 'medio', 'alto']
            risk_labels = {'baixo': 'Baixo Risco', 'medio': 'Médio Risco', 'alto': 'Alto Risco'}
            available_risks = [r for r in risk_options if r in panorama_data['classe_risco'].unique()]
            selected_risks = st.multiselect(
                "Níveis de Risco",
                options=available_risks,
                default=available_risks,
                format_func=lambda x: risk_labels.get(x, x),
                help="Filtre por nível de risco"
            )
        
        with filter_cols[2]:
            ordenacao_options = ['Maior Risco', 'Menor Risco', 'Alfabética A-Z', 'Alfabética Z-A']
            selected_ordenacao = st.selectbox(
                "Ordenação",
                options=ordenacao_options,
                help="Escolha como ordenar os dados"
            )
        
        with filter_cols[3]:
            show_percentages = st.checkbox("Exibir Percentuais", value=True, help="Mostrar percentuais nos gráficos")
    
    filtered_panorama = panorama_data[
        (panorama_data['subescala'].isin(selected_subescalas)) &
        (panorama_data['classe_risco'].isin(selected_risks))
    ]
    
    if len(filtered_panorama) == 0:
        st.warning("Nenhum dado encontrado com os filtros selecionados. Ajuste os filtros acima.")
        st.stop()
    
    total_respondentes = filtered_panorama.groupby('subescala')['qtd'].sum().iloc[0] if len(filtered_panorama) > 0 else 0
    total_subscalas = filtered_panorama['subescala'].nunique()
    
    panorama_pivot = filtered_panorama.pivot_table(
        index='subescala', columns='classe_risco', values='qtd', fill_value=0
    )
    panorama_pivot['total'] = panorama_pivot.sum(axis=1)
    
    if 'alto' in panorama_pivot.columns:
        panorama_pivot['alto_perc'] = (panorama_pivot['alto'] / panorama_pivot['total'] * 100).round(1)
        fatores_criticos = len(panorama_pivot[panorama_pivot['alto_perc'] >= 50])
    else:
        panorama_pivot['alto_perc'] = 0
        fatores_criticos = 0
    
    total_baixo = panorama_pivot['baixo'].sum() if 'baixo' in panorama_pivot.columns else 0
    total_medio = panorama_pivot['medio'].sum() if 'medio' in panorama_pivot.columns else 0
    total_alto = panorama_pivot['alto'].sum() if 'alto' in panorama_pivot.columns else 0
    total_geral = total_baixo + total_medio + total_alto
    
    perc_baixo = (total_baixo / total_geral * 100) if total_geral > 0 else 0
    perc_medio = (total_medio / total_geral * 100) if total_geral > 0 else 0
    perc_alto = (total_alto / total_geral * 100) if total_geral > 0 else 0
    
    kpi_cols = st.columns(4)
    
    with kpi_cols[0]:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(196, 166, 114, 0.25);
                        box-shadow: 0 3px 12px rgba(107, 88, 71, 0.1);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Fatores Avaliados
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #c4a672; line-height: 1; margin-bottom: 0.4rem;'>
                    {total_subscalas}
                </div>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Dimensões COPSOQ
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 226, 226, 0.95) 0%, rgba(252, 205, 205, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(220, 38, 38, 0.3);
                        box-shadow: 0 3px 12px rgba(220, 38, 38, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Alto Risco
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #dc2626; line-height: 1; margin-bottom: 0.4rem;'>
                    {fatores_criticos}
                </div>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Fatores críticos (&gt;50%)
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(196, 166, 114, 0.25);
                        box-shadow: 0 3px 12px rgba(107, 88, 71, 0.1);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Participação
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #b89656; line-height: 1; margin-bottom: 0.4rem;'>
                    {total_respondentes}
                </div>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Colaboradores respondentes
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        taxa = int((total_respondentes / 215) * 100) if total_respondentes > 0 else 0
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(209, 250, 229, 0.95) 0%, rgba(187, 247, 208, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(16, 185, 129, 0.3);
                        box-shadow: 0 3px 12px rgba(16, 185, 129, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #065f46; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Taxa de Adesão
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #10b981; line-height: 1; margin-bottom: 0.4rem;'>
                    {taxa}%
                </div>
                <div style='color: #065f46; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    +12pp acima da meta
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.1) 0%, rgba(232, 220, 200, 0.06) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border-left: 4px solid #c4a672;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <h3 style='margin: 0 0 1.5rem 0; color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Entendendo o Cenário
            </h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: clamp(1rem, 3vw, 2rem);'>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Problema Resolvido
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Percepções fragmentadas transformadas em <strong>diagnóstico estruturado e mensurável</strong>
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Pergunta Respondida
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6; font-style: italic;'>
                        "Qual o real estado psicossocial da organização hoje?"
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Valor Estratégico
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Base objetiva para <strong>identificação e caracterização</strong> conforme NR-01
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(196, 166, 114, 0.2);
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);
                    margin-bottom: 2rem;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;'>
                <div style='flex: 1; min-width: 250px;'>
                    <h3 style='margin: 0; color: #5a4a3a; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                        Semáforo de Risco por Fator Psicossocial
                    </h3>
                    <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                        Distribuição percentual de colaboradores por nível de risco em cada dimensão
                    </p>
                </div>
                <div style='display: flex; gap: clamp(0.8rem, 2vw, 1.5rem); font-size: clamp(0.75rem, 1.8vw, 0.85rem); flex-wrap: wrap;'>
                    <div style='display: flex; align-items: center; gap: 0.5rem;'>
                        <div style='width: 14px; height: 14px; background: #10b981; border-radius: 3px;'></div>
                        <span style='color: #6b5847; font-weight: 600;'>Baixo Risco</span>
                    </div>
                    <div style='display: flex; align-items: center; gap: 0.5rem;'>
                        <div style='width: 14px; height: 14px; background: #f59e0b; border-radius: 3px;'></div>
                        <span style='color: #6b5847; font-weight: 600;'>Médio Risco</span>
                    </div>
                    <div style='display: flex; align-items: center; gap: 0.5rem;'>
                        <div style='width: 14px; height: 14px; background: #dc2626; border-radius: 3px;'></div>
                        <span style='color: #6b5847; font-weight: 600;'>Alto Risco</span>
                    </div>
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    for col in ['baixo', 'medio', 'alto']:
        if col in panorama_pivot.columns:
            panorama_pivot[f'{col}_perc'] = (panorama_pivot[col] / panorama_pivot['total'] * 100).round(1)
    
    if selected_ordenacao == 'Maior Risco':
        panorama_pivot = panorama_pivot.sort_values('alto_perc', ascending=True)
    elif selected_ordenacao == 'Menor Risco':
        panorama_pivot = panorama_pivot.sort_values('alto_perc', ascending=False)
    elif selected_ordenacao == 'Alfabética A-Z':
        panorama_pivot = panorama_pivot.sort_index(ascending=True)
    elif selected_ordenacao == 'Alfabética Z-A':
        panorama_pivot = panorama_pivot.sort_index(ascending=False)
    
    num_items = len(panorama_pivot)
    chart_height = calculate_responsive_height(num_items, min_height=400, item_height=40)
    layout_config = create_responsive_layout_config()

    fig1 = go.Figure()

    if 'baixo_perc' in panorama_pivot.columns and not panorama_pivot['baixo_perc'].empty:
        fig1.add_trace(go.Bar(
            name='Baixo Risco',
            y=panorama_pivot.index,
            x=panorama_pivot['baixo_perc'],
            orientation='h',
            marker=dict(color='#10b981', line=dict(width=0)),
            text=panorama_pivot['baixo_perc'].apply(lambda x: f'{x:.0f}%' if show_percentages and x >= 4 else ''),
            textposition='inside',
            textfont=dict(color='white', size=13, family='Arial', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Baixo Risco: %{x:.1f}%<extra></extra>'
        ))

    if 'medio_perc' in panorama_pivot.columns and not panorama_pivot['medio_perc'].empty:
        fig1.add_trace(go.Bar(
            name='Médio Risco',
            y=panorama_pivot.index,
            x=panorama_pivot['medio_perc'],
            orientation='h',
            marker=dict(color='#f59e0b', line=dict(width=0)),
            text=panorama_pivot['medio_perc'].apply(lambda x: f'{x:.0f}%' if show_percentages and x >= 4 else ''),
            textposition='inside',
            textfont=dict(color='white', size=13, family='Arial', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Médio Risco: %{x:.1f}%<extra></extra>'
        ))

    if 'alto_perc' in panorama_pivot.columns and not panorama_pivot['alto_perc'].empty:
        fig1.add_trace(go.Bar(
            name='Alto Risco',
            y=panorama_pivot.index,
            x=panorama_pivot['alto_perc'],
            orientation='h',
            marker=dict(color='#dc2626', line=dict(width=0)),
            text=panorama_pivot['alto_perc'].apply(lambda x: f'{x:.0f}%' if show_percentages and x >= 4 else ''),
            textposition='inside',
            textfont=dict(color='white', size=13, family='Arial', weight='bold'),
            hovertemplate='<b>%{y}</b><br>Alto Risco: %{x:.1f}%<extra></extra>'
        ))

    fig1.update_layout(
        **layout_config,
        barmode='stack',
        height=chart_height,
        showlegend=False,
        xaxis=dict(
            range=[0, 100],
            gridcolor='rgba(196, 166, 114, 0.2)',
            showline=False,
            ticksuffix='%',
            tickfont=dict(size=13, color='#6b5847', family='Arial', weight='bold')
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#5a4a3a', family='Arial', weight='bold'),
            showline=False
        )
    )

    st.plotly_chart(fig1, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_alert, col_dist = st.columns([2, 1])
    
    with col_alert:
        if len(panorama_pivot) > 0 and 'alto_perc' in panorama_pivot.columns:
            maior_risco = panorama_pivot['alto_perc'].idxmax()
            valor_maior = panorama_pivot['alto_perc'].max()
            
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                            padding: clamp(1rem, 3vw, 1.5rem) clamp(1.5rem, 4vw, 2rem);
                            border-radius: clamp(10px, 2vw, 14px);
                            box-shadow: 0 6px 20px rgba(220, 38, 38, 0.25);
                            height: 100%;
                            display: flex;
                            align-items: center;'>
                    <div style='display: flex; align-items: center; gap: clamp(1rem, 2vw, 1.5rem); width: 100%; flex-wrap: wrap;'>
                        <div style='min-width: 50px; height: 50px;
                                    background: rgba(255, 255, 255, 0.15);
                                    border-radius: 10px;
                                    display: flex; align-items: center; justify-content: center;'>
                            <svg width="28" height="28" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                                <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                            </svg>
                        </div>
                        <div style='flex: 1; min-width: 200px;'>
                            <div style='color: rgba(255, 255, 255, 0.85); font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.4rem;'>
                                Fator Mais Crítico
                            </div>
                            <div style='color: white; font-size: clamp(1rem, 2.5vw, 1.15rem); font-weight: 700; line-height: 1.4;'>
                                <strong>{maior_risco}</strong> com <span style='font-size: clamp(1.3rem, 3vw, 1.5rem); font-weight: 800;'>{valor_maior:.1f}%</span> em alto risco
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col_dist:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(196, 166, 114, 0.2);
                        height: 100%;'>
                <h4 style='margin: 0 0 1.2rem 0; color: #5a4a3a; font-size: clamp(0.9rem, 2vw, 1rem); font-weight: 700;'>
                    Distribuição Geral
                </h4>
                <div style='margin-bottom: 1rem;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 0.4rem;'>
                        <span style='color: #10b981; font-weight: 700; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>Baixo</span>
                        <span style='color: #5a4a3a; font-weight: 800; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>{perc_baixo:.1f}%</span>
                    </div>
                    <div style='background: #e8dcc8; height: 10px; border-radius: 5px; overflow: hidden;'>
                        <div style='background: #10b981; height: 100%; width: {perc_baixo}%; transition: width 0.3s;'></div>
                    </div>
                </div>
                <div style='margin-bottom: 1rem;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 0.4rem;'>
                        <span style='color: #f59e0b; font-weight: 700; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>Médio</span>
                        <span style='color: #5a4a3a; font-weight: 800; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>{perc_medio:.1f}%</span>
                    </div>
                    <div style='background: #e8dcc8; height: 10px; border-radius: 5px; overflow: hidden;'>
                        <div style='background: #f59e0b; height: 100%; width: {perc_medio}%; transition: width 0.3s;'></div>
                    </div>
                </div>
                <div>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 0.4rem;'>
                        <span style='color: #dc2626; font-weight: 700; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>Alto</span>
                        <span style='color: #5a4a3a; font-weight: 800; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>{perc_alto:.1f}%</span>
                    </div>
                    <div style='background: #e8dcc8; height: 10px; border-radius: 5px; overflow: hidden;'>
                        <div style='background: #dc2626; height: 100%; width: {perc_alto}%; transition: width 0.3s;'></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    col_prox1, col_prox2 = st.columns(2)
    
    with col_prox1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(219, 234, 254, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(59, 130, 246, 0.25);
                        border-left: 4px solid #3b82f6;
                        box-shadow: 0 3px 12px rgba(59, 130, 246, 0.1);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 42px; height: 42px;
                                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M9 5l7 7-7 7"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #1e40af; font-size: clamp(0.95rem, 2vw, 1.05rem); font-weight: 700;'>
                        Próximo Passo
                    </h4>
                </div>
                <p style='margin: 0; color: #1e3a8a; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                    Acesse <strong>Priorização de Riscos</strong> para definir cronograma estratégico de intervenções
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_prox2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(209, 250, 229, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(16, 185, 129, 0.25);
                        border-left: 4px solid #10b981;
                        box-shadow: 0 3px 12px rgba(16, 185, 129, 0.1);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 42px; height: 42px;
                                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #065f46; font-size: clamp(0.95rem, 2vw, 1.05rem); font-weight: 700;'>
                        Conformidade NR-01
                    </h4>
                </div>
                <p style='margin: 0; color: #064e3b; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                    Atende requisitos de <strong>identificação</strong> e <strong>caracterização</strong> de riscos
                </p>
            </div>
        """, unsafe_allow_html=True)

elif pagina == "Priorização de Riscos":
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 100%;
            padding: clamp(0.5rem, 2vw, 2rem);
        }
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem;
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        
        [data-testid="stExpander"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 242, 230, 0.6) 100%);
            border: 1px solid rgba(196, 166, 114, 0.3);
            border-radius: 10px;
        }
        
        [data-testid="stExpander"] summary {
            color: #5a4a3a !important;
            font-weight: 600;
        }
        
        .stMultiSelect [data-baseweb="select"] {
            min-height: 38px;
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stMultiSelect [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #c4a672 !important;
            color: white !important;
            border-radius: 6px;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stSlider [data-baseweb="slider"] [role="slider"] {
            background-color: #c4a672 !important;
        }
        
        .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
            background: linear-gradient(90deg, #c4a672 0%, #b89656 100%);
        }
        
        .stCheckbox label {
            color: #5a4a3a;
            font-weight: 500;
        }
        
        .stCheckbox [data-testid="stCheckbox"] {
            accent-color: #c4a672;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.12) 0%, rgba(232, 220, 200, 0.08) 100%);
                    padding: clamp(1rem, 3vw, 1.5rem) clamp(1.5rem, 4vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    margin-bottom: 2rem;
                    border-left: 4px solid #c4a672;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;'>
                <div style='flex: 1; min-width: 200px;'>
                    <h1 style='margin: 0; color: #5a4a3a; font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: 800; letter-spacing: -0.5px;'>
                        Priorização de Riscos
                    </h1>
                    <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.85rem, 2vw, 1rem);'>
                        Hierarquização estratégica para tomada de decisão
                    </p>
                </div>
                <div style='background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);
                            padding: 0.7rem 1.3rem;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 12px rgba(168, 136, 70, 0.3);'>
                    <div style='color: rgba(255, 255, 255, 0.85); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;'>
                        CONFORME
                    </div>
                    <div style='color: white; font-size: 1.3rem; font-weight: 800; letter-spacing: 1.5px;'>
                        NR-01
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Filtros e Configurações", expanded=False):
        filter_cols = st.columns([1, 1, 1, 1])
        
        with filter_cols[0]:
            unique_subescalas_rank = sorted(ranking_data['subescala'].unique().tolist())
            selected_subescalas_rank = st.multiselect(
                "Fatores Psicossociais",
                options=unique_subescalas_rank,
                default=unique_subescalas_rank,
                help="Selecione os fatores que deseja analisar",
                key='rank_subescalas'
            )
        
        with filter_cols[1]:
            min_perc = float(ranking_data['perc_alto'].min() * 100)
            max_perc = float(ranking_data['perc_alto'].max() * 100)
            selected_perc_range = st.slider(
                "Percentual Alto Risco",
                min_value=0.0,
                max_value=100.0,
                value=(min_perc, max_perc),
                step=5.0,
                help="Filtre pelo percentual de alto risco"
            )
        
        with filter_cols[2]:
            ordenacao_rank_options = ['Maior Risco', 'Menor Risco', 'Alfabética A-Z', 'Alfabética Z-A']
            selected_ordenacao_rank = st.selectbox(
                "Ordenação",
                options=ordenacao_rank_options,
                help="Escolha como ordenar os dados",
                key='rank_ordenacao'
            )
        
        with filter_cols[3]:
            show_percentages_rank = st.checkbox("Exibir Percentuais", value=True, help="Mostrar percentuais nos gráficos", key='rank_show_perc')
    
    filtered_ranking = ranking_data[
        (ranking_data['subescala'].isin(selected_subescalas_rank)) &
        (ranking_data['perc_alto'] * 100 >= selected_perc_range[0]) &
        (ranking_data['perc_alto'] * 100 <= selected_perc_range[1])
    ]
    
    if len(filtered_ranking) == 0:
        st.warning("Nenhum dado encontrado com os filtros selecionados. Ajuste os filtros acima.")
        st.stop()
    
    criticos = len(filtered_ranking[filtered_ranking['perc_alto'] >= 0.7])
    altos = len(filtered_ranking[(filtered_ranking['perc_alto'] >= 0.5) & (filtered_ranking['perc_alto'] < 0.7)])
    monitoramento = len(filtered_ranking[filtered_ranking['perc_alto'] < 0.5])
    
    kpi_cols = st.columns(3)
    
    with kpi_cols[0]:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 226, 226, 0.95) 0%, rgba(252, 205, 205, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(220, 38, 38, 0.3);
                        box-shadow: 0 3px 12px rgba(220, 38, 38, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Críticos
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #dc2626; line-height: 1; margin-bottom: 0.4rem;'>
                    {criticos}
                </div>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    ≥70% | Ação imediata
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 243, 199, 0.95) 0%, rgba(253, 224, 171, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(245, 158, 11, 0.3);
                        box-shadow: 0 3px 12px rgba(245, 158, 11, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #92400e; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Altos
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #f59e0b; line-height: 1; margin-bottom: 0.4rem;'>
                    {altos}
                </div>
                <div style='color: #92400e; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    50-70% | Curto prazo
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(196, 166, 114, 0.25);
                        box-shadow: 0 3px 12px rgba(107, 88, 71, 0.1);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Monitoramento
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #b89656; line-height: 1; margin-bottom: 0.4rem;'>
                    {monitoramento}
                </div>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    &lt;50% | Acompanhamento
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.1) 0%, rgba(232, 220, 200, 0.06) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border-left: 4px solid #c4a672;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <h3 style='margin: 0 0 1.5rem 0; color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Entendendo a Priorização
            </h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: clamp(1rem, 3vw, 2rem);'>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Problema Resolvido
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Elimina dispersão de recursos. Nem tudo pode ser tratado simultaneamente - <strong>foco estratégico</strong> é essencial
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Pergunta Respondida
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6; font-style: italic;'>
                        "Quais fatores exigem atenção primeiro e quais podem aguardar?"
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Valor Estratégico
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Demonstra <strong>critério objetivo de hierarquização</strong>, atendendo à avaliação de riscos da NR-01
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(196, 166, 114, 0.2);
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);
                    margin-bottom: 2rem;'>
            <div style='margin-bottom: 1.5rem;'>
                <h3 style='margin: 0; color: #5a4a3a; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                    Ranking de Criticidade
                </h3>
                <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                    Do mais urgente ao menos urgente - Percentual de colaboradores em alto risco por fator
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    if selected_ordenacao_rank == 'Maior Risco':
        ranking_sorted = filtered_ranking.sort_values('perc_alto', ascending=True)
    elif selected_ordenacao_rank == 'Menor Risco':
        ranking_sorted = filtered_ranking.sort_values('perc_alto', ascending=False)
    elif selected_ordenacao_rank == 'Alfabética A-Z':
        ranking_sorted = filtered_ranking.sort_values('subescala', ascending=True)
    elif selected_ordenacao_rank == 'Alfabética Z-A':
        ranking_sorted = filtered_ranking.sort_values('subescala', ascending=False)
    
    colors_rank = []
    for perc in ranking_sorted['perc_alto']:
        if perc >= 0.7:
            colors_rank.append('#dc2626')
        elif perc >= 0.5:
            colors_rank.append('#f59e0b')
        elif perc >= 0.3:
            colors_rank.append('rgba(245, 158, 11, 0.6)')
        else:
            colors_rank.append('#10b981')
    
    num_items_rank = len(ranking_sorted)
    chart_height_rank = calculate_responsive_height(num_items_rank, min_height=400, item_height=40)

    fig2 = go.Figure(go.Bar(
        x=ranking_sorted['perc_alto'] * 100,
        y=ranking_sorted['subescala'],
        orientation='h',
        marker=dict(
            color=colors_rank,
            line=dict(color='rgba(0,0,0,0.05)', width=1)
        ),
        text=ranking_sorted['perc_alto'].apply(lambda x: f"{x*100:.1f}%" if show_percentages_rank else ""),
        textposition='outside',
        textfont=dict(size=14, color='#5a4a3a', family='Arial', weight='bold'),
        customdata=np.column_stack((ranking_sorted['media_score'], ranking_sorted['perc_alto']*100)),
        hovertemplate='<b>%{y}</b><br>Alto Risco: %{customdata[1]:.1f}%<br>Score Médio: %{customdata[0]:.2f}<extra></extra>'
    ))

    layout_config = create_responsive_layout_config()
    fig2.update_layout(
        **layout_config,
        height=chart_height_rank,
        showlegend=False,
        xaxis=dict(
            range=[0, 100],
            gridcolor='rgba(196, 166, 114, 0.2)',
            showline=False,
            ticksuffix='%',
            title='Percentual em Alto Risco',
            tickfont=dict(size=13, color='#6b5847', family='Arial', weight='bold'),
            title_font=dict(size=14, color='#5a4a3a', family='Arial', weight='bold')
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#5a4a3a', family='Arial', weight='bold'),
            showline=False
        )
    )

    st.plotly_chart(fig2, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='margin: 2rem 0 1rem 0;'>
            <h3 style='color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Top 3 Prioridades Imediatas
            </h3>
            <p style='color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem); margin: 0.4rem 0 0 0;'>
                Fatores que exigem ação estratégica nos próximos 30-60 dias
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    top_3 = filtered_ranking.nlargest(3, 'perc_alto') if len(filtered_ranking) >= 3 else filtered_ranking
    
    cols = st.columns(min(3, len(top_3)))
    for idx, (col, row) in enumerate(zip(cols, top_3.itertuples()), 1):
        with col:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(220, 38, 38, 0.08) 0%, rgba(185, 28, 28, 0.05) 100%);
                            padding: clamp(1.2rem, 3vw, 1.8rem);
                            border-radius: clamp(10px, 2vw, 14px);
                            border: 2px solid rgba(220, 38, 38, 0.2);
                            border-left: 5px solid #dc2626;
                            box-shadow: 0 4px 16px rgba(220, 38, 38, 0.1);'>
                    <div style='display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;'>
                        <div style='width: 40px; height: 40px;
                                    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                                    border-radius: 10px;
                                    display: flex; align-items: center; justify-content: center;
                                    color: white; font-weight: 800; font-size: 1.2rem;
                                    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);'>
                            #{idx}
                        </div>
                        <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.75rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>
                            Prioridade
                        </div>
                    </div>
                    <h3 style='margin: 0 0 1rem 0; color: #7f1d1d; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700; line-height: 1.3;'>
                        {row.subescala}
                    </h3>
                    <div style='margin-bottom: 1rem;'>
                        <div style='font-size: clamp(2rem, 4.5vw, 2.5rem); font-weight: 800; color: #dc2626; line-height: 1;'>
                            {row.perc_alto*100:.1f}%
                        </div>
                        <div style='color: #991b1b; font-size: clamp(0.75rem, 1.8vw, 0.85rem); margin-top: 0.3rem;'>
                            em alto risco
                        </div>
                    </div>
                    <div style='background: rgba(220, 38, 38, 0.08);
                                padding: 0.8rem;
                                border-radius: 8px;
                                border-left: 3px solid #dc2626;'>
                        <div style='color: #7f1d1d; font-size: clamp(0.75rem, 1.8vw, 0.8rem); font-weight: 600;'>
                            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24" style='display: inline; margin-right: 0.5rem; vertical-align: middle;'>
                                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                            Ação: 30-60 dias
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                    padding: clamp(1rem, 3vw, 1.5rem) clamp(1.5rem, 4vw, 2rem);
                    border-radius: clamp(10px, 2vw, 14px);
                    border: 2px solid rgba(196, 166, 114, 0.2);
                    margin-bottom: 2rem;'>
            <h4 style='margin: 0 0 1.2rem 0; color: #5a4a3a; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                Critérios de Classificação
            </h4>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: clamp(1rem, 2vw, 1.5rem);'>
                <div>
                    <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                        <div style='width: 16px; height: 16px; background: #dc2626; border-radius: 4px;'></div>
                        <span style='color: #991b1b; font-weight: 700; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>Crítico</span>
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.75rem, 1.7vw, 0.85rem); line-height: 1.5;'>
                        ≥70% | Curto prazo<br>
                        <strong>30-60 dias</strong>
                    </div>
                </div>
                <div>
                    <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                        <div style='width: 16px; height: 16px; background: #f59e0b; border-radius: 4px;'></div>
                        <span style='color: #92400e; font-weight: 700; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>Alto</span>
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.75rem, 1.7vw, 0.85rem); line-height: 1.5;'>
                        50-70% | Médio prazo<br>
                        <strong>3-6 meses</strong>
                    </div>
                </div>
                <div>
                    <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                        <div style='width: 16px; height: 16px; background: #f59e0b; opacity: 0.6; border-radius: 4px;'></div>
                        <span style='color: #92400e; font-weight: 700; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>Moderado</span>
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.75rem, 1.7vw, 0.85rem); line-height: 1.5;'>
                        30-50% | Longo prazo<br>
                        <strong>6-12 meses</strong>
                    </div>
                </div>
                <div>
                    <div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;'>
                        <div style='width: 16px; height: 16px; background: #10b981; border-radius: 4px;'></div>
                        <span style='color: #065f46; font-weight: 700; font-size: clamp(0.8rem, 1.8vw, 0.9rem);'>Baixo</span>
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.75rem, 1.7vw, 0.85rem); line-height: 1.5;'>
                        &lt;30% | Contínuo<br>
                        <strong>Monitoramento</strong>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_prox1, col_prox2 = st.columns(2)
    
    with col_prox1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(219, 234, 254, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(59, 130, 246, 0.25);
                        border-left: 4px solid #3b82f6;
                        box-shadow: 0 3px 12px rgba(59, 130, 246, 0.1);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 42px; height: 42px;
                                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M9 5l7 7-7 7"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #1e40af; font-size: clamp(0.95rem, 2vw, 1.05rem); font-weight: 700;'>
                        Próximo Passo
                    </h4>
                </div>
                <p style='margin: 0; color: #1e3a8a; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                    Explore <strong>Análise por Cargo</strong> para entender como os riscos se distribuem por função
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_prox2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(209, 250, 229, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(16, 185, 129, 0.25);
                        border-left: 4px solid #10b981;
                        box-shadow: 0 3px 12px rgba(16, 185, 129, 0.1);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 42px; height: 42px;
                                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #065f46; font-size: clamp(0.95rem, 2vw, 1.05rem); font-weight: 700;'>
                        Conformidade NR-01
                    </h4>
                </div>
                <p style='margin: 0; color: #064e3b; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                    Atende requisitos de <strong>avaliação</strong> e <strong>hierarquização</strong> de riscos
                </p>
            </div>
        """, unsafe_allow_html=True)

####### ANALISE POR CARGO ########
elif pagina == "Análise por Cargo":
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 100%;
            padding: clamp(0.5rem, 2vw, 2rem);
        }
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem;
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        
        [data-testid="stExpander"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 242, 230, 0.6) 100%);
            border: 1px solid rgba(196, 166, 114, 0.3);
            border-radius: 10px;
        }
        
        [data-testid="stExpander"] summary {
            color: #5a4a3a !important;
            font-weight: 600;
        }
        
        .stMultiSelect [data-baseweb="select"] {
            min-height: 38px;
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stMultiSelect [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #c4a672 !important;
            color: white !important;
            border-radius: 6px;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stSlider [data-baseweb="slider"] [role="slider"] {
            background-color: #c4a672 !important;
        }
        
        .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
            background: linear-gradient(90deg, #c4a672 0%, #b89656 100%);
        }
        
        .stCheckbox label {
            color: #5a4a3a;
            font-weight: 500;
        }
        
        .stCheckbox [data-testid="stCheckbox"] {
            accent-color: #c4a672;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.12) 0%, rgba(232, 220, 200, 0.08) 100%);
                    padding: clamp(1rem, 3vw, 1.5rem) clamp(1.5rem, 4vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    margin-bottom: 2rem;
                    border-left: 4px solid #c4a672;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;'>
                <div style='flex: 1; min-width: 200px;'>
                    <h1 style='margin: 0; color: #5a4a3a; font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: 800; letter-spacing: -0.5px;'>
                        Análise por Cargo
                    </h1>
                    <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.85rem, 2vw, 1rem);'>
                        Risco associado à atividade profissional, não ao indivíduo
                    </p>
                </div>
                <div style='background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);
                            padding: 0.7rem 1.3rem;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 12px rgba(168, 136, 70, 0.3);'>
                    <div style='color: rgba(255, 255, 255, 0.85); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;'>
                        CONFORME
                    </div>
                    <div style='color: white; font-size: 1.3rem; font-weight: 800; letter-spacing: 1.5px;'>
                        NR-01
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Filtros e Configurações", expanded=False):
        filter_cols = st.columns([1, 1, 1, 1])
        
        with filter_cols[0]:
            unique_cargos = sorted(cargo_data['cargo'].unique().tolist())
            selected_cargos = st.multiselect(
                "Cargos",
                options=unique_cargos,
                default=unique_cargos,
                help="Selecione os cargos que deseja analisar"
            )
        
        with filter_cols[1]:
            unique_subescalas_cargo = sorted(cargo_data['subescala'].unique().tolist())
            selected_subescalas_cargo = st.multiselect(
                "Dimensões Psicossociais",
                options=unique_subescalas_cargo,
                default=unique_subescalas_cargo,
                help="Selecione as dimensões para análise",
                key='cargo_subescalas'
            )
        
        with filter_cols[2]:
            ordenacao_cargo_options = ['Maior Risco', 'Menor Risco', 'Alfabética A-Z', 'Alfabética Z-A']
            selected_ordenacao_cargo = st.selectbox(
                "Ordenação",
                options=ordenacao_cargo_options,
                help="Escolha como ordenar os dados",
                key='cargo_ordenacao'
            )
        
        with filter_cols[3]:
            show_values_cargo = st.checkbox("Exibir Valores", value=True, help="Mostrar valores nos gráficos", key='cargo_show_values')
    
    filtered_cargo = cargo_data[
        (cargo_data['cargo'].isin(selected_cargos)) &
        (cargo_data['subescala'].isin(selected_subescalas_cargo))
    ]
    
    if len(filtered_cargo) == 0:
        st.warning("Nenhum dado encontrado com os filtros selecionados. Ajuste os filtros acima.")
        st.stop()
    
    # ===== DEFINIR ESCALAS POSITIVAS E NEGATIVAS =====
    escalas_positivas = {
        "Influência no trabalho",
        "Possibilidades de desenvolvimento",
        "Previsibilidade",
        "Transparência do papel",
        "Recompensas",
        "Apoio social colegas",
        "Apoio social superiores",
        "Comunidade social",
        "Qualidade da liderança",
        "Confiança horizontal",
        "Confiança vertical",
        "Justiça e respeito",
        "Autoeficácia",
        "Significado do trabalho",
        "Compromisso",
        "Satisfação"
    }
    
    cargos_unicos = filtered_cargo['cargo'].nunique()
    cargo_media = filtered_cargo.groupby('cargo')['media'].mean()
    cargo_critico = cargo_media.idxmax()
    cargo_critico_nome = cargo_critico.split('(')[0].strip()
    media_geral = filtered_cargo['media'].mean()
    diferenca_max = cargo_media.max() - media_geral
    
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(196, 166, 114, 0.25);
                        box-shadow: 0 3px 12px rgba(107, 88, 71, 0.1);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Cargos Mapeados
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #c4a672; line-height: 1; margin-bottom: 0.4rem;'>
                    {cargos_unicos}
                </div>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Funções analisadas
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi2:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 226, 226, 0.95) 0%, rgba(252, 205, 205, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(220, 38, 38, 0.3);
                        box-shadow: 0 3px 12px rgba(220, 38, 38, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Cargo Mais Crítico
                </div>
                <div style='font-size: clamp(1.1rem, 2.5vw, 1.4rem); font-weight: 800; color: #dc2626; line-height: 1.2; margin-bottom: 0.4rem; min-height: 3.5rem; display: flex; align-items: center; justify-content: center; padding: 0 0.5rem;'>
                    {cargo_critico_nome}
                </div>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Score: {cargo_media.max():.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi3:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(196, 166, 114, 0.25);
                        box-shadow: 0 3px 12px rgba(107, 88, 71, 0.1);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Média Organizacional
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #b89656; line-height: 1; margin-bottom: 0.4rem;'>
                    {media_geral:.2f}
                </div>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Baseline geral
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.1) 0%, rgba(232, 220, 200, 0.06) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border-left: 4px solid #c4a672;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <h3 style='margin: 0 0 1.5rem 0; color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Entendendo o Risco por Função
            </h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: clamp(1rem, 3vw, 2rem);'>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Problema Resolvido
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Evita interpretação pessoal dos riscos. <strong>Desloca o foco da pessoa para a atividade</strong> profissional
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Pergunta Respondida
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6; font-style: italic;'>
                        "Alguns riscos estão associados ao tipo de função exercida?"
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Valor Estratégico
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Protege contra personalização e <strong>direciona para mudanças organizacionais</strong>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== HEATMAP 1: PROBLEMAS (ESCALAS NEGATIVAS) =====
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(220, 38, 38, 0.08) 0%, rgba(185, 28, 28, 0.05) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(220, 38, 38, 0.2);
                    border-left: 4px solid #dc2626;
                    box-shadow: 0 4px 16px rgba(220, 38, 38, 0.08);
                    margin-bottom: 2rem;'>
            <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;'>
                <div style='width: 48px; height: 48px;
                            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                            border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);'>
                    <svg width="24" height="24" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                </div>
                <div>
                    <h3 style='margin: 0; color: #991b1b; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                        Mapa de Problemas por Cargo
                    </h3>
                    <p style='margin: 0.3rem 0 0 0; color: #7f1d1d; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                        Quanto mais vermelho, maior o problema - Identifica onde os riscos são mais graves
                    </p>
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    # Filtrar apenas escalas NEGATIVAS
    filtered_cargo_neg = filtered_cargo[~filtered_cargo['subescala'].isin(escalas_positivas)]
    
    if len(filtered_cargo_neg) > 0:
        cargo_pivot_neg = filtered_cargo_neg.pivot_table(
            index='cargo',
            columns='subescala',
            values='media',
            aggfunc='mean'
        )
        
        num_cargos_neg = len(cargo_pivot_neg)
        heatmap_height_neg = calculate_responsive_height(num_cargos_neg, min_height=500, item_height=45)

        fig3_neg = go.Figure(data=go.Heatmap(
            z=cargo_pivot_neg.values,
            x=cargo_pivot_neg.columns,
            y=cargo_pivot_neg.index,
            colorscale='RdYlGn_r',  # Vermelho = Alto = RUIM ✅
            text=cargo_pivot_neg.values.round(2),
            texttemplate='%{text}' if show_values_cargo else '',
            textfont={"size": 12, "color": "#1e293b", "family": "Arial", "weight": "bold"},
            colorbar=dict(
                title=dict(
                    text="Score<br>(Problema)",
                    side='right',
                    font=dict(size=13, color='#991b1b', family='Arial', weight='bold')
                ),
                tickfont=dict(size=12, color='#7f1d1d', family='Arial', weight='bold')
            ),
            hovertemplate='<b>%{y}</b><br>%{x}<br>Score: <b>%{z:.2f}</b><br>(Quanto maior, pior)<extra></extra>'
        ))

        layout_config = create_responsive_layout_config()
        fig3_neg.update_layout(
            **layout_config,
            height=heatmap_height_neg,
            xaxis=dict(
                title='',
                tickfont=dict(size=13, color='#991b1b', family='Arial', weight='bold'),
                tickangle=-45
            ),
            yaxis=dict(
                title='',
                tickfont=dict(size=13, color='#991b1b', family='Arial', weight='bold')
            )
        )
        st.plotly_chart(fig3_neg, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    else:
        st.info("Nenhuma escala negativa (problemas) selecionada nos filtros.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ===== HEATMAP 2: PROTEÇÕES (ESCALAS POSITIVAS) =====
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(16, 185, 129, 0.2);
                    border-left: 4px solid #10b981;
                    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08);
                    margin-bottom: 2rem;'>
            <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;'>
                <div style='width: 48px; height: 48px;
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                    <svg width="24" height="24" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                    </svg>
                </div>
                <div>
                    <h3 style='margin: 0; color: #065f46; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                        Mapa de Proteções por Cargo
                    </h3>
                    <p style='margin: 0.3rem 0 0 0; color: #064e3b; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                        Quanto mais verde, maior a proteção - Identifica onde há mais fatores protetivos
                    </p>
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    # Filtrar apenas escalas POSITIVAS
    filtered_cargo_pos = filtered_cargo[filtered_cargo['subescala'].isin(escalas_positivas)]
    
    if len(filtered_cargo_pos) > 0:
        cargo_pivot_pos = filtered_cargo_pos.pivot_table(
            index='cargo',
            columns='subescala',
            values='media',
            aggfunc='mean'
        )
        
        num_cargos_pos = len(cargo_pivot_pos)
        heatmap_height_pos = calculate_responsive_height(num_cargos_pos, min_height=500, item_height=45)

        fig3_pos = go.Figure(data=go.Heatmap(
            z=cargo_pivot_pos.values,
            x=cargo_pivot_pos.columns,
            y=cargo_pivot_pos.index,
            colorscale='RdYlGn',  # Verde = Alto = BOM ✅ (sem o _r!)
            text=cargo_pivot_pos.values.round(2),
            texttemplate='%{text}' if show_values_cargo else '',
            textfont={"size": 12, "color": "#1e293b", "family": "Arial", "weight": "bold"},
            colorbar=dict(
                title=dict(
                    text="Score<br>(Proteção)",
                    side='right',
                    font=dict(size=13, color='#065f46', family='Arial', weight='bold')
                ),
                tickfont=dict(size=12, color='#064e3b', family='Arial', weight='bold')
            ),
            hovertemplate='<b>%{y}</b><br>%{x}<br>Score: <b>%{z:.2f}</b><br>(Quanto maior, melhor)<extra></extra>'
        ))

        layout_config = create_responsive_layout_config()
        fig3_pos.update_layout(
            **layout_config,
            height=heatmap_height_pos,
            xaxis=dict(
                title='',
                tickfont=dict(size=13, color='#065f46', family='Arial', weight='bold'),
                tickangle=-45
            ),
            yaxis=dict(
                title='',
                tickfont=dict(size=13, color='#065f46', family='Arial', weight='bold')
            )
        )
        st.plotly_chart(fig3_pos, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    else:
        st.info("Nenhuma escala positiva (proteções) selecionada nos filtros.")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== RANKING (CONTINUA IGUAL) =====
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(196, 166, 114, 0.2);
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);
                    margin-bottom: 2rem;'>
            <div style='margin-bottom: 1.5rem;'>
                <h3 style='margin: 0; color: #5a4a3a; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                    Ranking de Cargos por Score Médio
                </h3>
                <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                    Cargos ordenados do menor ao maior risco médio - Identificação de funções prioritárias
                </p>
            </div>
    """, unsafe_allow_html=True)

    cargo_ranking = filtered_cargo.groupby('cargo').agg({
        'media': 'mean',
        'qtd': 'first'
    }).reset_index()

    if selected_ordenacao_cargo == 'Maior Risco':
        cargo_ranking = cargo_ranking.sort_values('media', ascending=True)
    elif selected_ordenacao_cargo == 'Menor Risco':
        cargo_ranking = cargo_ranking.sort_values('media', ascending=False)
    elif selected_ordenacao_cargo == 'Alfabética A-Z':
        cargo_ranking = cargo_ranking.sort_values('cargo', ascending=True)
    elif selected_ordenacao_cargo == 'Alfabética Z-A':
        cargo_ranking = cargo_ranking.sort_values('cargo', ascending=False)

    colors_cargo = [get_risk_color(score) for score in cargo_ranking['media']]

    num_items_cargo = len(cargo_ranking)
    chart_height_cargo = calculate_responsive_height(num_items_cargo, min_height=400, item_height=40)

    fig4 = go.Figure(go.Bar(
        x=cargo_ranking['media'],
        y=cargo_ranking['cargo'],
        orientation='h',
        marker=dict(
            color=colors_cargo,
            line=dict(width=1, color='rgba(0,0,0,0.05)')
        ),
        text=cargo_ranking['media'].round(2) if show_values_cargo else '',
        textposition='outside',
        textfont=dict(size=14, color='#5a4a3a', family='Arial', weight='bold'),
        customdata=cargo_ranking['qtd'],
        hovertemplate='<b>%{y}</b><br>Score: <b>%{x:.2f}</b><br>Respondentes: %{customdata}<extra></extra>'
    ))

    layout_config_cargo = create_responsive_layout_config()
    fig4.update_layout(
        **layout_config_cargo,
        height=chart_height_cargo,
        showlegend=False,
        xaxis=dict(
            range=[0, 5],
            gridcolor='rgba(196, 166, 114, 0.2)',
            showline=False,
            title=dict(
                text='Score Médio de Risco',
                font=dict(size=14, color='#5a4a3a', family='Arial', weight='bold')
            ),
            tickfont=dict(size=13, color='#6b5847', family='Arial', weight='bold')
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#5a4a3a', family='Arial', weight='bold'),
            showline=False
        )
    )
    st.plotly_chart(fig4, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.05) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(10px, 2vw, 14px);
                    border-left: 4px solid #3b82f6;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.08);'>
            <div style='display: flex; align-items: flex-start; gap: clamp(0.8rem, 2vw, 1.2rem); flex-wrap: wrap;'>
                <div style='min-width: 48px; height: 48px;
                            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                            border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                    <svg width="24" height="24" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                    </svg>
                </div>
                <div style='flex: 1; min-width: 250px;'>
                    <h4 style='margin: 0 0 0.8rem 0; color: #1e40af; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        Insight Estratégico
                    </h4>
                    <div style='color: #1e3a8a; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.7;'>
                        Os riscos variam <strong>significativamente entre funções</strong>. A diferença de {diferenca_max:.2f} pontos 
                        entre o cargo mais crítico e a média organizacional evidencia que <strong>o problema não está nas pessoas, 
                        mas nas condições e demandas da atividade</strong>.
                        <br><br>
                        <strong>Recomendação:</strong> Intervenções devem focar em <strong>redesenho de processos</strong>, 
                        <strong>gestão da carga de trabalho</strong> e <strong>ajuste de demandas por cargo</strong>.
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_prox1, col_prox2 = st.columns(2)
    
    with col_prox1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(219, 234, 254, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(59, 130, 246, 0.25);
                        border-left: 4px solid #3b82f6;
                        box-shadow: 0 3px 12px rgba(59, 130, 246, 0.1);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 42px; height: 42px;
                                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M9 5l7 7-7 7"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #1e40af; font-size: clamp(0.95rem, 2vw, 1.05rem); font-weight: 700;'>
                        Próximo Passo
                    </h4>
                </div>
                <p style='margin: 0; color: #1e3a8a; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                    Explore <strong>Análise por Setor</strong> para entender como os riscos se distribuem por área
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_prox2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(209, 250, 229, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(16, 185, 129, 0.25);
                        border-left: 4px solid #10b981;
                        box-shadow: 0 3px 12px rgba(16, 185, 129, 0.1);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 42px; height: 42px;
                                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #065f46; font-size: clamp(0.95rem, 2vw, 1.05rem); font-weight: 700;'>
                        Conformidade NR-01
                    </h4>
                </div>
                <p style='margin: 0; color: #064e3b; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                    Atende análise de <strong>ambiente</strong> e <strong>organização do trabalho</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)

elif pagina == "Análise por Setor":
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 100%;
            padding: clamp(0.5rem, 2vw, 2rem);
        }
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem;
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        
        [data-testid="stExpander"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 242, 230, 0.6) 100%);
            border: 1px solid rgba(196, 166, 114, 0.3);
            border-radius: 10px;
        }
        
        [data-testid="stExpander"] summary {
            color: #5a4a3a !important;
            font-weight: 600;
        }
        
        .stMultiSelect [data-baseweb="select"] {
            min-height: 38px;
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stMultiSelect [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #c4a672 !important;
            color: white !important;
            border-radius: 6px;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stSlider [data-baseweb="slider"] [role="slider"] {
            background-color: #c4a672 !important;
        }
        
        .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {
            background: linear-gradient(90deg, #c4a672 0%, #b89656 100%);
        }
        
        .stCheckbox label {
            color: #5a4a3a;
            font-weight: 500;
        }
        
        .stCheckbox [data-testid="stCheckbox"] {
            accent-color: #c4a672;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.12) 0%, rgba(232, 220, 200, 0.08) 100%);
                    padding: clamp(1rem, 3vw, 1.5rem) clamp(1.5rem, 4vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    margin-bottom: 2rem;
                    border-left: 4px solid #c4a672;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;'>
                <div style='flex: 1; min-width: 200px;'>
                    <h1 style='margin: 0; color: #5a4a3a; font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: 800; letter-spacing: -0.5px;'>
                        Análise por Setor
                    </h1>
                    <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.85rem, 2vw, 1rem);'>
                        Onde agir na organização - Mapeamento territorial dos riscos
                    </p>
                </div>
                <div style='background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);
                            padding: 0.7rem 1.3rem;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 12px rgba(168, 136, 70, 0.3);'>
                    <div style='color: rgba(255, 255, 255, 0.85); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;'>
                        CONFORME
                    </div>
                    <div style='color: white; font-size: 1.3rem; font-weight: 800; letter-spacing: 1.5px;'>
                        NR-01
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Filtros e Configurações", expanded=False):
        filter_cols = st.columns([1, 1, 1, 1])
        
        with filter_cols[0]:
            unique_setores = sorted(setor_data['setor'].unique().tolist())
            selected_setores = st.multiselect(
                "Setores",
                options=unique_setores,
                default=unique_setores,
                help="Selecione os setores que deseja analisar"
            )
        
        with filter_cols[1]:
            unique_subescalas_setor = sorted(setor_data['subescala'].unique().tolist())
            selected_subescalas_setor = st.multiselect(
                "Dimensões Psicossociais",
                options=unique_subescalas_setor,
                default=unique_subescalas_setor,
                help="Selecione as dimensões para análise",
                key='setor_subescalas'
            )
        
        with filter_cols[2]:
            ordenacao_setor_options = ['Maior Risco', 'Menor Risco', 'Alfabética A-Z', 'Alfabética Z-A']
            selected_ordenacao_setor = st.selectbox(
                "Ordenação",
                options=ordenacao_setor_options,
                help="Escolha como ordenar os dados",
                key='setor_ordenacao'
            )
        
        with filter_cols[3]:
            show_values_setor = st.checkbox("Exibir Valores", value=True, help="Mostrar valores nos gráficos", key='setor_show_values')
    
    filtered_setor = setor_data[
        (setor_data['setor'].isin(selected_setores)) &
        (setor_data['subescala'].isin(selected_subescalas_setor))
    ]
    
    if len(filtered_setor) == 0:
        st.warning("Nenhum dado encontrado com os filtros selecionados. Ajuste os filtros acima.")
        st.stop()
    
    # ===== DEFINIR ESCALAS POSITIVAS E NEGATIVAS =====
    escalas_positivas = {
        "Influência no trabalho",
        "Possibilidades de desenvolvimento",
        "Previsibilidade",
        "Transparência do papel",
        "Recompensas",
        "Apoio social colegas",
        "Apoio social superiores",
        "Comunidade social",
        "Qualidade da liderança",
        "Confiança horizontal",
        "Confiança vertical",
        "Justiça e respeito",
        "Autoeficácia",
        "Significado do trabalho",
        "Compromisso",
        "Satisfação"
    }
    
    setores_unicos = filtered_setor['setor'].nunique()
    setor_media = filtered_setor.groupby('setor')['media'].mean()
    setor_critico = setor_media.idxmax()
    media_org = filtered_setor['media'].mean()
    diferenca_max = setor_media.max() - media_org
    desvio_padrao = setor_media.std()
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(196, 166, 114, 0.25);
                        box-shadow: 0 3px 12px rgba(107, 88, 71, 0.1);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Setores Mapeados
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #c4a672; line-height: 1; margin-bottom: 0.4rem;'>
                    {setores_unicos}
                </div>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Áreas organizacionais
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi2:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 226, 226, 0.95) 0%, rgba(252, 205, 205, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(220, 38, 38, 0.3);
                        box-shadow: 0 3px 12px rgba(220, 38, 38, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Setor Mais Crítico
                </div>
                <div style='font-size: clamp(1.1rem, 2.5vw, 1.4rem); font-weight: 800; color: #dc2626; line-height: 1.2; margin-bottom: 0.4rem; min-height: 3.5rem; display: flex; align-items: center; justify-content: center; padding: 0 0.5rem;'>
                    {setor_critico}
                </div>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Score: {setor_media.max():.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi3:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(196, 166, 114, 0.25);
                        box-shadow: 0 3px 12px rgba(107, 88, 71, 0.1);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Média Organizacional
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #b89656; line-height: 1; margin-bottom: 0.4rem;'>
                    {media_org:.2f}
                </div>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Baseline geral
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi4:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 243, 199, 0.95) 0%, rgba(253, 224, 171, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(245, 158, 11, 0.3);
                        box-shadow: 0 3px 12px rgba(245, 158, 11, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #92400e; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Dispersão
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #f59e0b; line-height: 1; margin-bottom: 0.4rem;'>
                    {desvio_padrao:.2f}
                </div>
                <div style='color: #92400e; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Desvio padrão
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.1) 0%, rgba(232, 220, 200, 0.06) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border-left: 4px solid #c4a672;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <h3 style='margin: 0 0 1.5rem 0; color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Entendendo o Risco Territorial
            </h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: clamp(1rem, 3vw, 2rem);'>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Problema Resolvido
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Elimina dúvida sobre <strong>onde agir primeiro</strong>. Mapeia geograficamente os pontos críticos da organização
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Pergunta Respondida
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6; font-style: italic;'>
                        "Em quais áreas da empresa esses riscos aparecem com mais força?"
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Valor Estratégico
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Risco é <strong>contextual</strong> - ligado a processos, fluxos e gestão local. Base para ações territoriais
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== HEATMAP 1: PROBLEMAS (ESCALAS NEGATIVAS) =====
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(220, 38, 38, 0.08) 0%, rgba(185, 28, 28, 0.05) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(220, 38, 38, 0.2);
                    border-left: 4px solid #dc2626;
                    box-shadow: 0 4px 16px rgba(220, 38, 38, 0.08);
                    margin-bottom: 2rem;'>
            <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;'>
                <div style='width: 48px; height: 48px;
                            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                            border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);'>
                    <svg width="24" height="24" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                </div>
                <div>
                    <h3 style='margin: 0; color: #991b1b; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                        Mapa de Problemas por Setor
                    </h3>
                    <p style='margin: 0.3rem 0 0 0; color: #7f1d1d; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                        Quanto mais vermelho, maior o problema - Identifica onde os riscos são mais graves por área
                    </p>
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    # Filtrar apenas escalas NEGATIVAS
    filtered_setor_neg = filtered_setor[~filtered_setor['subescala'].isin(escalas_positivas)]
    
    if len(filtered_setor_neg) > 0:
        setor_pivot_neg = filtered_setor_neg.pivot_table(
            index='setor',
            columns='subescala',
            values='media',
            aggfunc='mean'
        )
        
        num_setores_neg = len(setor_pivot_neg)
        heatmap_height_setor_neg = calculate_responsive_height(num_setores_neg, min_height=500, item_height=45)

        fig_heatmap_neg = go.Figure(data=go.Heatmap(
            z=setor_pivot_neg.values,
            x=setor_pivot_neg.columns,
            y=setor_pivot_neg.index,
            colorscale='RdYlGn_r',  # Vermelho = Alto = RUIM ✅
            text=setor_pivot_neg.values.round(2),
            texttemplate='%{text}' if show_values_setor else '',
            textfont={"size": 12, "color": "#1e293b", "family": "Arial", "weight": "bold"},
            colorbar=dict(
                title=dict(
                    text="Score<br>(Problema)",
                    side='right',
                    font=dict(size=13, color='#991b1b', family='Arial', weight='bold')
                ),
                tickfont=dict(size=12, color='#7f1d1d', family='Arial', weight='bold')
            ),
            hovertemplate='<b>%{y}</b><br>%{x}<br>Score: <b>%{z:.2f}</b><br>(Quanto maior, pior)<extra></extra>'
        ))

        layout_config = create_responsive_layout_config()
        fig_heatmap_neg.update_layout(
            **layout_config,
            height=heatmap_height_setor_neg,
            xaxis=dict(
                title='',
                tickfont=dict(size=13, color='#991b1b', family='Arial', weight='bold'),
                tickangle=-45
            ),
            yaxis=dict(
                title='',
                tickfont=dict(size=13, color='#991b1b', family='Arial', weight='bold')
            )
        )
        st.plotly_chart(fig_heatmap_neg, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    else:
        st.info("Nenhuma escala negativa (problemas) selecionada nos filtros.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ===== HEATMAP 2: PROTEÇÕES (ESCALAS POSITIVAS) =====
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(16, 185, 129, 0.2);
                    border-left: 4px solid #10b981;
                    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08);
                    margin-bottom: 2rem;'>
            <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;'>
                <div style='width: 48px; height: 48px;
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                    <svg width="24" height="24" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                    </svg>
                </div>
                <div>
                    <h3 style='margin: 0; color: #065f46; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                        Mapa de Proteções por Setor
                    </h3>
                    <p style='margin: 0.3rem 0 0 0; color: #064e3b; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                        Quanto mais verde, maior a proteção - Identifica onde há mais fatores protetivos por área
                    </p>
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    # Filtrar apenas escalas POSITIVAS
    filtered_setor_pos = filtered_setor[filtered_setor['subescala'].isin(escalas_positivas)]
    
    if len(filtered_setor_pos) > 0:
        setor_pivot_pos = filtered_setor_pos.pivot_table(
            index='setor',
            columns='subescala',
            values='media',
            aggfunc='mean'
        )
        
        num_setores_pos = len(setor_pivot_pos)
        heatmap_height_setor_pos = calculate_responsive_height(num_setores_pos, min_height=500, item_height=45)

        fig_heatmap_pos = go.Figure(data=go.Heatmap(
            z=setor_pivot_pos.values,
            x=setor_pivot_pos.columns,
            y=setor_pivot_pos.index,
            colorscale='RdYlGn',  # Verde = Alto = BOM ✅ (sem o _r!)
            text=setor_pivot_pos.values.round(2),
            texttemplate='%{text}' if show_values_setor else '',
            textfont={"size": 12, "color": "#1e293b", "family": "Arial", "weight": "bold"},
            colorbar=dict(
                title=dict(
                    text="Score<br>(Proteção)",
                    side='right',
                    font=dict(size=13, color='#065f46', family='Arial', weight='bold')
                ),
                tickfont=dict(size=12, color='#064e3b', family='Arial', weight='bold')
            ),
            hovertemplate='<b>%{y}</b><br>%{x}<br>Score: <b>%{z:.2f}</b><br>(Quanto maior, melhor)<extra></extra>'
        ))

        layout_config = create_responsive_layout_config()
        fig_heatmap_pos.update_layout(
            **layout_config,
            height=heatmap_height_setor_pos,
            xaxis=dict(
                title='',
                tickfont=dict(size=13, color='#065f46', family='Arial', weight='bold'),
                tickangle=-45
            ),
            yaxis=dict(
                title='',
                tickfont=dict(size=13, color='#065f46', family='Arial', weight='bold')
            )
        )
        st.plotly_chart(fig_heatmap_pos, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    else:
        st.info("Nenhuma escala positiva (proteções) selecionada nos filtros.")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== RANKING (CONTINUA IGUAL) =====
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(196, 166, 114, 0.2);
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);
                    margin-bottom: 2rem;'>
            <div style='margin-bottom: 1.5rem;'>
                <h3 style='margin: 0; color: #5a4a3a; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                    Ranking de Setores por Score Médio
                </h3>
                <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                    Áreas ordenadas do menor ao maior risco - Priorização territorial de recursos
                </p>
            </div>
    """, unsafe_allow_html=True)

    setor_ranking = filtered_setor.groupby('setor').agg({
        'media': 'mean',
        'qtd': 'first'
    }).reset_index()

    if selected_ordenacao_setor == 'Maior Risco':
        setor_ranking = setor_ranking.sort_values('media', ascending=True)
    elif selected_ordenacao_setor == 'Menor Risco':
        setor_ranking = setor_ranking.sort_values('media', ascending=False)
    elif selected_ordenacao_setor == 'Alfabética A-Z':
        setor_ranking = setor_ranking.sort_values('setor', ascending=True)
    elif selected_ordenacao_setor == 'Alfabética Z-A':
        setor_ranking = setor_ranking.sort_values('setor', ascending=False)

    colors_setor = [get_risk_color(score) for score in setor_ranking['media']]

    num_items_setor = len(setor_ranking)
    chart_height_setor = calculate_responsive_height(num_items_setor, min_height=400, item_height=40)

    fig5 = go.Figure(go.Bar(
        x=setor_ranking['media'],
        y=setor_ranking['setor'],
        orientation='h',
        marker=dict(
            color=colors_setor,
            line=dict(width=1, color='rgba(0,0,0,0.05)')
        ),
        text=setor_ranking['media'].round(2) if show_values_setor else '',
        textposition='outside',
        textfont=dict(size=14, color='#5a4a3a', family='Arial', weight='bold'),
        customdata=setor_ranking['qtd'],
        hovertemplate='<b>%{y}</b><br>Score: <b>%{x:.2f}</b><br>Colaboradores: %{customdata}<extra></extra>'
    ))

    layout_config_setor = create_responsive_layout_config()
    fig5.update_layout(
        **layout_config_setor,
        height=chart_height_setor,
        showlegend=False,
        xaxis=dict(
            range=[0, 5],
            gridcolor='rgba(196, 166, 114, 0.2)',
            showline=False,
            title=dict(
                text='Score Médio de Risco',
                font=dict(size=14, color='#5a4a3a', family='Arial', weight='bold')
            ),
            tickfont=dict(size=13, color='#6b5847', family='Arial', weight='bold')
        ),
        yaxis=dict(
            tickfont=dict(size=14, color='#5a4a3a', family='Arial', weight='bold'),
            showline=False
        )
    )
    st.plotly_chart(fig5, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div style='margin: 2rem 0 1rem 0;'>
            <h3 style='color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Setores Prioritários para Intervenção
            </h3>
            <p style='color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem); margin: 0.4rem 0 0 0;'>
                Áreas que demandam atenção estratégica imediata
            </p>
        </div>
    """, unsafe_allow_html=True)
    top_setores = setor_ranking.nlargest(3, 'media')
    cols = st.columns(min(3, len(top_setores)))
    
    for idx, (col, row) in enumerate(zip(cols, top_setores.itertuples()), 1):
        with col:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(220, 38, 38, 0.08) 0%, rgba(185, 28, 28, 0.05) 100%);
                            padding: clamp(1.2rem, 3vw, 1.8rem);
                            border-radius: clamp(10px, 2vw, 14px);
                            border: 2px solid rgba(220, 38, 38, 0.2);
                            border-left: 5px solid #dc2626;
                            box-shadow: 0 4px 16px rgba(220, 38, 38, 0.1);'>
                    <div style='display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;'>
                        <div style='width: 40px; height: 40px;
                                    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                                    border-radius: 10px;
                                    display: flex; align-items: center; justify-content: center;
                                    color: white; font-weight: 800; font-size: 1.2rem;
                                    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);'>
                            #{idx}
                        </div>
                        <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.75rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>
                            Prioridade
                        </div>
                    </div>
                    <h3 style='margin: 0 0 1rem 0; color: #7f1d1d; font-size: clamp(1rem, 2.2vw, 1.2rem); font-weight: 700; line-height: 1.3;'>
                        {row.setor}
                    </h3>
                    <div style='margin-bottom: 1rem;'>
                        <div style='font-size: clamp(2rem, 4.5vw, 2.8rem); font-weight: 800; color: #dc2626; line-height: 1;'>
                            {row.media:.2f}
                        </div>
                        <div style='color: #991b1b; font-size: clamp(0.75rem, 1.8vw, 0.85rem); margin-top: 0.3rem;'>
                            score médio
                        </div>
                    </div>
                    <div style='background: rgba(220, 38, 38, 0.08);
                                padding: 0.8rem;
                                border-radius: 8px;
                                border-left: 3px solid #dc2626;'>
                        <div style='color: #7f1d1d; font-size: clamp(0.75rem, 1.8vw, 0.8rem); font-weight: 600;'>
                            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24" style='display: inline; margin-right: 0.5rem; vertical-align: middle;'>
                                <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                            </svg>
                            {row.qtd} colaboradores
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(10px, 2vw, 14px);
                    border-left: 4px solid #10b981;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08);'>
            <div style='display: flex; align-items: flex-start; gap: clamp(0.8rem, 2vw, 1.2rem); flex-wrap: wrap;'>
                <div style='min-width: 48px; height: 48px;
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                    <svg width="24" height="24" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                </div>
                <div style='flex: 1; min-width: 250px;'>
                    <h4 style='margin: 0 0 0.8rem 0; color: #065f46; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        Recomendação Estratégica
                    </h4>
                    <div style='color: #064e3b; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.7;'>
                        Iniciar intervenções pelos <strong>3 setores prioritários</strong> identificados. A diferença de 
                        {diferenca_max:.2f} pontos entre o setor mais crítico e a média organizacional indica 
                        <strong>variação contextual significativa</strong>.
                        <br><br>
                        <strong>Próximas ações:</strong>
                        <ul style='margin: 0.5rem 0 0 0; padding-left: 1.5rem;'>
                            <li>Diagnóstico aprofundado dos setores críticos</li>
                            <li>Investigar causas raiz: sobrecarga, recursos, conflitos de gestão, ambiente físico</li>
                            <li>Desenvolver plano de ação <strong>contextualizado</strong> para cada realidade setorial</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_prox1, col_prox2 = st.columns(2)
    
    with col_prox1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(219, 234, 254, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(59, 130, 246, 0.25);
                        border-left: 4px solid #3b82f6;
                        box-shadow: 0 3px 12px rgba(59, 130, 246, 0.1);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 42px; height: 42px;
                                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M9 5l7 7-7 7"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #1e40af; font-size: clamp(0.95rem, 2vw, 1.05rem); font-weight: 700;'>
                        Próximo Passo
                    </h4>
                </div>
                <p style='margin: 0; color: #1e3a8a; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                    Acesse <strong>Matriz de Risco</strong> para visualizar probabilidade × severidade
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_prox2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(209, 250, 229, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(16, 185, 129, 0.25);
                        border-left: 4px solid #10b981;
                        box-shadow: 0 3px 12px rgba(16, 185, 129, 0.1);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 42px; height: 42px;
                                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #065f46; font-size: clamp(0.95rem, 2vw, 1.05rem); font-weight: 700;'>
                        Conformidade NR-01
                    </h4>
                </div>
                <p style='margin: 0; color: #064e3b; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                    Atende análise de <strong>ambiente</strong> e <strong>organização do trabalho</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)


####### MATRIZ DE RISCO ########
elif pagina == "Matriz de Risco":
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 100%;
            padding: clamp(0.5rem, 2vw, 2rem);
        }
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem;
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        
        [data-testid="stExpander"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 242, 230, 0.6) 100%);
            border: 1px solid rgba(196, 166, 114, 0.3);
            border-radius: 10px;
        }
        
        [data-testid="stExpander"] summary {
            color: #5a4a3a !important;
            font-weight: 600;
        }
        
        .stMultiSelect [data-baseweb="select"] {
            min-height: 38px;
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stMultiSelect [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #c4a672 !important;
            color: white !important;
            border-radius: 6px;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        
        .stCheckbox label {
            color: #5a4a3a;
            font-weight: 500;
        }
        
        .stCheckbox [data-testid="stCheckbox"] {
            accent-color: #c4a672;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.12) 0%, rgba(232, 220, 200, 0.08) 100%);
                    padding: clamp(1rem, 3vw, 1.5rem) clamp(1.5rem, 4vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    margin-bottom: 2rem;
                    border-left: 4px solid #c4a672;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;'>
                <div style='flex: 1; min-width: 200px;'>
                    <h1 style='margin: 0; color: #5a4a3a; font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: 800; letter-spacing: -0.5px;'>
                        Matriz de Risco - Classificação
                    </h1>
                    <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.85rem, 2vw, 1rem);'>
                        Probabilidade × Severidade = Nível de Risco (Crítico, Alto, Médio, Baixo)
                    </p>
                </div>
                <div style='background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);
                            padding: 0.7rem 1.3rem;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 12px rgba(168, 136, 70, 0.3);'>
                    <div style='color: rgba(255, 255, 255, 0.85); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;'>
                        CONFORME
                    </div>
                    <div style='color: white; font-size: 1.3rem; font-weight: 800; letter-spacing: 1.5px;'>
                        NR-01
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Filtros e Configurações", expanded=False):
        filter_cols = st.columns([1, 1])
        
        with filter_cols[0]:
            unique_subescalas_matriz2 = sorted(matriz_data['subescala'].unique().tolist())
            selected_subescalas_matriz2 = st.multiselect(
                "Fatores Psicossociais",
                options=unique_subescalas_matriz2,
                default=unique_subescalas_matriz2,
                help="Selecione os fatores para visualizar na matriz",
                key='matriz2_subescalas'
            )
        
        with filter_cols[1]:
            show_labels_matriz2 = st.checkbox("Exibir Rótulos", value=True, help="Mostrar nomes dos fatores no gráfico", key='matriz2_labels')
    
    filtered_matriz2 = matriz_data[matriz_data['subescala'].isin(selected_subescalas_matriz2)].copy()
    
    if len(filtered_matriz2) == 0:
        st.warning("Nenhum dado encontrado com os filtros selecionados. Ajuste os filtros acima.")
        st.stop()
    
    # ===== FUNÇÃO CORRIGIDA =====
    def classificar_risco(prob, sev):
        """
        Classifica o risco com base em probabilidade e severidade.
        
        Probabilidade (prob): % de pessoas em risco alto (0-1)
        - ≥0.60 (≥60%) = Permanente (peso 2.0)
        - 0.40-0.59 (40-59%) = Intermitente (peso 1.5)
        - 0.20-0.39 (20-39%) = Esporádica (peso 1.0)
        - <0.20 (<20%) = Eventual (peso 0.5)
        
        Severidade (sev): Score médio (0-5)
        - >3.66 = Crítica (peso 10.0)
        - 2.33-3.66 = Grave (peso 3.0)
        - 1.50-2.33 = Moderada (peso 2.0)
        - <1.50 = Leve (peso 1.0)
        """
        # Mapear probabilidade para peso
        if prob >= 0.60:  # 60%+ = Permanente (A)
            prob_peso = 2.0
        elif prob >= 0.40:  # 40-60% = Intermitente (B)
            prob_peso = 1.5
        elif prob >= 0.20:  # 20-40% = Esporádica (C)
            prob_peso = 1.0
        else:  # <20% = Eventual (D)
            prob_peso = 0.5
        
        # Mapear severidade para peso (alinhado com risk_class)
        if sev > 3.66:  # Crítica (IV)
            sev_peso = 10.0
        elif sev >= 2.33:  # Grave (III)
            sev_peso = 3.0
        elif sev >= 1.50:  # Moderada (II)
            sev_peso = 2.0
        else:  # Leve (I)
            sev_peso = 1.0
        
        # Calcular pontuação
        pontuacao = prob_peso * sev_peso
        
        # Classificar resultado
        if pontuacao >= 5.0:
            return 'CRÍTICO', pontuacao
        elif pontuacao >= 3.0:
            return 'ALTO', pontuacao
        elif pontuacao >= 1.5:
            return 'MÉDIO', pontuacao
        else:
            return 'BAIXO', pontuacao
    
    # Aplicar classificação
    filtered_matriz2['classificacao'] = filtered_matriz2.apply(
        lambda row: classificar_risco(row['probabilidade'], row['severidade'])[0], axis=1
    )
    filtered_matriz2['pontuacao'] = filtered_matriz2.apply(
        lambda row: classificar_risco(row['probabilidade'], row['severidade'])[1], axis=1
    )
    
    # Contar por classificação
    critico = len(filtered_matriz2[filtered_matriz2['classificacao'] == 'CRÍTICO'])
    alto = len(filtered_matriz2[filtered_matriz2['classificacao'] == 'ALTO'])
    medio = len(filtered_matriz2[filtered_matriz2['classificacao'] == 'MÉDIO'])
    baixo = len(filtered_matriz2[filtered_matriz2['classificacao'] == 'BAIXO'])
    
    # KPIs
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 226, 226, 0.95) 0%, rgba(252, 205, 205, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(220, 38, 38, 0.3);
                        box-shadow: 0 3px 12px rgba(220, 38, 38, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Crítico
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #dc2626; line-height: 1; margin-bottom: 0.4rem;'>
                    {critico}
                </div>
                <div style='color: #991b1b; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Pontuação ≥ 5.0
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi2:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 243, 199, 0.95) 0%, rgba(253, 224, 171, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(245, 158, 11, 0.3);
                        box-shadow: 0 3px 12px rgba(245, 158, 11, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #92400e; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Alto
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #f59e0b; line-height: 1; margin-bottom: 0.4rem;'>
                    {alto}
                </div>
                <div style='color: #92400e; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Pontuação 3.0 - 4.9
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi3:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(254, 249, 195, 0.95) 0%, rgba(253, 246, 178, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(234, 179, 8, 0.3);
                        box-shadow: 0 3px 12px rgba(234, 179, 8, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #713f12; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Médio
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #eab308; line-height: 1; margin-bottom: 0.4rem;'>
                    {medio}
                </div>
                <div style='color: #713f12; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Pontuação 1.5 - 2.9
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with kpi4:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(219, 234, 254, 0.95) 0%, rgba(191, 219, 254, 0.8) 100%);
                        padding: clamp(1rem, 3vw, 1.5rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(59, 130, 246, 0.3);
                        box-shadow: 0 3px 12px rgba(59, 130, 246, 0.12);
                        text-align: center;
                        min-height: 120px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;'>
                <div style='color: #1e3a8a; font-size: clamp(0.7rem, 1.5vw, 0.8rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                    Baixo
                </div>
                <div style='font-size: clamp(2rem, 5vw, 2.5rem); font-weight: 800; color: #3b82f6; line-height: 1; margin-bottom: 0.4rem;'>
                    {baixo}
                </div>
                <div style='color: #1e3a8a; font-size: clamp(0.7rem, 1.5vw, 0.75rem);'>
                    Pontuação < 1.5
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.1) 0%, rgba(232, 220, 200, 0.06) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border-left: 4px solid #c4a672;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <h3 style='margin: 0 0 1.5rem 0; color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Matriz de Classificação de Riscos
            </h3>
            <div style='overflow-x: auto;'>
                <table style='width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden;'>
                    <thead>
                        <tr style='background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);'>
                            <th rowspan='2' style='padding: 1rem; color: white; border: 1px solid rgba(255,255,255,0.2); text-align: center; font-weight: 700;'>SEVERIDADE</th>
                            <th colspan='4' style='padding: 1rem; color: white; border: 1px solid rgba(255,255,255,0.2); text-align: center; font-weight: 700;'>PROBABILIDADE</th>
                        </tr>
                        <tr style='background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);'>
                            <th style='padding: 0.8rem; color: white; border: 1px solid rgba(255,255,255,0.2); text-align: center; font-size: 0.9rem;'>A<br>Permanente<br>(2,0)</th>
                            <th style='padding: 0.8rem; color: white; border: 1px solid rgba(255,255,255,0.2); text-align: center; font-size: 0.9rem;'>B<br>Intermitente<br>(1,5)</th>
                            <th style='padding: 0.8rem; color: white; border: 1px solid rgba(255,255,255,0.2); text-align: center; font-size: 0.9rem;'>C<br>Esporádica<br>(1,0)</th>
                            <th style='padding: 0.8rem; color: white; border: 1px solid rgba(255,255,255,0.2); text-align: center; font-size: 0.9rem;'>D<br>Eventual<br>(0,5)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; font-weight: 600; background: #f9fafb;'><strong>IV</strong> - Crítica/Catastrófica (10,0)</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #dc2626; color: white; font-weight: 700;'>CRÍTICO<br>20,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #dc2626; color: white; font-weight: 700;'>CRÍTICO<br>15,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #dc2626; color: white; font-weight: 700;'>CRÍTICO<br>10,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #dc2626; color: white; font-weight: 700;'>CRÍTICO<br>5,0</td>
                        </tr>
                        <tr>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; font-weight: 600; background: #f9fafb;'><strong>III</strong> - Grave (3,0)</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #dc2626; color: white; font-weight: 700;'>CRÍTICO<br>6,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #f59e0b; color: white; font-weight: 700;'>ALTO<br>4,5</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #f59e0b; color: white; font-weight: 700;'>ALTO<br>3,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #eab308; color: white; font-weight: 700;'>MÉDIO<br>1,5</td>
                        </tr>
                        <tr>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; font-weight: 600; background: #f9fafb;'><strong>II</strong> - Moderada (2,0)</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #f59e0b; color: white; font-weight: 700;'>ALTO<br>4,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #f59e0b; color: white; font-weight: 700;'>ALTO<br>3,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #eab308; color: white; font-weight: 700;'>MÉDIO<br>2,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #3b82f6; color: white; font-weight: 700;'>BAIXO<br>1,0</td>
                        </tr>
                        <tr>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; font-weight: 600; background: #f9fafb;'><strong>I</strong> - Leve (1,0)</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #eab308; color: white; font-weight: 700;'>MÉDIO<br>2,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #eab308; color: white; font-weight: 700;'>MÉDIO<br>1,5</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #3b82f6; color: white; font-weight: 700;'>BAIXO<br>1,0</td>
                            <td style='padding: 1rem; border: 1px solid #e5e7eb; text-align: center; background: #3b82f6; color: white; font-weight: 700;'>BAIXO<br>0,5</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style='margin-top: 1.5rem; padding: 1rem; background: rgba(255, 255, 255, 0.7); border-radius: 8px; border-left: 3px solid #c4a672;'>
                <p style='margin: 0; color: #6b5847; font-size: 0.9rem; line-height: 1.6;'>
                    <strong>Probabilidade:</strong> Probabilidade de ocorrência do possível dano e/ou lesão<br>
                    <strong>Severidade:</strong> Consequências do dano e/ou lesão criados, ou seja, a amplitude da gravidade deste dano
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(196, 166, 114, 0.2);
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);
                    margin-bottom: 2rem;'>
            <div style='margin-bottom: 1.5rem;'>
                <h3 style='margin: 0; color: #5a4a3a; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                    Distribuição dos Riscos na Matriz
                </h3>
                <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                    Visualização dos fatores psicossociais por nível de criticidade
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    # Normalizar probabilidade para eixo X (0-10)
    filtered_matriz2['prob_norm'] = filtered_matriz2['probabilidade'] * 10
    
    matriz_height = calculate_responsive_height(len(filtered_matriz2), min_height=600, item_height=25, max_height=850)
    
    fig7 = go.Figure()

    # ===== ZONAS COLORIDAS CORRIGIDAS =====
    # ZONAS CRÍTICAS (Vermelho) - Severidade > 3.66
    fig7.add_shape(type="rect", x0=6, y0=3.66, x1=10, y1=5, fillcolor="rgba(220, 38, 38, 0.15)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=4, y0=3.66, x1=6, y1=5, fillcolor="rgba(220, 38, 38, 0.15)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=2, y0=3.66, x1=4, y1=5, fillcolor="rgba(220, 38, 38, 0.15)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=0, y0=3.66, x1=2, y1=5, fillcolor="rgba(220, 38, 38, 0.15)", line=dict(width=0), layer="below")
    
    # ZONAS ALTAS (Laranja) - Severidade 2.33-3.66, Probabilidade conforme
    fig7.add_shape(type="rect", x0=6, y0=2.33, x1=10, y1=3.66, fillcolor="rgba(245, 158, 11, 0.12)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=4, y0=2.33, x1=6, y1=3.66, fillcolor="rgba(245, 158, 11, 0.12)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=2, y0=2.33, x1=4, y1=3.66, fillcolor="rgba(245, 158, 11, 0.12)", line=dict(width=0), layer="below")
    
    # ZONAS MÉDIAS (Amarelo) - Severidade 1.50-2.33 ou combinações que dão Médio
    fig7.add_shape(type="rect", x0=0, y0=2.33, x1=2, y1=3.66, fillcolor="rgba(234, 179, 8, 0.10)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=2, y0=1.50, x1=4, y1=2.33, fillcolor="rgba(234, 179, 8, 0.10)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=4, y0=1.50, x1=6, y1=2.33, fillcolor="rgba(234, 179, 8, 0.10)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=6, y0=1.50, x1=10, y1=2.33, fillcolor="rgba(234, 179, 8, 0.10)", line=dict(width=0), layer="below")
    
    # ZONAS BAIXAS (Azul) - Severidade < 1.50
    fig7.add_shape(type="rect", x0=0, y0=0, x1=2, y1=1.50, fillcolor="rgba(59, 130, 246, 0.08)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=2, y0=0, x1=4, y1=1.50, fillcolor="rgba(59, 130, 246, 0.08)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=4, y0=0, x1=6, y1=1.50, fillcolor="rgba(59, 130, 246, 0.08)", line=dict(width=0), layer="below")
    fig7.add_shape(type="rect", x0=6, y0=0, x1=10, y1=1.50, fillcolor="rgba(59, 130, 246, 0.08)", line=dict(width=0), layer="below")
    
    # Adicionar pontos por classificação
    color_map_class = {
        'CRÍTICO': '#dc2626',
        'ALTO': '#f59e0b',
        'MÉDIO': '#eab308',
        'BAIXO': '#3b82f6'
    }
    
    for classificacao in ['BAIXO', 'MÉDIO', 'ALTO', 'CRÍTICO']:
        df_class = filtered_matriz2[filtered_matriz2['classificacao'] == classificacao]
        if len(df_class) > 0:
            fig7.add_trace(go.Scatter(
                x=df_class['prob_norm'],
                y=df_class['severidade'],
                mode='markers+text' if show_labels_matriz2 else 'markers',
                name=classificacao,
                marker=dict(
                    size=24,
                    color=color_map_class[classificacao],
                    line=dict(width=3, color='white'),
                    opacity=0.9
                ),
                text=df_class['subescala'].str[:20] if show_labels_matriz2 else '',
                textposition='top center',
                textfont=dict(size=11, color='#1e293b', family='Arial', weight='bold'),
                hovertemplate='<b>%{text}</b><br>Probabilidade: %{x:.1f}/10 (%{customdata[0]:.0%})<br>Severidade: %{y:.2f}/5<br>Pontuação: %{customdata[1]:.1f}<br><b>Risco: ' + classificacao + '</b><extra></extra>',
                customdata=df_class[['probabilidade', 'pontuacao']].values
            ))
    
    # ===== LINHAS HORIZONTAIS CORRIGIDAS =====
    fig7.add_hline(y=3.66, line_dash="dash", line_color="#dc2626", line_width=2.5, 
                annotation_text="Severidade Crítica (>3.66)", annotation_position="right",
                annotation_font=dict(size=12, color='#dc2626', family='Arial', weight='bold'))
    fig7.add_hline(y=2.33, line_dash="dash", line_color="#f59e0b", line_width=2,
                annotation_text="Severidade Grave (2.33-3.66)", annotation_position="right",
                annotation_font=dict(size=11, color='#f59e0b', family='Arial'))
    fig7.add_hline(y=1.50, line_dash="dash", line_color="#eab308", line_width=1.5,
                annotation_text="Severidade Moderada (1.50-2.33)", annotation_position="right",
                annotation_font=dict(size=10, color='#eab308', family='Arial'))
    
    # ===== LINHAS VERTICAIS CORRIGIDAS =====
    fig7.add_vline(x=6, line_dash="dash", line_color="#dc2626", line_width=2.5,
                annotation_text="Prob. Permanente (60%)", annotation_position="top",
                annotation_font=dict(size=12, color='#dc2626', family='Arial', weight='bold'))
    fig7.add_vline(x=4, line_dash="dash", line_color="#f59e0b", line_width=2,
                annotation_text="Prob. Intermitente (40%)", annotation_position="top",
                annotation_font=dict(size=11, color='#f59e0b', family='Arial'))
    fig7.add_vline(x=2, line_dash="dash", line_color="#eab308", line_width=1.5,
                annotation_text="Prob. Esporádica (20%)", annotation_position="top",
                annotation_font=dict(size=10, color='#eab308', family='Arial'))
    
    # Layout
    layout_config = create_responsive_layout_config()
    fig7.update_layout(
        **layout_config,
        height=matriz_height,
        xaxis=dict(
            range=[0, 10],
            gridcolor='rgba(196, 166, 114, 0.2)',
            showline=True,
            linewidth=2,
            linecolor='rgba(107, 88, 71, 0.3)',
            title=dict(
                text='<b>Probabilidade de Ocorrência</b> (0 = Eventual → 10 = Permanente)',
                font=dict(size=14, color='#5a4a3a', family='Arial', weight='bold')
            ),
            tickfont=dict(size=13, color='#6b5847', family='Arial', weight='bold'),
            dtick=1
        ),
        yaxis=dict(
            range=[0, 5],
            gridcolor='rgba(196, 166, 114, 0.2)',
            showline=True,
            linewidth=2,
            linecolor='rgba(107, 88, 71, 0.3)',
            title=dict(
                text='<b>Severidade do Impacto</b> (0 = Leve → 5 = Catastrófica)',
                font=dict(size=14, color='#5a4a3a', family='Arial', weight='bold')
            ),
            tickfont=dict(size=13, color='#6b5847', family='Arial', weight='bold'),
            dtick=1
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.95)',
            bordercolor='rgba(196, 166, 114, 0.4)',
            borderwidth=2,
            font=dict(size=13, family='Arial', color='#5a4a3a', weight='bold')
        )
    )
    
    st.plotly_chart(fig7, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='margin: 2rem 0 1rem 0;'>
            <h3 style='color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Guia de Ação por Nível de Risco
            </h3>
            <p style='color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem); margin: 0.4rem 0 0 0;'>
                Estratégias recomendadas conforme pontuação de risco
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(220, 38, 38, 0.08) 0%, rgba(185, 28, 28, 0.05) 100%);
                        padding: clamp(1.2rem, 3vw, 1.8rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(220, 38, 38, 0.2);
                        border-left: 5px solid #dc2626;
                        height: 100%;'>
                <div style='display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;'>
                    <div style='width: 40px; height: 40px;
                                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #991b1b; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        CRÍTICO
                    </h4>
                </div>
                <div style='color: #7f1d1d; font-size: clamp(0.85rem, 2vw, 0.9rem); line-height: 1.7;'>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Pontuação:</strong> ≥ 5.0
                    </div>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Ação:</strong> Imediata
                    </div>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Prazo:</strong> 30 dias
                    </div>
                    <div style='background: rgba(220, 38, 38, 0.08); padding: 0.6rem; border-radius: 6px; margin-top: 1rem;'>
                        Intervenção urgente necessária
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(217, 119, 6, 0.05) 100%);
                        padding: clamp(1.2rem, 3vw, 1.8rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(245, 158, 11, 0.2);
                        border-left: 5px solid #f59e0b;
                        height: 100%;'>
                <div style='display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;'>
                    <div style='width: 40px; height: 40px;
                                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #92400e; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        ALTO
                    </h4>
                </div>
                <div style='color: #78350f; font-size: clamp(0.85rem, 2vw, 0.9rem); line-height: 1.7;'>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Pontuação:</strong> 3.0 - 4.9
                    </div>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Ação:</strong> Prioritária
                    </div>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Prazo:</strong> 60-90 dias
                    </div>
                    <div style='background: rgba(245, 158, 11, 0.08); padding: 0.6rem; border-radius: 6px; margin-top: 1rem;'>
                        Plano de ação estruturado
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(234, 179, 8, 0.08) 0%, rgba(202, 138, 4, 0.05) 100%);
                        padding: clamp(1.2rem, 3vw, 1.8rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(234, 179, 8, 0.2);
                        border-left: 5px solid #eab308;
                        height: 100%;'>
                <div style='display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;'>
                    <div style='width: 40px; height: 40px;
                                background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(234, 179, 8, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #713f12; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        MÉDIO
                    </h4>
                </div>
                <div style='color: #854d0e; font-size: clamp(0.85rem, 2vw, 0.9rem); line-height: 1.7;'>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Pontuação:</strong> 1.5 - 2.9
                    </div>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Ação:</strong> Programada
                    </div>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Prazo:</strong> 3-6 meses
                    </div>
                    <div style='background: rgba(234, 179, 8, 0.08); padding: 0.6rem; border-radius: 6px; margin-top: 1rem;'>
                        Monitoramento ativo
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.05) 100%);
                        padding: clamp(1.2rem, 3vw, 1.8rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(59, 130, 246, 0.2);
                        border-left: 5px solid #3b82f6;
                        height: 100%;'>
                <div style='display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1rem;'>
                    <div style='width: 40px; height: 40px;
                                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                        <svg width="20" height="20" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #1e40af; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        BAIXO
                    </h4>
                </div>
                <div style='color: #1e3a8a; font-size: clamp(0.85rem, 2vw, 0.9rem); line-height: 1.7;'>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Pontuação:</strong> < 1.5
                    </div>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Ação:</strong> Observação
                    </div>
                    <div style='margin-bottom: 0.8rem;'>
                        <strong>Prazo:</strong> Contínuo
                    </div>
                    <div style='background: rgba(59, 130, 246, 0.08); padding: 0.6rem; border-radius: 6px; margin-top: 1rem;'>
                        Manutenção preventiva
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

elif pagina == "Detalhamento & Ações":
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 100%;
            padding: clamp(0.5rem, 2vw, 2rem);
        }
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem;
            }
            [data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        
        .stSelectbox [data-baseweb="select"] {
            background: white;
            border: 2px solid rgba(196, 166, 114, 0.3);
            border-radius: 8px;
        }
        
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: #c4a672;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.12) 0%, rgba(232, 220, 200, 0.08) 100%);
                    padding: clamp(1rem, 3vw, 1.5rem) clamp(1.5rem, 4vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    margin-bottom: 2rem;
                    border-left: 4px solid #c4a672;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;'>
                <div style='flex: 1; min-width: 200px;'>
                    <h1 style='margin: 0; color: #5a4a3a; font-size: clamp(1.5rem, 4vw, 2.2rem); font-weight: 800; letter-spacing: -0.5px;'>
                        Detalhamento & Ações
                    </h1>
                    <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.85rem, 2vw, 1rem);'>
                        Da identificação à ação concreta - Planos fundamentados
                    </p>
                </div>
                <div style='background: linear-gradient(135deg, #c4a672 0%, #b89656 100%);
                            padding: 0.7rem 1.3rem;
                            border-radius: 10px;
                            text-align: center;
                            box-shadow: 0 4px 12px rgba(168, 136, 70, 0.3);'>
                    <div style='color: rgba(255, 255, 255, 0.85); font-size: 0.7rem; font-weight: 600; letter-spacing: 0.5px;'>
                        CONFORME
                    </div>
                    <div style='color: white; font-size: 1.3rem; font-weight: 800; letter-spacing: 1.5px;'>
                        NR-01
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.1) 0%, rgba(232, 220, 200, 0.06) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border-left: 4px solid #c4a672;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);'>
            <h3 style='margin: 0 0 1.5rem 0; color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Entendendo o Detalhamento Operacional
            </h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: clamp(1rem, 3vw, 2rem);'>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Problema Resolvido
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Elimina abstração. Sai do conceito genérico e vai para <strong>intervenção específica e fundamentada</strong>
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Pergunta Respondida
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6; font-style: italic;'>
                        "O que exatamente dentro desse fator está elevando o risco?"
                    </div>
                </div>
                <div>
                    <div style='color: #c4a672; font-weight: 700; font-size: clamp(0.75rem, 1.5vw, 0.8rem); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem;'>
                        Valor Estratégico
                    </div>
                    <div style='color: #6b5847; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        <strong>Conecta dado → causa → ação.</strong> Fecha o ciclo NR-01 com medidas fundamentadas
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    subscalas_disponiveis = sorted(detalhamento_data['subescala'].unique())
    
    col_sel1, col_sel2, col_sel3 = st.columns([2, 1, 1])
    
    with col_sel1:
        st.markdown("""
            <div style='margin-bottom: 0.5rem;'>
                <label style='color: #5a4a3a; font-weight: 700; font-size: clamp(0.85rem, 2vw, 0.9rem);'>
                    Selecione o Fator para Análise Detalhada
                </label>
            </div>
        """, unsafe_allow_html=True)
        subscala_selecionada = st.selectbox(
            "",
            options=subscalas_disponiveis,
            index=0,
            label_visibility="collapsed"
        )
    
    with col_sel2:
        qtd_itens = len(detalhamento_data[detalhamento_data['subescala'] == subscala_selecionada])
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(0.8rem, 2vw, 1rem);
                        border-radius: clamp(10px, 2vw, 12px);
                        border: 2px solid rgba(196, 166, 114, 0.2);
                        text-align: center;
                        margin-top: 1.8rem;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem); font-weight: 600; text-transform: uppercase; margin-bottom: 0.3rem;'>
                    Perguntas
                </div>
                <div style='color: #c4a672; font-size: clamp(1.5rem, 4vw, 1.8rem); font-weight: 800;'>
                    {qtd_itens}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_sel3:
        df_temp = detalhamento_data[detalhamento_data['subescala'] == subscala_selecionada]
        media_fator = df_temp['media'].mean()
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                        padding: clamp(0.8rem, 2vw, 1rem);
                        border-radius: clamp(10px, 2vw, 12px);
                        border: 2px solid rgba(196, 166, 114, 0.2);
                        text-align: center;
                        margin-top: 1.8rem;'>
                <div style='color: #8b7663; font-size: clamp(0.7rem, 1.5vw, 0.75rem); font-weight: 600; text-transform: uppercase; margin-bottom: 0.3rem;'>
                    Média Geral
                </div>
                <div style='color: #b89656; font-size: clamp(1.5rem, 4vw, 1.8rem); font-weight: 800;'>
                    {media_fator:.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 242, 230, 0.9) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(12px, 2vw, 16px);
                    border: 2px solid rgba(196, 166, 114, 0.2);
                    box-shadow: 0 4px 16px rgba(107, 88, 71, 0.08);
                    margin-bottom: 2rem;'>
            <div style='margin-bottom: 1.5rem;'>
                <h3 style='margin: 0; color: #5a4a3a; font-size: clamp(1.2rem, 3vw, 1.4rem); font-weight: 700;'>
                    Análise Granular por Item
                </h3>
                <p style='margin: 0.4rem 0 0 0; color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
                    Cada barra representa uma pergunta específica do questionário - Scores mais altos = maior risco percebido
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    df_detalhe = detalhamento_data[detalhamento_data['subescala'] == subscala_selecionada].copy()
    df_detalhe = df_detalhe.sort_values('media', ascending=True)
    
    colors_detalhe = [get_risk_color_classe(classe) for classe in df_detalhe['classe_risco']]
    
    num_items_detalhe = len(df_detalhe)
    chart_height_detalhe = calculate_responsive_height(num_items_detalhe, min_height=400, item_height=35)

    fig7 = go.Figure(go.Bar(
        x=df_detalhe['media'],
        y=df_detalhe['pergunta'],
        orientation='h',
        marker=dict(
            color=colors_detalhe,
            line=dict(width=1, color='rgba(0,0,0,0.05)')
        ),
        text=df_detalhe['media'].round(2),
        textposition='outside',
        textfont=dict(size=14, color='#5a4a3a', family='Arial', weight='bold'),
        customdata=df_detalhe['classe_risco'],
        hovertemplate='<b>%{y}</b><br>Score Médio: <b>%{x:.2f}</b><br>Classe: %{customdata}<extra></extra>'
    ))

    layout_config = create_responsive_layout_config()
    fig7.update_layout(
        **layout_config,
        height=chart_height_detalhe,
        showlegend=False,
        xaxis=dict(
            range=[0, 5],
            gridcolor='rgba(196, 166, 114, 0.2)',
            showline=False,
            title=dict(
                text='Score Médio (0 = Baixo Risco → 5 = Alto Risco)',
                font=dict(size=14, color='#5a4a3a', family='Arial', weight='bold')
            ),
            tickfont=dict(size=13, color='#6b5847', family='Arial', weight='bold')
        ),
        yaxis=dict(
            tickfont=dict(size=13, color='#5a4a3a', family='Arial', weight='bold'),
            showline=False
        )
    )
    st.plotly_chart(fig7, use_container_width=True, config={'responsive': True, 'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)
    
    item_critico = df_detalhe.nlargest(1, 'media').iloc[0]
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(10px, 2vw, 14px);
                    margin-bottom: 2rem;
                    box-shadow: 0 6px 20px rgba(220, 38, 38, 0.25);
                    border: 2px solid rgba(255, 255, 255, 0.15);'>
            <div style='display: flex; align-items: center; gap: clamp(0.8rem, 2vw, 1.2rem); flex-wrap: wrap;'>
                <div style='min-width: 50px; height: 50px;
                            background: rgba(255, 255, 255, 0.15);
                            border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;'>
                    <svg width="26" height="26" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                </div>
                <div style='flex: 1; min-width: 250px;'>
                    <div style='color: rgba(255, 255, 255, 0.85); font-size: clamp(0.7rem, 1.5vw, 0.75rem); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.3rem;'>
                        Item Mais Crítico Identificado
                    </div>
                    <div style='color: white; font-size: clamp(0.95rem, 2.2vw, 1.05rem); font-weight: 600; line-height: 1.4;'>
                        "{item_critico['pergunta']}" 
                        <span style='display: inline-block; margin-left: 0.8rem; padding: 0.3rem 0.8rem; background: rgba(255, 255, 255, 0.2); border-radius: 20px; font-size: clamp(1rem, 2.5vw, 1.2rem); font-weight: 800;'>
                            {item_critico['media']:.2f}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='margin: 2rem 0 1.5rem 0;'>
            <h3 style='color: #5a4a3a; font-size: clamp(1.1rem, 2.5vw, 1.3rem); font-weight: 700;'>
                Plano de Ação Fundamentado
            </h3>
            <p style='color: #8b7663; font-size: clamp(0.8rem, 2vw, 0.9rem); margin: 0.4rem 0 0 0;'>
                Medidas preventivas, corretivas e indicadores de acompanhamento
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_acao1, col_acao2 = st.columns(2)
    
    with col_acao1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.05) 100%);
                        padding: clamp(1.2rem, 3vw, 1.8rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(59, 130, 246, 0.2);
                        border-left: 5px solid #3b82f6;
                        margin-bottom: 1.5rem;
                        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.08);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 45px; height: 45px;
                                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);'>
                        <svg width="22" height="22" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #1e40af; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        Medida Preventiva
                    </h4>
                </div>
                <div style='color: #1e3a8a; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.7;'>
                    Implementar programa estruturado de <strong>feedback trimestral</strong> com metodologia 360°, 
                    garantindo que colaboradores recebam retorno claro sobre desempenho e contribuições.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(220, 38, 38, 0.08) 0%, rgba(185, 28, 28, 0.05) 100%);
                        padding: clamp(1.2rem, 3vw, 1.8rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(220, 38, 38, 0.2);
                        border-left: 5px solid #dc2626;
                        box-shadow: 0 4px 16px rgba(220, 38, 38, 0.08);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 45px; height: 45px;
                                background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);'>
                        <svg width="22" height="22" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #991b1b; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        Medida Corretiva
                    </h4>
                </div>
                <div style='color: #7f1d1d; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.7;'>
                    Revisar processos de <strong>reconhecimento</strong>, criar plano de carreira visível e transparente, 
                    implementar sistema de recompensas alinhado ao esforço e resultados.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_acao2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.05) 100%);
                        padding: clamp(1.2rem, 3vw, 1.8rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(16, 185, 129, 0.2);
                        border-left: 5px solid #10b981;
                        margin-bottom: 1.5rem;
                        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 45px; height: 45px;
                                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                        <svg width="22" height="22" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #065f46; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        Indicadores
                    </h4>
                </div>
                <div style='color: #064e3b; font-size: clamp(0.85rem, 2vw, 0.9rem); line-height: 1.8;'>
                    <div style='margin-bottom: 0.6rem;'><strong>Meta:</strong> Score &lt; 2.5 em 6 meses</div>
                    <div style='margin-bottom: 0.6rem;'><strong>Frequência:</strong> Pulse surveys mensais</div>
                    <div style='margin-bottom: 0.6rem;'><strong>Responsáveis:</strong> RH + Gestão direta</div>
                    <div><strong>Evidências:</strong> Atas de feedback, registros</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(168, 85, 247, 0.08) 0%, rgba(147, 51, 234, 0.05) 100%);
                        padding: clamp(1.2rem, 3vw, 1.8rem);
                        border-radius: clamp(10px, 2vw, 14px);
                        border: 2px solid rgba(168, 85, 247, 0.2);
                        border-left: 5px solid #a855f7;
                        box-shadow: 0 4px 16px rgba(168, 85, 247, 0.08);'>
                <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
                    <div style='width: 45px; height: 45px;
                                background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%);
                                border-radius: 10px;
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);'>
                        <svg width="22" height="22" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                            <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                    </div>
                    <h4 style='margin: 0; color: #7e22ce; font-size: clamp(1rem, 2.2vw, 1.1rem); font-weight: 700;'>
                        Cronograma
                    </h4>
                </div>
                <div style='color: #6b21a8; font-size: clamp(0.85rem, 2vw, 0.9rem); line-height: 1.8;'>
                    <div style='margin-bottom: 0.5rem;'><strong>Fase 1 (30d):</strong> Workshop lideranças</div>
                    <div style='margin-bottom: 0.5rem;'><strong>Fase 2 (60d):</strong> Piloto + ajustes</div>
                    <div style='margin-bottom: 0.5rem;'><strong>Fase 3 (90d):</strong> Expansão total</div>
                    <div><strong>Fase 4 (6m):</strong> Avaliação eficácia</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
                    padding: clamp(1.5rem, 3vw, 2rem);
                    border-radius: clamp(10px, 2vw, 14px);
                    border-left: 4px solid #10b981;
                    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08);'>
            <div style='display: flex; align-items: center; gap: clamp(0.8rem, 2vw, 1.2rem); flex-wrap: wrap;'>
                <div style='min-width: 50px; height: 50px;
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            border-radius: 10px;
                            display: flex; align-items: center; justify-content: center;
                            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                    <svg width="26" height="26" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24">
                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                </div>
                <div style='flex: 1; min-width: 250px;'>
                    <h4 style='margin: 0 0 0.5rem 0; color: #065f46; font-size: clamp(1.1rem, 2.5vw, 1.2rem); font-weight: 700;'>
                        Ciclo NR-01 Completo
                    </h4>
                    <div style='color: #064e3b; font-size: clamp(0.85rem, 2vw, 0.95rem); line-height: 1.6;'>
                        Análise finalizada com <strong>identificação → caracterização → hierarquização → contextualização → fundamentação de ações</strong>. 
                        Todos os requisitos da NR-01 foram atendidos de forma estruturada e baseada em dados.
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

## footer geral ##

st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(196, 166, 114, 0.08) 0%, rgba(232, 220, 200, 0.05) 100%);
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                border: 2px solid rgba(196, 166, 114, 0.15);'>
        <div style='color: #5a4a3a; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.8rem;'>
            Dashboard NR-01 - Gestão de Riscos Psicossociais
        </div>
        <div style='color: #8b7663; font-size: 0.9rem; line-height: 1.7;'>
            <strong>Metodologia:</strong> COPSOQ (Copenhagen Psychosocial Questionnaire)<br>
            <strong>Conformidade:</strong> NR-01 - Programa de Gerenciamento de Riscos<br>
            <em>Análise estruturada para fundamentar medidas preventivas e corretivas</em>
        </div>
        <div style='margin-top: 1.5rem; padding-top: 1.5rem; border-top: 2px solid rgba(196, 166, 114, 0.2);'>
            <div style='color: #c4a672; font-size: 0.85rem; font-weight: 600; letter-spacing: 1px;'>
                LUANA PORTELLA • JANEIRO 2026
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
