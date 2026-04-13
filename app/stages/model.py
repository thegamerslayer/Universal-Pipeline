import pandas as pd
from sklearn.cluster import KMeans
from app.core.base import BaseStage

class MLStage(BaseStage):
    def run(self, data: any) -> any:
        if not isinstance(data, pd.DataFrame):
            self.logger.warning("MLStage expects a pandas DataFrame")
            return data

        if data.empty:
            self.logger.warning("Data is empty, skipping MLStage")
            return data

        # Example: Simple K-Means clustering on numeric columns
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            self.logger.info(f"Running K-Means on columns: {list(numeric_cols)}")
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            data['cluster'] = kmeans.fit_predict(data[numeric_cols].fillna(0))
            self.logger.info("Clustering complete")
        else:
            self.logger.warning("No numeric columns found for clustering")

        return data
