<?php

$conn = pg_connect("host=localhost dbname=project_db user=postgres password=YOUR_PASSWORD");

if (!$conn) {
    die("Database connection failed: " . pg_last_error());
}


$query_users = "
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
";

$result_users = pg_query($conn, $query_users);
if ($result_users) {
    echo "Table 'users' created successfully.<br>";
} else {
    echo "Failed to create 'users' table: " . pg_last_error($conn) . "<br>";
}


$query_files = "
CREATE TABLE IF NOT EXISTS files (
    file_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT,
    file_type VARCHAR(100),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE
);
";

$result_files = pg_query($conn, $query_files);
if ($result_files) {
    echo "Table 'files' created successfully.<br>";
} else {
    echo "Failed to create 'files' table: " . pg_last_error($conn) . "<br>";
}

pg_close($conn);

?>
