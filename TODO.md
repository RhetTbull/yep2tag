# BUGS TO FIX

* Emptying trash during call can cause applescript Finder busy error:

```Traceback (most recent call last):
  File "/Users/rhet/bin/yep2tag.py", line 231, in <module>
    main()
  File "/Users/rhet/bin/yep2tag.py", line 219, in main
    md.finder_comment = yep_comment
  File "/Users/rhet/anaconda3/lib/python3.7/site-packages/osxmetadata/__init__.py", line 317, in finder_comment
    self.__scpt_set_finder_comment.run(fname, fc)
  File "/Users/rhet/anaconda3/lib/python3.7/site-packages/osxmetadata/_applescript.py", line 120, in run
    return self._unpackresult(*self._script.executeAppleEvent_error_(evt, None))
  File "/Users/rhet/anaconda3/lib/python3.7/site-packages/osxmetadata/_applescript.py", line 95, in _unpackresult
    raise ScriptError(errorinfo)
osxmetadata._applescript.ScriptError: Finder got an error: The Finder is busy. (-15260) app='Finder' range=142-200
```

