import requests
import json

# Ensure this matches your n8n Webhook 'Test URL'
URL = "http://localhost:5678/webhook-test/data-agent"

def talk_to_agent(question):
    print(f"⏳ Sending query to n8n...")
    query = f"Read the file 'models/marts/fct_orders.sql' from our GitHub and check for naming errors."
    payload = {
        "chatInput": query, 
        "sessionId": "kate-dbt-audit"
    }
    
    try:
        response = requests.post(URL, json=payload)
        
        if response.status_code == 200:
            # 1. Get the raw JSON from n8n
            data = response.json()
            
            # 2. Extract the 'output' string 
            raw_output = data.get('output', 'No response found.')
            
            # 3. Clean up the "Unreadable" Markdown and newlines
            clean_output = raw_output.replace('```json', '').replace('```', '').replace('\\n', '\n').strip()
            
            print("\n" + "="*40)
            print("🤖 AGENT AUDIT REPORT")
            print("="*40)
            print(clean_output)
            print("="*40 + "\n")
            
        else:
            print(f"❌ n8n Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    # Test it with a real dbt audit question
    user_query = "Check the latest dbt model for naming convention errors."
    talk_to_agent(user_query)