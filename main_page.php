<!DOCTYPE html>
<html>
	<head>
		<title>SEARCH PAGE</title>
	</head>
	<body>
		<form method="post" action="<?php $_PHP_SELF; ?>">
			SEARCH <input type="text" name="search">
			<input type="submit" name="submit" value="submit">
		</form>
	</body>
</html>
<?php
   class MyDB extends SQLite3
   {
      function __construct()
      {
         $this->open('C:\Users\Gaurav Mitra\Desktop\Learning\Web Crawler\crawler.sqlite');
      }
   }
   $db = new MyDB();
   if(!$db){
      echo $db->lastErrorMsg();
   } else {
      echo "Opened database successfully\n";
   }
   $variable = $_POST["search"];

   $sql =<<<EOF
      SELECT pages FROM Inverse WHERE word = "$variable";
EOF;

   $ret = $db->query($sql);
	   if($row = $ret->fetchArray(SQLITE3_ASSOC) ){
	   	$pages = $row['pages'];
	   	$pages = "$pages";
	   	$arr = explode(',', $pages);
	   	foreach ($arr as $value) {
	   		$sql = " SELECT url FROM Pages WHERE id = $value";
	   		$ret1 = $db->query($sql);
	   		if($row1 = $ret1->fetchArray(SQLITE3_ASSOC) ) {
	   			$link = $row1['url'];
				//echo "<h1>".$row1['url']."</h1>";
				echo "<a href=$link>".$link."</a>";
			}
	   	}
   }
   //echo "Operation done successfully\n";
   $db->close();

      //echo "ID = ". $row['id'] . "\n";
      //echo "WORD = ". $row['word'] . "\n";  
      //echo "PAGE = ". $row['pages'] . "\n";
   		/*$pages = $row['pages'];
   		$pages = "$pages";
   		$arr = explode(',', $pages);
   		foreach ($arr as $value) {
   			$sql1 =<<<EOF
   				SELECT url FROM Pages WHERE id = $value;
EOF;		
			$ret1 = $db->query($sql1);
			if($row1 = $ret1->fetchArray(SQLITE3_ASSOC) ) {
				echo "Here";
			}
   		
   }
   echo "Operation done successfully\n";
   $db->close();*/
?>