#
# Sublime-JSHintOnSave - https://github.com/martinkr/Sublime-JSHintOnSave
#
# Validates your js-files every time you save it. The best part: a growl notification showing a summary of errors and warnings.
# Inspired by "Cross-Platform JSLint Support for Sublime Text Editor 2 (using NodeJS) by Eduardo A Lundgren Melo"
#
# Install
# - Copy files to your sublime-packages directory
# - Install node.js and npm: http://nodejs.org/#download (http://npmjs.org/ if necessary)
# - Install JSHint using npm: npm install jshint -g
# - Install growl and growlnotify: http://growl.info/extras.php
#
# Sublime-JSHintOnSave.sublime-settings
# - Set the locations of all three binaries
# - Specify the rules in your JS-file using /* JSHint */
#
# @author Martin Krause public@mkrause.info
# @copyright Martin Krause (martinkr.github.com)
# @license MIT http://www.opensource.org/licenses/mit-license.php
# @license GNU http://www.gnu.org/licenses/gpl-3.0.html
#
# @requires node.js
#   http://nodejs.org/
#   https://github.com/joyent/node/wiki/Installation
#
# @requires JSHint
#   http://JSHint.com/
#
# @requires growlnotify
#  http://growl.info/extras.php
#

import os, re, subprocess, sublime, sublime_plugin

package = "Sublime-JSHintOnSave"

class JSHintOnSave(sublime_plugin.EventListener):

    settings =  sublime.load_settings(package + '.sublime-settings')

    def getPackageSetting(self,key):
      return self.settings.get(key)


    def growlNotify(self, result ,fileName):

      imgDir = os.path.join(sublime.packages_path(), package) + '/images/'

      if result.count('errors') > 0:
          image = 'error.png'
      else:
          image = 'success.png'

      a = []
      a.append('')
      a.append( str(result.count('errors') ) )
      a.append(' Errors, ')
      a.append( str(result.count('warnings') ) )
      a.append(' Warnings')
      title  =  ''.join(a)
      msg = fileName.split('/');
      os.popen(self.getPackageSetting('pathGrowlNotify') +' -m \"%(msg)s\" -t \"%(title)s\" --image \"%(image)s\"'% {"msg": msg[-2]+'/'+msg[-1],"title":title,"image": imgDir + image} )

      print "\r\n"
      print "JSHint Results"
      print "--------------"
      print result

    def lint(self, path):
      result = subprocess.Popen(self.getPackageSetting('pathNode') +' '+ self.getPackageSetting('pathJSHint')+' '+path , shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      return ''.join(result.stdout.readlines())

    def on_post_save(self, view):
      fileName = view.file_name()
      result = re.search('\.(js)$', fileName )

      if result == None:
        return
      elif result.group(1) == 'js':
       self.growlNotify(self.lint( fileName ),fileName)
