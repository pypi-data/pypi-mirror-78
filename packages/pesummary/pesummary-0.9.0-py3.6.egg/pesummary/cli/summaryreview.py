#! /usr/bin/env python

# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from pesummary.utils.utils import logger
import subprocess


def command_line():
    """Generate an Argument Parser object to control the command line options
    """
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-w", "--webdir", dest="webdir",
                        help="make page and plots in DIR", metavar="DIR",
                        default="./")
    parser.add_argument("-s", "--samples", dest="samples",
                        help="Posterior samples hdf5 file",
                        default=None)
    return parser


def get_executable_path(executable):
    """Return the path to the executable

    Parameters
    ----------
    executable: str
        name of the executable
    """
    try:
        path = subprocess.check_output(["which", "%s" % (executable)])
        path = path.decode("utf-8")
    except Exception:
        path = None
    return path


def launch_lalinference(webdir, path_to_results_file, trigger_file=None):
    """Launch a subprocess to generate the lalinference pages

    Parameters
    ----------
    webdir: str
        path to the directory to store the output pages
    path_to_results_file: str
        path to the results file. Must be compatible with the LALInference
        pipeline
    trigger_file: str, optional
        path to an xml trigger file.
    """
    executable = "cbcBayesPostProc"
    executable_path = get_executable_path(executable)
    if executable_path is None:
        raise Exception(
            "'cbcbayespostproc' is not installed in your environment. failed "
            "to generate lalinference pages")

    webdir += "/lalinference"
    default_arguments = ["--skyres", "0.5", "--outpath", webdir,
                         path_to_results_file]

    if trigger_file is not None:
        default_arguments.append("--trig")
        default_arguments.append(trigger_file)

    cli = executable + " " + " ".join(default_arguments)
    logger.info("Running %s" % (cli))
    ess = subprocess.Popen(
        cli, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ess.wait()


def launch_pesummary(webdir, path_to_results_file, trigger_file=None):
    """Launch a subprocess to generate the PESummary pages

    Parameters
    ----------
    webdir: str
        path to the directory to store the output pages
    path_to_results_file: str
        path to the results file. Must be compatible with the LALInference
        pipeline
    trigger_file: str, optional
        path to an xml trigger file.
    """
    executable = "summarypages"
    executable_path = get_executable_path(executable)

    if executable_path is None:
        raise Exception(
            "'summarypages' is not installed in your environment. failed "
            "to generate PESummary pages")

    webdir += "/pesummary"
    default_arguments = ["--webdir", webdir, "--samples", path_to_results_file,
                         "--approximant", "IMRPhenomPv2", "--gw",
                         "--labels", "pesummary", '--no_ligo_skymap',
                         "--cosmology", "planck15_lal"]

    if trigger_file is not None:
        default_arguments.append("--trig_file")
        default_arguments.append(trigger_file)

    cli = executable + " " + " ".join(default_arguments)
    logger.info("Running %s" % (cli))
    ess = subprocess.Popen(
        cli, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ess.wait()


def make_table_of_images(html_file, contents):
    """Make a table of images

    Parameters
    ----------
    html_file: pesummary.core.webpage.webpage.page
        open html file to write the information to
    contents: nd list
        list of images to put in the table
    """
    html_file.add_content("<div class='mx-auto d-block'>")
    html_file.add_content("<div class='row'>")
    for idx, j in enumerate(contents):
        html_file.add_content("<div class='column'>")
        html_file.add_content("<img src='%s' style='align-items:center; height:425px'>" % (j[0]))
        html_file.add_content("</div>")
    html_file.add_content("</div>")
    html_file.add_content("</div>")


def get_list_of_plots(webdir, lalinference=False, pesummary=False):
    """Get a list of plots generated by either lalinference or pesummary

    Parameters
    ----------
    webdir: str
        path to the directory to store the output pages
    lalinference: Bool
        if True, return the plots generated by LALInference. Default False
    pesummary: Bool
        if True, return the plots generated by PESummary. Default False
    """
    from glob import glob

    if lalinference:
        histogram_plots = sorted(
            glob(webdir + "/lalinference/1Dpdf/*.png"))
        params = [
            i.split("/")[-1].split(".png")[0] for i in histogram_plots]
    elif pesummary:
        histogram_plots = sorted(
            glob(webdir + "/pesummary/plots/*_1d_posterior*.png"))
        params = [
            i.split("/")[-1].split("_1d_posterior_")[1].split(".png")[0] for i
            in histogram_plots]
    return histogram_plots, params


def make_basic_comparison_html(webdir):
    """Make a basic comparison html page

    Parameters
    ----------
    webdir: str
        path to the directory to store the output pages
    """
    from pesummary.core.webpage import webpage
    from pesummary.gw.file.standard_names import standard_names
    from glob import glob
    import os
    import numpy as np

    try:
        lalinference_data = np.genfromtxt(
            os.path.join(webdir, "lalinference", "posterior_samples.dat"),
            names=True
        )
        pesummary_dat = glob(os.path.join(webdir, "pesummary", "samples", "*.dat"))
        pesummary_data = np.genfromtxt(pesummary_dat[0], names=True)
    except Exception:
        logger.info("Not printing maximum difference between samples")
        lalinference_data, pesummary_data = None, None

    lalinference_1d_histograms, lalinference_params = get_list_of_plots(
        webdir, lalinference=True)
    pesummary_1d_histograms, pesummary_params = get_list_of_plots(
        webdir, pesummary=True)
    names = [[standard_names[i], i] for i in lalinference_params if i in list(
             standard_names.keys())]
    extra = [i for i in lalinference_params if i not in list(
             standard_names.keys())]

    pages = ["home"]
    webpage.make_html(web_dir=webdir, pages=pages)
    html_file = webpage.open_html(
        web_dir=webdir, base_url="./", html_page="home")

    html_file.add_content("<link rel='stylesheet' href='./pesummary/css/font.css'>")
    html_file.make_div(_class="banner", _style="font-size: 48px")
    html_file.add_content("PESummary review")
    html_file.end_div()
    html_file.make_div(_class='paragraph')
    html_file.add_content("Here we show the comparison between the plots generated by "
                          "'cbcBayesPostProc' and 'PESummary'")
    html_file.end_div()

    html_file.make_div(_class="banner", _style="font-size:36px")
    html_file.add_content("1d histogram plot comparison")
    html_file.end_div()
    included_pesummary = []
    for num, i in enumerate(names):
        if i[0] in pesummary_params:
            included_pesummary.append(i[0])
            html_file.make_container()
            contents = [["./lalinference/1Dpdf/%s.png" % (i[1])],
                        ["./pesummary/plots/pesummary_1d_posterior_%s.png" % (i[0])]]
            make_table_of_images(html_file, contents)
            contents = [["./lalinference/1Dsamps/%s_acf.png" % (i[1])],
                        ["./pesummary/plots/pesummary_autocorrelation_%s.png" % (i[0])]]
            make_table_of_images(html_file, contents)
            contents = [["./lalinference/1Dsamps/%s_samps.png" % (i[1])],
                        ["./pesummary/plots/pesummary_sample_evolution_%s.png" % (i[0])]]
            make_table_of_images(html_file, contents)
            html_file.end_container()
            try:
                html_file.make_div(_class="banner", _style="font-size:28px")
                html_file.add_content(
                    "max difference in %s samples: "
                    "%s" % (
                        i[0], np.max(
                            np.abs(
                                lalinference_data[i[1]] - pesummary_data[i[0]]
                            )
                        )
                    )
                )
                html_file.end_div()
            except Exception:
                pass

    html_file.make_div(_class="banner", _style="font-size:28px")
    html_file.add_content("Plots only made my 'summarypages'")
    html_file.end_div()
    extra_pesummary = [i for i in pesummary_params if i not in included_pesummary]
    for num, i in enumerate(extra_pesummary):
        contents = [["./pesummary/plots/pesummary_1d_posterior_%s.png" % (i)]]
        html_file.make_container()
        make_table_of_images(html_file, contents)
        html_file.end_container()

    html_file.make_div(_class="banner", _style="font-size:28px")
    html_file.add_content("Plots only made my 'cbcBayesPostProc'")
    html_file.end_div()
    for num, i in enumerate(extra):
        contents = [["./lalinference/1Dpdf/%s.png" % (i)]]
        html_file.make_container()
        make_table_of_images(html_file, contents)
        html_file.end_container()

    html_file.make_div(_class="banner", _style="font-size:36px")
    html_file.add_content("Waveform plot comparison")
    html_file.end_div()
    html_file.make_container()
    contents = [["./lalinference/Waveform/WF_DetFrame.png"],
                ["./pesummary/plots/pesummary_waveform.png"],
                ["./pesummary/plots/pesummary_waveform_timedomain.png"]]
    make_table_of_images(html_file, contents)
    html_file.end_container()

    html_file.make_div(_class="banner", _style="font-size:36px")
    html_file.add_content("Skymap comparison")
    html_file.end_div()
    html_file.make_container()
    contents = [["./lalinference/skymap.png"],
                ["pesummary/plots/pesummary_skymap.png"]]
    make_table_of_images(html_file, contents)
    html_file.end_container()
    html_file.close()


def main(args=None):
    """Top level interface for `summaryreview`
    """
    import time

    parser = command_line()
    opts = parser.parse_args(args=args)
    logger.info("Starting to generate plots using 'cbcBayesPostProc'")
    t0 = time.time()
    launch_lalinference(opts.webdir, opts.samples)
    t1 = time.time() - t0
    logger.info("Starting to generate plots using 'summarypages'")
    t0 = time.time()
    launch_pesummary(opts.webdir, opts.samples)
    t2 = time.time() - t0
    logger.info("Making a basic comparison page")
    make_basic_comparison_html(opts.webdir)
    logger.info(
        "Different in runtime: 'cbcBayesPostProc' took {}s and 'summarypages' "
        "took {}s".format(t1, t2))


if __name__ == "__main__":
    main()
