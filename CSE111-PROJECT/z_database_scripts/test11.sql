INSERT INTO logic_profile_following (profile_id, user_id)
VALUES (
    (SELECT id FROM logic_profile WHERE username = 'johnnn_doe'),
    (SELECT id FROM auth_user WHERE username = 'adiaz')
);
