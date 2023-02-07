# cTAKES Installation Instructions:

### Windows
-install tortoiseSVN https://tortoisesvn.net/downloads.html  <br/>
-Make sure to check "command line client tools" when downloading tortoiseSVN<br/>
-Once tortoiseSVN is downloaded, open IntelliJ settings, go to the Version control tab on the left hand side. Select the subversion tab, then in the "path to Subversion executable" field fill in : `C:\Program Files\TortoiseSVN\bin\svn.exe` <br/>
-Download ctakes project using the `get from VCS` button on the "Welcome to IntelliJ" page.
-Select the svn option from the Version Control dropdown and add https://svn.apache.org/repos/asf/ctakes/trunk/ then checkout<br/> 
-Select the 1.8 working format of cTakes <br/>
-Go back to the "Welcome to IntelliJ" page and use the `get from VCS` button again, this time we want to use git. <br/>
-Copy this link "https://github.com/Johnsd11/ctakes-pbj-v-1.0" and then save the repo in cTakes under the folder "ctakes-pbj" <br/>


### Mac and Linux
-Install Subversion using homebrew then type the command `brew install subversion`(for mac and linux) <br/>
-Download ctakes project using the `get from VCS` button on the "Welcome to IntelliJ" page.
-Select the svn option from the Version Control dropdown and add https://svn.apache.org/repos/asf/ctakes/trunk/ then checkout<br/> 
-Select the 1.8 working format of cTakes <br/>
-Go back to the "Welcome to IntelliJ" page and use the `get from VCS` button again, this time we want to use git. <br/>
-Copy this link "https://github.com/Johnsd11/Ctakes_PBJ" and then save the repo in cTakes under the folder "ctakes-pbj" <br/>


### Windows
-install maven using a package manager: chocolatey<br/>
https://www.how2shout.com/how-to/download-and-install-maven-on-windows-10-or-11-via-command-line.html<br/>


### Mac and Linux
-install maven using brew : `brew install maven` <br/>

---

-Search for and open `pom.xml` for ctakes trunk<br/>
    - Once in the file scroll down until you come across the `<modules>` list<br/>
    - add this line `<module>ctakes-pbj</module>` anywhere on the list<br/>
    - Next look for the `<dependency>` list<br/>
    - add these lines <br/>
    `<dependency>` <br/>
         `<groupId>org.apache.ctakes</groupId>`<br/> 
         `<artifactId>ctakes-pbj</artifactId>`<br/>
         `<version>${project.version}</version>`<br/>
    `</dependency>`<br/>
-Next open the maven tab on the top right of the intellij window, click Apache cTAKES, Lifecycle, install<br/>
-After this step, the ctakes-pbj directory will appear to have a blue square on it in the left hand side of IntelliJ that displays project structure.



### Configurations
-add python plugin from the IntelliJ plugins store <br/>
-Set Project SDK: corretto-1.8<br/>
-Set Project language level: SDK default (8)<br/>
-install the latest version of java<br/>
-open Project Structure, navigate to modules tab on the left side, find ctakes-pbj, click on it and then press the plus sign and add python 3.8 to it<br/>
-**IMPORTANT:** You need to make sure that you follow the step above first before you mark the python and java directories as source roots. <br/>
-Make sure to mark the ctakes-pbj/src/main/python and ctakes-pbj/src/main/java directories as a source roots <br/>
  

 # Artemis Instructions For making a Broker:
-First download ActiveMQ Artemis here: https://activemq.apache.org/components/artemis/download/<br/>
-Naviagate to the downloaded apache-artemis folder in your command line<br/>
-from there cd into bin, then while in bin, type "./artemis create mybroker" for MAC or for windows "artemis create mybroker"<br/>
-This will prompt a Username and Password which can be anything you want<br/>
-It will also prompt something called `--allow-anonymous`, Press `Y` <br/>
-From here you can now cd into mybroker/bin<br/>
-Once you are in bin again you can run "./artemis run" for MAC or "artemis run" for windows to start the broker<br/>
-Here are more directions if you need more help or clarification<br/>
-https://activemq.apache.org/components/artemis/documentation/1.0.0/running-server.html<br/>


# Usage

Example piper files can be found in ctakes-examples and example py files can be found in the ctakes-pbj/examples folder<br/>

### Creating a Piper file

This is an example piper file that will spin up a complete pbj pipeline.<br/>
```
#  This piper will start the Apache Artemis broker pointed to by the -a parameter on the command line.
#  It will pause for 5 seconds to allow Artemis to fully launch.
#
#  This piper will then launch another instance of Apache cTAKES.
#  That instance of cTAKES will run the third and final bit of the entire PBJ pipeline.
#
#  This piper will then launch a python PBJ bit of the entire pipeline.

```
We set setJavaHome = no, this is keep things consistent ??????<br/>
```
set SetJavaHome=no
```

The parameters you need to run the piper file are:<br/>
```
#
#  To run this pipeline from the command line, use the parameters:
#  -p PbjFirstStep
#  -d {python environment Directory}
#  -a {Artemis Broker Directory}
#  -i {Input Document Directory}
#  -o {Output Directory}

```

Sets up required parameters, starts your Artemis Broker, pips the PBJ project.<br/>
```
load PbjStarter
```

Start another instance of cTAKES, running the pipeline in StartAllExample_end.piper<br/>
$OutputDirectory will substitute the value of this cTAKES pipeline's value for OutputDirectory.<br/>
$ArtemisBroker will substitute the value of this cTAKES pipeline's value for ArtemisBroker.<br/>
```
add CtakesRunner Pipeline="-p PbjThirdStep -o $OutputDirectory -a $ArtemisBroker"
```

