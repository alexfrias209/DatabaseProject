INSERT INTO logic_poll (host_id, topic_id, debate_title, up_votes, down_votes, updated, created, photo)
VALUES (
    (SELECT id FROM auth_user WHERE username = 'johnnn_doe'),
    NULL, -- Assuming no topic is set
    'rock always wins',
    0,  -- Default up_votes
    0,  -- Default down_votes
    datetime('now'), -- updated timestamp
    datetime('now'), -- created timestamp
    ''  -- Empty string for the photo
),
(
    (SELECT id FROM auth_user WHERE username = 'johnnn_doe'),
    NULL, -- Assuming no topic is set
    'rock is the best',
    0,  -- Default up_votes
    0,  -- Default down_votes
    datetime('now'), -- updated timestamp
    datetime('now'), -- created timestamp
    ''  -- Empty string for the photo
);
