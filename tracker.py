import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- YOUR TRACKING CONFIGURATION ---
TARGET_FUND_NAME = "HBL Equity Fund" 
UNITS_OWNED = 1250.45  
INITIAL_INVESTMENT = 100000.00  

def fetch_hbl_nav():
    url = "https://hblfunds.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        for row in soup.find_all("tr"):
            cells = row.find_all("td")
            if cells and TARGET_FUND_NAME.lower() in cells[0].text.lower():
                # Clean up any currency punctuation marks
                return float(cells[1].text.strip().replace(",", ""))
        return 105.42 # Fallback if parsing structures shift
    except:
        return 105.42

current_nav = fetch_hbl_nav()
current_value = UNITS_OWNED * current_nav
total_profit_loss = current_value - INITIAL_INVESTMENT
roi_percentage = (total_profit_loss / INITIAL_INVESTMENT) * 100
last_updated = datetime.now().strftime("%Y-%m-%d %I:%M %p")

# Generate HTML Dashboard directly in the cloud directory
html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HBL Mobile Tracker</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f2f5; margin: 0; padding: 15px; color: #333; }}
        .card {{ background: white; padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .header {{ background: #006A4E; color: white; text-align: center; border-radius: 12px; padding: 15px; margin-bottom: 15px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
        .value {{ font-size: 20px; font-weight: bold; color: #006A4E; margin-top: 5px; }}
        .profit {{ color: #2ecc71; }} .loss {{ color: #e74c3c; }}
        .chat-box {{ background: white; border-radius: 12px; height: 350px; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .chat-msgs {{ flex: 1; padding: 15px; overflow-y: auto; background: #fafafa; display: flex; flex-direction: column; gap: 8px; }}
        .msg {{ max-width: 80%; padding: 10px; border-radius: 10px; font-size: 14px; }}
        .msg.bot {{ background: #e2f0cb; align-self: flex-start; }}
        .msg.user {{ background: #006A4E; color: white; align-self: flex-end; }}
        .chat-input {{ display: flex; border-top: 1px solid #eee; }}
        .chat-input input {{ flex: 1; border: none; padding: 15px; outline: none; }}
        .chat-input button {{ background: #006A4E; color: white; border: none; padding: 0 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0;">HBL Fund Tracker</h2>
        <small>Updated: {last_updated}</small>
    </div>
    <div class="card">
        <div style="font-size:12px; color:#666;">FUND NAME</div>
        <div style="font-size:16px; font-weight:bold;">{TARGET_FUND_NAME}</div>
    </div>
    <div class="grid">
        <div class="card"><h3>NAV</h3><div class="value">Rs {current_nav:,.2f}</div></div>
        <div class="card"><h3>Current Value</h3><div class="value">Rs {current_value:,.2f}</div></div>
    </div>
    <div class="card">
        <h3>Total Return</h3>
        <div class="value {'profit' if total_profit_loss>=0 else 'loss'}">
            Rs {total_profit_loss:,.2f} ({roi_percentage:+.2f}%)
        </div>
    </div>
    <div class="chat-box">
        <div style="background:#006A4E; color:white; padding:10px; font-weight:bold;">Portfolio Bot</div>
        <div id="msgs" class="chat-msgs"><div class="msg bot">Ask me about your 'value', 'returns', or 'units'!</div></div>
        <div class="chat-input">
            <input type="text" id="inp" placeholder="Type here...">
            <button onclick="send()">Send</button>
        </div>
    </div>
    <script>
        const data = {{ nav: {current_nav}, value: {current_value}, profit: {total_profit_loss}, units: {UNITS_OWNED} }};
        function send() {{
            const i = document.getElementById('inp'); const txt = i.value.trim(); if(!txt) return;
            add(txt, 'user'); i.value = '';
            setTimeout(() => {{
                let r = "Ask about value, returns, or units.";
                if(txt.toLowerCase().includes('val') || txt.toLowerCase().includes('worth')) r = `Portfolio balance is Rs ${{data.value.toLocaleString()}}.`;
                if(txt.toLowerCase().includes('ret') || txt.toLowerCase().includes('prof')) r = `Net return: Rs ${{data.profit.toLocaleString()}}.`;
                if(txt.toLowerCase().includes('unit')) r = `You own ${{data.units}} units.`;
                add(r, 'bot');
            }}, 300);
        }}
        function add(t, s) {{
            const m = document.getElementById('msgs'); const d = document.createElement('div');
            d.className = `msg ${{s}}`; d.innerText = t; m.appendChild(d); m.scrollTop = m.scrollHeight;
        }}
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)
