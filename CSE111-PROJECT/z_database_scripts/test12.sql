DELETE FROM logic_profile_following
WHERE
  profile_id = (SELECT id FROM logic_profile WHERE username = 'johnnn_doe') AND
  user_id = (SELECT id FROM auth_user WHERE username = 'adiaz');
