version = '2020.08.30'
try: # For import from setup.py
    import supybot.utils.python
    supybot.utils.python._debug_software_version = version
except ImportError:
    pass
