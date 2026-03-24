import os
import json
import requests
import logging
from bs4 import BeautifulSoup as bs
from pydantic import ValidationError
# import schema as schema.build_dynamic_model
from schema import build_dynamic_model
# ... (Include the build_dynamic_model and clean_data functions here) ...


# Configure logging to output to console for easier debugging in Docker
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def save_to_jsonl(data):
    output_file = os.getenv("OUTPUT_FILE", "/app/data/scraped_data.jsonl")
    
    # NEW: This part ensures the folder exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created directory: {output_dir}")

    with open(output_file, "a", encoding="utf-8") as f:
        for record in data:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def scrape():
    print("--- 🏁 ENGINE STARTED ---") # ADD THIS
    # 1. Setup Configuration from Environment
    target_url = os.getenv("TARGET_URL")
    container_selector = os.getenv("CONTAINER_SELECTOR")
    # This now contains your validation rules too!
    fields_json = os.getenv("FIELDS_TO_EXTRACT", "{}") 

    print(f"🚀 Starting scrape on: {target_url}")

    # 2. Build the "Gatekeeper" Model
    # This creates the ScrapedItem class based on your JSON rules
    ScrapedItem = build_dynamic_model(fields_json)

    # 3. Fetch and Parse
    response = requests.get(target_url)
    soup = bs(response.text, "html.parser")
    items = soup.select(container_selector)

    print(f"📦 Found {len(items)} items with selector '{container_selector}'") # ADD THIS

    final_data = []

    rules = json.loads(fields_json)
    # 4. The Loop: Extract -> Validate -> Save
    for item in items:
        raw_row = {}
        
        
        for field_name, rule in rules.items():
            # Get the CSS selector for this specific field
            selector = rule.get("selector") 
            element = item.select_one(selector)
            raw_row[field_name] = element.get_text(strip=True) if element else None

        try:
            # VALIDATION HAPPENS HERE
            # Pydantic cleans the data and checks types
            validated_item = ScrapedItem(**raw_row)
            
            # .model_dump() converts the Pydantic object back to a clean dict
            final_data.append(validated_item.model_dump())

            print(f"✅ Successfully validated: {validated_item.name}")
            
        except ValidationError as e:
            # ERROR HANDLING: If data is bad, we log it instead of crashing
            print(f"⚠️ Validation Failed for an item: {e.json()}")
            continue 

    

    # 5. Save the clean data
    save_to_jsonl(final_data)

    print(f"💾 Data saved to JSONL. Scrape Complete!")

if __name__ == "__main__":
    scrape()