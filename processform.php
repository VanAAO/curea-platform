<?php

$host = 'localhost';
$username = 'root';
$password = '';
$dbname = 'cuedb';

// Enable error reporting for debugging
//error_reporting(E_ALL);
//ini_set('display_errors', 1);

// Create connection
$conn = new mysqli($host, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed".$conn->connect_error);
} 
echo "Connection Successfull";
if (isset($_POST["submit"])) {
    // Retrieve and sanitize form data
    $fname = ($_POST['fname']);
    $lname = ($_POST['lname']);
    $email = ($_POST['email']);
    $phone = ($_POST['phone']);

    $sql = "select * from subscribers where username = '$fname', '$lname', '$email', '$phone'";
    $result = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    $count = mysqli_num_rows($result);
    if($count==1){
        header("Location:form.php")
    }
    else{
        echo `<script>
        window.location.href= "processform.php";
        alert("Login failed. Invalid username or password")
        </script>`
    }
}

?>
/*else {
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Retrieve and sanitize form data
        $fname = ($_POST['fname']);
        $lname = ($_POST['lname']);
        $email = ($_POST['email']);
        $phone = ($_POST['phone']);

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
