# Copyright 2012 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import zc.buildout
from isotoma.recipe import gocaptain
import jinja2
import missingbits

try:
    from hashlib import sha1
except ImportError:
    import sha
    def sha1(str):
        return sha.new(str)

def sibpath(filename):
    return os.path.join(os.path.dirname(__file__), filename)

class Stunnel(object):

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options
        self.buildout = buildout
        self.outputdir = os.path.join(self.buildout['buildout']['parts-directory'], self.name)

        self.cfgfile = os.path.join(self.outputdir, "stunnel.conf")

        self.options.setdefault('executable', '/usr/bin/stunnel4')

        # Logging options
        self.options.setdefault('loglevel', "2")
        self.options.setdefault('logfile', "/var/log/stunnel4/stunnel.log")

        self.backends = [buildout[opt] for opt in self.options.get_list("backends")]

        if not "pidfile" in self.options:
            if 'run-directory' in self.buildout['buildout']:
                self.options["pidfile"] = os.path.join(self.buildout['buildout']['run-directory'], self.name, "%s.pid" % self.name)
            else:
                self.options["pidfile"] = os.path.join(self.buildout['buildout']['directory'], "var", self.name, "%s.pid" % self.name)

        # 'Security enhancements'
        self.options.setdefault('user', 'stunnel4')
        self.options.setdefault('group', 'stunnel4')
        self.options.setdefault('chroot', os.path.dirname(self.options['pidfile']))

        if options["chroot"]:
            self.options.setdefault('chroot_pidfile', "/" + os.path.relpath(options['pidfile'], options['chroot']))
        else:
            self.options.setdefault("chroot_pidfile", self.options["pidfile"])

    def install(self):
        if not os.path.exists(self.options['chroot']):
            os.makedirs(self.options['chroot'])

        if not os.path.isdir(self.outputdir):
            os.mkdir(self.outputdir)
        self.options.created(self.outputdir)

        env = jinja2.Environment(loader=jinja2.PackageLoader("isotoma.recipe.stunnel", "templates"))
        templ = env.get_template("stunnel.conf.j2")

        fp = open(self.cfgfile, "w")
        fp.write(templ.render(opts=self.options, backends=self.backends))
        fp.close()
        self.options.created(self.cfgfile)

        self.runscript()

        return self.options.created()

    def runscript(self):
        target = os.path.join(self.buildout["buildout"]["bin-directory"], self.name)

        gc = gocaptain.Automatic()
        gc.write(open(target, "wt"),
            daemon=self.options['executable'],
            args=self.cfgfile,
            pidfile=self.options["pidfile"],
            name=self.name,
            description="%s daemon" % self.name)
        os.chmod(target, 0755)

        self.options.created(target)

    def update(self):
        pass

