import pandas as pd

def generate_report_text(df_filtered: pd.DataFrame) -> str:
    """Generates a crisp, high-impact Markdown reputation report."""
    if df_filtered.empty:
        return "✨ **No data found.** Your reputation is currently quiet."

    total = len(df_filtered)
    critical = len(df_filtered[df_filtered['risk_flag'] == 'Respond Now'])
    positive = len(df_filtered[df_filtered['sentiment_flag'] == 'Positive'])
    negative = len(df_filtered[df_filtered['sentiment_flag'] == 'Negative'])

    report = []
    
    report.append("### 🚦 Risk & Sentiment Status")
    report.append(f"- 🚨 **Critical Threats:** {critical} requires immediate review.")
    report.append(f"- 📈 **Sentiment Bias:** {positive} Positive | {negative} Negative | {total - (positive+negative)} Neutral.")

    report.append("### 📰 Brief of Mentions")
    
    # Summarize Positives
    pos_df = df_filtered[df_filtered['sentiment_flag'] == 'Positive']
    if not pos_df.empty:
        pos_summary = "; ".join([f"{r['target_entity']} ({r['source_platform']}): {r['content_body'][:100]}..." for _, r in pos_df.iterrows()])
        report.append(f"- **Positive:** {pos_summary}")
    else:
        report.append("- **Positive:** No positive mentions.")

    # Summarize Negatives
    neg_df = df_filtered[df_filtered['sentiment_flag'] == 'Negative']
    if not neg_df.empty:
        neg_summary = "; ".join([f"{r['target_entity']} ({r['source_platform']}): {r['content_body'][:100]}..." for _, r in neg_df.iterrows()])
        report.append(f"- **Negative:** {neg_summary}")
    else:
        report.append("- **Negative:** No negative mentions.")

    # Summarize Neutrals (includes Ambiguous)
    neu_df = df_filtered[~df_filtered['sentiment_flag'].isin(['Positive', 'Negative'])]
    if not neu_df.empty:
        neu_summary = "; ".join([f"{r['target_entity']} ({r['source_platform']}): {r['content_body'][:100]}..." for _, r in neu_df.iterrows()])
        report.append(f"- **Neutral:** {neu_summary}")
    else:
        report.append("- **Neutral:** No neutral mentions.")
    
    return "\n".join(report)
