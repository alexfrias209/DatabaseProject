INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
)
VALUES (
    'pbkdf2_sha256$600000$rFyIAmlVf36VmxEAoEHlri$tUi8RjzLP8tjV4d+ItelmTsTEfx6aOgfFD2SmlmH8Wk=', 
    datetime('now'), 
    0, 
    'johnnn_doe', 
    'Johnnn',
    'Doe', 
    'johnnn.doe@example.com',
    0, 
    1, 
    datetime('now') 
);
