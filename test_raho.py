from cryptography.fernet import Fernet
from raho import *
import pytest
import re
if sys.version_info >= (3, 3):
    from unittest.mock import call, patch
else:
    from mock import call, patch


@pytest.fixture(scope='session')
def key():
    return b'banbdHh1ZbX5cbz_Gd9G51EeDwLoHzRhG8R3p226aUM='


@pytest.fixture(scope='session')
def fernet(key):
    return Fernet(key)


@pytest.fixture(scope='session')
def key_file(tmpdir_factory, key):
    key_file = tmpdir_factory.mktemp('key_files').join('key_file')
    key_file.write(urlsafe_b64encode(key).decode())
    return str(key_file)


@pytest.fixture
def new_key_file(tmpdir):
    key_file = tmpdir.mkdir('key_files').join('another_key_file')
    return str(key_file)


def test_decrypt(fernet):
    message = 'Z0FBQUFBQmRocFhXSmRpdzVDcGhXdExRcUp6MnBwa0ljb1ZGRFFEZ1lwY25JQi1aZk5XVUpHTkp1eEV3bU4zeHM2Q3ZYY1ZwMkhvVDZoVEpyZ0w4QUtZY2ZjWnducDhYUU5mVmF5b2toVEdxV2lPa2N4RVhFVUU9'
    assert decrypt(message, fernet) == 'camels are amongst us'

    message = 'A' + message[1:]
    with pytest.raises(DecryptError) as e:
        decrypt(message, fernet)
    assert str(e.value) == 'Invalid encrypted format or incorrect key'

    with pytest.raises(DecryptError) as e:
        decrypt('YWJjZA==', fernet)
    assert str(e.value) == 'Invalid encrypted format or incorrect key'

    with pytest.raises(DecryptError) as e:
        decrypt('12345', fernet)
    assert str(e.value) == 'Invalid encrypted format'


def test_decrypt_with_key_file(key_file):
    message = 'Z0FBQUFBQmRocDFEWTZjQy1LcWlCQkZyTEZpcGFvLVRaYlg0dzBxMmM1ZGlVZ2ZJeWhqcklqdEpxdlFudVZBRnFVc2MydWpOUzc4bnNSa3FzSDJjRFJrdkFSNnFQS1pDdUE9PQ=='
    assert decrypt_with_key_file(message, key_file) == 'meet at 5pm'


def test_decrypt_with_password():
    message = 'Z0FBQUFBQmRocDlJaU5uM1djdGVxMi1scVJKZHBSLW0tcmg3SlQ0S0R3eDB5Nlp0ZW1RUngwX1lHanJfLXpBZlJSd0xZWnZMemJLa2QwczdScU03NGlmRy04c2NaSE1IVWJYYXRkSXdySjhESll0VGpnQ2ltamM9,2LZKzeVnB-Wj2yzuOdX7Ng=='
    assert decrypt_with_password(message, 'sunshine') == 'they know about us!'

    with pytest.raises(DecryptError) as e:
        decrypt_with_password(message, '123456')
    assert str(e.value) == 'Invalid encrypted format or incorrect key'

    with pytest.raises(DecryptError) as e:
        decrypt_with_password('totally invalid', 'sunshine')
    assert str(e.value) == 'Invalid encrypted format'


def test_encrypt(fernet):
    message = encrypt('mums the word', fernet)
    assert decrypt(message, fernet) == 'mums the word'


def test_encrypt_with_key_file(key_file):
    message = encrypt_with_key_file('shhh', key_file)
    assert decrypt_with_key_file(message, key_file) == 'shhh'


def test_encrypt_with_password():
    message = encrypt_with_password('I am going home', 'monkey')
    assert decrypt_with_password(message, 'monkey') == 'I am going home'


def test_generate_fernet():
    fernet = generate_fernet()
    assert type(fernet) == Fernet


def test_generate_key_file(new_key_file):
    generate_key_file(new_key_file)
    assert os.path.isfile(new_key_file)

    with pytest.raises(OSError):
        generate_key_file(new_key_file)


def test_get_key_file_fernet(key_file):
    fernet = get_key_file_fernet(key_file)
    assert type(fernet) == Fernet


def test_get_key_file_fernet_with_bad_format(new_key_file):
    open(new_key_file, 'w').write('ABC')
    with pytest.raises(DecryptError) as e:
        get_key_file_fernet(new_key_file)
    assert str(e.value) == 'Invalid key format'


def test_get_password_fernet():
    fernet = get_password_fernet('123456', b'salt')
    assert type(fernet) == Fernet


@patch('raho._read_stdin')
@patch('raho._print_stdout')
def test_main_with_key_file(_print_stdout, _read_stdin, new_key_file):
    main(['-k', new_key_file, 'generate'])
    assert _print_stdout.mock_calls[0] == call(
        'Generating key: %s' % new_key_file)
    assert os.path.isfile(new_key_file)

    _read_stdin.return_value = 'secret message'
    main(['-k', new_key_file, 'encrypt'])
    message = _print_stdout.mock_calls[1][1][0]
    assert re.match(r'^Z0FB.+$', message)

    _read_stdin.return_value = message
    main(['--key-file', new_key_file, 'decrypt'])
    assert _print_stdout.mock_calls[2] == call('secret message')


@patch('getpass.getpass')
@patch('raho._print_stdout')
def test_main_with_password_and_prompt_text(_print_stdout, getpass):
    getpass.side_effect = ('iloveyou', 'secret message')
    main(['-p', '-t', 'encrypt'])
    message = _print_stdout.mock_calls[0][1][0]
    assert re.match(r'^Z0FB.+$', message)

    getpass.side_effect = ('iloveyou', message)
    main(['--password', '--prompt-text', 'decrypt'])
    assert _print_stdout.mock_calls[1] == call('secret message')
