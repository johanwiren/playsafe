
playsafe
========

Simple flask/angular application to download streams from SVT Play

[![Build Status](https://travis-ci.org/johanwiren/playsafe.png?branch=master)](https://travis-ci.org/johanwiren/playsafe)

Requirements
------------

ffmpeg compiled with the following options:

    --enable-openssl --enable-nonfree --enable-gpl --enable-libx264

Config
------

*config.yml* should contain these settings:

    ---
    port: 8000
    output_dir: /tmp

Usage
-----

Start the server 

    ./web.py

Copy-paste url's to shows you want to download into the web interface at http://localhost:8000
