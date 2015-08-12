PlotSummary is a python program that will scan a specified directory for plaintext files and produce a range of graphs based on the frequency and distribution of words within those files.

A great deal of the groundwork for PlotSummary was achieved by David McClure, who wrote the excellent [TextPlot](https://github.com/davidmcclure/textplot). PlotSummary is derived from this work, although I have substantially modified parts of TextPlot and have focused only on its intermediate generation functions, which are not the ultimate goal of TextPlot's network generation functions.

# Basic Usage

    """plotsummary: Plots various graphs for a series of plaintext files in a directory

    Usage:
        plotsummary.py single <directory> <term_file> [options]
        plotsummary.py hist <directory> <term_file> [options]
        plotsummary.py group <directory> <term_file> <term_name> <second_term_file> <second_term_name> [options]
        plotsummary.py overlap <directory> <first_term> <second_term> [options]
        plotsummary.py rawcount <directory> <term_file> [options]
        plotsummary.py search <directory> <term> <count> [options]
        plotsummary.py (-h | --help)
        plotsummary.py --version

    Options:
        -c, --caption <caption>                         Specify the output caption
        -d, --debug                                     Enable debug output
        -h --help                                       Show this screen.
        -n, --nostem <nostem>                           Specify a path containing words that should not be stemmed
        --version                                       Show version.
        -w, --words <words>                             Specify the word frequency to sample (default: 5000)
    """

There are six different modes in which PlotSummary can be run, which should be passed as the first argument to the script: single, hist, group, overlap,rawcount and search.

Single mode will produce a kernel density estimate graph for the provided terms.

Group mode will produce a kernel density estimates for two groups of provided terms.

Hist mode will produce a histogram of term frequencies spread across 5,000 word intervals.

Overlap mode will produce a graph showing the degree to which two terms overlap in a kernel density estimation (using Bray-Curtis dissimilarity).

Rawcount mode will produce a line graph of term frequencies across 5,000 word intervals.

Search mode will take a single term and tell you the top X other terms that occur in the same areas of the text.

The "term_file" (and "second_term_file") argument(s) should be an absolute path to a file that contains a list of terms to plot; one term per line.

The "term_name" (and "second_term_name") argument(s) should be strings given on the command line. These will be used as labels for each set of terms.

"first_term" and second_term" arguments for options that compare two terms should just be the raw terms.

The "count" argument (used with search) will let you limit the number of results.

The --caption option allows you to title the resulting graph.

The --debug option will let you see what's going on. I recommend enabling it.

The --nostem option allows you to specify a file containing a list of words that should be exempt from stemming. PlotSummary uses the Porter2 algorithm for stemming, which has some known false positives. For instance, "university" becomes "univers". The debug option (as above) will show how your terms are being stemmed. You can, therefore, use the nostem list to specify that such terms should be exempted.

The --words option allows you to set the number of words sampled in hist and rawcount modes.

#Example usage: rawcount
./plotsummary.py rawcount ~/Barth/ ~/term_file.txt -d -n ~/data/no_stem.txt -c 'University Terms' > ~/Averages.out

__Input files__


Inside ~/term_file.txt:

    university
    professor
    student
    lecturer
    college

Inside ~/data/no_stem.txt:

    university

In the directory ~/Barth is a plaintext version of John Barth's novel, _Giles Goat Boy_.

__Output files__

In ~/Averages.out:

    [plotsummary] university will not be stemmed
    [plotsummary] professor will be stemmed to professor
    [plotsummary] student will be stemmed to student
    [plotsummary] lecturer will be stemmed to lectur
    [plotsummary] college will be stemmed to colleg
    [plotsummary] Loading Barth.txt
    [plotsummary] Plotting Barth.txt
    [plotsummary] The term university appears on average 2 times every 5000 words
    [plotsummary] The term professor appears on average 1 times every 5000 words
    [plotsummary] The term student appears on average 5 times every 5000 words
    [plotsummary] The term lecturer appears on average 0 times every 5000 words
    [plotsummary] The term college appears on average 4 times every 5000 words
    [plotsummary] Saving Barth.png

In ~/Barth/Barth.png:

![Barth](docs/JohnBarthExample.png?raw=true)

#Example usage: search and overlap

./plotsummary.py search ~/GR/ blicero 20 --debug > out.txt

__Input Files__
In the directory ~/GR is a single plaintext version of Thomas Pynchon's _Gravity's Rainbow_ (Pynchon.txt).

__Output Files__

In out.txt:

    [plotsummary] blicero will be stemmed to blicero
    [plotsummary] Loading Pynchon.txt
    [plotsummary] Plotting Pynchon.txt
    [plotsummary] Top twenty correlated terms (with more than one occurrence) for blicero: 
    [plotsummary] gottfri
    [plotsummary] lager
    [plotsummary] wandervogel
    [plotsummary] thanatz
    [plotsummary] kalahari
    [plotsummary] stadt
    [plotsummary] flotsam
    [plotsummary] recogniz
    [plotsummary] execution
    [plotsummary] asham
    [plotsummary] tray
    [plotsummary] silhouett
    [plotsummary] heath
    [plotsummary] crotch
    [plotsummary] fungu
    [plotsummary] crippl
    [plotsummary] erd
    [plotsummary] exempt
    [plotsummary] butt
    [plotsummary] wand
    [plotsummary] infinit

These are the terms, in _Gravity's Rainbow_ that most closely correlate to Blicero.

We can verify this through two commands and the resulting output graphs:

./plotsummary.py overlap ~/GR/ blicero gottfried --debug

![Blicero and Gottfried in Gravity's Rainbow](docs/PynchonExample2.png?raw=true)

./plotsummary.py overlap ~/GR/ blicero thanatz --debug

![Blicero and Thanatz in Gravity's Rainbow](docs/PynchonExample1.png?raw=true)


#Components and Licensing
PlotSummary is copyright Martin Paul Eve 2015. It is released under the terms specified in [LICENSE](LICENSE).

PlotSummary makes use of several other open-source/free-software projects, including:

* [TextPlot](https://github.com/davidmcclure/textplot). Copyright (c) 2014-2015 David McClure with an [MIT license](https://github.com/davidmcclure/textplot/blob/master/LICENSE.txt).
* [docopt](https://github.com/docopt). Copyright (c) 2012 Vladimir Keleshev, <vladimir@keleshev.com> with an [MIT license](https://github.com/docopt/docopt/blob/master/LICENSE-MIT).