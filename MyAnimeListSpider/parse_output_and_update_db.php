<?php


class MyDB extends SQLite3
{
    function __construct()
    {
        $this->open('animeDB.sqlite');
    }
}

$db = new MyDB();
$db->query("delete from companies");
$db->query("delete from animes");
$db->query("delete from genres");
$db->query("delete from animes_companies");
$db->query("delete from animes_genres");


function insert1($name, $tablename)
{
   global $db;
   $query_1 = "INSERT INTO $tablename ( \"name\" )";                    
   $query2 = " \"$name\" " ;                     
   $qq     = "$query_1 VALUES ( $query2 );";
   //echo $qq;
   $db->query($qq);
}


function insert_anime($anime)
{
  global $db;


  if ($anime["name"] == "NULL")
  {
    $anime["name"] = $anime["romaji"];
  }

$keys = "";
$values = "";


foreach ($anime as $key => $value) 
{
  $value = str_replace("\"", " ", $value);
  $values .= "\"$value\", ";
  $keys .= "$key, ";
}

$values = substr($values, 0, strlen($values)-2);
$keys = substr($keys, 0, strlen($keys)-2);



 return $qq = "INSERT INTO animes ($keys) VALUES ($values);";
 //echo $qq; echo "\n\n";
 //$result = $db->query($qq);

}


function get_id($name, $tablename)
{
    global $db;

     //replace internal quotation
    $name = str_replace("\"", " ", $name);

    $q1 = "SELECT ID FROM $tablename WHERE name = \"$name\" ";
    //echo $q1;
    $result = $db->query($q1)->fetchArray(SQLITE3_ASSOC);

    if ($result === FALSE)
    {
      return FALSE;
    }else
    {
      return $result["id"];
    }
    //var_dump($result->fetchArray(SQLITE3_ASSOC));
}


date_default_timezone_set("Asia/Tokyo");

function get_value($name,$str)
{
     if(preg_match("/$anime:\s*(.+)/", $str, $m ))
    {
        return  $m[1];
    }else
    {
        return "NULL";
    }

}


function parse_date_string($s)
{
      if (isset($s)&&strpos($s, "?") !== FASLE) 
       {

        if (strpos($s, ",") == FASLE||strlen($s) <= 5){return $s;}

          $time = strtotime($s); 

          if ($time != -1&& $time != 0)
          {
            return date('Y-m-d',$time);
          }else
          {
            return  "NULL";
          }
       }
       else
       {
           return  "NULL";
      }

}

$companies = array();
$genres = array();

$f = file("anime.txt");


$anime_insert_q = " ";

$anime = array();
$creating_entry = false;

