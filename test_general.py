from api import split_url

def test_url_page():
    url = 'https://canvas.instance.com/courses/12345/pages/page_name'
    result = split_url(url, 'page')
    assert result == ('https://canvas.instance.com', '12345', 'page', 'page_name')

def test_url_folder():
    url = 'https://canvas.instance.com/courses/12345/files/folder/folder_name'
    result = split_url(url, 'folder')
    assert result == ('https://canvas.instance.com', '12345', 'folder', 'folder_name')
