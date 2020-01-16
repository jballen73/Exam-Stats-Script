# Exam-Stats-Script
A Python script with GUI input for comparing different versions of exams


# Use Instructions

## Creating venv
Install virualenv and create an environment where you download these files, then install the packages from requirements.txt
```
$ virtualenv <env_name>
$ source <env_name>/bin/activate
(<env_name>)$ pip install -r path/to/requirements.txt
```

Then simply run the script with `python main.py`

## Using the script

Add each version of the exam individually, entering the name, mean score, and standard deviation for each question.
If multiple versions of the exam use slightly different questions, be sure to use a generic name for equivalent questions across versions,
as the name must be the same for each version.

Once you have entered all of the questions for each version, you can press 'submit' to finalize that version.  The next time you 
add a version, you will see that all of the questions you added to the first version remain, with blank scores, for you to fill in with 
scores from the new version.  These question names cannot be changed after you have finalized a version.  If a question does not exist within
a specific version of the exam, simply leave the scores for that line blank (if you accidentally create extra blank lines, they will be ignored
if you leave them completely blank).

Once you have entered scores for each version of your exam, press the "Select Comparisons" button to indicate which pairings of exams you
want to compare. The first row of checkboxes indicates the first group, and the second row indicates the second group.  For example, 
if you had three exam versions (A, B, and C), and you wished to compare versions A and B, you would check A in the first row of boxes
and B in the second.  Then press "Add Comparison" to add these groupings to the list of what the script will run.  The script also supports
comparing combinations of versions against each other.  For example, to compare the combined A and B versions against version C, you would 
check A and B in the first row, and C in the second.  This will show in the script output as "A+B vs C".

Once you have added all of your comparisons (don't forget to add the last comparison you input, running the script will not automatically
add the currently selected configuration if you have checkboxes still selected), press "Evaluate" to run the script.  You will be 
prompted to enter a filename, which you should enter without any extension.  For example, if you wish your output to be in a file called
Spring_2020_Exam_1.txt, you would simply enter "Spring_2020_Exam_1".  Then press "Evaluate" again and your output will be in the named file
after a few seconds (note: the UI may freeze up while the script is running, but it should only take a few seconds to complete.  If it takes 
more than 30 seconds to run, this may be a bug).

## Running the script on a file

It is also possible to run the script with a .csv input and no UI, however this requires specific formatting of the csv file to work correctly.

Instructions on how to format the csv file will be updated here at a later point.
