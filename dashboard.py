import streamlit as st
import pandas as pd
from database import get_db_connection, init_db
from ingestion import run_ingestion
from llm.classifier import MentionClassifier
from llm.responder import DraftResponder
from services.brief_generator import generate_report_text
from datetime import datetime, timezone, date, timedelta
import uuid

# Ensure DB is ready
init_db()

st.set_page_config(page_title="Growpido Reputation Dashboard", layout="wide")

st.title("🛡️ Growpido Reputation Dashboard")
st.markdown("Monitor reputation risks across LinkedIn, Open Web, and News.")

# --- Helpers ---
def load_data():
    conn = get_db_connection()
    query = '''
        SELECT rm.*, cl.sentiment_flag, cl.risk_flag, hg.generated_draft, hg.action_timestamp
        FROM raw_mentions rm
        LEFT JOIN classification_log cl ON rm.mention_id = cl.mention_id
        LEFT JOIN human_gate_actions hg ON rm.mention_id = hg.mention_id
        WHERE rm.content_body IS NOT NULL 
          AND rm.content_body != '' 
          AND TRIM(rm.content_body) != ''
        ORDER BY rm.published_timestamp DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_pending(entity_filter=None):
    conn = get_db_connection()
    query = '''
        SELECT cl.mention_id, rm.content_body, rm.target_entity, rm.source_platform, cl.sentiment_flag, cl.risk_flag
        FROM classification_log cl
        JOIN raw_mentions rm ON cl.mention_id = rm.mention_id
        LEFT JOIN human_gate_actions hg ON cl.mention_id = hg.mention_id
        WHERE (cl.risk_flag = 'Respond Now' OR cl.sentiment_flag IN ('Negative', 'Ambiguous')) 
        AND hg.action_id IS NULL
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty:
        df = df[df['content_body'].fillna('').str.strip() != '']
    if entity_filter and not df.empty:
        df = df[df['target_entity'].isin(entity_filter)]
    return df

# --- Sidebar: Research Control ---
st.sidebar.header("🔍 Subjects & Search")
search_entities = st.sidebar.text_input("Entity Names", "Growpido, Nidhi Hooda")
entity_list = [e.strip() for e in search_entities.split(",") if e.strip()]
platforms = st.sidebar.multiselect("Platforms", ["LinkedIn", "Open Web", "News"], default=["LinkedIn", "Open Web", "News"])

# Timerange Filter
today = date.today()
default_start = today - timedelta(days=7)
date_range = st.sidebar.date_input("Time Range", [default_start, today])

if st.sidebar.button("🚀 Research"):
    with st.spinner("Executing Reputation Research..."):
        added = run_ingestion(entities=entity_list, platforms=platforms)
        classified = MentionClassifier().process_unclassified_mentions()
    st.sidebar.success(f"Research Complete! Found {added} new, analyzed {classified} total.")

st.sidebar.divider()

# --- Main View Flow ---
df = load_data()
if not df.empty:
    df_f = df[df['target_entity'].isin(entity_list)]
    
    # Filter by date range
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_f = df_f[pd.to_datetime(df_f['published_timestamp']).dt.date.between(start_date, end_date)]
    
    # Drop rows that are missing critical content or are just whitespace
    df_f = df_f.dropna(subset=['published_timestamp', 'target_entity', 'content_body'])
    df_f = df_f[df_f['content_body'].astype(str).str.strip() != '']
    
    # 1. Table
    with st.expander("📊 Evidance", expanded=False):
        if not df_f.empty:
            st.dataframe(
                df_f[['published_timestamp', 'target_entity', 'source_platform', 'content_body', 'sentiment_flag', 'risk_flag']],
                use_container_width=True,
                hide_index=True,
                height=300
            )
        else:
            st.write("No mentions found for the selected criteria.")

    # 3. Summary
    st.divider()
    st.subheader("📄 Summary")
    st.markdown(generate_report_text(df_f))
    
    # 4. Human Gate
    st.divider()
    st.subheader("🚨 Human Gate")
    st.caption("Mentions flagged as Critical, Negative, or Ambiguous requiring oversight.")
    pending = get_pending(entity_filter=entity_list)
    
    if pending.empty:
        st.write("✅ No critical, negative, or ambiguous mentions requiring immediate action.")
    else:
        for _, row in pending.iterrows():
            mention_id = row['mention_id']
            tag = f"[{row['sentiment_flag']}/{row['risk_flag']}]"
            with st.expander(f"{tag} {row['target_entity']} on {row['source_platform']}"):
                st.warning(f"**Potential Risk:** {row['content_body']}")
                
                if st.button("Generate", key=f"btn_gen_{mention_id}"):
                    with st.spinner("Drafting response via GPT-OSS..."):
                        draft = DraftResponder().generate_draft(row['content_body'])
                        st.session_state[f"txt_{mention_id}"] = draft
                
                edited_draft = st.text_area("Response Draft", key=f"txt_{mention_id}", height=150)
                
                if st.button("Approve", key=f"btn_app_{mention_id}"):
                    conn = get_db_connection()
                    c = conn.cursor()
                    c.execute('''
                        INSERT INTO human_gate_actions (action_id, mention_id, slack_reviewer_id, review_decision, generated_draft, action_timestamp)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (str(uuid.uuid4()), mention_id, "DASHBOARD_ADMIN", "Approved", edited_draft, datetime.now(timezone.utc).isoformat()))
                    conn.commit()
                    conn.close()
                    st.success("Draft Authorized!")
                    st.rerun()

    # Export
    st.divider()
    st.download_button("📥 Export Logs (CSV)", df_f.to_csv(index=False).encode('utf-8'), "growpido_logs.csv", "text/csv")
else:
    st.info("No data available. Click 'Research' in the sidebar to begin.")
