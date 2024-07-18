import pytest

import whtft.app


@pytest.mark.filterwarnings("ignore: directory")
def test_settings():
    settings = whtft.app.Settings()
    assert settings.default_log_config == whtft.app.DEFAULT_LOG_CONFIG
