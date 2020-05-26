from api import split_url

def test_url_page():
    url = 'https://canvas.instance.com/courses/12345/pages/page_name'
    result = split_url(url, expected = 'page')
    assert result == ('https://canvas.instance.com', '12345', 'page_name')

def test_url_page_no_expected():
    url = 'https://canvas.instance.com/courses/12345/pages/page_name'
    result = split_url(url)
    assert result == ('https://canvas.instance.com', '12345', 'page_name', 'page')

def test_url_folder():
    url = 'https://canvas.instance.com/courses/12345/files/folder/folder_name'
    result = split_url(url, expected = 'folder')
    assert result == ('https://canvas.instance.com', '12345', 'folder_name')

def test_url_folder_no_expected():
    url = 'https://canvas.instance.com/courses/12345/files/folder/folder_name'
    result = split_url(url)
    assert result == ('https://canvas.instance.com', '12345', 'folder_name', 'folder')

def test_url_only():
    url = 'https://canvas.instance.com/courses/12345'
    result = split_url(url, expected = 'url only')
    assert result == ('https://canvas.instance.com', '12345', '')

def test_url_only_no_expected():
    url = 'https://canvas.instance.com/courses/12345'
    result = split_url(url)
    assert result == ('https://canvas.instance.com', '12345', '', 'url only')
