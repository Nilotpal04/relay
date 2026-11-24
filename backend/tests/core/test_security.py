from relay.core.security import hash_password, verify_password


def test_hash_password_does_not_return_plaintext():
    password = "correct-horse-battery-staple"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_verify_password_with_correct_password():
    password = "correct-horse-battery-staple"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True


def test_verify_password_with_incorrect_password():
    password = "correct-horse-battery-staple"
    hashed_password = hash_password(password)

    assert verify_password("wrong-password", hashed_password) is False


def test_same_password_produces_different_hashes():
    password = "correct-horse-battery-staple"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash
