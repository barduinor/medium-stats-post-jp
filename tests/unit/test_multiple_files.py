

from scan import scan


def test_two_post_read():
    """ should read 2 files and return 2 posts data"""
    data = scan('tests/data')
    
    post_ids_set = set()

    for line in data:
        if line.startswith('id'):
            continue
        x = line.split(',')
        post_ids_set.add(x[0])

    assert len(post_ids_set) == 2