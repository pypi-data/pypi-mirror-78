import os
import apt
import sys
import subprocess


def mount(path_name, credentials):
    mounted = False
    with open("/proc/mounts", "r") as f:
        for line in f.readlines():
            info = line.split()
            if info[0] == "s3fs" and info[1] == path_name:
                mounted = True

    if not mounted:
        pkg_name = "s3fs"

        cache = apt.cache.Cache()
        cache.update()
        cache.open()

        pkg = cache[pkg_name]
        if pkg.is_installed:
            print("{pkg_name} already installed".format(pkg_name=pkg_name))
        else:
            print("installing {pkg_name}".format(pkg_name=pkg_name))
            pkg.mark_install()
            try:
                cache.commit()
            except Exception as err:
                print(
                    "package installation failed [{err}]".format(err=str(err)),
                    file=sys.stderr,
                )

        os.environ["AWSACCESSKEYID"] = credentials["access_key_id"]
        os.environ["AWSSECRETACCESSKEY"] = credentials["secret_access_key"]
        os.makedirs(path_name, exist_ok=True)

        p = subprocess.Popen(
            [
                "s3fs",
                credentials["bucket"],
                path_name,
                "-o",
                "url=https://s3.us.cloud-object-storage.appdomain.cloud",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
