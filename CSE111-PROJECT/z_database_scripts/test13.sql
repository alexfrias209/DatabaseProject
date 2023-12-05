INSERT INTO logic_profile_saved_posts (profile_id, poll_id)
VALUES
(
    (SELECT id FROM logic_profile WHERE username = 'johnnn_doe'),
    (SELECT id FROM logic_poll WHERE debate_title = "Am i Funny?")
),
(
    (SELECT id FROM logic_profile WHERE username = 'johnnn_doe'),
    (SELECT id FROM logic_poll WHERE debate_title = "Is this political?")
);
