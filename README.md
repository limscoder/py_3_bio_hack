py_3_bio_hack
=============

Hacking together some Python 3 scripts for processing bio files.

**Parse sequence length percentages from fastq files**

    fastq_length_report.py

**Parse sequence counts from fasta file**

    fasta_frequency.py

**Annotate chromosome locations with gene names from gtf file.**

    annotate.py

**Webapp UI (fastq quality inspector)**

Open ./webapp/dist/sequence/app.html in browser.

    /usr/bin/open -a "/Applications/Google Chrome.app" ./webapp/dist/sequence/app.html

Project build (requires node/npm: brew install node)

    cd webapp
    npm install
    grunt build
