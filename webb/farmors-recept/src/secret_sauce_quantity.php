<?php
    require "api.php";

    $rawData = file_get_contents("php://input");
    $data = json_decode($rawData, true);

    if (!array_key_exists("dish", $data)) {
        die("error");
    }

    echo getSecretSouceQuantity($data["dish"]);
?>