<?php

$conn = pg_connect("host=localhost dbname=postgres user=postgres password=YOUR_PASSWORD");
if (!$conn) {
    die("Connection failed");
}

$dbname = "project_db";

$query = "CREATE DATABASE $dbname";
$result = pg_query($conn, $query);

if ($result) {
    echo "Database '$dbname' created successfully.";
} else {
    echo "Error creating database: " . pg_last_error($conn);
}

pg_close($conn);
