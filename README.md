# Postprocessing Script for Anime

This script will hash your downloaded Anime from **SABnzbd+** or **NZBGet** and sync it with your anidb.net account. The file will be renamed and moved to your specified target-directory.

## Installation

To use the script, extract the zip into your sabnzbd script folder and select sabtoanidb.py as your post processing script in your anime category.

## Config

First, rename anime.cfg.default to anime.cfg

You have to enter your anidb username and password into the config file. Also you have to modify the target directory in the config file to tell the script, where your anime folder is. (the script will copy the files to a directory with the name of the anime in that folder.)

####[AniDB]

<table>
  <tr>
    <th>config field</th><th>description</th>
  </tr>
  <tr>
    <td>username</td><td>your anidb.net username</td>
  </tr>
  <tr>
    <td>password</td><td>your anidb.net password</td>
  </tr>
  <tr>
    <td>suffix</td><td>only files with these suffix will be processed</td>
  </tr>
  <tr>
    <td>directory</td><td>target directory to copy your files to (every anime will get its own sub directory)</td>
  </tr>
  <tr>
    <td>directorymovie</td><td>target directory to copy non-tvdb movies (every anime movie will get its own sub directory)</td>
  </tr>
</table>

####[plex]

<table>
  <tr>
    <th>config field</th><th>description</th>
  </tr>
  <tr>
    <td>host</td><td>hostname or ip for plex media server (if this is empty, plex update is disabled)</td>
  </tr>
  <tr>
    <td>sections</td><td>which section of your plex media server should be updated (if more than one, separate by comma)? if this is empty, all sections will be updated</td>
  </tr>
</table>

####[xbmc]

<table>
  <tr>
    <th>config field</th><th>description</th>
  </tr>
  <tr>
    <td>host</td><td>hostname or ip for xbmc (if this is empty, xbmc update is disabled)</td>
  </tr>
  <tr>
    <td>port</td><td>port of your xbmc</td>
  </tr>
  <tr>
    <td>user</td><td>username for xbmc</td>
  </tr>
  <tr>
    <td>password</td><td>password for xbmc</td>
  </tr>
  <tr>
    <td>path</td><td>library path for updating only the added anime (leave empty to force update of whole library). If more than one episode is added, the whole library will be scanned.</td>
  </tr>
</table>

####[rename]

<table>
  <tr>
    <th>config field</th><th>description</th>
  </tr>
  <tr>
    <td>tvformat</td><td>rename pattern for tv shows (see below for tags)</td>
  </tr>
  <tr>
    <td>movieformat</td><td>rename pattern for movies (see below for tags)</td>
  </tr>
  <tr>
    <td>ovaformat</td><td>rename pattern for ova (see below for tags)</td>
  </tr>
  <tr>
    <td>foldername</td><td>naming pattern for anime-subfolder (only used when moving file)</td>
  </tr>
  <tr>
    <td>foldernamemovie</td><td>naming pattern for anime movie subfolder (only used when moving file)</td>
  </tr>
  <tr>
    <td>TVDBEpisodeFormat</td><td>rename pattern for Episodes, when using TVDB (see below for tags)</td>
  </tr>
  <tr>
    <td>TVDBFolderName</td><td>rename pattern for Folder, when using TVDB (see below for tags)</td>
  </tr>
  <tr>
    <td>TVDBSeasonFolder</td><td>rename pattern for Season Folder, when using TVDB (see below for tags)</td>
  </tr>
  <tr>
    <td>TVDBSpecialsFolder</td><td>rename pattern for Specials Folder, when using TVDB (see below for tags)</td>
  </tr>
</table>

####[integration]

<table>
  <tr>
    <th>config field</th><th>help</th>
  </tr>
  <tr>
    <td>nzbtoanidb_switches</td><td>defines, what nzbToAnidb.py should do (see below for anidb.py switches)</td>
  </tr>
</table>

Note:
If you use the delete option to delete the sourcefolder after moving, external sub-files will be lost!

#### Tags for renaming:

    %ATr%: Anime Name (Romaji)
    %ATe%: Anime Name (English)
    %ATk%: Anime Name (Kanji)
    
    %ETr%: Episode title (romaji)
    %ETe%: Episode title (english)
    %ETk%: Episode title (kanji)
    
    %GTs%: Group Name (short)
    %GTl%: Group Name (long)
    
    %EpHiNo%: Highest (subbed) episode number
    %EpCount%: Anime Episode count
    %AYearBegin%: The beginning year of the anime
    %AYearEnd%:  The ending year of the anime
    
    %EpNo%: File's Episode number
    
    %Type%: Anime type, Value: Movie, TV, OVA, Web
    %Depr%: File is deprecated if the value is '1'
    %Cen%: File is censored if the value is '1'
    %Ver%: File version
    %Source%: Where the file came from (HDTV, DTV, WWW, etc)
    %Quality%: How good the quality of the file is (Very Good, Good, Eye Cancer)
    %CurrentFN%: Current Filename
    %FCrc% : The file's crc
    %FCRC%: The file's crc in upper letters
    %FVideoRes%: Video Resolution (e.g. 1920x1080)
    %FALng%: List of available audio languages
    %FSLng%: List of available subtitle languages
    %FACodec%: Codecs used for the Audiostreams
    %FVCodec%: Codecs used for the Videostreams
    %suf%: File Suffix
	
	Only for TVDB:
	
	%TSTe%: TVDB Anime name
	%TETe%: TVDB episode title
	%TS%: TVDB Season
	%TE%: TVDB Episode Number
	%TSE%: TVDB Season/Episode Combination (like S01E12)


#### anidb.py has several commandline arguments:

    Options:
      -h, --help            show this help message and exit
      -u USERNAME, --username=USERNAME
                            AniDB username.
      -p PASSWORD, --password=PASSWORD
                            AniDB password.
      -r, --recursive       Recurse into directories.
      -s SUFFIX, --suffix=SUFFIX
                            File suffix for recursive matching.
      -c, --no-cache        Do not use cached values.
      -t, --tvdb            Use TVDB
      -l, --multihash       Calculate additional checksums.
      -i, --identify        Identify files.
      -a, --add             Add files to mylist.
      -w, --watched         Mark files watched.
      -n, --rename          Rename files.
      -m, --move            Move Files
      -x, --delete          Delete Folders after moving files
      -d DIRECTORY, --directory=DIRECTORY
                            Target parent directory.
      -k DIRECTORY, --directory-movie=DIRECTORY
                            Target parent directory for anime movies.
	  -o, --no-color        Disable color output.
	  -y, --update          Refresh Media Server (Plex or XBMC)

