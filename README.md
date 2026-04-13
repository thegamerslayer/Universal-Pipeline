# 🚀 Universal Pipeline Framework

A modular, containerized Python framework for building flexible Data Processing and Machine Learning pipelines. This project transforms raw data into validated, model-ready formats with a configuration-driven approach.

---

## 🌟 Key Features

- **🧩 Fully Modular**: Define your pipeline stages (Scraping, Transformation, ML) as reusable components.
- **⚙️ Configuration-Driven**: Reorder stages and update parameters via a single `pipeline_config.yaml` file—no code changes required.
- **🐳 Containerized**: Fully Dockerized with out-of-the-box support for both automated runs and interactive development.
- **📓 Jupyter Integration**: Includes a dedicated Jupyter Notebook environment for data exploration and debugging.
- **🛠️ Production Ready**: Centralized logging, robust error handling, and dynamic Pydantic schema validation.
- **📊 CSV Export**: Automatically transforms and saves processed data into user-friendly CSV formats.

---

## 📂 Project Structure

```text
Universal-Pipeline/
├── app/
│   ├── core/           # Framework Engine & Base Classes
│   ├── stages/         # Individual Pipeline Stages (Scrape, ML, etc.)
│   └── main.py         # Primary Entry Point
├── config/             # YAML Configuration Files
├── notebooks/          # Workspace for Jupyter Notebooks
├── output/             # Processed data, CSVs, and artifacts
├── Dockerfile          # Container definition
├── docker-compose.yml  # Multi-service orchestration
└── requirements.txt    # Python dependencies
```

---

## 🚀 Quick Start

Ensure you have **Docker** and **Docker Compose** installed.

### 1. Run the Automated Pipeline
To execute the full data pipeline (Scrape -> Clean -> ML):
```bash
docker-compose up pipeline
```
Check the results in `./output/scraped_data.csv`.

### 2. Interactive Development
To launch the Jupyter environment for data exploration:
```bash
docker-compose up notebook
```
Then visit **`http://localhost:8888`** in your browser.

---

## ⚙️ Customizing the Pipeline

The framework is built to be flexible. You can modify the order or behavior of stages in `config/pipeline_config.yaml`:

```yaml
pipeline:
  - name: "MyScraper"
    module: "app.stages.scraper"
    class: "ScrapeStage"
    params:
      target_url: "https://example.com"
      ...
```

---

## 🛠️ Built With

- **Python 3.12**
- **Docker & Docker Compose**
- **Pandas**: Data transformation
- **Scikit-learn**: Machine Learning
- **BeautifulSoup4**: Web scraping
- **Pydantic**: Dynamic data validation
- **PyYAML**: Configuration management

---

## 📝 License

This project is open-source and available under the MIT License.
