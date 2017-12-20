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
		'url'=>'https://dbwebb.se/forum/feed.php',
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
	4410, 4411, 4412, 4413, 4414, 4415, 4416, 4417, // oophp ht15

      141,142,143,144,145,146,147,148,149,150, 	// phpmvc vt12 campus
      450,451,452,453,454,455,456,457,458, 		// phpmvc ht12
      800,                                    // phpmvc vt13
	1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, //phpmvc ht13
	4418, 4419, 4420, 4421, 4422, 4423, 4424, 4425, //phpmvc ht15

      367,368,369,370,371,372,373,374,375,376,  // javascript ht12
      367,368,369,370,371,372,373,374,375,376,  // javascript ht12 campus TBD
      801,                                      // javascript vt13
      1398, 1399, 1400, 1401, 1403, 1404, 1405, 1406, //javascript ht13
	2533, 2534, 2535, 2536, 2537, 2538, 2539, 2540, // javascript ht14
	4426, 4427, 4428, 4429, 4430, 4431, 4432, 4433, // javascript ht15

      85,70,69,68,67,66,65,64, 			// dbwebb1 vt12
      86,75,74,73,72,71, 				// dbwebb2 vt12

      1868,1869,1870,1871, //vt14 welcome upprop
      1875,1876,1877,1878,1879,1880,1881,1882, // phpmvc version 2
      2525, 2526, 2527, 2528, 2529, 2530, 2531, 2532, // phpmvc ht14

	2461,2462,2463,2464,2465,2466,2467,2468, // javascript1 ht14, vt15
	4384,4385,4386,4387,4388,4389,4390,4391, // javascript1 ht15
	

	2470,2471,2472,2473,2474,2475,2476,2477,2478, // python ht14, vt15
	4376,4377,4378,4379,4380,4381,4382,4383, // python ht15

	4392,4393,4394,4395,4396,4397,4398,4399, // linux ht15

	4401,4402,4403,4404,4405,4406,4407,4408, // webapp ht15

	3448,3449,3450,3451,3452,3453, 				// uppropstrådar vt15
	4937,4938,4939,4940,4941,4942,4943,4944, 	// uppropstrådar vt16

	4434, //webtopic ht15
	
	5416, 5417, 5418, 5419, 5420, 5421, 5422, 5423, // python ht16
	5449, 5450, 5451, 5452, 5453, 5454, 5455, 5456, // htmlphp ht16
	5424, 5425, 5426, 5427, 5428, 5429, 5430, 5431, // javascript1 ht16
	5473, 5474, 5475, 5476, 5477, 5478, 5479, 5480, // design ht16
	5432, 5433, 5434, 5435, 5436, 5437, 5438, 5439, // linux ht16
	5440, 5441, 5442, 5443, 5444, 5445, 5446, 5447, // webapp ht16
	5465, 5466, 5467, 5468, 5469, 5470, 5471, 5472, // javascript ht16
	5457, 5458, 5459, 5460, 5461, 5462, 5463, 5464, // phpmvc ht16
	5408, 5409, 5410, 5411, 5412, 5413, 5414, 5415,  // oophp ht16
	
	6056, 6068, 6069, 6131, // upprop vt2017
	
	6057, 6058, 6059, 6060, 6061, 6062, 6063, 6064, // oopython vt17
	6343, 6344, 6345, 6346, 6347, 6348, 6349, 6351, // webapp vt17
	6352, 6353, 6354, 6355, 6356, 6357, 6358, 6359, // oophp vt17

	6550, 6551, 6552, 6553, 6554, 6555, 6556, 6557, // python ht17
	6558, 6559, 6560, 6561, 6562, 6563, 6564, 6565, // htmlphp ht17
	6566, 6567, 6568, 6569, 6570, 6571, 6572, 6573, // javascrip1 ht17
	6574, 6575, 6576, 6577, 6578, 6579, 6580, 6581, // design ht17
	6582, 6583, 6584, 6585, 6586, 6587, 6588, 6589, // ramverk1 ht17
	6590, 6591, 6592, 6593, 6594, 6595, 6596, 6597, // ramverk2 ht17
	
	7119, 7120, 7121, 7122, 7123, 7124, 7125, 7126, // linux vt18
	
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
    CURLOPT_URL => 'https://dbwebb.se/forum/ucp.php?mode=login',
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
  curl_setopt($ch, CURLOPT_URL, 'https://dbwebb.se/forum/feed.php');
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
  $str = html_entity_decode("Forumet \"{$val['title']}\" av {$val['author']}{$mfl} https://dbwebb.se/f/{$val['post']}", ENT_QUOTES, 'UTF-8');
  file_put_contents(tempnam(__DIR__ . "/incoming", "forum"), $str);  
}
file_put_contents('aggregate.error', implode($error, '\n'), FILE_APPEND);
file_put_contents('aggregate.ignore', implode($ignored, '\n'), FILE_APPEND);
file_put_contents(__DIR__ . "/aggregate.log", date(DATE_RFC822) . " $count new items. Success=".count($success).", duplicates={$duplicates}, ignored=".count($ignored).", error=".count($error).".\n", FILE_APPEND);
