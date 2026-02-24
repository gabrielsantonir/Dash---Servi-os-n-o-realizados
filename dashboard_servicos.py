import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# ══════════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Dashboard Serviços Não Realizados",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════════
# CSS CUSTOMIZADO - DARK PREMIUM THEME
# ══════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ─── Base ──────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main .block-container {
        padding: 1.5rem 2rem 2rem 2rem;
        max-width: 100%;
    }
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 100%);
        border-bottom: 1px solid rgba(124, 58, 237, 0.2);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F0F1A 0%, #12122B 100%);
        border-right: 1px solid rgba(124, 58, 237, 0.15);
    }

    /* ─── Title Bar ─────────────────────────────────────── */
    .dashboard-title {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #1A1A2E 100%);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 16px;
        padding: 1.2rem 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 24px rgba(124, 58, 237, 0.08);
    }
    .dashboard-title h1 {
        margin: 0;
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #7C3AED, #A78BFA, #C4B5FD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .dashboard-title p {
        margin: 0.3rem 0 0 0;
        color: #9CA3AF;
        font-size: 0.85rem;
        font-weight: 400;
    }

    /* ─── KPI Cards ─────────────────────────────────────── */
    .kpi-card {
        background: linear-gradient(145deg, #1A1A2E, #16213E);
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 14px 14px 0 0;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(124, 58, 237, 0.15);
        border-color: rgba(124, 58, 237, 0.4);
    }
    .kpi-card .kpi-icon {
        font-size: 1.6rem;
        margin-bottom: 0.3rem;
    }
    .kpi-card .kpi-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #9CA3AF;
        margin-bottom: 0.25rem;
    }
    .kpi-card .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .kpi-card .kpi-sub {
        font-size: 0.72rem;
        color: #6B7280;
        margin-top: 0.2rem;
    }

    /* Card color variants */
    .kpi-total::before { background: linear-gradient(90deg, #7C3AED, #A78BFA); }
    .kpi-total .kpi-value { color: #A78BFA; }

    .kpi-realizado::before { background: linear-gradient(90deg, #10B981, #34D399); }
    .kpi-realizado .kpi-value { color: #34D399; }

    .kpi-pendente::before { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
    .kpi-pendente .kpi-value { color: #FBBF24; }

    .kpi-percent::before { background: linear-gradient(90deg, #EF4444, #F87171); }
    .kpi-percent .kpi-value { color: #F87171; }

    .kpi-entrega::before { background: linear-gradient(90deg, #3B82F6, #60A5FA); }
    .kpi-entrega .kpi-value { color: #60A5FA; }

    .kpi-coleta::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
    .kpi-coleta .kpi-value { color: #A78BFA; }

    /* ─── Section Headers ───────────────────────────────── */
    .section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: #E0E0E0;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(124, 58, 237, 0.25);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ─── Chart Container ───────────────────────────────── */
    .chart-container {
        background: linear-gradient(145deg, #1A1A2E, #16213E);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    }

    /* ─── Data Table ────────────────────────────────────── */
    .dataframe-container {
        background: linear-gradient(145deg, #1A1A2E, #16213E);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 14px;
        padding: 1rem;
        overflow-x: auto;
    }
    div[data-testid="stDataFrame"] > div {
        border-radius: 10px;
    }

    /* ─── Upload Area ───────────────────────────────────── */
    section[data-testid="stSidebar"] .stFileUploader {
        border: 2px dashed rgba(124, 58, 237, 0.35);
        border-radius: 12px;
        padding: 0.5rem;
        transition: border-color 0.3s;
    }
    section[data-testid="stSidebar"] .stFileUploader:hover {
        border-color: rgba(124, 58, 237, 0.7);
    }

    /* ─── Tabs ──────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #1A1A2E;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(124, 58, 237, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.55rem 1.5rem;
        font-weight: 600;
        font-size: 0.85rem;
        color: #9CA3AF;
        border: none;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 10px rgba(124, 58, 237, 0.35);
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
    }

    /* ─── Scrollbar ─────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0F0F1A; }
    ::-webkit-scrollbar-thumb { background: #7C3AED55; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #7C3AED; }

    /* ─── Hide Streamlit branding ───────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════════
# PLOTLY THEME
# ══════════════════════════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#D1D5DB", size=12),
    margin=dict(l=20, r=40, t=60, b=20),
)

COLOR_REALIZADO = "#34D399"
COLOR_PENDENTE = "#FBBF24"
COLOR_PALETTE = ["#7C3AED", "#A78BFA", "#C4B5FD", "#3B82F6", "#60A5FA",
                 "#10B981", "#34D399", "#F59E0B", "#FBBF24", "#EF4444",
                 "#F87171", "#EC4899", "#F472B6", "#6366F1", "#818CF8"]
STATUS_COLORS = {
    "COLETADA": "#34D399",
    "ENTREGUE": "#10B981",
    "NÃO ENTREGUE": "#FBBF24",
    "NÃO COLETADA": "#F59E0B",
}


# ══════════════════════════════════════════════════════════════════════════════════
# HELPER: Read uploaded file
# ══════════════════════════════════════════════════════════════════════════════════
def read_uploaded_file(uploaded_file):
    """Read the uploaded .xls / .xlsx file and return a clean DataFrame."""
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name.lower()

    # Try read_html first (common for HTML-disguised .xls files)
    try:
        tables = pd.read_html(io.BytesIO(file_bytes))
        if tables:
            raw = tables[0]
        else:
            raise ValueError("Nenhuma tabela encontrada")
    except Exception:
        # Fall back to openpyxl / xlrd
        try:
            raw = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
        except Exception:
            raw = pd.read_excel(io.BytesIO(file_bytes), engine="xlrd")

    # ── Detect header row (look for "Coleta/Entrega" in any cell) ────────────
    header_row = None
    for idx in range(min(20, len(raw))):
        row_vals = raw.iloc[idx].astype(str).str.strip().tolist()
        if "Coleta/Entrega" in row_vals:
            header_row = idx
            break

    if header_row is None:
        st.error("❌ Não foi possível encontrar o cabeçalho 'Coleta/Entrega' no arquivo.")
        return None

    # ── Build DataFrame with proper headers ──────────────────────────────────
    headers = raw.iloc[header_row].astype(str).str.strip().tolist()
    df = raw.iloc[header_row + 1:].copy()
    df.columns = headers
    df = df.reset_index(drop=True)

    # Drop rows that are still metadata (NaN in key columns or repeat headers)
    df = df[df["Coleta/Entrega"].isin(["COLETA", "ENTREGA", "DESPACHO"])].copy()
    df = df.reset_index(drop=True)

    # ── Clean Ocorrência ─────────────────────────────────────────────────────
    if "Ocorrência" in df.columns:
        df["Ocorrência"] = df["Ocorrência"].fillna("EM BRANCO").astype(str).str.strip()
        df.loc[df["Ocorrência"] == "", "Ocorrência"] = "EM BRANCO"
        df.loc[df["Ocorrência"] == "nan", "Ocorrência"] = "EM BRANCO"

    # ── Derived columns ──────────────────────────────────────────────────────
    status_col = "Status Manifesto"
    df["Classificação"] = df[status_col].apply(
        lambda x: "Realizado" if x in ("COLETADA", "ENTREGUE") else "Pendente"
    )

    # Número do Serviço: Pedido para COLETA, Minuta para ENTREGA
    df["Número Serviço"] = df.apply(
        lambda r: r.get("Pedido Coleta", "") if r["Coleta/Entrega"] == "COLETA"
        else r.get("Minuta/Conhecimento", ""),
        axis=1,
    )

    # Cidade contextual
    df["Cidade Ref"] = df.apply(
        lambda r: r.get("Cidade", "") if r["Coleta/Entrega"] == "COLETA"
        else r.get("Cidade Final", ""),
        axis=1,
    )
    df["Tipo Cidade"] = df["Coleta/Entrega"].apply(
        lambda x: "Cidade Origem" if x == "COLETA" else "Cidade Destino"
    )

    return df


# ══════════════════════════════════════════════════════════════════════════════════
# HELPER: KPI Card HTML
# ══════════════════════════════════════════════════════════════════════════════════
def kpi_card(icon, label, value, sub="", variant="total"):
    return f"""
    <div class="kpi-card kpi-{variant}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """


# ══════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.2rem;">
        <span style="font-size:2.2rem;">📦</span>
        <h3 style="margin:0.3rem 0 0 0; font-weight:700;
                    background: linear-gradient(135deg, #7C3AED, #A78BFA);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;">
            Serviços Logísticos
        </h3>
        <p style="color:#6B7280; font-size:0.75rem; margin:0;">
            Análise de Manifestos
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    uploaded_file = st.file_uploader(
        "📁 Carregar arquivo de Manifesto",
        type=["xls", "xlsx"],
        help="Selecione o arquivo .xls ou .xlsx exportado do sistema.",
    )
    st.markdown("---")

    st.markdown("""
    <div style="background: rgba(124,58,237,0.08); border-radius: 10px;
                padding: 0.8rem; border: 1px solid rgba(124,58,237,0.15);">
        <p style="color:#A78BFA; font-size:0.75rem; font-weight:600; margin:0 0 0.3rem 0;">
            ℹ️ LEGENDA DE STATUS
        </p>
        <p style="color:#34D399; font-size:0.72rem; margin:0.15rem 0;">
            ● COLETADA / ENTREGUE = <b>Realizado</b>
        </p>
        <p style="color:#FBBF24; font-size:0.72rem; margin:0.15rem 0;">
            ● NÃO COLETADA / NÃO ENTREGUE = <b>Pendente</b>
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════════

# Title
st.markdown("""
<div class="dashboard-title">
    <h1>📦 Dashboard — Serviços Não Realizados</h1>
    <p>Visão consolidada de serviços logísticos realizados e pendentes</p>
</div>
""", unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center; padding:4rem 2rem;">
        <span style="font-size:4rem; opacity:0.4;">📁</span>
        <h3 style="color:#6B7280; margin-top:1rem;">Nenhum arquivo carregado</h3>
        <p style="color:#4B5563; font-size:0.9rem;">
            Utilize a barra lateral para carregar o arquivo de Manifesto (.xls ou .xlsx)
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load data ────────────────────────────────────────────────────────────────────
df = read_uploaded_file(uploaded_file)
if df is None:
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["📊 Visão Geral", "🔍 Análise de Pendentes"])

# ╔══════════════════════════════════════════════════════════════════════════════════
# ║ TELA 1 — VISÃO GERAL
# ╚══════════════════════════════════════════════════════════════════════════════════
with tab1:
    total = len(df)
    realizados = len(df[df["Classificação"] == "Realizado"])
    pendentes = len(df[df["Classificação"] == "Pendente"])
    pct_pendentes = (pendentes / total * 100) if total > 0 else 0

    # ── KPI Row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("📦", "Total de Serviços", f"{total:,}",
                             "coletas + entregas", "total"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("✅", "Realizados", f"{realizados:,}",
                             f"{realizados/total*100:.1f}% do total" if total else "—", "realizado"),
                    unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("⏳", "Pendentes", f"{pendentes:,}",
                             f"{pct_pendentes:.1f}% do total", "pendente"),
                    unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("🚨", "% Pendentes", f"{pct_pendentes:.1f}%",
                             "serviços não realizados", "percent"),
                    unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Charts Row 1: Donut + Status Breakdown ──────────────────────────────
    col_left, col_right = st.columns([1, 1.3])

    with col_left:
        st.markdown('<div class="section-header">🍩 Realizados vs Pendentes</div>',
                    unsafe_allow_html=True)
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Realizado", "Pendente"],
            values=[realizados, pendentes],
            hole=0.6,
            marker=dict(colors=[COLOR_REALIZADO, COLOR_PENDENTE],
                        line=dict(color="#0F0F1A", width=3)),
            textinfo="label+percent",
            textfont=dict(size=13, color="#E0E0E0"),
            hoverinfo="label+value+percent",
        )])
        donut_layout = {**PLOTLY_LAYOUT, "height": 340, "showlegend": True,
                        "legend": dict(orientation="h", y=-0.1, x=0.5, xanchor="center",
                                       bgcolor="rgba(26,26,46,0.8)",
                                       bordercolor="rgba(124,58,237,0.2)", borderwidth=1,
                                       font=dict(size=11, color="#D1D5DB"))}
        fig_donut.update_layout(**donut_layout)
        fig_donut.add_annotation(text=f"<b>{total}</b><br><span style='font-size:11px'>Total</span>",
                                  x=0.5, y=0.5, showarrow=False,
                                  font=dict(size=22, color="#A78BFA"))
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        st.markdown('<div class="section-header">📊 Detalhamento por Status</div>',
                    unsafe_allow_html=True)
        status_counts = df["Status Manifesto"].value_counts().reset_index()
        status_counts.columns = ["Status", "Quantidade"]
        colors = [STATUS_COLORS.get(s, "#7C3AED") for s in status_counts["Status"]]

        fig_status = go.Figure(data=[go.Bar(
            x=status_counts["Status"],
            y=status_counts["Quantidade"],
            marker=dict(color=colors, line=dict(color="rgba(0,0,0,0.2)", width=1),
                        cornerradius=6),
            text=status_counts["Quantidade"],
            textposition="outside",
            textfont=dict(size=13, color="#E0E0E0", family="Inter"),
            cliponaxis=False,
        )])
        fig_status.update_layout(**PLOTLY_LAYOUT, height=380,
                                  yaxis=dict(gridcolor="rgba(124,58,237,0.08)",
                                             zeroline=False, showticklabels=False,
                                             range=[0, status_counts["Quantidade"].max() * 1.2]),
                                  xaxis=dict(gridcolor="rgba(0,0,0,0)", zeroline=False))
        st.plotly_chart(fig_status, use_container_width=True, config={"displayModeBar": False})

    # ── Chart Row 2: Ocorrência ──────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Distribuição por Ocorrência (Pendentes)</div>',
                unsafe_allow_html=True)

    df_pend_ocorrencia = df[df["Classificação"] == "Pendente"]
    ocorrencia_counts = df_pend_ocorrencia["Ocorrência"].value_counts().reset_index()
    ocorrencia_counts.columns = ["Ocorrência", "Quantidade"]

    fig_ocorrencia = go.Figure(data=[go.Bar(
        y=ocorrencia_counts["Ocorrência"],
        x=ocorrencia_counts["Quantidade"],
        orientation="h",
        marker=dict(
            color=[COLOR_PALETTE[i % len(COLOR_PALETTE)] for i in range(len(ocorrencia_counts))],
            line=dict(color="rgba(0,0,0,0.15)", width=1),
            cornerradius=5,
        ),
        text=ocorrencia_counts["Quantidade"],
        textposition="outside",
        textfont=dict(size=12, color="#E0E0E0"),
    )])
    fig_ocorrencia.update_layout(
        **PLOTLY_LAYOUT, height=max(280, len(ocorrencia_counts) * 42),
        yaxis=dict(autorange="reversed", gridcolor="rgba(0,0,0,0)", zeroline=False,
                   tickfont=dict(size=11)),
        xaxis=dict(gridcolor="rgba(124,58,237,0.06)", zeroline=False, showticklabels=False),
    )
    st.plotly_chart(fig_ocorrencia, use_container_width=True, config={"displayModeBar": False})

    # ── Data Table ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📄 Tabela de Serviços</div>',
                unsafe_allow_html=True)

    display_cols = ["Coleta/Entrega", "Número Serviço", "Motorista", "Cliente",
                    "Tipo Cidade", "Cidade Ref", "Status Manifesto", "Ocorrência"]
    available_cols = [c for c in display_cols if c in df.columns]
    df_display = df[available_cols].copy()

    # Rename for clarity
    rename_map = {"Cidade Ref": "Cidade", "Número Serviço": "Nº Serviço"}
    df_display = df_display.rename(columns=rename_map)

    st.dataframe(df_display, use_container_width=True, height=420,
                 hide_index=True)


# ╔══════════════════════════════════════════════════════════════════════════════════
# ║ TELA 2 — ANÁLISE DE PENDENTES
# ╚══════════════════════════════════════════════════════════════════════════════════
with tab2:
    df_pendentes = df[df["Classificação"] == "Pendente"].copy()

    if df_pendentes.empty:
        st.markdown("""
        <div style="text-align:center; padding:4rem 2rem;">
            <span style="font-size:4rem;">🎉</span>
            <h3 style="color:#34D399; margin-top:1rem;">Nenhum serviço pendente!</h3>
            <p style="color:#6B7280;">Todos os serviços foram realizados com sucesso.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    entregas_pend = df_pendentes[df_pendentes["Coleta/Entrega"] == "ENTREGA"]
    coletas_pend = df_pendentes[df_pendentes["Coleta/Entrega"] == "COLETA"]

    total_pend = len(df_pendentes)
    total_entregas_pend = len(entregas_pend)
    total_coletas_pend = len(coletas_pend)

    # ── KPI Row ──────────────────────────────────────────────────────────────
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(kpi_card("🚨", "Total Pendentes", f"{total_pend:,}",
                             "entregas + coletas", "pendente"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("🚚", "Entregas Pendentes", f"{total_entregas_pend:,}",
                             f"{total_entregas_pend/total_pend*100:.1f}% dos pendentes" if total_pend else "—",
                             "entrega"), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("📥", "Coletas Pendentes", f"{total_coletas_pend:,}",
                             f"{total_coletas_pend/total_pend*100:.1f}% dos pendentes" if total_pend else "—",
                             "coleta"), unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Charts: Entregas + Coletas Pendentes ─────────────────────────────────
    col_ent, col_col = st.columns(2)

    with col_ent:
        st.markdown('<div class="section-header">🚚 Entregas Pendentes por Cidade Destino</div>',
                    unsafe_allow_html=True)
        if not entregas_pend.empty:
            city_ent = entregas_pend["Cidade Final"].fillna("NÃO INFORMADO").value_counts().reset_index()
            city_ent.columns = ["Cidade Destino", "Quantidade"]

            fig_ent = go.Figure(data=[go.Bar(
                y=city_ent["Cidade Destino"],
                x=city_ent["Quantidade"],
                orientation="h",
                marker=dict(
                    color=["#3B82F6" if i == 0 else "#60A5FA" if i == 1 else "#93C5FD"
                           for i in range(len(city_ent))],
                    line=dict(color="rgba(0,0,0,0.2)", width=1),
                    cornerradius=5,
                ),
                text=city_ent["Quantidade"],
                textposition="outside",
                textfont=dict(size=12, color="#E0E0E0"),
                cliponaxis=False,
            )])
            fig_ent.update_layout(**PLOTLY_LAYOUT,
                                   height=max(300, len(city_ent) * 38),
                                   yaxis=dict(autorange="reversed", gridcolor="rgba(0,0,0,0)",
                                              zeroline=False, tickfont=dict(size=11)),
                                   xaxis=dict(gridcolor="rgba(124,58,237,0.06)",
                                              zeroline=False, showticklabels=False))
            st.plotly_chart(fig_ent, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Nenhuma entrega pendente encontrada.")

    with col_col:
        st.markdown('<div class="section-header">📥 Coletas Pendentes por Cidade Origem</div>',
                    unsafe_allow_html=True)
        if not coletas_pend.empty:
            city_col = coletas_pend["Cidade"].fillna("NÃO INFORMADO").value_counts().reset_index()
            city_col.columns = ["Cidade Origem", "Quantidade"]

            fig_col = go.Figure(data=[go.Bar(
                y=city_col["Cidade Origem"],
                x=city_col["Quantidade"],
                orientation="h",
                marker=dict(
                    color=["#8B5CF6" if i == 0 else "#A78BFA" if i == 1 else "#C4B5FD"
                           for i in range(len(city_col))],
                    line=dict(color="rgba(0,0,0,0.2)", width=1),
                    cornerradius=5,
                ),
                text=city_col["Quantidade"],
                textposition="outside",
                textfont=dict(size=12, color="#E0E0E0"),
                cliponaxis=False,
            )])
            fig_col.update_layout(**PLOTLY_LAYOUT,
                                   height=max(300, len(city_col) * 38),
                                   yaxis=dict(autorange="reversed", gridcolor="rgba(0,0,0,0)",
                                              zeroline=False, tickfont=dict(size=11)),
                                   xaxis=dict(gridcolor="rgba(124,58,237,0.06)",
                                              zeroline=False, showticklabels=False))
            st.plotly_chart(fig_col, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Nenhuma coleta pendente encontrada.")

    # ── Chart: Motoristas com Pendentes ──────────────────────────────────────
    st.markdown('<div class="section-header">👤 Serviços Não Realizados por Motorista</div>',
                unsafe_allow_html=True)

    motorista_counts = df_pendentes["Motorista"].fillna("NÃO INFORMADO").value_counts().reset_index()
    motorista_counts.columns = ["Motorista", "Quantidade"]

    fig_mot = go.Figure(data=[go.Bar(
        y=motorista_counts["Motorista"],
        x=motorista_counts["Quantidade"],
        orientation="h",
        marker=dict(
            color=[COLOR_PALETTE[i % len(COLOR_PALETTE)] for i in range(len(motorista_counts))],
            line=dict(color="rgba(0,0,0,0.15)", width=1),
            cornerradius=5,
        ),
        text=motorista_counts["Quantidade"],
        textposition="outside",
        textfont=dict(size=12, color="#E0E0E0"),
    )])
    fig_mot.update_layout(
        **PLOTLY_LAYOUT, height=max(320, len(motorista_counts) * 48),
        yaxis=dict(autorange="reversed", gridcolor="rgba(0,0,0,0)", zeroline=False,
                   tickfont=dict(size=11)),
        xaxis=dict(gridcolor="rgba(124,58,237,0.06)", zeroline=False, showticklabels=False),
    )
    st.plotly_chart(fig_mot, use_container_width=True, config={"displayModeBar": False})

    # ── Detail Table ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📄 Detalhamento dos Serviços Pendentes</div>',
                unsafe_allow_html=True)

    pend_display_cols = ["Coleta/Entrega", "Número Serviço", "Motorista", "Cliente",
                         "Tipo Cidade", "Cidade Ref", "Status Manifesto", "Ocorrência"]
    pend_available = [c for c in pend_display_cols if c in df_pendentes.columns]
    df_pend_display = df_pendentes[pend_available].copy()
    df_pend_display = df_pend_display.rename(columns={"Cidade Ref": "Cidade", "Número Serviço": "Nº Serviço"})

    st.dataframe(df_pend_display, use_container_width=True, height=420, hide_index=True)
