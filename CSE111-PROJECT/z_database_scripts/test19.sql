DELETE FROM logic_message
WHERE user_id = (SELECT id FROM auth_user WHERE username = 'johnnn_doe');
