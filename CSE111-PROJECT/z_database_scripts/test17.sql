INSERT INTO logic_message (user_id, post_id, body, updated, created)
VALUES (
    (SELECT id FROM auth_user WHERE username = 'johnnn_doe'),
    (SELECT id FROM logic_poll WHERE debate_title = 'Am i Funny?'),
    'You are wrong',
    datetime('now'), -- Timestamp for when the comment was updated
    datetime('now')  -- Timestamp for when the comment was created
);

INSERT INTO logic_message (user_id, post_id, body, updated, created)
VALUES (
    (SELECT id FROM auth_user WHERE username = 'johnnn_doe'),
    (SELECT id FROM logic_poll WHERE debate_title = 'Am i Funny?'),
    'blah',
    datetime('now'), -- Timestamp for when the comment was updated
    datetime('now')  -- Timestamp for when the comment was created
);
