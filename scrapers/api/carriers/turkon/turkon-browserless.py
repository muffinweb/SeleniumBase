import requests
import os

token = os.getenv("BROWSERLESS_TOKEN")

endpoint = "https://production-sfo.browserless.io/chrome/bql"
query_string = {
    "token": token,
    "humanlike": "true",
    "blockConsentModals": "true",
}
headers = {
    "Content-Type": "application/json",
}
payload = {
    "query": """
mutation TurkonScrapeXHR {
  goto(url: "https://myturkonline.turkon.com/tracking", waitUntil: load) {
    status
  }
  
  verify(type: cloudflare){
    found
    solved
    time
  }
  
  type(selector: "input", text: "10186971"){
    time
  }
  
  click(selector: "button[type=\"submit\"]"){
    time
  }
  
  html(clean: {
      removeAttributes: true,
      removeNonTextNodes: true
    }) {
      html
    }
}
    """,
    "operationName": "TurkonScrapeXHR",
}

response = requests.post(endpoint, params=query_string, headers=headers, json=payload)
print(response.json())

