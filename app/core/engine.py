import yaml
import logging
import importlib
from typing import List, Any
from app.core.base import BaseStage

class PipelineEngine:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.stages: List[BaseStage] = []
        self.logger = logging.getLogger("PipelineEngine")
        self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            self.logger.info(f"Loaded config from {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            raise

    def _initialize_stages(self):
        pipeline_definition = self.config.get('pipeline', [])
        for stage_cfg in pipeline_definition:
            module_name = stage_cfg['module']
            class_name = stage_cfg['class']
            name = stage_cfg.get('name', class_name)
            params = stage_cfg.get('params', {})

            try:
                module = importlib.import_module(module_name)
                stage_class = getattr(module, class_name)
                stage_instance = stage_class(name=name, config=params)
                self.stages.append(stage_instance)
                self.logger.info(f"Initialized stage: {name}")
            except (ImportError, AttributeError) as e:
                self.logger.error(f"Failed to initialize stage {name}: {e}")
                raise

    def run(self, initial_data: Any = None):
        if not self.stages:
            self._initialize_stages()

        current_data = initial_data
        self.logger.info("--- Starting Pipeline Execution ---")
        
        try:
            for stage in self.stages:
                self.logger.info(f"Running stage: {stage.name}")
                current_data = stage.run(current_data)
            self.logger.info("--- Pipeline Completed Successfully ---")
        except Exception as e:
            self.logger.error(f"Pipeline failed at stage {stage.name}: {e}")
            # Raise exception to ensure production environments see the failure
            raise
        
        return current_data
