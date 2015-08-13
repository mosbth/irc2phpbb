<?php
/**
 * Fetching rss feeds from a defined set of sources, enables action for all new items found.
 * 
 * Used to retrieve rss feeds and while discovering new items a callback can be made to decide
 * some action. This is basically used to create new files in the incoming library for the 
 * Marvin irc bot which helps him to notify on new posts in the forum.
 *
 */
chdir(__DIR__);

define('MAGPIE_INPUT_ENCODING', 'UTF-8');
define('MAGPIE_OUTPUT_ENCODING', 'UTF-8');
require(__DIR__ . '/magpierss/rss_fetch.inc');

$feeds = array(
	array(
		'file'=>__DIR__.'/cache/dbwebb_feed.xml',
		'url'=>'http://dbwebb.se/forum/feed.php',
    'ignore' => array(      
      83,63,62,61,60,59,58,57, 			// htmlphp vt12     
      389,390,391,392,393,394,395,396, 	// htmlphp ht12
      424,425,426,427,428,429,430,431, 	// htmlphp ht12 campus
      798,                              // htmlphp vt13  
      1373, 1374, 1375, 1376, 1377, 1378, 1379, 1380, // htmlphp ht13
	2508, 2509, 2510, 2511, 2512, 2513, 2514, 2515, // htmlphp ht14
	4366, 4367, 4368, 4369, 4370, 4371, 4372, 4373, // htmlphp ht15
	
      
      84,82,81,80,79,78,77,76, 			// oophp vt12
      432,433,434,435,436,437,438,439,	// oophp ht12
      799,                              // oophp vt13
      1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, //oophp v2 ht13
      2517, 2518, 2519, 2520, 2521, 2522, 2523, 2524, // oophp ht14

      141,142,143,144,145,146,147,148,149,150, 	// phpmvc vt12 campus
      450,451,452,453,454,455,456,457,458, 		// phpmvc ht12
      800,                                    // phpmvc vt13
      1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, //phpmvc ht13

      367,368,369,370,371,372,373,374,375,376,  // javascript ht12
      367,368,369,370,371,372,373,374,375,376,  // javascript ht12 campus TBD
      801,                                      // javascript vt13
      1398, 1399, 1400, 1401, 1403, 1404, 1405, 1406, //javascript ht13
      2533, 2534, 2535, 2536, 2537, 2538, 2539, 2540, // javascript ht14

      85,70,69,68,67,66,65,64, 			// dbwebb1 vt12
      86,75,74,73,72,71, 				// dbwebb2 vt12

      1868,1869,1870,1871, //vt14 welcome upprop
      1875,1876,1877,1878,1879,1880,1881,1882, // phpmvc version 2
      2525, 2526, 2527, 2528, 2529, 2530, 2531, 2532, // phpmvc ht14

      2461,2462,2463,2464,2465,2466,2467,2468, // javascript1

      2470,2471,2472,2473,2474,2475,2476,2477,2478, // python

      3448,3449,3450,3451,3452,3453, // uppropstrådar vt15

    ),
		'callback'=>function($item, $ignore=array()) {
		  global $success, $ignored, $error;
      $matches = array();
      preg_match('/t=(\d+)&p=(\d+)/', $item['id'], $matches);
      $t = isset($matches[1]) ? $matches[1] : null;
      $p = isset($matches[2]) ? $matches[2] : null;      
      if(!($t && $p)) {
        $error[] = $item['id'];
      }
      else if(in_array($t, $ignore) == true) {
  			$ignored[] = $item['id'];
  		}
      else {
        if(isset($success["$t"])) {
          $success["$t"]['nr']++;
          $success["$t"]['author'] = $item['author_name'];
          $success["$t"]['post'] = $p;
        } else {
  			  $success["$t"] = array('nr'=>1, 'title'=>$item['title'], 'author'=>$item['author_name'], 'post'=>$p);
  			}
  		}
		},
	),
);


// Prepare feed from dbwebb.se, login and store feed as local file
if(isset($feeds[0]['file'])) {
  require('config.php');
  $cookieFile = tempnam(__DIR__."/cache", "COOKIE");
  $ch = curl_init();
  curl_setopt_array($ch, array(
    CURLOPT_URL => 'http://dbwebb.se/forum/ucp.php?mode=login',
    CURLOPT_USERAGENT => "Mozilla/4.0 (compatible; MSIE 6.0; FreeBSD 8.1)",
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_CONNECTTIMEOUT => 30,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_COOKIESESSION => true,
    CURLOPT_COOKIEJAR => $cookieFile,
    CURLOPT_COOKIEFILE => $cookieFile,
    CURLOPT_POST => true,
    CURLOPT_RETURNTRANSFER => true,
    //CURLOPT_POSTFIELDS => "username=".USER."&password=".PWD."&login=do&redirect=feed.php&sid=".$sid."&autologin=0&viewonline=0",
    CURLOPT_POSTFIELDS => array('username'=>USER, 'password'=>PWD, 'login'=>'do'),
  ));
  curl_exec($ch);
  //print_r(curl_getinfo($ch));
  //echo curl_errno($ch) . curl_error($ch);
  curl_setopt($ch, CURLOPT_URL, 'http://dbwebb.se/forum/feed.php');
  file_put_contents($feeds[0]['file'], curl_exec($ch));
  //print_r(curl_getinfo($ch));
  curl_close($ch);
  unlink($cookieFile);
}


//sqlite> create table aggregate (id INTEGER PRIMARY KEY AUTOINCREMENT, feed text, key text UNIQUE);
$db = new PDO("sqlite:" . __DIR__ . "/db.sqlite");
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING); // Display errors, but continue script
$stmt = $db->prepare("INSERT OR IGNORE INTO aggregate(feed,key) VALUES(?,?)");


// get feed, loop though all items and try to add key to database, if succeed then callback.
$count = 0;
$success=array();
$ignored=array();
$error=array();
foreach($feeds as $feed) {
  if(isset($feed['file'])) {
    $rss = new MagpieRSS(file_get_contents($feed['file']), 'UTF-8');
  } else {
  	$rss = @fetch_rss($feed['url']);
  }
	foreach ($rss->items as $item ) {
  	$stmt->execute(array($feed['url'], $item['id']));
  	if($stmt->rowCount()) {
			call_user_func($feed['callback'], $item, $feed['ignore']);
			$count++;
  	}
	}
}

// Log last run to file
date_default_timezone_set('Europe/Stockholm');

$str=null;
$duplicates=0;
foreach($success as $key => $val) {
  $mfl = $val['nr'] > 1 ? "+".($val['nr']-1) : null;
  $duplicates += $val['nr']-1;
  $str = html_entity_decode("Forumet \"{$val['title']}\" av {$val['author']}{$mfl} http://dbwebb.se/f/{$val['post']}", ENT_QUOTES, 'UTF-8');
  file_put_contents(tempnam(__DIR__ . "/incoming", "forum"), $str);  
}
file_put_contents('aggregate.error', implode($error, '\n'), FILE_APPEND);
file_put_contents('aggregate.ignore', implode($ignored, '\n'), FILE_APPEND);
file_put_contents(__DIR__ . "/aggregate.log", date(DATE_RFC822) . " $count new items. Success=".count($success).", duplicates={$duplicates}, ignored=".count($ignored).", error=".count($error).".\n", FILE_APPEND);
