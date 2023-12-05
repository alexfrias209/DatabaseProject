UPDATE logic_profile
SET bio = 'blahhhhh'
WHERE user_id = (SELECT id FROM auth_user WHERE username = 'johnnn_doe');
