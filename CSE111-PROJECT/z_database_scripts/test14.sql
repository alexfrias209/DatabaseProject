DELETE FROM logic_profile_saved_posts
WHERE
  profile_id = (SELECT id FROM logic_profile WHERE username = 'johnnn_doe') AND
  (
    poll_id = (SELECT id FROM logic_poll WHERE debate_title = "Am i Funny?") OR
    poll_id = (SELECT id FROM logic_poll WHERE debate_title = "Is this political?")
  );
