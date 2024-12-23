<?php
// This script expects parameters: Title, MPN, Model, UPC, ProductReferenceID
// It will check if any of these parameters contain any of the values found in 
// the first 3 columns of the rolex.csv file.
// If a match is found, it will print the "Retail Price" and "Market Price" 
// columns in a nice HTML table.

// Retrieve parameters from URL (case-insensitive)
$params = array(
    'Title' => isset($_GET['Title']) ? $_GET['Title'] : '',
    'MPN' => isset($_GET['MPN']) ? $_GET['MPN'] : '',
    'Model' => isset($_GET['Model']) ? $_GET['Model'] : '',
    'UPC' => isset($_GET['UPC']) ? $_GET['UPC'] : '',
    'ProductReferenceID' => isset($_GET['ProductReferenceID']) ? $_GET['ProductReferenceID'] : ''
);

// Convert all parameters to lowercase for case-insensitive search
foreach ($params as $key => $value) {
    $params[$key] = strtolower($value);
}

$filename = 'rolex.csv';

if (!file_exists($filename)) {
    echo "CSV file not found.";
    exit;
}

// Read the CSV
$handle = fopen($filename, 'r');
if (!$handle) {
    echo "Unable to open the CSV file.";
    exit;
}

// The CSV columns are expected to be:
// Model Number, Model Name, Variant, Retail Price, Market Price
$results = array();

// Skip header
$header = fgetcsv($handle);

// Process each line
while (($data = fgetcsv($handle)) !== FALSE) {
    // Extract columns
    $modelNumber = isset($data[0]) ? $data[0] : '';
    $modelName   = isset($data[1]) ? $data[1] : '';
    $variant     = isset($data[2]) ? $data[2] : '';
    $retailPrice = isset($data[3]) ? $data[3] : '';
    $marketPrice = isset($data[4]) ? $data[4] : '';

    // Only process if model number is not empty and at least 4 chars
    if (strlen($modelNumber) >= 4) {
        // Lowercase values for comparison
        $lowerModelNumber = strtolower($modelNumber);

        // Check if any parameter contains this model number
        foreach ($params as $paramValue) {
            if ($paramValue !== '' && strpos($paramValue, $lowerModelNumber) !== false) {
                $results[] = array($modelNumber, $modelName, $variant, $retailPrice, $marketPrice);
                break;
            }
        }
    }
}
fclose($handle);

// Print the results if any
if (!empty($results)) {
    echo "<table border='1' cellpadding='5' cellspacing='0'>";
    echo "<tr><th>Model Number</th><th>Model Name</th><th>Variant</th><th>Retail Price</th><th>Market Price</th></tr>";
    foreach ($results as $row) {
        echo "<tr><td>{$row[0]}</td><td>{$row[1]}</td><td>{$row[2]}</td><td>{$row[3]}</td><td>{$row[4]}</td></tr>";
    }
    echo "</table>";
} else {
    echo "No matches found.";
}
?>
