#!/usr/bin/env python

import stream


def test_original_server():
    client = stream.connect('5e62adrfbcxw', 'qxshw6rvbgcv4ghb342fevzp75h53qhga8vajmd6s4pr6f7kcyfx72w5j693xe3t')
    f = client.feed('feed', "user_9_0_5600c2359e08b6b9653ce87e_official")
    res = f.get(offset=0,limit=1)
    print res

    assert 'duration' in res
    assert 'results' in res
    assert 'next' in res
    assert len(res['results']) <= 1


def test_new_server():
    client = stream.connect('5e62adrfbcxw', 'qxshw6rvbgcv4ghb342fevzp75h53qhga8vajmd6s4pr6f7kcyfx72w5j693xe3t')
    # change from original endpoint to the new one to test
    client.base_url = "http://192.168.99.100:5000/api/"
    f = client.feed('feed', "user_9_0_5600c2359e08b6b9653ce87e_official")
    res = f.get(offset=0,limit=1)
    print res

    assert 'duration' in res
    assert 'results' in res
    assert 'next' in res
    assert len(res['results']) <= 1
