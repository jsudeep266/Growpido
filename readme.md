# Growpido Reputation Advisory & Risk Monitoring

A professional dashboard for monitoring reputation risks across LinkedIn, News, and the Open Web.

## 🚀 Features
- **Multi-Platform Ingestion**: Pulls data from LinkedIn (Proxycurl), Google News, and Web Search (SerpApi).
- **Groq-Powered Analysis**: Uses Llama 3 to classify mentions by Sentiment and Risk Level (Ignore, Watch, Respond Now).
- **Executive Weekly Brief**: Generates a 3-minute read summary for busy stakeholders.
- **Human-in-the-Loop**: Authorized AI responses via a secure "Human Gate" dashboard.

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
**## Entity Name: "Growpido" or "Nidhi Hooda"** as we have data for those

- **Research**: Fetches new data and runs AI classification.
- **Executive Brief**: Click the button in the sidebar for a text-based weekly summary.
- **Human Gate**: Expand any "Critical" mention to generate and approve an AI response draft.
