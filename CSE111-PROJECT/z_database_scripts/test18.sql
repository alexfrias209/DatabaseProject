UPDATE logic_message
SET body = 'You are right',
    updated = datetime('now')
WHERE user_id = (SELECT id FROM auth_user WHERE username = 'johnnn_doe')
AND post_id = (SELECT id FROM logic_poll WHERE debate_title = 'Am i Funny?')
AND body = 'You are wrong';
