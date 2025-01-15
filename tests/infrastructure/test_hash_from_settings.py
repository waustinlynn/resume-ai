from app.infrastructure.settings import Settings
from app.infrastructure.utilities.hashing import hash_value


def test_hash_text_is_successfully_hashed():
    settings = Settings()
    value_to_hash = "test@email.com"
    hashed_value = hash_value(value_to_hash, settings.hashing_secret)
    assert hashed_value != value_to_hash


def test_hashing_with_different_secret_returns_different_value():
    settings = Settings()
    value_to_hash = "test@email.com"
    hashed_value = hash_value(value_to_hash, settings.hashing_secret)
    different_hashed_value = hash_value(value_to_hash, "some-different-hashing-secret")
    assert hashed_value != different_hashed_value
