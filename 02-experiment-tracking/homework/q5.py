import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient

HPO_EXPERIMENT_NAME = "random-forest-hyperopt"
mlflow.set_tracking_uri("http://127.0.0.1:5000")
client = MlflowClient()

# Retrieve the top_n model runs and log the models
experiment = client.get_experiment_by_name(HPO_EXPERIMENT_NAME)
runs = client.search_runs(
    experiment_ids=experiment.experiment_id,
    run_view_type=ViewType.ACTIVE_ONLY,
    max_results=1,
    order_by=["metrics.rmse ASC"]
)

run = runs[0]
print(f"Q5: {run.data.metrics['rmse']:.3f}")
