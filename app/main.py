import os
import logging
from app.core.engine import PipelineEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def main():
    config_path = os.getenv("PIPELINE_CONFIG", "config/pipeline_config.yaml")
    
    if not os.path.exists(config_path):
        logging.error(f"Config file not found: {config_path}")
        return

    try:
        engine = PipelineEngine(config_path)
        final_result = engine.run()
        logging.info("Pipeline run finished.")
    except Exception as e:
        logging.critical(f"Pipeline crashed: {e}")

if __name__ == "__main__":
    main()
