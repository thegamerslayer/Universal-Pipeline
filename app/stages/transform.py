import os
import pandas as pd
from app.core.base import BaseStage

class TransformStage(BaseStage):
    def run(self, data: any) -> any:
        if not data:
            self.logger.warning("No data provided to TransformStage")
            return []

        # Convert to DataFrame for easy manipulation
        df = pd.DataFrame(data)
        
        # Example transformation: Basic cleaning or feature engineering
        # Let's clean the column names or handle missing values if needed
        self.logger.info(f"Processing DataFrame with shape: {df.shape}")
        
        # Output as CSV if specified in config
        output_path = self.config.get("output_path", "/app/data/output.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            df.to_csv(output_path, index=False)
            self.logger.info(f"Data saved to CSV: {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save CSV: {e}")
            raise

        return df
