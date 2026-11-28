from churn.train import main


def test_training_on_sample_gives_a_valid_auc(capsys):
    auc = main("tests/fixtures/customers_sample.csv")
    assert 0.0 <= auc <= 1.0
    assert "test AUC" in capsys.readouterr().out
