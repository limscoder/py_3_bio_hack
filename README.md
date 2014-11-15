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

Requires node/npm

    brew install node

Project build

    cd webapp
    npm install
    grunt build
    /usr/bin/open -a "/Applications/Google Chrome.app" ./dist/sequence/app.html
