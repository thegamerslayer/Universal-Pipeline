import os
import json
import requests
from bs4 import BeautifulSoup as bs
from pydantic import ValidationError
from app.core.base import BaseStage
from app.core.schema import build_dynamic_model

class ScrapeStage(BaseStage):
    def run(self, data: any = None) -> any:
        target_url = self.config.get("target_url")
        container_selector = self.config.get("container_selector")
        fields_json = self.config.get("fields_to_extract", "{}")

        self.logger.info(f"Starting scrape on: {target_url}")

        # Build the dynamic model
        ScrapedItem = build_dynamic_model(fields_json)

        # Fetch and Parse
        try:
            response = requests.get(target_url)
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to fetch content from {target_url}: {e}")
            raise

        soup = bs(response.text, "html.parser")
        items = soup.select(container_selector)

        self.logger.info(f"Found {len(items)} items with selector '{container_selector}'")

        final_data = []
        rules = json.loads(fields_json)

        for item in items:
            raw_row = {}
            for field_name, rule in rules.items():
                selector = rule.get("selector")
                element = item.select_one(selector)
                raw_row[field_name] = element.get_text(strip=True) if element else None

            try:
                validated_item = ScrapedItem(**raw_row)
                final_data.append(validated_item.model_dump())
            except ValidationError as e:
                self.logger.warning(f"Validation failed for an item: {e}")
                continue

        self.logger.info(f"Successfully scraped and validated {len(final_data)} items")
        return final_data
