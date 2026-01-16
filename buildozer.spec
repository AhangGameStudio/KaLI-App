[app]

# (str) Title of your application
title = Kali Matrix

# (str) Package name
package.name = kalimatrix

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (str) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
android.presplash_color = black

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Automatically accept SDK license agreements
android.accept_sdk_license = True

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (str) Android additional adb arguments
#android.adb_args = -H 127.0.0.1

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/abi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't sleep on app
#dont_sleep = False

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,common/asdf.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) Android AAR archives to add (currently works only with sdl2_gradle
# bootstrap)
#android.add_aars =

# (list) Gradle dependencies to add (currently works only with sdl2_gradle
# bootstrap)
#android.gradle_dependencies =

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package that references AndroidX.
# True by default
android.enable_androidx = True

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for more information
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
# e.g. android.gradle_repositories = "maven { url 'https://jitpack.io' }"
#android.gradle_repositories =

# (list) Packaging options to add 
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle_dependencies
# please enclose in double quotes 
# e.g. android.packaging_options = "pickFirst 'lib/*/libc++_shared.so'"
#android.packaging_options =

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) Python source code to contain the main.py, using the .py extension
#source.main = main.py

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# (str) The entry point of the application
#entrypoint = main.py

# (list) List of inclusions using pattern matching
#include_patterns = assets/*,images/*.png

# (list) List of exclusions using pattern matching
#exclude_patterns = license,images/*/*.jpg

# (list) List of directory to exclude (let empty to not exclude anything)
#exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
# Do not change this unless you know what you are doing
#exclude_common_patterns = .git/*,.idea/*,*.pyc,*.pyo,*.swp,*.swo,*.DS_Store,build/*,dist/*

# (list) List of shared libraries to include
#add_libs =

# (list) List of requirements to install with pip
#pip_requirements =

# (list) List of custom garden requirements
#garden_requirements =

# (list) List of custom garden requirements to install with pip
#garden_pip_requirements =

# (list) List of urls of recipes to download
#recipes_urls =

# (list) List of recipes to use
#recipes =

# (list) List of p4a dists to use
#p4a_dists =

# (list) List of p4a dists to use
#p4a_dist_name =

# (list) List of p4a dists to use
#p4a_dist_dir =

# (list) List of p4a dists to use
#p4a_bootstrap = sdl2

# (int) Port number for the web server
#port = 8080

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# (str) The entry point of the application
#entrypoint = main.py
