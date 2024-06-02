from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

import mlflow

from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.metrics import mean_squared_error



if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(df, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here

    categorical = ['PULocationID', 'DOLocationID']
    target = 'duration'


    train_dict = df[categorical].to_dict(orient='records')
    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dict)
    y_train = df[target].values

    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("hw3")
    # mlflow.sklearn.autolog()


    with mlflow.start_run():

        lr = LinearRegression()
        lr.fit(X_train, y_train)
        print(lr.intercept_)

        y_predict = lr.predict(X_train)
        rmse = mean_squared_error(y_train, y_predict, squared=False)

        mlflow.log_metric("rmse", rmse)

        # Log the sklearn model and register as version 1
        mlflow.sklearn.log_model(
            sk_model=lr,
            artifact_path="sklearn-model",
            registered_model_name="sk-learn-lrt-reg-model",
        )

    return X_train, y_train, dv, lr


