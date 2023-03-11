#!/usr/bin/perl
use strict;
use warnings;
use 5.010;
# by Torben Menke http:/entorb.net

# pp -u -M Excel::Writer::XLSX -o script.exe script.pl & copy script.exe c:\tmp

# TODO

# IDEAS

# DONE

# Perl Standard Modules
use Data::Dumper;
use File::Basename;
use utf8;
# use open ":encoding(UTF-8)"; # for all files
use Encode;
my $encodingSay   = 'CP850'; # Linux: 'UTF-8', DOS: 'CP850';
my $encodingFileSystem = 'Latin1'; # Linux: 'UTF-8', DOS: 'CP850';
use MIME::Base64; # for PHOTO extraction

# CPAN Modules
# use Excel::Writer::XLSX;
# perl -MCPAN -e "install Excel::Writer::XLSX"

my $s;
my @L;

my $fileIn = '../2021/ab-torben-nc-2021-01-15.vcf';
# my $fileIn = "ab-franca-oc-2018-08-01a.vcf";
my $outputfolder = $fileIn;
$outputfolder =~ s/\.vcf$//;
mkdir $outputfolder unless -d $outputfolder;

open(my $fhIn, '<:encoding(UTF-8)', $fileIn)
or die encode $encodingSay, "ERROR: Can't read from file '$fileIn': $!";
# binmode ($fhIn, ":encoding(UTF-8)");
my $cont = join '',<$fhIn>;
close $fhIn;

$cont =~ s/\r\n/\n/g; # EOL -> Linux
@L = split /BEGIN:VCARD\n/, $cont;
undef $cont;
shift @L; # remove first empty card

foreach my $vcard (@L) {
  $vcard = "BEGIN:VCARD\n$vcard";
  my $fn;
  if ($vcard =~ m/^FN:(.*)\n/m) {
    $fn = $1;
  } else {
    die encode $encodingSay, "ERROR: 'FN:' not found in card: \n'$vcard'\n";
  }
  $fn =~ s/\\,/,/g;
  $fn =~ s/[^\w ]+//g; # remove /,\ and other non-word-chars

  # say encoding $encodingSay, $fn;

  my $fileOut = encode $encodingFileSystem, "$outputfolder/$fn.vcf";
  $fileOut =~ s/\?/_/g; # remove unknown chars

# Extract Photo
  my $photo;
  if ($vcard =~ m/\nPHOTO[^:]*:(.*?)(?=\n[A-Z\-]+[:;])/s) {
  $photo = $1;
  if (defined($photo)) {
    my $photoOut = $fileOut;
    $photoOut =~ s/\.vcf$/.jpg/;
    print $photoOut;
    my $photoDecoded= MIME::Base64::decode_base64($photo);
    open my $fhPhoto, '>', $photoOut or die $!;
    binmode $fhPhoto;
    print $fhPhoto $photoDecoded;
    close $fhPhoto;
    }
  }

  open (my $fhOut, '>:encoding(UTF-8)', $fileOut)
  or die (encode $encodingSay, "ERROR: Can't write to file '$fileOut': $!");
  # binmode ($fhOut, ":encoding(UTF-8)");
  print $fhOut $vcard;
  close $fhOut;
} # foreach my $vcard (@L) {
