<?php
    header("Content-Type:application/json");
    error_reporting(0);

    function getSecretSouceQuantity($dish) {
        $db = new SQLite3("recipes.db", SQLITE3_OPEN_READONLY);
        $dish = str_replace(" ","",$dish);

        // Buil in WAF that protects against super scary sqlmap :)
        $danger = array("drop", "delete", "randomblob", "else", "like", "upper", "coalesce", "sleep", "attach", "create", "insert");
        $dish_lower = strtolower($dish);
        foreach ($danger as $word) {
            if (strpos($dish_lower, $word) !== FALSE) {
                return "danger:injection!";
            }
        }

        $query = "SELECT secret_sauce_quantity FROM recipes WHERE dish = '$dish'";
        $result = $db->query($query) or die("error");
        $row = $result->fetchArray();

        $db->close();

        return json_encode(array("secret_sauce_quantity" => floatval($row['secret_sauce_quantity'])));
    }

    function getIngredients($dish) {
        $db = new SQLite3("recipes.db", SQLITE3_OPEN_READONLY);

        $stmt = $db->prepare("SELECT id, ingredients FROM recipes WHERE dish=:dish");
        $stmt->bindValue(":dish", $dish, SQLITE3_TEXT);

        $result = $stmt->execute() or die("error");
        $row = $result->fetchArray();

        $db->close();
        return json_encode(array("id" => $row["id"], "ingredients" => $row["ingredients"]));
    }

    function getAllDishes() {
        $db = new SQLite3("recipes.db", SQLITE3_OPEN_READONLY);

        $query = "SELECT id, dish FROM recipes";
        $result = $db->query($query) or die("error");

        $dishes = array();
        while($row = $result->fetchArray()) {
            $dishes[$row["id"]] = $row["dish"];
        }

        $db->close();

        return json_encode($dishes);
    }

    function ping() {
        $db = new SQLite3("recipes.db", SQLITE3_OPEN_READONLY);

        $query = "SELECT secret_sauce_quantity FROM recipes WHERE dish='pizza'";
        $result = $db->query($query) or die("error");
        $row = $result->fetchArray();
        
        if ($row["secret_sauce_quantity"] == 3.241) {
            echo "pong";
        } else {
            die("error");
        }
        
        $db->close();
    }
?>
