# config/skill_taxonomy.py
# Master skill taxonomy organized by category and role relevance

SKILL_TAXONOMY = {
    "programming_languages": {
        "skills": ["python", "go", "rust", "java", "javascript", "typescript", "c++", "scala", "r", "julia"],
        "weight": 1.0
    },
    "ml_frameworks": {
        "skills": ["pytorch", "tensorflow", "keras", "jax", "scikit-learn", "xgboost", "lightgbm", "hugging face", "transformers", "diffusers"],
        "weight": 1.2
    },
    "llm_tools": {
        "skills": ["langchain", "llamaindex", "openai api", "anthropic api", "autogen", "crewai", "langraph", "dspy", "guidance", "instructor"],
        "weight": 1.3
    },
    "mlops_tools": {
        "skills": ["mlflow", "kubeflow", "dvc", "feast", "bentoml", "seldon", "argo workflows", "prefect", "zenml", "evidently"],
        "weight": 1.2
    },
    "vector_databases": {
        "skills": ["pinecone", "weaviate", "chroma", "qdrant", "milvus", "faiss", "elasticsearch", "pgvector"],
        "weight": 1.1
    },
    "data_engineering": {
        "skills": ["apache spark", "kafka", "airflow", "dbt", "flink", "beam", "databricks", "delta lake", "iceberg", "hudi"],
        "weight": 1.0
    },
    "databases": {
        "skills": ["postgresql", "mysql", "mongodb", "redis", "cassandra", "snowflake", "bigquery", "redshift", "pinot", "clickhouse"],
        "weight": 0.9
    },
    "devops_tools": {
        "skills": ["docker", "kubernetes", "terraform", "helm", "argocd", "github actions", "jenkins", "ansible", "vault", "consul"],
        "weight": 1.0
    },
    "cloud_platforms": {
        "skills": ["aws", "gcp", "azure", "aws sagemaker", "vertex ai", "azure ml", "lambda", "gke", "eks"],
        "weight": 1.0
    },
    "monitoring": {
        "skills": ["prometheus", "grafana", "datadog", "new relic", "opentelemetry", "loki", "jaeger", "pagerduty", "sentry"],
        "weight": 0.9
    },
    "web_frameworks": {
        "skills": ["fastapi", "flask", "django", "react", "nextjs", "express", "grpc", "graphql"],
        "weight": 0.8
    },
    "ai_concepts": {
        "skills": ["rag", "fine-tuning", "rlhf", "reinforcement learning", "transformers", "diffusion models", "prompt engineering",
                   "agent", "function calling", "embeddings", "llm", "multimodal"],
        "weight": 1.2
    }
}

ROLE_FOCUS = {
    "AI/ML": {
        "primary": ["ml_frameworks", "llm_tools", "ai_concepts", "programming_languages"],
        "secondary": ["vector_databases", "data_engineering", "web_frameworks"],
        "description": "AI & Machine Learning Engineer"
    },
    "MLOps": {
        "primary": ["mlops_tools", "devops_tools", "cloud_platforms", "monitoring"],
        "secondary": ["ml_frameworks", "data_engineering", "programming_languages"],
        "description": "ML Operations Engineer"
    },
    "DevOps": {
        "primary": ["devops_tools", "cloud_platforms", "monitoring", "programming_languages"],
        "secondary": ["web_frameworks", "databases", "mlops_tools"],
        "description": "DevOps / Platform Engineer"
    },
    "Data": {
        "primary": ["data_engineering", "databases", "programming_languages"],
        "secondary": ["monitoring", "devops_tools", "ml_frameworks"],
        "description": "Data Engineer"
    }
}

LEARNING_RESOURCES = {
    "python": {"url": "https://docs.python.org", "platform": "Official Docs"},
    "pytorch": {"url": "https://pytorch.org/tutorials", "platform": "PyTorch"},
    "langchain": {"url": "https://python.langchain.com", "platform": "LangChain Docs"},
    "mlflow": {"url": "https://mlflow.org/docs/latest", "platform": "MLflow Docs"},
    "kubernetes": {"url": "https://kubernetes.io/docs", "platform": "Kubernetes"},
    "docker": {"url": "https://docs.docker.com", "platform": "Docker Docs"},
    "terraform": {"url": "https://developer.hashicorp.com/terraform", "platform": "HashiCorp"},
    "fastapi": {"url": "https://fastapi.tiangolo.com", "platform": "FastAPI Docs"},
    "default": {"url": "https://www.coursera.org", "platform": "Coursera / YouTube"}
}
