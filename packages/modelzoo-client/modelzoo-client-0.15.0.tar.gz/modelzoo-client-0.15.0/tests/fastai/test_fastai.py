import pandas as pd
import modelzoo
import modelzoo.fastai
from fastai.text.all import (
    URLs,
    untar_data,
    TextDataLoaders,
    text_classifier_learner,
    AWD_LSTM,
)

from tests.mock_api_server import mock_api_server


def test_text_classifier_deploy() -> None:
    path = untar_data(URLs.IMDB_SAMPLE)
    df = pd.read_csv(path / "texts.csv")
    dls = TextDataLoaders.from_df(
        df, path=path, text_col="text", label_col="label", valid_col="is_valid"
    )
    learn = text_classifier_learner(dls, AWD_LSTM)

    with mock_api_server():
        assert (
            modelzoo.fastai.deploy(learn, model_name="test", api_key="test") == "test"
        )

        modelzoo.list(api_key="test")
        modelzoo.info("test-model", api_key="test")
        modelzoo.stop("test-model", api_key="test")
        modelzoo.start("test-model", api_key="test")
        modelzoo.fastai.predict("test-model", input_value="test")
