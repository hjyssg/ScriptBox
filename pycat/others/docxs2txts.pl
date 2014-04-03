use File::Basename;
 
##this simple script converts a directory of docx files into
##txt files by using docx2txt.pl
##http://docx2txt.sourceforge.net/

##usage: put docxc2txts.pl and docx2txt.pl into the direct where
##contains the docx file that you want to convert
##and then perl run this script. it will convert all docx files 
##into txt files

 @files = <*.docx>;
 foreach $file (@files) 
 {
  $fn = basename($file, ".docx"); 
  $ofn = $fn.".txt";

  $command ="perl docx2txt.pl "."\"$file\""."  "."\"$ofn\"";
  #print $command, "\n";
  $result = `$command`;
}