foreach ($f as $key => $line) {
  

   if (strpos($line,"---------begin-of-entry------") !== false)
   {
        $creating_entry = true;
        $anime = array();
        $anime["name"] = "NULL";
        $anime["romaji"] = "NULL";
        $anime["type"] = "NULL";
        $anime["episodes"] = "NULL";
        $anime["status"] = "NULL";
        $anime["begin_date"] = "NULL";
        $anime["end_date"] = "NULL";
        $anime["rating"] = "NULL";


   }else if (strpos($line,"-----end-of-entry----") !== false)
   {
          $creating_entry = false;

          $anime_insert_q .= insert_anime($anime);

          $anime = array();
          //var_dump($anime);

   }else if($creating_entry)
   {
             $line =  substr($line, 1, strlen($line)-3);
             $line = trim($line);

            if (strlen($line)==0)
            {
                continue;
            }
            if(strpos($line, "Japanese:") !== false)
            {
                //echo $line;
                
                 $line = get_value("Japanese:",$line);
                $line = str_replace("\"", " ", $line);
                 $anime["name"] = $line;
               
            }else if(strpos($line, "Type:") !== false)
            {
                $anime["type"] = get_value("Type:",$line);
            }
            else if(strpos($line,"Episodes:" ) !== false)
            {
                $anime["episodes"] = get_value("Episodes:",$line);
            }
            else if(strpos($line,"Status:" ) !== false)
            {
                $anime["status"] = get_value("Status:",$line);
            }
            else if(strpos($line, "Aired:") !== false)
            {
                $line =  get_value("Aired:",$line);            

               $tks =  explode("to", $line);

               $time = strtotime($tks[0]); 

               $anime["begin_date"] = parse_date_string($tks[0]);

              $anime["end_date"] = parse_date_string($tks[1]);
            }
            else if(strpos($line,"Producers:" ) !== false)
            {
                 $line = get_value("Producers:",$line);

                  $tks =  explode(",", $line); 

                  foreach ($tks as $cmpy) {

                      $cmpy = trim($cmpy);

                      if( !isset($companies[$cmpy])   ){ $companies[$cmpy] = array(); }
                       if ($anime["name"] == "NULL")
                      {
                        $anime["name"] = $anime["romaji"];
                      }

                      array_push( $companies[$cmpy], $anime["name"]);
                  }

            }
            else if(strpos($line,"Genres:" ) !== false)
            {
                //$anime["genres"] = get_value("Genres:",$line);

                 $line = get_value("Genres:",$line);

                  $tks =  explode(",", $line); 

                  foreach ($tks as $gg) {

                    $gg = trim($gg);

                      if(   !isset($genres[$gg])   ){ $genres[$gg] = array(); }

                       if ($anime["name"] == "NULL")
                      {
                        $anime["name"] = $anime["romaji"];
                      }
                      array_push( $genres[$gg], $anime["name"]);
                  }

            }
            else if(strpos($line,"Duration:" ) !== false)
            {
                $line = get_value("Duration:",$line);

                $time = "NULL";
                if(preg_match("/(\d+) hr. (\d+) min/", $line, $m))
                {
                  $time = intval($m[1])*60 + intval($m[2]);
                }else if (preg_match("/(\d+) min/", $line, $m))
                {
                  $time = intval($m[1]);
                }

                $anime["minutes"] = $time;

            }
            else if(strpos($line, "Rating:") !== false)
            {
                $anime["rating"] = get_value("Rating:",$line);
            }
            else
            {
                $anime["romaji"] = $line;
            }
   }
}

$t1 = time();

$db->query("BEGIN TRANSACTION;");
$db->query($anime_insert_q);
$db->query("END TRANSACTION;");

$t2 = time();
echo $t2-$t1." s to inset anime table\n";


$q1 = "SELECT name, id FROM animes";
$result = $db->query($q1);

$anime_name_id_table = array();
while ($value = $result->fetchArray(SQLITE3_NUM))
{
  //var_dump($value);
  $anime_name_id_table[$value[0]] = $value[1];
}

//var_dump($anime_name_id_table);


$t1 = time();
$db->query("BEGIN TRANSACTION;");
$bigq = " ";
foreach ($genres as $key => $value) {

  insert1($key, "genres");
  $g_id = get_id($key, "genres");

  foreach ($value as $key2 => $value2) 
  {
    //$anime_id = get_id($value2, "animes");
    $value2 = str_replace("\"", " ", $value2);
    $anime_id = $anime_name_id_table[$value2];
    //echo $value2;

    $query_1 = "INSERT INTO animes_genres ( genre_id, anime_id ) ";                 
    $qq     = "$query_1 VALUES  ($g_id, $anime_id );";
    //echo $qq; echo "\n";
    //$db->query($qq);
    $bigq .= $qq;
  }
}

$db->query($bigq);
$db->query("END TRANSACTION;");
$t2 = time();
echo $t2-$t1." s to insert  genres and animes_genres  tables\n";



$t1 = time();
$db->query("BEGIN TRANSACTION;");
$bigq = " ";


foreach ($companies as $key => $value) {

  insert1($key, "companies");
  $g_id = get_id($key, "companies");

  $g_id = 2;

  foreach ($value as $key2 => $value2) 
  {
    //$anime_id = get_id($value2, "animes");
     $value2 = str_replace("\"", " ", $value2);
    $anime_id = $anime_name_id_table[$value2];
    $query_1 = "INSERT INTO animes_companies ( company_id, anime_id ) ";                 
    $qq     = "$query_1 VALUES  ($g_id, $anime_id );";
    //echo $qq;echo "\n";
    //$db->query($qq);
    $bigq .= $qq;
  }
}


$db->query($bigq);
$db->query("END TRANSACTION;");


$t2 = time();
echo $t2-$t1." s to insert  companies and animes_companies  tables\n";
