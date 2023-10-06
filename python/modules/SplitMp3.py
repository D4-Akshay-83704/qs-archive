"""Use Mp3DirectCut.exe to split the session audio files into individual excerpts based on start and end times from Database.json"""

from __future__ import annotations

import os, json
import Utils, Alert, Link
import Mp3DirectCut
from typing import List

Mp3DirectCut.SetExecutable(Utils.PosixToWindows(Utils.PosixJoin('tools','Mp3DirectCut')))

def IncludeRedactedExcerpts() -> List[dict]:
    "Merge the redacted excerpts back into the main list in order to split mp3 files"
    
    allExcerpts = gDatabase["excerpts"] + gDatabase["excerptsRedacted"]
    allExcerpts = [x for x in allExcerpts if x["startTime"] != "Session"] # Session excerpts don't need split mp3 files
    orderedEvents = list(gDatabase["event"].keys()) # Look up the event in this list to sort excerpts by event order in gDatabase
    
    allExcerpts.sort(key = lambda x: (orderedEvents.index(x["event"]),x["sessionNumber"],x["fileNumber"]))
        # Sort by event, then by session, then by file number
    
    return allExcerpts

def AddArguments(parser):
    "Add command-line arguments used by this module"
    parser.add_argument('--overwriteMp3',action='store_true',help="Overwrite existing mp3 files; otherwise leave existing files untouched")

def ParseArguments() -> None:
    pass

def Initialize() -> None:
    pass

gOptions = None
gDatabase:dict[str] = {} # These globals are overwritten by QSArchive.py, but we define them to keep PyLint happy

def main():
    """ Split the Q&A session mp3 files into individual excerpts.
    Read the beginning and end points from Database.json."""
    
    sessionCount = 0
    mp3SplitCount = 0
    errorCount = 0
    alreadySplit = 0
    excerpts = IncludeRedactedExcerpts()
    for session in gDatabase["sessions"]:
        
        sessionNumber = session["sessionNumber"]
        event = session["event"]
        if gOptions.events != "All" and event not in gOptions.events:
            continue

        excerptList = []
        fileNumber = 1
        sessionCount += 1
        
        baseFileName = f"{event}_S{sessionNumber:02d}_"
        sessionExcerpts = [x for x in excerpts if x["event"] == event and x["sessionNumber"] == sessionNumber]
        if not any(Link.LocalItemNeeded(x) for x in sessionExcerpts):
            continue # If no local excerpts are needed in this session, then no need to split mp3 files

        for x in sessionExcerpts:
            fileName = baseFileName + f"F{fileNumber:02d}"
            startTime = Utils.StrToTimeDelta(x["startTime"])
            
            endTimeStr = x["endTime"].strip()
            if endTimeStr:
                excerptList.append((fileName,startTime,Utils.StrToTimeDelta(endTimeStr)))
            else:
                excerptList.append((fileName,startTime))
                
            fileNumber += 1
        
        eventDir = Utils.PosixJoin(gOptions.sessionMp3Dir,event)
        sessionFilePath = Utils.PosixJoin(eventDir,session["filename"])
        if not os.path.exists(sessionFilePath):
            Alert.warning("Cannot locate",sessionFilePath)
            errorCount += 1
            continue
        
        outputDir = Utils.PosixJoin(gOptions.excerptMp3Dir,event)
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        
        allOutputFilesExist = True
        for x in excerptList:
            if not os.path.exists(Utils.PosixJoin(outputDir,x[0]+'.mp3')):
                allOutputFilesExist = False
        
        if allOutputFilesExist and not gOptions.overwriteMp3:
            alreadySplit += 1
            continue
        
        # We use eventDir as scratch space for newly generated mp3 files.
        # So first clean up any files left over from previous runs.
        for x in excerptList:
            scratchFilePath = Utils.PosixToWindows(Utils.PosixJoin(eventDir,x[0]+'.mp3'))
            if os.path.exists(scratchFilePath):
                os.remove(scratchFilePath)
        
        # Next invoke Mp3DirectCut:
        try:
            Mp3DirectCut.Split(Utils.PosixToWindows(sessionFilePath),excerptList)
        except Mp3DirectCut.ExecutableNotFound as err:
            Alert.error(err)
            Alert.status("Continuing to next module.")
            return
        except Mp3DirectCut.Mp3CutError as err:
            Alert.error(err)
            Alert.status("Continuing to next mp3 file.")
            continue
        except (ValueError,OSError) as err:
            Alert.error(f"Error: {err} occured when processing session {session}")
            errorCount += 1
            Alert.status("Continuing to next mp3 file.")
            continue
        
        # Now move the files to their destination
        for x in excerptList:
            scratchFilePath = Utils.PosixJoin(eventDir,x[0]+'.mp3')
            outputFilePath = Utils.PosixJoin(outputDir,x[0]+'.mp3')
            if os.path.exists(outputFilePath):
                os.remove(outputFilePath)
            
            os.rename(scratchFilePath,outputFilePath)
        
        mp3SplitCount += 1
        Alert.info(f"Split {session['filename']} into {len(excerptList)} files.")
    
    Alert.status(f"   {mp3SplitCount} sessions split; {errorCount} sessions had errors; all files already present for {alreadySplit} sessions.")