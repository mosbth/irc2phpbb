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
require(__DIR__ . '/magpierss/rss_fetch.inc');

$feeds = array(
	array(
		'url'=>'http://dbwebb.se/forum/feed.php', 
		'callback'=>function($item) {
			file_put_contents(tempnam(__DIR__ . "/incoming", "forum"), "Nytt foruminlägg av " . utf8_encode($item['author_name']) . ": " . utf8_encode($item['title']) . " (" . utf8_encode($item['id']) . ")");
		},
	),
);

//sqlite> create table aggregate (id INTEGER PRIMARY KEY AUTOINCREMENT, feed text, key text UNIQUE);
$db = new PDO("sqlite:" . __DIR__ . "/db.sqlite");
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_WARNING); // Display errors, but continue script
$stmt = $db->prepare("INSERT OR IGNORE INTO aggregate(feed,key) VALUES(?,?)");

$count = 0;
// get feed, loop though all items and try to add key to database, if succeed then callback.
foreach($feeds as $val) {
	$rss = @fetch_rss($val['url']);
	foreach ($rss->items as $item ) {
  	$stmt->execute(array($val['url'], $item['id']));
  	if($stmt->rowCount()) {
			call_user_func($val['callback'], $item);
			$count++;
  	}
	}
}

// Log last run to file
date_default_timezone_set('Europe/Stockholm');
file_put_contents(__DIR__ . "/aggregate.log", date(DATE_RFC822) . " $count new items.");