Declare the python pipeline defining the second step in the total pipeline.<br/>
```
set PbjSecondStep=ctakes_pbj.examples.word_finder_pipeline
```

There is a fixed order to queue specification in python pipelines.<br/>
The incoming (receiver) queue is named first, the outgoing (sender) queue is named second.<br/>
```
add PythonRunner Command="-m $PbjSecondStep JavaToPy PyToJava" LogFile=word_finder_pipeline.log
```

The pipeline run by this instance of cTAKES. <br/>
Load a simple token processing pipeline from another pipeline file <br/>
```
load DefaultTokenizerPipeline
```

Send CAS to Artemis at the specified queue.  Send stop signal when processing has finished.<br/>
```
add PbjSender SendQueue=JavaToPy SendStop=yes
```
### Example py file: WordFinder.py

Start with a function names process<br/>
```
def process(self, cas):
    
```
While we could use ct.create_type to create and add types, for each type lookup the cas array is searched.<br/>
So it is faster to get the types first and then create instances with ct.add_type<br/>

```
anatomy_type = cas.typesystem.get_type(AnatomicalSiteMention)
symptom_type = cas.typesystem.get_type(SignSymptomMention)
procedure_type = cas.typesystem.get_type(ProcedureMention)
```

Assigning values to sites, findings, and procedures.
```
sites = ['breast']
findings = ['hernia', 'pain', 'migraines', 'allergies']
procedures = ['thyroidectomy', 'exam']
```

Not sure what to write here<br/>
```
for segment in cas.select(Segment):
    text = segment.get_covered_text()
    for word in sites:
        begin = text.find(word)
        if begin > -1:
            print("found Anatomic Site")
            end = begin + len(word)
            add_type(cas, anatomy_type, begin, end)
    for word in findings:
        begin = text.find(word)
        if begin > -1:
            print("found Sign or Symptom")
            end = begin + len(word)
            add_type(cas, symptom_type, begin, end)
    for word in procedures:
        begin = text.find(word)
        if begin > -1:
            print("found Procedure")
            end = begin + len(word)
            add_type(cas, procedure_type, begin, end)
 ``` 
 
 ### Example pipeline file: WordFinderPipeline.py
 
 
Start by creating an instance of the pipeline
```
pipeline = PBJPipeline()
```
Then adding the process(es) 
```
pipeline.add(WordFinder())
...
```
Last is adding the sender and receiver while also initializing the pipeline
```
pipeline.add(PBJSender())
pipeline.initialize()
start_receiver(pipeline)
```

 
# Running an Example
-You can start running an example by creating an application configuration<br/>
-You can call it whatever you want, we called it "StartAllExample"<br/>
-Copy down the information you see in the picture below <br/>
![step3](https://user-images.githubusercontent.com/34665038/181270724-c1dbc854-397a-4b1f-b5db-e194adf074d5.png)<br/>
-p "org/apache/ctakes/pbj/pipeline/StartAllExample" <br/>
-i "org/apache/ctakes/examples/notes/annotated" <br/>
-a "[Destination of your Artemis Broker]" <br/>
-d "[Destinaiton of your python.exe]" <br/>
![step1](https://user-images.githubusercontent.com/34665038/181271047-cf112a93-0d8c-4734-aa21-1281377e6762.png)<br/>

## End-to-end PBJ Examples
### Temporal Example
- You first need to get the API side up and running. To do this you need to follow the steps listed [here.](https://github.com/Machine-Learning-for-Medical-Language/cnlp_transformers)
- Once that is running you need to then create this configuration for StartTemporalExample.piper file.<br/>
-p<br/>
org/apache/ctakes/pbj/pipeline/StartTemporalExample<br/>
-i<br/>
(input)<br/>
-a<br/>
(folder where your Artemis broker is)<br/>
-d<br/>
(enviroment) <br/>
-o<br/>
(output)<br/>
--key<br/>
(UMLS key)<br/>
- You should now be able to run that piper file while the API side is running. You can look at the output of running the piper file in "temporal_py.log" as well
as the output file that you put into the configuration.<br/>

### Negation Example
- You first need to get the API side up and running. To do this you need to follow the steps listed [here.](https://github.com/Machine-Learning-for-Medical-Language/cnlp_transformers)
- Once that is running you need to then create this configuration for StartNegationExample.piper file.<br/>
-p<br/>
org/apache/ctakes/pbj/pipeline/StartNegationExample<br/>
-i<br/>
(input)<br/>
-a<br/>
(folder where your Artemis broker is)<br/>
-d<br/>
(enviroment) <br/>
-o<br/>
(output)<br/>
--key<br/>
(UMLS key)<br/>
- You should now be able to run that piper file while the API side is running. You can look at the output of running the piper file in "negation_py.log" as well
as the output file that you put into the configuration.<br/>

### DTR Example
- You first need to get the API side up and running. To do this you need to follow the steps listed [here.](https://github.com/Machine-Learning-for-Medical-Language/cnlp_transformers)
- Once that is running you need to then create this configuration for StartDtrExample.piper file.<br/>
-p<br/>
org/apache/ctakes/pbj/pipeline/StartDtrExample<br/>
-i<br/>
(input)<br/>
-a<br/>
(folder where your Artemis broker is)<br/>
-d<br/>
(enviroment) <br/>
-o<br/>
(output)<br/>
--key<br/>
(UMLS key)<br/>
- You should now be able to run that piper file while the API side is running. You can look at the output of running the piper file in "dtr_py.log" as well
as the output file that you put into the configuration.<br/>

  
  

    
