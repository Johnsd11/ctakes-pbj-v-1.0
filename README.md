# cTAKES Installation Instructions:

-install tortoiseSVN https://tortoisesvn.net/downloads.html <br/>
-Make sure to check "command line client tools" when downloading tortoiseSVN<br/>
-Set Version control, subversion, path to subverison exe to :  C:\Program Files\TortoiseSVN\bin\svn.exe<br/> 
-Download ctakes project using the svn option in intelliJ "svn co https://svn.apache.org/repos/asf/ctakes/trunk/"<br/> 
-Download ctakes_pbj off of "https://github.com/Johnsd11/Ctakes_PBJ" into the ctakes project directory under the name "ctakes-pbj"<br/> 
-Set Project SDK: corretto-1.8<br/>
-Set Project language level: SDK default (8)<br/>
-install java, install maven<br/>
for windows: I installed maven using a package manager: chocolatey<br/>
https://www.how2shout.com/how-to/download-and-install-maven-on-windows-10-or-11-via-command-line.html<br/>
-Add pbj module to main project pom.xml<br/>
    - scroll down until you come across `<modules>` list<br/>
    - add this line `<module>ctakes-pbj</module>` anywhere on the list<br/>
    - Next look for the `<dependency>` list<br/>
    - add these lines <br/>
    `<dependency>` <br/>
                    `<groupId>org.apache.ctakes</groupId>`<br/> 
                    `<artifactId>ctakes-pbj</artifactId>`<br/>
                    `<version>${project.version}</version>`<br/>
                `</dependency>`<br/>
-Next open the maven tab on the top right of the intellij window, click Apache cTAKES, Lifecycle, compile<br/>
  
-open Project Structure, navigate to modules tab on the left side, find ctakes-pbj, click on it and then press the plus sign and add python 3.8 to it<br/> 


  # Artemis Instructions For making a Broker: <br/>
  -First download ActiveMQ Artemis here: https://activemq.apache.org/components/artemis/download/<br/>
  -Naviagate to the downloaded apache-artemis folder in your command line<br/>
  -from there cd into bin, then while in bin, type "./artemis create mybroker" for MAC or for windows "artemis create mybroker"<br/>
  -This will prompt a Username and Password which can be anything you want<br/>
  -From here you can now cd into mybroker/bin<br/>
  -Once you are in bin again you can run "./artemis run" for MAC or "artemis run" for windows to start the broker<br/>
  -Here are more directions if you need more help or clarification<br/>
  -https://activemq.apache.org/components/artemis/documentation/1.0.0/running-server.html<br/>
    
