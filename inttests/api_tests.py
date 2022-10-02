def test_create_event(create_event, get_event, approve_event, default_event):
    create_resp = create_event(default_event)
    assert create_resp.status_code == 200

    get_event_code, returned_event = get_event(default_event.id, user_id='user1_id')
    assert returned_event == default_event

    get_event_code, returned_event = get_event('no such id', user_id='user1_id')

    assert get_event_code == 404
    assert not returned_event


def test_private_event(create_event, get_event, default_event):
    private_event = default_event
    private_event.is_private = True
    create_event(private_event)
    get_event_code, returned_event = get_event(private_event.id, user_id='user3_id')

    assert get_event_code == 403
    assert not returned_event


def test_approve_event(create_event, get_event, approve_event, default_event):
    create_event(default_event)
    approve_event_resp = approve_event(default_event.id, 'user2_id')
    assert approve_event_resp.status_code == 200

    get_event_code, event = get_event(event_id=default_event.id, user_id='user1_id')
    assert event.accepted == ['user1_id', 'user2_id']

    approve_event_resp = approve_event(event.id, 'user3_id')
    assert approve_event_resp.status_code == 403

    approve_event_resp = approve_event('no_such_event_id', 'user2_id')
    assert approve_event_resp.status_code == 404
