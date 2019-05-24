"""
Copyright 2019 Oliver Smith

This file is part of pmbootstrap.

pmbootstrap is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pmbootstrap is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pmbootstrap.  If not, see <http://www.gnu.org/licenses/>.
"""
import logging

import pmb.chroot
import pmb.build
import pmb.helpers.run
import pmb.helpers.pmaports


def update(args, pkgname):
    """ Fetch all sources and update the checksums in the APKBUILD. """
    pmb.build.init(args)
    pmb.build.copy_to_buildpath(args, pkgname)
    logging.info("(native) generate checksums for " + pkgname)
    pmb.chroot.user(args, ["abuild", "checksum"],
                    working_dir="/home/pmos/build")

    # Copy modified APKBUILD back
    source = args.work + "/chroot_native/home/pmos/build/APKBUILD"
    target = pmb.helpers.pmaports.find(args, pkgname) + "/"
    pmb.helpers.run.user(args, ["cp", source, target])


def verify(args, pkgname):
    """ Fetch all sources and verify their checksums. """
    pmb.build.init(args)
    pmb.build.copy_to_buildpath(args, pkgname)
    logging.info("(native) verify checksums for " + pkgname)

    # Fetch and verify sources, "fetch" alone does not verify them:
    # https://github.com/alpinelinux/abuild/pull/86
    pmb.chroot.user(args, ["abuild", "fetch", "verify"],
                    working_dir="/home/pmos/build")
