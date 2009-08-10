This is Skype2Prowl
===================

This python script push a notification of [Skype](http://www.skype.com/) message to iPhone via [Prowl](http://prowl.weks.net/).
You have to need to install Prowl and getting Prowl [API Key](https://prowl.weks.net/settings.php) before using this script.
Also you have to run Skype application itself on the same machine.

Install
-------

This script requires [Skype4Py](https://developer.skype.com/wiki/Skype4Py) module. If you already installed *[easy_install](http://peak.telecommunity.com/DevCenter/EasyInstall)*,

	% easy_install Skype4Py

else please refer [Skype4Py installation guide](https://developer.skype.com/wiki/Skype4Py/installation).

Usage
-----

When you finish to setup above installation, you run *skype2prowl.py* script with two arguments.

	$ python skype2prowl.py -u <your skype username> -k <your prowl api key>
	
At initial run, you can see a confirmation dialog at Skype. please choose allowed access to Skype from Skype4Py.

Description
-----------