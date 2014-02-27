<?php
ini_set('display_errors',1);
error_reporting(E_ALL);

function connect_to_db(){
  $hostname = "blabberbots.com";
  $username = "root";
  $password = "425things";
  $db_name  = "fourtwofive";

  $dsn = "mysql:dbname=$db_name;host=$hostname";

  try{
     $dbh = new PDO($dsn,$username,$password);
     $dbh->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
     return $dbh;
  }catch (PDOException $e){
     echo "Connection Failed: ". $e->getMessage();
     return false;
  }
}


function check_book($bookid,$dbh){

    $book = json_decode($bookid,true);

    $sql_prep = $dbh->prepare("SELECT count(record) FROM person_record WHERE username = ?");
    $sql_prep->bindParam(1,$username);

    $username = $book['bookid'];

    try{
        $sql_prep->execute();
        $rows = $sql_prep->fetchColumn();
        if ($rows >= 1){
            // We got some stored records
            print "true";
        }else{
            // We do not have stored records
            print "false";
        }
    }catch(Exception $e){
        exit("false $e");
    }
}

function write_record($objJSON,$dbh){


    // This decodes the JSON we sent from the front end and loads it into a named (or associative) array
    // You MUST include the 'true' in this function call to get an associative array.
    $user = json_decode($objJSON,true);

    // This section sets up a prepared statement that we will send to the database. This method prevents SQL injection.
    // The question marks are substitutes for the variables that will go in that spot.
    $sql_prep = $dbh->prepare("INSERT INTO person_record(username, stored_fullname, stored_rating, stored_phone, stored_long, stored_lat) VALUES(?, ?, ?, ?, ?, ?)");

    // The number in the bindParam function corresponds to the question mark place holder. That's why username is first.
    // You're telling SQL which variables will be used in the query once they are set.
    $sql_prep->bindParam(1,$username);
    $sql_prep->bindParam(2,$fullname);
    $sql_prep->bindParam(3,$rating);
    $sql_prep->bindParam(4,$phone);
    $sql_prep->bindParam(5,$long);
    $sql_prep->bindParam(6,$lat);

    // Now, you set the variables. These will populate the variables with the data the SQL server needs.
    $username = $user['username'];
    $fullname = $user['stored_fullname'];
    $rating   = $user['stored_rating'];
    $phone    = $user['stored_phone'];
    $long     = $user['stored_long'];
    $lat      = $user['stored_lat'];

    try{
        // This actually sends the query to the database. If there is no error the program continues.
        // We want our javascript to pickup the 'true' or 'false' so we print them to the page.
        $sql_prep->execute();
        print "true";
    }catch (Exception $e){
        print "false";
    }
}

function get_all_records($recordID,$dbh){

    $user = json_decode($recordID,true);

    $sql_prep = $dbh->prepare("SELECT * FROM person_record WHERE username = ?");
    $sql_prep->bindParam(1,$username);

    $username = $user['username'];

    try{
        $sql_prep->execute();
        $results  = $sql_prep->fetchall(PDO::FETCH_ASSOC);
        print json_encode($results);
    }catch (Exception $e){
        print "false: $e";
    }
}

function get_single_record($recordID,$dbh){
    $sql_prep = $dbh->prepare("SELECT * FROM person_record WHERE record = ? AND username = ?");

    $sql_prep->bindParam(1,$record);
    $sql_prep->bindParam(2,$username);

    $username = "Art";
    $record = 3;

    try{
        $sql_prep->execute();
        $results  = $sql_prep->fetchall(PDO::FETCH_ASSOC);
        print json_encode($results);
    }catch (Exception $e){
        print "false: $e";
    }
}

$conn = connect_to_db();
$api_key_name = 'api_type';
$JSONname = 'jsonData';

if (array_key_exists($api_key_name,$_GET)){
    $api = $_GET[$api_key_name];
}else{
    exit("false. provide an api-type");
}

if (array_key_exists($JSONname,$_GET)){
    $objJSON = $_GET[$JSONname];
}else{
    $objJSON = "Art";
}


if ($api == 'add_record'){
    write_record($objJSON,$conn);
}elseif ($api == "get_all"){
    get_all_records($objJSON,$conn);
}elseif ($api == "get_single"){
    get_single_record($objJSON,$conn);
}elseif ($api == "checkbook"){
    check_book($objJSON,$conn);
}else{
    print "false: bad api key";
}

?>