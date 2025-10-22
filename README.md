<center>

# Beautiful Data Lake
<br>
<p>This project's name is inspired in the Python module BeautifulSoup user for parsing text.<br> Its purpose is to resemble one of the latest uses of technology to help enterprises<br> understand their business and what goes on inside them. That is, the Data Lake</p>
<p>It is a "Demo version" of such entity so it lacks functionality, like being<br> able to take in unstructured data making Beautiful DataLake more similar to a traditional Data Warehouse</p>
<p>However it attempts to serve the same purpose, to help enterprises win, by improving data storage and communication between different layers of a business.</p>
</center>


<br><br>
## -- versioning
<hr><br><br>


<details>
<summary><b>List of modules required</b></summary>
<br>


<hr><b><i><center>
pytest <br>
flask <br>
flask_sqlalchemy <br>
pymysql <br>
flask-wtf <br>
wtforms <br>
pytest-cov <br>
sqlalchemy <br>
flask_testing <br>
gunicorn <br>
<center></b></i><hr>


</details>


<br><br>
Which for ease of use can be automatically installed following this instructions:
<br><br>

[Linux environment required]:

        use:
            . run.sh





 
<br><br>
## -- contributors 
<hr>
<br><br>

There has been only one main contributor to the project.

GitHub user:

[ddiazsouto](https://github.com/ddiazsouto/DataLake)

Also, [Dara oladapo](https://github.com/DaraOladapo), my teacher from QA has helped me troubleshooting mainly with testing


<br><br>

## -- Project Breakdown
<hr>
<br><br>
The structure of the files in the app follows the following pattern:
<br><br>

![Folder Tree](https://github.com/ddiazsouto/DataLake/blob/master/imgs/FolderTree.PNG?raw=true)

<br><br>
This is the architecture of the database
<br>


![Database Architecture](https://github.com/ddiazsouto/DataLake/blob/master/imgs/DBarchitecture.png?raw=true)


<br><br>
First sprint
<br>
![Sprint1](https://github.com/ddiazsouto/DataLake/blob/master/imgs/02-03%5BSprint%20planning%5D.PNG?raw=true)


<br><br>
Second sprint
<br>
![Sprint1](https://github.com/ddiazsouto/DataLake/blob/master/imgs/05-03%5B2-Sprint%20Planning%5D.PNG?raw=true)

<br><br>
Third sprint
<br>
![Sprint1](https://github.com/ddiazsouto/DataLake/blob/master/imgs/05-03%5B2-Sprint%20Planning%5D.PNG?raw=true)

<br><br>
Third sprint
<br>
![Sprint1](https://github.com/ddiazsouto/DataLake/blob/master/imgs/09-03%5B3-Sprint%20Backlog%5D%201%20Ready%20for%20sprint.PNG?raw=true)

<br><br>
Fourth sprint
<br>
![Sprint1](https://github.com/ddiazsouto/DataLake/blob/master/imgs/11-03%20%5B4-Sprint%20Backlog%5D.PNG?raw=true)

<br><br>
Fifth sprint
<br>
![Sprint1](https://github.com/ddiazsouto/DataLake/blob/master/imgs/15-03%20%5B5-Sprint%20Backklog%5D%20starting%20the%20last%20sprint.PNG?raw=true)

<br><br>
End of fifth sprint 
<br>
![Sprint1](https://github.com/ddiazsouto/DataLake/blob/master/imgs/19-03%20%5B5-Sprint%20Backklog%5D%20Finished.PNG?raw=true)



<br><br>
## -- acknowledgements 
<hr>
<br><br>


A photo has been used as background: [This photo](https://images.hdqwalls.com/wallpapers/lake-reflections-4k-wide.jpg)

Which is not subject to copyright by the own page definition: [Click here to see source](https://hdqwalls.com/copyright)

If there are some request to modify or remove please don't hesitate contacting me at DDiazSouto@academytrainee.com
<br><br>
<p>
Also as aforementioned, Dara oladapo, from QA, has been a great help as they have been all my colleagues at QA for sharing their thoughts and ideas
</p>
<br><br>

## -- Risk assessment
<hr>
<br><br>


| Description |Evaluation| Likelihood  | Impact Level | Responsability |  Response  |  Control Measures  
| :---        | :----:   |  :----:     |  :----:      |  :----:        |  :----:    |---:
| Code not working |potential last changes on code may be the cause| Medium/Low  |High | Person who did last commit |  Git Revert  |  Revert to last stable build
| VM not running as desired |slow, poor connection or buggy when reading modules| Medium  |Medium/High | GCP/me |  Use redundant VM alocated for this purpose  |  Git Pull to use the same code
|none of the VMs runs as desired|	there are failures on main VM and redundant VM| Very low |	High | GCP/me	|Create a new Virtual machine|	Clone repository and execute run.sh for quick set up 	
|none of the VMs runs even when creating a new one|	there are failures on main VM and redundant VM and can not create a new VM| Extremely low |	High | GCP	|Use AWS VM|	Clone repository and execute run.sh for quick set up 	
Aplication has bugs  | Production environment doesn't behave like Dev environment|Medium | High | Me | I can push to GitHub a copy of last stable version that run in production using the run.sh file in a Ubuntu Machine 
| Production environment an not be accessed via HTTP | External machine can not access the app | Low  | Medium/High | Me |  Check firewalls and labels  |  n/a              
   



<br><br>

## -- Licensing
<hr>
<br><br>

<p>MIT License</p>

<p>Copyright (c) 2021 Daniel Diaz Souto </p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy<br>
of this software and associated documentation files (the "Software"), to deal<br>
in the Software without restriction, including without limitation the rights<br>
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell<br>
copies of the Software, and to permit persons to whom the Software is<br>
furnished to do so, subject to the following conditions:<br></p>

<p>The above copyright notice and this permission notice shall be included in all<br>
copies or substantial portions of the Software.<br></p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR<br>
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,<br>
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE<br>
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER<br>
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,<br>
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE<br>
SOFTWARE.</p>
