DELETE FROM logic_poll
WHERE debate_title IN ('rock always wins', 'rock is the best')
AND host_id = (SELECT id FROM auth_user WHERE username = 'johnnn_doe');
