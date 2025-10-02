# dashboard_france_tv_all_channels.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="France Télévisions - Toutes Chaînes Live",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #0055A4, #FFFFFF, #EF4135);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .live-badge {
        background: linear-gradient(45deg, #0055A4, #EF4135);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    .channel-card {
        background: rgba(0, 85, 164, 0.08);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0055A4;
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    .channel-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .positive { color: #00C851; font-weight: bold; }
    .negative { color: #ff4444; font-weight: bold; }
    .neutral { color: #ffbb33; font-weight: bold; }
    .metric-large {
        font-size: 1.4rem;
        font-weight: bold;
        color: #0055A4;
    }
</style>
""", unsafe_allow_html=True)

class FranceTVAllChannels:
    def __init__(self):
        self.data_history = {}
        self.initialize_all_channels_data()
        
    def initialize_all_channels_data(self):
        """Initialise les données pour toutes les chaînes France Télévisions"""
        self.current_time = datetime.now()
        
        # Données réalistes pour toutes les chaînes
        self.channels_data = {
            'France 2': {
                'viewers': 2100000,
                'share': 13.2,
                'program': 'Journal de 13h',
                'trend': 'up',
                'change': '+2.1%',
                'category': 'Généraliste',
                'color': '#0055A4',
                'peak_today': 4200000
            },
            'France 3': {
                'viewers': 1800000,
                'share': 10.5,
                'program': 'Magazines régionaux',
                'trend': 'stable',
                'change': '+0.3%',
                'category': 'Régionale',
                'color': '#EF4135',
                'peak_today': 3200000
            },
            'France 4': {
                'viewers': 450000,
                'share': 2.8,
                'program': 'Jeunesse et divertissement',
                'trend': 'up',
                'change': '+1.5%',
                'category': 'Jeunesse',
                'color': '#00A8E8',
                'peak_today': 850000
            },
            'France 5': {
                'viewers': 850000,
                'share': 4.8,
                'program': 'Documentaire scientifique',
                'trend': 'up',
                'change': '+1.2%',
                'category': 'Savoir',
                'color': '#8A2BE2',
                'peak_today': 1800000
            },
            'France Info': {
                'viewers': 350000,
                'share': 2.1,
                'program': 'Info continue',
                'trend': 'stable',
                'change': '+0.8%',
                'category': 'Info',
                'color': '#FF6B00',
                'peak_today': 650000
            },
            'Culturebox': {
                'viewers': 280000,
                'share': 1.7,
                'program': 'Spectacle vivant',
                'trend': 'up',
                'change': '+2.3%',
                'category': 'Culture',
                'color': '#FF4081',
                'peak_today': 520000
            },
            'France Ô': {
                'viewers': 180000,
                'share': 1.1,
                'program': 'Magazine Outre-Mer',
                'trend': 'stable',
                'change': '+0.5%',
                'category': 'Outre-Mer',
                'color': '#FFD700',
                'peak_today': 380000
            }
        }
        
        # Métriques globales
        self.global_metrics = {
            'total_viewers': 5418000,
            'total_share': 32.2,
            'digital_traffic': 12500000,
            'mobile_percent': 65,
            'engagement_rate': 72,
            'market_rank': 1
        }
        
        # Données géographiques détaillées
        self.geo_data = {
            'Île-de-France': 1250000,
            'Auvergne-Rhône-Alpes': 680000,
            'Provence-Alpes-Côte d\'Azur': 580000,
            'Occitanie': 520000,
            'Hauts-de-France': 480000,
            'Nouvelle-Aquitaine': 450000,
            'Grand Est': 420000,
            'Normandie': 320000,
            'Pays de la Loire': 350000,
            'Bretagne': 300000,
            'Bourgogne-Franche-Comté': 280000,
            'Centre-Val de Loire': 260000,
            'Corse': 75000,
            'Outre-Mer': 180000
        }
        
        # Plateformes
        self.platform_data = {
            'Télévision traditionnelle': 68,
            'France.tv (replay)': 18,
            'Application mobile': 9,
            'Web direct': 3,
            'TV connectée': 2
        }
        
        self.init_history_data()
    
    def init_history_data(self):
        """Initialise l'historique des données pour toutes les chaînes"""
        timestamps = [datetime.now() - timedelta(minutes=x) for x in range(120, 0, -2)]
        
        self.data_history = {'timestamp': timestamps}
        
        for channel in self.channels_data:
            base_viewers = self.channels_data[channel]['viewers']
            self.data_history[channel] = [
                base_viewers + random.randint(-int(base_viewers * 0.1), int(base_viewers * 0.1))
                for _ in range(60)
            ]
        
        self.data_history['total'] = [
            self.global_metrics['total_viewers'] + random.randint(-200000, 200000)
            for _ in range(60)
        ]
        self.data_history['digital'] = [
            self.global_metrics['digital_traffic'] + random.randint(-500000, 500000)
            for _ in range(60)
        ]
    
    def update_live_data(self):
        """Met à jour toutes les données en temps réel"""
        current_time = datetime.now()
        hour = current_time.hour
        
        # Facteurs saisonniers réalistes
        if hour in [8, 13, 20]:  # Pic des journaux
            volatility = 0.07
        elif 20 <= hour <= 23:  # Prime time
            volatility = 0.05
        elif 0 <= hour <= 6:  # Nuit
            volatility = 0.12
        else:  # Journée normale
            volatility = 0.04
        
        # Mise à jour de chaque chaîne
        total_viewers = 0
        
        for channel in self.channels_data:
            current_viewers = self.channels_data[channel]['viewers']
            change = random.randint(-int(current_viewers * volatility), int(current_viewers * volatility))
            
            new_viewers = max(current_viewers + change, int(current_viewers * 0.3))
            self.channels_data[channel]['viewers'] = new_viewers
            total_viewers += new_viewers
            
            # Mise à jour tendance et changement
            trend = self.get_trend(change, current_viewers)
            self.channels_data[channel]['trend'] = trend
            self.channels_data[channel]['change'] = f"{change/current_viewers*100:+.1f}%"
            
            # Mise à jour pic du jour
            if new_viewers > self.channels_data[channel]['peak_today']:
                self.channels_data[channel]['peak_today'] = new_viewers
        
        # Mise à jour métriques globales
        self.global_metrics['total_viewers'] = total_viewers + random.randint(500000, 800000)
        
        # Digital (variations plus importantes)
        digital_change = random.randint(-1000000, 1500000)
        self.global_metrics['digital_traffic'] = max(
            self.global_metrics['digital_traffic'] + digital_change, 
            8000000
        )
        
        # Mise à jour historique
        self.update_history_data()
        
        # Rotation occasionnelle des programmes
        if random.random() < 0.15:
            self.rotate_programs()
    
    def get_trend(self, change, current):
        """Détermine la tendance"""
        if abs(change/current) < 0.005:  # Moins de 0.5% de changement
            return 'stable'
        return 'up' if change > 0 else 'down'
    
    def rotate_programs(self):
        """Change occasionnellement les programmes"""
        programs = {
            'France 2': ['Journal de 13h', 'Feuilleton', 'Débat politique', 'Magazine culturel', 'Sport'],
            'France 3': ['Magazines régionaux', 'Documentaire régional', 'Jeu', 'Information locale'],
            'France 4': ['Jeunesse et divertissement', 'Série animée', 'Divertissement', 'Rediffusion'],
            'France 5': ['Documentaire scientifique', 'Émission santé', 'Histoire', 'Environnement'],
            'France Info': ['Info continue', 'Débat d\'actualité', 'Reportage', 'Interview'],
            'Culturebox': ['Spectacle vivant', 'Concert', 'Théâtre', 'Opéra'],
            'France Ô': ['Magazine Outre-Mer', 'Documentaire DOM-TOM', 'Culture outre-mer', 'Débats']
        }
        
        for channel, program_list in programs.items():
            if random.random() < 0.3:  # 30% de chance par chaîne
                self.channels_data[channel]['program'] = random.choice(program_list)
    
    def update_history_data(self):
        """Met à jour l'historique"""
        current_time = datetime.now()
        
        self.data_history['timestamp'].append(current_time)
        
        for channel in self.channels_data:
            self.data_history[channel].append(self.channels_data[channel]['viewers'])
        
        self.data_history['total'].append(self.global_metrics['total_viewers'])
        self.data_history['digital'].append(self.global_metrics['digital_traffic'])
        
        # Garde seulement les 60 dernières valeurs
        for key in self.data_history:
            if len(self.data_history[key]) > 60:
                self.data_history[key] = self.data_history[key][-60:]

class AllChannelsDashboard:
    def __init__(self):
        self.data_manager = FranceTVAllChannels()
        self.last_update = datetime.now()
        
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/fr/thumb/3/3f/France_T%C3%A9l%C3%A9visions_2018.svg/1200px-France_T%C3%A9l%C3%A9visions_2018.svg.png", 
                    width=150)
        
        with col2:
            st.markdown('<h1 class="main-header">FRANCE TÉLÉVISIONS LIVE</h1>', unsafe_allow_html=True)
            st.markdown('<div class="live-badge">📡 TOUTES LES CHAÎNES - DONNÉES TEMPS RÉEL</div>', unsafe_allow_html=True)
        
        with col3:
            current_time = datetime.now().strftime('%H:%M:%S')
            st.markdown(f"**🕐 {current_time}**")
            st.markdown(f"**📅 {datetime.now().strftime('%d/%m/%Y')}**")
            st.markdown(f"**👥 {self.data_manager.global_metrics['total_viewers']:,} téléspectateurs**".replace(',', ' '))
    
    def display_global_metrics(self):
        """Affiche les métriques globales"""
        st.markdown("### 📊 **VUE D'ENSEMBLE DU GROUPE**")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="**AUDIENCE TOTALE**",
                value=f"{self.data_manager.global_metrics['total_viewers']:,}".replace(',', ' '),
                delta=f"{self.data_manager.global_metrics['total_share']}% part marché"
            )
        
        with col2:
            st.metric(
                label="**FRANCE.TV**",
                value=f"{self.data_manager.global_metrics['digital_traffic']:,}".replace(',', ' '),
                delta="+25% vs 2023"
            )
        
        with col3:
            st.metric(
                label="**ENGAGEMENT**",
                value=f"{self.data_manager.global_metrics['engagement_rate']}%",
                delta="+8%"
            )
        
        with col4:
            st.metric(
                label="**MOBILE**",
                value=f"{self.data_manager.global_metrics['mobile_percent']}%",
                delta="+12%"
            )
        
        with col5:
            rank = self.data_manager.global_metrics['market_rank']
            st.metric(
                label="**CLASSEMENT**",
                value=f"{rank}er groupe français",
                delta="Leader"
            )
    
    def display_channels_grid(self):
        """Affiche la grille de toutes les chaînes"""
        st.markdown("### 📺 **CHAÎNES EN DIRECT**")
        
        # Crée 4 colonnes pour afficher les chaînes
        cols = st.columns(4)
        
        for idx, (channel, data) in enumerate(self.data_manager.channels_data.items()):
            with cols[idx % 4]:
                trend_icon = "📈" if data['trend'] == 'up' else "📉" if data['trend'] == 'down' else "➡️"
                trend_class = "positive" if data['trend'] == 'up' else "negative" if data['trend'] == 'down' else "neutral"
                
                st.markdown(f"""
                <div class="channel-card">
                    <h4>{channel} {trend_icon}</h4>
                    <div class="metric-large">{data['viewers']:,}</div>
                    <p><span class="{trend_class}">{data['change']}</span> • {data['share']}% part</p>
                    <p><small>📺 {data['program']}</small></p>
                    <p><small>🏆 Pic: {data['peak_today']:,}</small></p>
                </div>
                """.replace(',', ' '), unsafe_allow_html=True)
    
    def create_live_charts(self):
        """Crée les graphiques en temps réel"""
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Évolution Audience", "📊 Comparaison Chaînes", "🗺️ Carte Audience", "📱 Plateformes"])
        
        with tab1:
            self.create_evolution_chart()
        
        with tab2:
            self.create_comparison_chart()
        
        with tab3:
            self.create_geo_chart()
        
        with tab4:
            self.create_platforms_chart()
    
    def create_evolution_chart(self):
        """Graphique d'évolution temporelle"""
        fig = go.Figure()
        
        # Ajoute les 3 chaînes principales
        main_channels = ['France 2', 'France 3', 'France 5']
        colors = ['#0055A4', '#EF4135', '#8A2BE2']
        
        for i, channel in enumerate(main_channels):
            fig.add_trace(go.Scatter(
                x=self.data_manager.data_history['timestamp'],
                y=self.data_manager.data_history[channel],
                name=channel,
                line=dict(color=colors[i], width=3),
                mode='lines'
            ))
        
        fig.update_layout(
            title="Évolution de l'Audience - 60 Dernières Minutes",
            xaxis_title="Heure",
            yaxis_title="Téléspectateurs",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_comparison_chart(self):
        """Graphique de comparaison entre chaînes"""
        channels = list(self.data_manager.channels_data.keys())
        viewers = [self.data_manager.channels_data[channel]['viewers'] for channel in channels]
        colors = [self.data_manager.channels_data[channel]['color'] for channel in channels]
        
        fig = px.bar(
            x=channels, 
            y=viewers,
            title="Audience Actuelle par Chaîne",
            labels={'x': 'Chaîne', 'y': 'Téléspectateurs'},
            color=channels,
            color_discrete_sequence=colors
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    def create_geo_chart(self):
        """Carte géographique de l'audience"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            regions_data = {
                'Région': list(self.data_manager.geo_data.keys()),
                'Téléspectateurs': list(self.data_manager.geo_data.values())
            }
            df_regions = pd.DataFrame(regions_data)
            
            fig = px.choropleth(
                df_regions,
                locations='Région',
                locationmode='country names',
                color='Téléspectateurs',
                hover_name='Région',
                title="Audience par Région - France Télévisions",
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏆 Top 5 Régions")
            top_regions = sorted(self.data_manager.geo_data.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for i, (region, viewers) in enumerate(top_regions, 1):
                percentage = (viewers / sum(self.data_manager.geo_data.values())) * 100
                st.markdown(f"""
                <div class="channel-card">
                    <h4>#{i} {region}</h4>
                    <div class="metric-large">{viewers:,}</div>
                    <p>{percentage:.1f}% du total</p>
                </div>
                """.replace(',', ' '), unsafe_allow_html=True)
    
    def create_platforms_chart(self):
        """Graphique des plateformes de visionnage"""
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                values=list(self.data_manager.platform_data.values()),
                names=list(self.data_manager.platform_data.keys()),
                title="Répartition par Plateforme",
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Analyse Digital")
            
            digital_metrics = {
                'Temps moyen/session': '12:45 min',
                'Pages vues/session': '4.2',
                'Taux de rebond': '28%',
                'Nouveaux visiteurs': '42%',
                'Replay +7j': '+35%'
            }
            
            for metric, value in digital_metrics.items():
                st.metric(label=metric, value=value)
    
    def display_france_info_special(self):
        """Section spéciale pour France Info TV"""
        st.markdown("---")
        st.markdown("### 📰 **FRANCE INFO TV - SPÉCIAL INFO CONTINUE**")
        
        france_info_data = self.data_manager.channels_data['France Info']
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FF6B00, #FF8C00); color: white; padding: 1.5rem; border-radius: 10px;">
                <h3>🎙️ {france_info_data['program']}</h3>
                <h2>{france_info_data['viewers']:,} téléspectateurs</h2>
                <p>📊 {france_info_data['share']}% de part d'audience • {france_info_data['change']} vs dernière heure</p>
            </div>
            """.replace(',', ' '), unsafe_allow_html=True)
        
        with col2:
            st.metric("Audience mobile", "58%", "+5%")
            st.metric("Durée moyenne", "22 min", "+3 min")
        
        with col3:
            st.metric("Alertes envoyées", "48K", "+12%")
            st.metric("Social mentions", "3.2K", "+28%")
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Mise à jour des données
        self.data_manager.update_live_data()
        
        # Affichage des composants
        self.display_header()
        self.display_global_metrics()
        self.display_channels_grid()
        self.create_live_charts()
        self.display_france_info_special()
        
        # Contrôles de rafraîchissement
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            refresh_rate = st.slider("Rafraîchissement (s)", 5, 60, 15)
        
        with col2:
            if st.button("🔄 Actualiser maintenant"):
                st.rerun()
        
        with col3:
            st.markdown("""
            <div style="text-align: center; color: #666; font-size: 0.8rem;">
                📊 Données simulées temps réel • France Télévisions 2024 • Service Public
            </div>
            """, unsafe_allow_html=True)
        
        # Auto-rafraîchissement
        time.sleep(refresh_rate)
        st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = AllChannelsDashboard()
    dashboard.run_dashboard()