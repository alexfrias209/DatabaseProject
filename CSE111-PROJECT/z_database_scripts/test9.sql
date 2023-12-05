BEGIN TRANSACTION;

INSERT INTO logic_profile (
    user_id, 
    username, 
    name, 
    email, 
    bio,
    profile_image 
) VALUES (
    (SELECT id FROM auth_user WHERE username = 'johnnn_doe'), 
    'johnnn_doe',
    'Johnnn Doe',
    'johnnn.doe@example.com',
    'This is the bio of Johnnn Doe.',
    'profiles/user-default.png'
);

COMMIT;
