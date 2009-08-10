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

When you finish to setup above installation, you run *skype2prowl.py* script with arguments.

	$ python skype2prowl.py -u <your skype username> -k <your prowl api key> [-i <interval second>]
	
At initial run, you can see a confirmation dialog at Skype. please choose allowed access to Skype from Skype4Py.
If you can see below output on your terminal, you could correctly run this script. 

	******************************************************************************
	Username      : <your skype username>
	Prowl API Key : <your prowl api key>
	Interval(sec) : <interval second>
	Encodeing     : utf-8
	Connecting to Skype..
	API attachment status: Pending Authorization
	API attachment status: Success
	******************************************************************************

After that, If Skype receive message from someone in interval seconds or later from last message, script will post notification to Prowl. And you can get push message on your iPhone.
