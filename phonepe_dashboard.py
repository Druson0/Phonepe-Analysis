import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import random
import colorsys
import plotly.express as px

st.set_page_config(page_title="PhonePe Pulse Insights", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    /* Force text elements to be white/light */
    p, span, label, .stMarkdown, .stText {
        color: #f8fafc !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #cbd5e1 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">PhonePe Pulse: India\'s Digital Revolution</p>', unsafe_allow_html=True)
st.markdown('<p style="color:#e2e8f0; font-size:1.1rem; margin-bottom:20px;">Interactive 3D Demographic Map & Graph Reports</p>', unsafe_allow_html=True)

# 25 Insights Data
insights_data = {
    "1. Transaction Dynamics": [
        {"title": "P2P Dominance vs. Untapped Potential", "desc": "Peer-to-peer (P2P) transactions are the primary volume driver, while insurance-related payments remain a minimal share, representing a significant cross-sell opportunity.", "states": []},
        {"title": "626% Hyper-growth in Merchant Payments", "desc": "Between 2019 and 2021, merchant onboarding and QR adoption saw explosive growth, accelerated by a structural shift toward contactless payments.", "states": []},
        {"title": "Post-2020 Growth Acceleration", "desc": "Transaction growth accelerated significantly after 2010, transitioning from a temporary spike to a permanent behavioral shift in the Indian economy.", "states": []},
        {"title": "Strong User Retention and Frequency", "desc": "The absence of prolonged stagnation periods suggests that once users adopt the platform, they maintain high transaction frequency and retention.", "states": []},
        {"title": "Network Effects in Full Force", "desc": "Steepening growth curves through 2024 indicate that expanding merchant networks and user bases are creating a self-reinforcing ecosystem.", "states": []}
    ],
    "2. Geographic & District Insights": [
        {"title": "Economic Powerhouses Lead Volume", "desc": "Telangana, Karnataka, and Maharashtra contribute the highest total transaction value, reflecting strong adoption in economically active states.", "states": ["Telangana", "Karnataka", "Maharashtra"]},
        {"title": "Metro Concentration Risk", "desc": "High transaction concentration is seen in top metro districts (like Pune), which often contribute over 70% of a state's total digital payment value.", "states": ["Maharashtra"]},
        {"title": "Breakout Districts: The 3,000% Club", "desc": "Non-metro districts like Koderma (Jharkhand) and Dhubri (Assam) recorded YoY growth rates exceeding 3,000%, far outstripping state averages.", "states": ["Jharkhand", "Assam"]},
        {"title": "The Tier-2 & Tier-3 Surge", "desc": "High growth in Rajasthan, Bihar, and Manipur proves that digital penetration is expanding aggressively into semi-urban and emerging regions.", "states": ["Rajasthan", "Bihar", "Manipur"]},
        {"title": "Shift to District-Specific Strategy", "desc": "Massive growth gaps within states necessitates a shift from broad state-level to hyper-local targeting.", "states": []}
    ],
    "3. User & Device Engagement": [
        {"title": "Android's Massive 62% Dominance", "desc": "The market is dominated by three brands: Xiaomi, Samsung, and Vivo, all within the Android ecosystem.", "states": []},
        {"title": "The Apple Segment: Small but Premium", "desc": "Apple users represent only 3% of the base but are the primary targets for high-value financial products and premium insurance.", "states": []},
        {"title": "Tecno and OnePlus Lead Engagement", "desc": "Tecno users are the most active, followed by OnePlus, showing outliers in budget and premium segments respectively.", "states": []},
        {"title": "High Engagement as a Trust Metric", "desc": "Andhra Pradesh and Telangana show the highest app-open frequency, marking them as the best markets for launching credit and investment products.", "states": ["Andhra Pradesh", "Telangana"]},
        {"title": "App Stability and Compatibility", "desc": "Given the dominance of diverse Android devices, business strategy must prioritize lightweight app-versions and broad device compatibility.", "states": []}
    ],
    "4. Insurance Adoption Trends": [
        {"title": "Transition to Structured Scaling", "desc": "Insurance adoption moved from a 'base effect' hyper-growth phase in 2021 to a structured scaling phase in 2024, with growth stabilizing between 10-22%.", "states": []},
        {"title": "Festive Season Demand Spikes", "desc": "Insurance demand shows sharp spikes in Q3 and Q4, coinciding with festive season spending and making it the ideal window for upsell campaigns.", "states": []},
        {"title": "South and West India Lead Adoption", "desc": "Karnataka, Maharashtra, Tamil Nadu, and Kerala are the primary revenue leaders, benefiting from high financial awareness and better distribution.", "states": ["Karnataka", "Maharashtra", "Tamil Nadu", "Kerala"]},
        {"title": "High Growth in Mid-Large States", "desc": "Odisha, Jharkhand, and Uttarakhand represent the 'Best Targets' for expansion, showing high growth and moderate current volumes.", "states": ["Odisha", "Jharkhand", "Uttarakhand"]},
        {"title": "Policy Volume Ups and Downs", "desc": "While policy volume shows quarterly volatility (e.g., -30% dips followed by +40% jumps), the overall long-term trend remains strongly positive.", "states": []}
    ],
    "5. Market Segmentation": [
        {"title": "Urban Micro-Transaction Economy", "desc": "Urban districts like Pune show extremely high volume but low average ticket size (~₹510), characterizing a daily 'digital lifestyle' economy.", "states": ["Maharashtra"]},
        {"title": "Rural Value-Driven Economy", "desc": "Smaller or North-East regions like Sadia show lower frequency but much higher ticket sizes (~₹5,000), indicating concentrated, high-value transactions.", "states": ["Assam", "Arunachal Pradesh"]},
        {"title": "The High Growth/Low Penetration Matrix", "desc": "States like Bihar (85% growth, 5% penetration) offer huge untapped opportunities for entry-level plans and user acquisition.", "states": ["Bihar"]},
        {"title": "Tiered Pricing Necessity", "desc": "Data suggests a single pricing strategy is ineffective; products must be tiered into Premium (High Ticket) and Price-Sensitive (Low Ticket) markets.", "states": []},
        {"title": "Mature vs. Emerging Acceleration", "desc": "Kerala and Tamil Nadu are accelerating mature markets, while states like Chhattisgarh are pure expansion zones with users just starting to adopt insurance.", "states": ["Kerala", "Tamil Nadu", "Chhattisgarh"]}
    ]
}

# --- State mapping for the 3D map ---
state_to_insight_text = {}
for topic, items in insights_data.items():
    for item in items:
        for st_name in item["states"]:
            if st_name in state_to_insight_text:
                state_to_insight_text[st_name] += f"<br/><br/><b>{item['title']}</b>: {item['desc']}"
            else:
                state_to_insight_text[st_name] = f"<b>{item['title']}</b>: {item['desc']}"

@st.cache_data
def load_data():
    df_trans = pd.read_csv(r"C:\Users\Vigne\OneDrive\Desktop\Phonepe Pulse\Agg_Trans.csv")
    df_user = pd.read_csv(r"C:\Users\Vigne\OneDrive\Desktop\Phonepe Pulse\Agg_user.csv")
    df_ins = pd.read_csv(r"C:\Users\Vigne\OneDrive\Desktop\Phonepe Pulse\Agg_insurance.csv")
    return df_trans, df_user, df_ins

df_trans, df_user, df_ins = load_data()

@st.cache_data
def load_geojson():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    try:
        return requests.get(url).json()
    except:
        return None

geojson_data = load_geojson()

def get_graph(topic, sub_title, df_trans, df_user, df_ins):
    df_trans.columns = df_trans.columns.str.lower()
    df_user.columns = df_user.columns.str.lower()
    df_ins.columns = df_ins.columns.str.lower()
    
    brand_col = 'device_brand' if 'device_brand' in df_user.columns else 'brand' if 'brand' in df_user.columns else 'brands'
    count_col = 'device_count' if 'device_count' in df_user.columns else 'count' if 'count' in df_user.columns else 'user_count'
    
    try:
        if "1. Transaction Dynamics" in topic:
            if "P2P" in sub_title:
                df_grp = df_trans.groupby("transaction_type")["transaction_amount"].sum().reset_index()
                fig = px.pie(df_grp, values="transaction_amount", names="transaction_type", title="Transaction Volume by Category", hole=0.4)
            elif "626%" in sub_title:
                df_grp = df_trans[df_trans["transaction_type"].str.contains("Merchant", na=False, case=False)]
                df_grp = df_grp.groupby("year")["transaction_amount"].sum().reset_index()
                fig = px.line(df_grp, x="year", y="transaction_amount", title="Merchant Payments Growth", markers=True)
            elif "Post-2020" in sub_title:
                df_grp = df_trans.groupby("year")["transaction_amount"].sum().reset_index()
                fig = px.area(df_grp, x="year", y="transaction_amount", title="Total Transaction Growth Post-2020")
            elif "Strong User Retention" in sub_title:
                df_grp = df_trans.groupby("quarter")["transaction_count"].sum().reset_index()
                fig = px.bar(df_grp, x="quarter", y="transaction_count", title="Transaction Frequency by Quarter")
            else:
                df_grp = df_trans.groupby(["year", "transaction_type"])["transaction_amount"].sum().reset_index()
                fig = px.line(df_grp, x="year", y="transaction_amount", color="transaction_type", title="Network Effects by Type", markers=True)
                
        elif "2. Geographic" in topic:
            if "Powerhouses" in sub_title:
                df_grp = df_trans.groupby("state")["transaction_amount"].sum().reset_index().sort_values("transaction_amount", ascending=False).head(5)
                fig = px.bar(df_grp, x="state", y="transaction_amount", title="Top 5 States by Volume", color="state")
            elif "Metro Concentration" in sub_title:
                df_grp = df_trans.groupby("state")["transaction_amount"].sum().reset_index().sort_values("transaction_amount", ascending=False).head(10)
                fig = px.treemap(df_grp, path=["state"], values="transaction_amount", title="Concentration in Top States")
            elif "3,000%" in sub_title:
                df_grp = df_trans.groupby("state")["transaction_count"].sum().reset_index().sort_values("transaction_count", ascending=False).tail(10)
                fig = px.bar(df_grp, x="state", y="transaction_count", title="Breakout States Volume")
            elif "Tier-2" in sub_title:
                df_grp = df_trans.groupby("state")[["transaction_amount", "transaction_count"]].sum().reset_index()
                fig = px.scatter(df_grp, x="transaction_count", y="transaction_amount", hover_name="state", title="Tier-2 Surge Matrix")
            else:
                df_grp = df_trans.groupby("state")["transaction_count"].sum().reset_index().sort_values("transaction_count").head(15)
                fig = px.bar(df_grp, x="transaction_count", y="state", orientation='h', title="District/State Level Distribution")

        elif "3. User" in topic:
            if "Android's Massive" in sub_title:
                df_grp = df_user.groupby(brand_col)[count_col].sum().reset_index()
                fig = px.pie(df_grp, values=count_col, names=brand_col, title="Brand Dominance in Market")
            elif "Apple" in sub_title:
                df_grp = df_user[df_user[brand_col].str.contains("Apple", na=False, case=False)]
                df_grp = df_grp.groupby("year")[count_col].sum().reset_index()
                fig = px.bar(df_grp, x="year", y=count_col, title="Apple Segment Growth")
            elif "Tecno" in sub_title:
                df_grp = df_user[df_user[brand_col].isin(["Tecno", "OnePlus"])]
                df_grp = df_grp.groupby(["year", brand_col])[count_col].sum().reset_index()
                fig = px.line(df_grp, x="year", y=count_col, color=brand_col, title="Tecno vs OnePlus Engagement", markers=True)
            elif "High Engagement" in sub_title:
                if 'app_opens' in df_user.columns:
                    df_grp = df_user.groupby("state")["app_opens"].sum().reset_index().sort_values("app_opens", ascending=False).head(10)
                    fig = px.bar(df_grp, x="state", y="app_opens", title="Top Engaging States (App Opens)", color="state")
                else:
                    df_grp = df_user.groupby("state")[count_col].sum().reset_index().sort_values(count_col, ascending=False).head(10)
                    fig = px.bar(df_grp, x="state", y=count_col, title="Top Engaging States")
            else:
                df_grp = df_user.groupby(brand_col)[count_col].sum().reset_index()
                fig = px.treemap(df_grp, path=[brand_col], values=count_col, title="App Compatibility Distribution")

        elif "4. Insurance" in topic:
            if "Structured Scaling" in sub_title:
                df_grp = df_ins.groupby("year")["insurance_amount"].sum().reset_index()
                fig = px.line(df_grp, x="year", y="insurance_amount", title="Insurance Scaling over Years", markers=True)
            elif "Festive Season" in sub_title:
                df_grp = df_ins.groupby("quarter")["insurance_count"].sum().reset_index()
                fig = px.bar(df_grp, x="quarter", y="insurance_count", title="Insurance Spikes by Quarter")
            elif "South and West" in sub_title:
                df_grp = df_ins.groupby("state")["insurance_amount"].sum().reset_index().sort_values("insurance_amount", ascending=False).head(8)
                fig = px.bar(df_grp, x="state", y="insurance_amount", title="Top States in Insurance Adoption", color="state")
            elif "High Growth" in sub_title:
                df_grp = df_ins.groupby("state")[["insurance_amount", "insurance_count"]].sum().reset_index()
                fig = px.scatter(df_grp, x="insurance_count", y="insurance_amount", hover_name="state", title="Growth Matrix for Mid-Large States")
            else:
                df_grp = df_ins.groupby(["year", "quarter"])["insurance_count"].sum().reset_index()
                df_grp["period"] = df_grp["year"].astype(str) + "-Q" + df_grp["quarter"].astype(str)
                fig = px.area(df_grp, x="period", y="insurance_count", title="Policy Volume Volatility")

        elif "5. Market" in topic:
            df_ts = df_trans.groupby("state")[["transaction_amount", "transaction_count"]].sum().reset_index()
            df_ts["ticket_size"] = df_ts["transaction_amount"] / df_ts["transaction_count"]
            
            if "Urban Micro" in sub_title:
                df_grp = df_ts.sort_values("transaction_count", ascending=False).head(10)
                fig = px.bar(df_grp, x="state", y="ticket_size", title="Ticket Size in High Volume States (Urban)", color="ticket_size")
            elif "Rural Value" in sub_title:
                df_grp = df_ts.sort_values("transaction_count", ascending=True).head(10)
                fig = px.bar(df_grp, x="state", y="ticket_size", title="Ticket Size in Low Volume States (Rural)", color="ticket_size")
            elif "Penetration" in sub_title:
                fig = px.scatter(df_ts, x="transaction_count", y="ticket_size", hover_name="state", title="Growth vs Penetration Matrix")
            elif "Tiered Pricing" in sub_title:
                fig = px.histogram(df_ts, x="ticket_size", nbins=15, title="Distribution of Ticket Sizes")
            else:
                df_grp = df_trans.groupby("year")["transaction_amount"].sum().reset_index()
                fig = px.area(df_grp, x="year", y="transaction_amount", title="Mature vs Emerging Market Growth")
                
        fig.update_layout(
            template="plotly_dark", 
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="rgba(0,0,0,0)", 
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(color="#f8fafc", size=14),
            legend=dict(font=dict(color="#f8fafc", size=13)),
            xaxis=dict(tickfont=dict(color="#cbd5e1"), title=dict(font=dict(color="#cbd5e1"))),
            yaxis=dict(tickfont=dict(color="#cbd5e1"), title=dict(font=dict(color="#cbd5e1")))
        )
        return fig
    except Exception as e:
        fig = px.bar(x=["Data Error"], y=[0], title=f"Could not generate graph: {str(e)}")
        fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        return fig

# --- Layout ---
col1, col2 = st.columns([1, 1.2])

with col1:
    if geojson_data:
        features = geojson_data['features']
        for i, feature in enumerate(features):
            st_name = feature['properties']['ST_NM']
            mapped = False
            for mapped_st, text in state_to_insight_text.items():
                if mapped_st.lower() in st_name.lower():
                    feature['properties']['insight'] = text
                    # MUCH flatter, controlled elevation
                    feature['properties']['elevation'] = 120000 + random.randint(5000, 15000)
                    feature['properties']['color'] = [236, 72, 153] # Pink
                    mapped = True
                    break
            
            if not mapped:
                feature['properties']['insight'] = "General State Data"
                # Keep elevation close so it is not 'huge vs flat'
                feature['properties']['elevation'] = 100000 + random.randint(5000, 15000)
                h = i / len(features)
                rgb = colorsys.hls_to_rgb(h, 0.3, 0.4)
                feature['properties']['color'] = [int(c * 255) for c in rgb]

        layer = pdk.Layer(
            "GeoJsonLayer",
            geojson_data,
            opacity=0.8,
            stroked=True,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation="properties.elevation",
            get_fill_color="properties.color",
            get_line_color=[255, 255, 255],
            pickable=True,
            elevation_scale=2,
        )
        
        view_state = pdk.ViewState(
            latitude=22.5937,
            longitude=78.9629,
            zoom=4.0,
            pitch=45,
            bearing=0
        )
        
        r = pdk.Deck(
            layers=[layer], 
            initial_view_state=view_state, 
            tooltip={
                "html": "<h4 style='margin:0;color:#3b82f6;'>{ST_NM}</h4><hr style='margin:5px 0;'/>{insight}",
                "style": {"backgroundColor": "#1e293b", "color": "white", "border": "1px solid #8b5cf6", "borderRadius": "8px", "padding": "12px", "maxWidth": "350px", "whiteSpace": "normal"}
            },
            map_style="mapbox://styles/mapbox/dark-v10"
        )
        st.pydeck_chart(r, use_container_width=True)

with col2:
    st.markdown("<h3 style='color: white; margin-top:0px;'>Insights Explorer</h3>", unsafe_allow_html=True)
    selected_topic = st.selectbox("Select Topic", list(insights_data.keys()))
    
    st.markdown("<hr style='margin:10px 0px;'/>", unsafe_allow_html=True)
    
    # Render Subtopics as Tabs
    subtopics = [item["title"] for item in insights_data[selected_topic]]
    tabs = st.tabs(subtopics)
    
    for i, tab in enumerate(tabs):
        with tab:
            item = insights_data[selected_topic][i]
            st.info(f"💡 **Finding:** {item['desc']}")
            
            # Show Detailed Graph
            fig = get_graph(selected_topic, item['title'], df_trans, df_user, df_ins)
            if fig:
                st.plotly_chart(fig, use_container_width=True, key=f"graph_{selected_topic}_{i}")
