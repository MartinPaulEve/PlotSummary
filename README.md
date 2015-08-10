PlotSummary is a python program that will scan a specified directory for plaintext files and produce a range of graphs based on the frequency and distribution of words within those files.

A great deal of the groundwork for PlotSummary was achieved by David McClure, who wrote the excellent [TextPlot](https://github.com/davidmcclure/textplot). PlotSummary is derived from this work, although I have substantially modified parts of TextPlot and have focused only on its intermediate generation functions, which are not the ultimate goal of TextPlot's network generation functions.

# Basic Usage

    """plotsummary: Plots various graphs for a series of plaintext files in a directory

    Usage:
        plotsummary.py single <directory> <term_file> [options]
        plotsummary.py hist <directory> <term_file> [options]
        plotsummary.py group <directory> <term_file> <term_name> <second_term_file> <second_term_name> [options]
        plotsummary.py rawcount <directory> <term_file> [options]
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

There are four different modes in which PlotSummary can be run, which should be passed as the first argument to the script: single, hist, group and rawcount.

Single mode will produce a kernel density estimate graph for the provided terms.

Group mode will produce a kernel density estimates for two groups of provided terms.

Hist mode will produce a histogram of term frequencies spread across 5,000 word intervals.

Rawcount mode will produce a line graph of term frequencies across 5,000 word intervals.

The "term_file" (and "second_term_file") argument(s) should be an absolute path to a file that contains a list of terms to plot; one term per line.

The "term_name" (and "second_term_name") argument(s) should be strings given on the command line. These will be used as labels for each set of terms.

The --caption option allows you to title the resulting graph.

The --debug option will let you see what's going on. I recommend enabling it.

The --nostem <nostem> argument allows you to specify a file containing a list of words that should be exempt from stemming. PlotSummary uses the Porter2 algorithm for stemming, which has some known false positives. For instance, "university" becomes "univers". The debug option (as above) will show how your terms are being stemmed. You can, therefore, use the nostem list to specify that such terms should be exempted.

#Example usage
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

#Components and Licensing
PlotSummary is copyright Martin Paul Eve 2015. It is released under the terms specified in [LICENSE](LICENSE).

PlotSummary makes use of several other open-source/free-software projects, including:

* [TextPlot](https://github.com/davidmcclure/textplot). Copyright (c) 2014-2015 David McClure with an [MIT license](https://github.com/davidmcclure/textplot/blob/master/LICENSE.txt).
* [docopt](https://github.com/docopt). Copyright (c) 2012 Vladimir Keleshev, <vladimir@keleshev.com> with an [MIT license](https://github.com/docopt/docopt/blob/master/LICENSE-MIT).