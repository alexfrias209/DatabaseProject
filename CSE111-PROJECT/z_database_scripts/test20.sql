UPDATE logic_profile
SET profile_image = 'profiles/picTest.jpg'
WHERE user_id = (SELECT id FROM auth_user WHERE username = 'johnnn_doe');
