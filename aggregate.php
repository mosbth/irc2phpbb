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
		'url'=>'http://dbwebb.se/forum/feed.php', 
    'ignore' => array(
      // htmlphp
      83,63,62,61,60,59,58,57,
      // oophp
      84,82,81,80,79,78,77,76,
      // dbwebb1
      85,70,69,68,67,66,65,64,
      // dbwebb2
      86,75,74,73,72,71,
    ),
		'callback'=>function($item, $ignore=array()) {
		  global $success, $ignored, $error;
      $matches = array();
      preg_match('/t=(\d+)&p=(\d+)/', $item['id'], $matches);
      //var_dump($item['id']);
      //var_dump($matches);
      $t = isset($matches[1]) ? $matches[1] : null;
      $p = isset($matches[2]) ? $matches[2] : null;      
      if(!($t && $p)) {
        file_put_contents('aggregate.error', "{$item['id']}\n", FILE_APPEND);
  			$error++;
      }
      else if(in_array($t, $ignore) == true) {
  			file_put_contents('aggregate.ignore', "{$item['id']}\n", FILE_APPEND);
  			$ignored++;
  		}
      else {
  			file_put_contents(tempnam(__DIR__ . "/incoming", "forum"), html_entity_decode("Forumet \"{$item['title']}\" av {$item['author_name']} http://dbwebb.se/f/$p", ENT_QUOTES, 'UTF-8'));
  			$success++;
  		}
		},
	),
);

//sqlite> create table aggregate (id INTEGER PRIMARY KEY AUTOINCREMENT, feed text, key text UNIQUE);
$db = new PDO("sqlite:" . __DIR__ . "/db.sqlite");
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING); // Display errors, but continue script
$stmt = $db->prepare("INSERT OR IGNORE INTO aggregate(feed,key) VALUES(?,?)");

$count = 0;
$success=0;
$ignored=0;
$error=0;
// get feed, loop though all items and try to add key to database, if succeed then callback.
foreach($feeds as $val) {
	$rss = @fetch_rss($val['url']);
	foreach ($rss->items as $item ) {
  	$stmt->execute(array($val['url'], $item['id']));
  	if($stmt->rowCount()) {
			call_user_func($val['callback'], $item, $val['ignore']);
			$count++;
  	}
	}
}

// Log last run to file
date_default_timezone_set('Europe/Stockholm');
file_put_contents(__DIR__ . "/aggregate.log", date(DATE_RFC822) . " $count new items. Success=$success, ignored=$ignored, error=$error.\n", FILE_APPEND);