<?php

require 'vendor/autoload.php';



function fetch($num)
{
        $client = new Goutte\Client();

        // Go to the symfony.com website
        $url1= "http://myanimelist.net/topanime.php?type=&limit=$num";
        $crawler = $client->request('POST', $url1);

        echo $url1;
        echo "http://myanimelist.net/topanime.php?type=&limit=$num"."\n";



        $result = "";



        //iterate each anime entry of the page
        $crawler->filter("tr td strong")->each(function ($node, $i) {


        try 
        {
        
             echo "---------begin-of-entry-------------\n";

             //get the name of name
             $name=  $node->text();
             echo "[".$name."]\n";
            
             //get the url
             $new_page_url = $node->parents()->first()->attr("href");

            //open it  
            $client = new Goutte\Client();
            $url = 'http://myanimelist.net/'.$new_page_url;
            $new_page_crawler = $client->request('POST', $url);


            //parse the opened page
            if (isset($new_page_crawler))
            {

                 $new_page_crawler->filter("div span")->each(function ($np_node)
                {
                    $ss =  $np_node->text();
                    $div = $np_node->parents()->first();

                    $tt = $div->text();

                    if (strlen($tt)>400)  { return ;}

                    $tagName =  $np_node->parents()->first()->getNode(0)->tagName;

                    $tt = trim(preg_replace('/\n/', ' ', $tt));

                    if (preg_match('[Japanese|Type|Episodes|Status|Aired|Producers|Duration|Rating|Genres|Duration]', $tt))
                    {
                            if ($tagName == "div")
                            {
                                  echo "[".$tt."]\n";  
                            }
                    } 
                });



            }else
            {
                   // echo $tagName;  
                    echo "-----fail to open subpage--[$url]---\n";  
            }

            usleep(5e+5);

            echo "---------end-of-entry-------------\n";
            echo "\n\n";

            // echo $reuslt;


            // $f = fopen($num.".txt", "a");
            // fwrite($f, $result);
            // fclose($f);

              } catch (Exception $e) 
        {
             echo 'Caught exception: ',  $e->getMessage(), "\n";
        }
          
        });


}

   
    
   // for ($ii=2790; $ii < 2790+30 ; $ii+= 30) { 

   //      try 
   //      {
   //          echo "------------begin at $ii-------------\n";    
   //          fetch($ii);
   //          echo "---------------------------------------\n\n\n\n\n\n\n";

   //              if($ii == 2100||$ii == 3300||$ii == 4500||$ii == 5700||$ii == 6900||$ii == 8100)
   //              {
   //                   usleep(6e+7);   
   //              }

   //      } catch (Exception $e) 
   //      {
   //           echo 'Caught exception: ',  $e->getMessage(), "\n";
   //      }
   //      usleep(3e+6);
   // }
   
fetch(2790);
fetch(4860);


?>
