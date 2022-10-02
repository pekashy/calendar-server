import copy
import datetime
import uuid


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

    assert returned_event
    assert not returned_event.description


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


def recreate_event(event):
    new_event = copy.deepcopy(event)
    new_event.id = 'event_' + str(uuid.uuid4())
    return new_event


def test_events_in_interval(create_event, get_event, approve_event, default_event, user_events):
    #  Test will fail after first time, as event uuids generated the same for some reason. TODO: Fix
    event_1 = recreate_event(default_event)
    event_2 = recreate_event(default_event)
    event_2.schedule_start += datetime.timedelta(hours=2)
    event_3 = recreate_event(default_event)
    event_3.schedule_start += datetime.timedelta(hours=4)
    event_4 = recreate_event(default_event)
    event_4.schedule_start += datetime.timedelta(hours=6)
    create_event(event_1)

    user = 'user2_id'

    assert not user_events(user, default_event.schedule_start, datetime.timedelta(hours=5))
    approve_event(event_1.id, user)
    assert user_events(user, default_event.schedule_start, datetime.timedelta(hours=5)) == [event_1.id]
    create_event(event_2)
    create_event(event_3)
    create_event(event_4)
    approve_event(event_2.id, user)
    approve_event(event_3.id, user)
    approve_event(event_4.id, user)
    assert set(user_events(user, default_event.schedule_start, datetime.timedelta(hours=5))) == {event_1.id, event_2.id,
                                                                                                 event_3.id}


def test_first_free_interval(create_event, get_event, approve_event, default_event, user_events, first_free_interval):
    event_1 = recreate_event(default_event)  # 00 to 01
    event_2 = recreate_event(default_event)
    event_2.schedule_start += datetime.timedelta(hours=2)
    event_2.duration = datetime.timedelta(hours=2)  # 02 to 04
    event_3 = recreate_event(default_event)
    event_3.schedule_start += datetime.timedelta(hours=5)
    event_3.duration = datetime.timedelta(hours=2)  # 05 to 07
    create_event(event_1)
    create_event(event_2)
    create_event(event_3)

    interval_start = first_free_interval(['user1_id'], interval_start=default_event.schedule_start,
                                         interval_duration=datetime.timedelta(minutes=30),
                                         search_interval_duration=datetime.timedelta(days=1))
    assert interval_start == default_event.schedule_start + datetime.timedelta(hours=1)

    event_4 = recreate_event(default_event)
    event_4.created_by = 'user2_id'
    event_4.accepted = ['user2_id']
    event_4.duration = datetime.timedelta(hours=4)  # 00 to 04
    create_event(event_4)

    interval_start = first_free_interval(['user1_id', 'user2_id'], interval_start=default_event.schedule_start,
                                         interval_duration=datetime.timedelta(minutes=30),
                                         search_interval_duration=datetime.timedelta(days=1))

    assert interval_start == default_event.schedule_start + datetime.timedelta(hours=4)
