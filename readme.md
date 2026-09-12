# Growpido Reputation Advisory & Risk Monitoring

A professional dashboard for monitoring reputation risks across LinkedIn, News, and the Open Web.

## 🚀 Features
- **Multi-Platform Ingestion**: Pulls data from LinkedIn (Proxycurl), Google News, and Web Search (SerpApi).
- **Groq-Powered Analysis**: Uses Llama 3 to classify mentions by Sentiment and Risk Level (Ignore, Watch, Respond Now).
- **Sentiment Summary**: Condensed 3-point brief (Positive, Negative, Neutral) for rapid situational awareness.
- **Evidance Toggle**: Collapsed raw data view for deep-dive verification.
- **Human-in-the-Loop**: Editable AI response drafting and authorization via the "Human Gate".

## 🛠️ Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Edit `.env` and add your keys:
   - `GROQ_API_KEY`: For Llama 3 analysis.
   - `SERPAPI_API_KEY`: For Web/News search.
   - `PROXYCURL_API_KEY`: For LinkedIn mentions.
   - `DATA_SOURCE`: Set to `external` for live data or `local` for testing.

3. **Run the Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

## 📊 Dashboard Usage
- **Entity Names**: Set search filters to `"Growpido"` or `"Nidhi Hooda"` as pre-seeded data is configured for these entities.
- **Research**: Fetches new data and runs AI classification.
- **Summary**: Displays the 3-point sentiment-grouped brief.
- **Evidance**: Toggle open the collapsed "Evidance" table to review tracked public metrics.
- **Human Gate**: Expand any critical mention, click "Generate" to construct a draft, edit the response manually if needed, and press "Approve".
