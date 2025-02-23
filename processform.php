<?php

$host = 'localhost';
$username = 'root';
$password = '';
$dbname = 'cuedb';

// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Create connection
$conn = new mysqli($host, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    $response = [
        'success' => false,
        'message' => 'Connection failed: ' . $conn->connect_error
    ];
} else {
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Retrieve and sanitize form data
        $fname = trim($_POST['fname']);
        $lname = trim($_POST['lname']);
        $email = trim($_POST['email']);
        $phone = trim($_POST['phone']);

        // Validate email format
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $response = [
                'success' => false,
                'message' => 'Invalid email format'
            ];
        } else {
            // Check if email already exists in the database
            $stmt = $conn->prepare("SELECT * FROM subscribers WHERE email = ?");
            $stmt->bind_param("s", $email);
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $response = [
                    'success' => false,
                    'message' => 'Email already exists'
                ];
            } else {
                // Insert form data into the database
                $stmt = $conn->prepare("INSERT INTO subscribers (fname, lname, email, phone) VALUES (?, ?, ?, ?)");
                $stmt->bind_param("ssss", $fname, $lname, $email, $phone);
                
                if ($stmt->execute()) {
                    $response = [
                        'success' => true,
                        'message' => 'Subscription successful'
                    ];
                } else {
                    $response = [
                        'success' => false,
                        'message' => 'Database error: ' . $conn->error
                    ];
                }
            }
            $stmt->close();
        }
    } else {
        $response = [
            'success' => false,
            'message' => 'Invalid request method'
        ];
    }
    $conn->close();
}
/*
// Return JSON response
header('Content-Type: application/json');
echo json_encode($response);
*/
?>
